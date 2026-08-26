<#
.SYNOPSIS
    Starts the viewer: the Node server that reads the delivery package, and the
    FastAPI service that holds accounts and validation verdicts.

.DESCRIPTION
    Two processes, because they do two different jobs. Node serves the
    contracts, schemas, boards and lineage on 4173. FastAPI holds the things a
    person writes — who they are, and what they decided — on 8787.

    Each gets its own window and each keeps running after this script finishes,
    so their logs stay where you can read them. A window that closes the instant
    something goes wrong takes the reason with it, which is exactly when you
    need it. Close a window to stop that half; -Shared runs both here instead.

.PARAMETER Port
    Where the viewer is served. Default 4173.

.PARAMETER ApiPort
    Where the accounts and validation service is served. Default 8787 — not
    8000, which falls inside a range Windows reserves and refuses to bind.

.PARAMETER NoApi
    Start only the viewer. Note that the viewer is behind a sign-in, and the
    accounts service is what answers it — so with this flag the viewer starts
    but nobody can get in. It is here for working on the server itself.

.PARAMETER NoBrowser
    Do not open a browser.

.PARAMETER Shared
    Run both in this one window instead of giving each its own, and stop both
    when this window is closed. Useful for a script or a CI job, where two extra
    windows are a nuisance rather than a help.

.EXAMPLE
    .\start.ps1

.EXAMPLE
    .\start.ps1 -Port 5000 -ApiPort 9000 -NoBrowser

.EXAMPLE
    .\start.ps1 -Shared
#>

[CmdletBinding()]
param(
    [int]    $Port      = 4173,
    [int]    $ApiPort   = 8787,
    [switch] $NoApi,
    [switch] $NoBrowser,
    [switch] $Shared
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
        Write-Warn 'No Python found, so the accounts service cannot start.'
        Write-Warn 'The viewer is behind a sign-in, so nobody will be able to get in.'
        Write-Warn 'Install Python and run this again.'
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
                Write-Warn 'Could not install the python dependencies, so nobody can sign in.'
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

<#
    Opens a half in its own window and leaves it there.

    The window runs the program directly and, whatever happens, does not close
    on its own: if the program dies at second three, the reason is still on
    screen an hour later. -NoExit alone is not enough, because a program that
    fails during startup scrolls its error past and then sits at a bare prompt;
    the trailing message says which half this was and what it did.
#>
function Start-Half {
    param(
        [string]$Title, [string]$Exe, [string]$Arguments, [string]$Colour = 'Gray'
    )
    $inner = @"
`$host.UI.RawUI.WindowTitle = '$Title'
Write-Host '$Title' -ForegroundColor $Colour
Write-Host 'Close this window to stop it.' -ForegroundColor DarkGray
Write-Host ''
& $Exe $Arguments
Write-Host ''
Write-Host '$Title stopped (exit code ' -NoNewline -ForegroundColor Yellow
Write-Host `$LASTEXITCODE -NoNewline -ForegroundColor Yellow
Write-Host '). This window stays open so you can read why.' -ForegroundColor Yellow
"@
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($inner))
    return Start-Process -FilePath 'powershell' `
        -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-EncodedCommand', $encoded) `
        -WorkingDirectory $PSScriptRoot -PassThru
}

function Wait-Until {
    param([scriptblock]$Test, [int]$Tries = 60)
    foreach ($attempt in 1..$Tries) {
        Start-Sleep -Milliseconds 250
        try { if (& $Test) { return $true } } catch { }
    }
    return $false
}

# ── accounts and validation ──────────────────────────────────────────
$health = $null
if (-not $NoApi) {
    Write-Host ''
    Write-Step "starting accounts and validation on $ApiPort"
    $apiArgs = "-m uvicorn api.main:app --port $ApiPort"
    if ($Shared) {
        $api = Start-Process -FilePath $python -ArgumentList $apiArgs `
            -WorkingDirectory $PSScriptRoot -NoNewWindow -PassThru
        $script:Started += $api
    }
    else {
        Start-Half -Title "TICVAI accounts :$ApiPort" -Exe "`"$python`"" `
            -Arguments $apiArgs -Colour 'Cyan' | Out-Null
    }

    if (Wait-Until { $script:health = Invoke-RestMethod -Uri "http://localhost:$ApiPort/api/health" -TimeoutSec 2; $true }) {
        $health = $script:health
        Write-Good "accounts and validation  http://localhost:$ApiPort/docs"
    }
    else {
        Write-Warn "The accounts service did not come up on $ApiPort."
        Write-Warn 'Its window is still open — the reason will be in it.'
    }
}

# ── the viewer ───────────────────────────────────────────────────────
Write-Host ''
Write-Step "starting the viewer on $Port"
$viewerArgs = "server.mjs --port $Port"
if ($Shared) {
    $viewer = Start-Process -FilePath 'node' -ArgumentList $viewerArgs `
        -WorkingDirectory $PSScriptRoot -NoNewWindow -PassThru
    $script:Started += $viewer
}
else {
    Start-Half -Title "TICVAI viewer :$Port" -Exe 'node' `
        -Arguments $viewerArgs -Colour 'Green' | Out-Null
}

if (-not (Wait-Until { Invoke-WebRequest -Uri "http://localhost:$Port/api/index" -UseBasicParsing -TimeoutSec 2 | Out-Null; $true })) {
    Write-Bad "The viewer did not come up on $Port."
    if (-not $Shared) { Write-Bad 'Its window is still open — the reason will be in it.' }
    if ($Shared) { Stop-Started }
    exit 1
}
Write-Good "viewer                   http://localhost:$Port"

# ── where to go first ────────────────────────────────────────────────
Write-Host ''
if ($null -ne $health -and $health.accounts -eq 0) {
    Write-Host '  No account exists yet.' -ForegroundColor Yellow
    Write-Host "  Open http://localhost:$Port and the first page will offer to make one." -ForegroundColor Yellow
    Write-Host "  It is an administrator, and it is the only account that page will ever make." -ForegroundColor DarkGray
    Write-Host ''
}

if (-not $NoBrowser) { Start-Process "http://localhost:$Port" | Out-Null }

if ($Shared) {
    Write-Host '  Both are running in this window. Ctrl+C stops them.' -ForegroundColor DarkGray
    Write-Host ''
    try {
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
    finally { Stop-Started }
}
else {
    Write-Host '  Each half has its own window and keeps running.' -ForegroundColor DarkGray
    Write-Host '  Close a window to stop that half. This one is finished.' -ForegroundColor DarkGray
    Write-Host ''
}
