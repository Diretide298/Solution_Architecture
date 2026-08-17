<#
.SYNOPSIS
    Starts the viewer: the Node server that reads the delivery package, and the
    FastAPI service that holds accounts and validation verdicts.

.DESCRIPTION
    Two processes, because they do two different jobs. Node serves the
    contracts, schemas, boards and lineage on 4173. FastAPI holds the things a
    person writes — who they are, and what they decided — on 8787.

    Both are started here and both are stopped when you press Ctrl+C, so you
    never leave half the application running.

.PARAMETER Port
    Where the viewer is served. Default 4173.

.PARAMETER ApiPort
    Where the accounts and validation service is served. Default 8787 — not
    8000, which falls inside a range Windows reserves and refuses to bind.

.PARAMETER NoApi
    Start only the viewer. It still reads everything; the verdict blocks say
    the service is not running rather than breaking the page.

.PARAMETER NoBrowser
    Do not open a browser.

.EXAMPLE
    .\start.ps1

.EXAMPLE
    .\start.ps1 -Port 5000 -ApiPort 9000 -NoBrowser
#>

[CmdletBinding()]
param(
    [int]    $Port      = 4173,
    [int]    $ApiPort   = 8787,
    [switch] $NoApi,
    [switch] $NoBrowser
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$script:Started = @()

function Write-Step { param([string]$Text) Write-Host "  $Text" -ForegroundColor DarkGray }
function Write-Good { param([string]$Text) Write-Host "  $Text" -ForegroundColor Green }
function Write-Warn { param([string]$Text) Write-Host "  $Text" -ForegroundColor Yellow }
function Write-Bad  { param([string]$Text) Write-Host "  $Text" -ForegroundColor Red }

function Test-PortFree {
    param([int]$Number)
    $inUse = Get-NetTCPConnection -LocalPort $Number -State Listen -ErrorAction SilentlyContinue
    return ($null -eq $inUse)
}

<#
    Runs a native command and returns its exit code, saying nothing.

    Not `& exe args 2>&1 | Out-Null`: in Windows PowerShell, redirecting a
    native command's stderr wraps each line in an ErrorRecord, and with
    $ErrorActionPreference = 'Stop' a program that merely writes a warning to
    stderr takes the whole script down with it. A probe that asks "can this
    Python import fastapi" must be allowed to answer no.
#>
function Invoke-Quiet {
    param([string]$Exe, [string[]]$Arguments)
    # Start-Process joins these with spaces and quotes nothing, so any argument
    # containing a space arrives as several. Quote them here, or a probe like
    # `-c "import fastapi"` reaches Python as `-c` and `import` and fails for a
    # reason that has nothing to do with what was being asked.
    $Arguments = @($Arguments | ForEach-Object {
        if ($_ -match '\s' -and $_ -notmatch '^".*"$') { '"' + $_ + '"' } else { $_ }
    })
    $out = [System.IO.Path]::GetTempFileName()
    $err = [System.IO.Path]::GetTempFileName()
    try {
        $proc = Start-Process -FilePath $Exe -ArgumentList $Arguments `
            -NoNewWindow -Wait -PassThru `
            -RedirectStandardOutput $out -RedirectStandardError $err
        return $proc.ExitCode
    }
    catch { return 1 }
    finally { Remove-Item $out, $err -Force -ErrorAction SilentlyContinue }
}

<#
    Finds a Python that can run the service.

    This machine has more than one, and they do not share installed packages —
    the one on PATH in one shell is not the one on PATH in another. So the test
    is not "is there a python" but "is there a python that can import what the
    service needs". One that can is used as it is; if none can, the first is
    used and the dependencies are installed into that one.
#>
function Find-Python {
    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($name in @('python', 'python3')) {
        foreach ($cmd in (Get-Command $name -All -ErrorAction SilentlyContinue)) {
            # the Windows Store stub is on PATH but is not an interpreter
            if ($cmd.Source -and $cmd.Source -notmatch 'WindowsApps') {
                $candidates.Add($cmd.Source)
            }
        }
    }
    # PATH is not the whole story. This machine has three Pythons and the one
    # holding the packages is not on PATH in every shell — a scheduled task and
    # an interactive prompt disagree about which `python` means. So the usual
    # install locations are searched too, and the choice is made on which one
    # can actually import what the service needs.
    $roots = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Python'),
        'C:\Python',
        'C:\ProgramData',
        $env:ProgramFiles
    ) | Where-Object { $_ -and (Test-Path $_) }

    foreach ($root in $roots) {
        Get-ChildItem -Path $root -Filter 'python.exe' -Recurse -Depth 2 -ErrorAction SilentlyContinue |
            ForEach-Object { $candidates.Add($_.FullName) }
    }

    $launcher = Get-Command 'py' -ErrorAction SilentlyContinue
    if ($null -ne $launcher) { $candidates.Add($launcher.Source) }

    $unique = $candidates | Select-Object -Unique
    foreach ($exe in $unique) {
        if ((Invoke-Quiet $exe @('-c', 'import fastapi, uvicorn, argon2')) -eq 0) {
            return [pscustomobject]@{ Exe = $exe; Ready = $true }
        }
    }
    if ($unique.Count -gt 0) {
        return [pscustomobject]@{ Exe = $unique[0]; Ready = $false }
    }
    return $null
}

function Stop-Started {
    if ($script:Started.Count -eq 0) { return }
    Write-Host ''
    Write-Host 'Stopping.' -ForegroundColor Cyan
    foreach ($proc in $script:Started) {
        if ($null -ne $proc -and -not $proc.HasExited) {
            Write-Step "stopping $($proc.Name) (pid $($proc.Id))"
            # Kill the tree: uvicorn --reload and npm both spawn children that
            # would otherwise keep the port held after the parent is gone.
            & taskkill /PID $proc.Id /T /F 2>&1 | Out-Null
        }
    }
    $script:Started = @()
}

Write-Host ''
Write-Host 'TICVAI viewer' -ForegroundColor Cyan
Write-Host ''

# ── what has to be here ──────────────────────────────────────────────
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Bad 'node is not on PATH. Install Node.js, then run this again.'
    exit 1
}
Write-Step "node      $(& node --version)"

$python = $null
if (-not $NoApi) {
    $found = Find-Python
    if ($null -eq $found) {
        Write-Warn 'No Python found, so accounts and validation will not start.'
        Write-Warn 'The viewer still reads everything. Install Python to enable sign-in.'
        $NoApi = $true
    }
    else {
        $python = $found.Exe
        Write-Step "python    $python"
        if (-not $found.Ready) {
            Write-Step 'installing python dependencies (first run)'
            $code = Invoke-Quiet $python @(
                '-m', 'pip', 'install', '--quiet',
                '-r', (Join-Path $PSScriptRoot 'api\requirements.txt')
            )
            if ($code -ne 0 -or (Invoke-Quiet $python @('-c', 'import fastapi, uvicorn, argon2')) -ne 0) {
                Write-Warn 'Could not install the python dependencies, so sign-in is off.'
                Write-Warn "Run: `"$python`" -m pip install -r api\requirements.txt"
                $NoApi = $true
            }
        }
    }
}

if (-not (Test-Path 'node_modules')) {
    Write-Step 'installing node dependencies (first run)'
    if ((Invoke-Quiet 'npm' @('install', '--silent')) -ne 0) {
        Write-Bad 'npm install failed.'
        exit 1
    }
}

# ── ports ────────────────────────────────────────────────────────────
if (-not (Test-PortFree -Number $Port)) {
    Write-Bad "Port $Port is already in use. Close what is on it, or pass -Port."
    exit 1
}
if (-not $NoApi -and -not (Test-PortFree -Number $ApiPort)) {
    Write-Bad "Port $ApiPort is already in use. Close what is on it, or pass -ApiPort."
    exit 1
}

# Stop both halves however this ends — Ctrl+C, an error, or a clean finish.
$handler = { Stop-Started }
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $handler | Out-Null

try {
    # ── accounts and validation ──────────────────────────────────────
    if (-not $NoApi) {
        Write-Host ''
        Write-Step "starting accounts and validation on $ApiPort"
        $api = Start-Process -FilePath $python `
            -ArgumentList @('-m', 'uvicorn', 'api.main:app', '--port', "$ApiPort", '--log-level', 'warning') `
            -WorkingDirectory $PSScriptRoot -NoNewWindow -PassThru
        $script:Started += $api

        # Wait for it to answer rather than guessing at a sleep.
        $ready = $false
        foreach ($attempt in 1..40) {
            Start-Sleep -Milliseconds 250
            if ($api.HasExited) { break }
            try {
                $health = Invoke-RestMethod -Uri "http://localhost:$ApiPort/api/health" -TimeoutSec 2
                $ready = $true
                break
            } catch { }
        }

        if ($ready) {
            Write-Good "accounts and validation  http://localhost:$ApiPort/docs"
            if ($health.accounts -eq 0) {
                Write-Host ''
                Write-Warn 'No accounts exist yet. Make the first one in another terminal:'
                Write-Warn "  python -m api.cli admin you@$($health.domain)"
                Write-Warn 'Then invite everyone else from the viewer.'
            }
        }
        else {
            Write-Warn "The validation service did not come up on $ApiPort."
            Write-Warn 'The viewer will still read everything; sign-in will be off.'
        }
    }

    # ── the viewer ───────────────────────────────────────────────────
    Write-Host ''
    Write-Step "starting the viewer on $Port"
    $viewer = Start-Process -FilePath 'node' `
        -ArgumentList @('server.mjs', '--port', "$Port") `
        -WorkingDirectory $PSScriptRoot -NoNewWindow -PassThru
    $script:Started += $viewer

    $ready = $false
    foreach ($attempt in 1..40) {
        Start-Sleep -Milliseconds 250
        if ($viewer.HasExited) { break }
        try {
            Invoke-WebRequest -Uri "http://localhost:$Port/api/index" -UseBasicParsing -TimeoutSec 2 | Out-Null
            $ready = $true
            break
        } catch { }
    }

    if (-not $ready) {
        Write-Bad "The viewer did not come up on $Port."
        Stop-Started
        exit 1
    }
    Write-Good "viewer                   http://localhost:$Port"

    if (-not $NoBrowser) { Start-Process "http://localhost:$Port" | Out-Null }

    Write-Host ''
    Write-Host '  Ctrl+C stops both.' -ForegroundColor DarkGray
    Write-Host ''

    # Hold here until something exits or the user interrupts. Waiting on the
    # processes rather than spinning keeps this off the CPU.
    while ($true) {
        Start-Sleep -Seconds 1
        foreach ($proc in $script:Started) {
            if ($proc.HasExited) {
                Write-Warn "$($proc.Name) (pid $($proc.Id)) stopped on its own."
                throw 'A process exited.'
            }
        }
    }
}
finally {
    Stop-Started
}
