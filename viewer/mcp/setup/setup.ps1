<#
.SYNOPSIS
    Creates a fresh backend or frontend project folder and connects Claude Code
    in it to ADAM.

.DESCRIPTION
    What a developer runs from the setup zip. The zip holds setup.cmd at the
    top and everything else in adam-connector\ beside it. Unzip it into the
    folder the project should be created in and run setup.cmd from there:

        C:\work\setup.cmd            (or double-click it)

    It:
      1. checks that Node.js 22+ and Claude Code are installed,
      2. asks for your ADAM email and password (the password is hidden),
      3. checks that they actually sign in to ADAM - before changing anything,
      4. lists the ADAM projects you can open and asks which one to use,
      5. asks whether you are a backend or a frontend developer,
      6. creates <project>-<role> beside setup.cmd from the matching starter:
         the code skeleton, CLAUDE.md, .claude\ (permissions and /ticket,
         /board, /done) and project-bible\setup\ (the coding standards),
         renamed for the project, as a new git repository,
      7. copies the connector to %USERPROFILE%\.adam\connector,
      8. registers it with Claude Code for that folder only,
      9. and, if you want, runs the full connection test.

    Only Claude Code sessions opened in that folder - in VS Code or a terminal -
    can use ADAM. Pointed at a folder that already has files, setup changes
    none of them and only connects ADAM there (after a password change, say).
    uninstall.cmd removes every registration.

    ASCII only, on purpose: Windows PowerShell 5.1 reads a script saved without
    a byte-order mark in the machine's ANSI code page, and a dash or a curly
    quote becomes a parse error on somebody else's computer.

.PARAMETER ViewerUrl
    Where ADAM is. Defaults to the live site.

.PARAMETER Email
    Your ADAM sign-in address. Asked for when not given.

.PARAMETER Project
    The ADAM project id (for example ticvai). Asked for when not given.

.PARAMETER Role
    backend or frontend - which starter a new folder is made from. Asked for when not given.

.PARAMETER Folder
    The project folder. A new or empty one is created from the starter; one
    with files in it is only connected. Asked for when not given. "all"
    connects every folder and creates nothing.

.PARAMETER Test
    ask (default), yes or no - whether to run the full connection test at the end.

.PARAMETER Uninstall
    Remove every registration setup made, and delete the installed files.

.PARAMETER RemoveFolder
    Remove the registration for this one folder only.

.PARAMETER Name
    The name Claude Code knows the connector by. Leave it as adam.

.PARAMETER InstallDir
    Where the connector files go. Leave it as the default.

.EXAMPLE
    C:\work\setup.cmd

.EXAMPLE
    C:\work\setup.cmd -Project ticvai -Role backend -Folder C:\work\ticvai-backend

.EXAMPLE
    .\setup.ps1 -RemoveFolder C:\work\ticvai-backend

.EXAMPLE
    .\setup.ps1 -Uninstall
#>
param(
    [string]$ViewerUrl = 'https://adam.ainfinite.ai',
    [string]$Email = '',
    [string]$Project = '',
    [ValidateSet('', 'backend', 'frontend')]
    [string]$Role = '',
    [string]$Folder = '',
    [ValidateSet('ask', 'yes', 'no')]
    [string]$Test = 'ask',
    [switch]$Uninstall,
    [string]$RemoveFolder = '',
    [string]$Name = 'adam',
    [string]$InstallDir = (Join-Path $env:USERPROFILE '.adam\connector')
)

$ErrorActionPreference = 'Stop'
# Where setup was started from, before anything moves. The new project folder
# goes there - which, double-clicked, is the folder setup.cmd sits in.
$LaunchDir = (Get-Location).ProviderPath
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
# The code skeletons, one per role, and the standards documents they share.
# Only in the zip: the installed copy can connect a folder but not create one.
$Starters = Join-Path $Here 'starters'
$Roles = [ordered]@{
    backend  = [pscustomobject]@{ Label = 'Backend  (.NET 10 API, clean architecture)'; Check = 'dotnet'; Docs = @(
        'naming-and-style', 'backend-patterns', 'api-conventions', 'quality-gates', 'git-and-mrs',
        'llm-conventions', 'data-and-storage', 'config-and-secrets', 'dependencies', 'adding-things', 'quickstart') }
    frontend = [pscustomobject]@{ Label = 'Frontend (Nx workspace: React Native apps and a web app)'; Check = 'pnpm'; Docs = @(
        'naming-and-style', 'frontend-patterns', 'api-conventions', 'quality-gates', 'git-and-mrs',
        'llm-conventions', 'data-and-storage', 'config-and-secrets', 'dependencies', 'adding-things', 'quickstart') }
}
# The connector itself. `version.mjs` and `update.mjs` are part of it and not
# an extra: without them an install has no way to tell it is out of date and
# no way to fix it, which is the whole point of shipping them. The same six
# are hashed by version.mjs and copied by build-zip.ps1 -- three lists that
# have to agree, and the build id is what says when they do not.
$Files = @('server.mjs', 'client.mjs', 'tools.mjs', 'mcp-check.mjs',
          'version.mjs', 'update.mjs')
# Kept beside the installed connector, so a folder can be removed later
# without the zip.
$Tools = @('setup.ps1', 'setup.cmd', 'uninstall.cmd')
$ViewerUrl = $ViewerUrl.TrimEnd('/')
# One line per registration setup has made: scope|folder|project. Read by the
# uninstall, which has to stand in each folder to remove that folder's entry.
$Ledger = Join-Path $InstallDir 'registrations.txt'

function Step([string]$text) { Write-Host ''; Write-Host "== $text" -ForegroundColor Cyan }
function Good([string]$text) { Write-Host "   ok  $text" -ForegroundColor Green }
function Note([string]$text) { Write-Host "       $text" -ForegroundColor Gray }
function Stop-Setup([string]$text) {
    Write-Host ''
    Write-Host "   !!  $text" -ForegroundColor Red
    Write-Host ''
    exit 1
}

# ---- running Claude Code -------------------------------------------------------
#
# npm installs `claude` as claude.ps1 and claude.cmd, and both are poor ways in:
# PowerShell drops a bare `--` on its way into the .ps1, and the .cmd goes
# through Command Prompt, which reads & % ^ | < > in a password as its own.
# The .cmd only starts bin\claude.exe beside it, so that is what is run, with
# every argument quoted the way a Windows program reads them. A claude.exe on
# the PATH (the native installer) is used as it is.
#
# An npm install can leave the .cmd without its claude.exe (a blocked or failed
# download), so every candidate must answer --version before it is used. The
# native installer's copy and the VS Code extension's own copy are tried too:
# all of them keep connectors in the same ~\.claude.json.
function Get-ClaudeVersion([string]$Path) {
    try {
        $info = New-Object System.Diagnostics.ProcessStartInfo
        $info.FileName = $Path
        $info.Arguments = '--version'
        $info.UseShellExecute = $false
        $info.CreateNoWindow = $true
        $info.RedirectStandardOutput = $true
        $info.RedirectStandardError = $true
        $info.WorkingDirectory = $env:USERPROFILE
        $process = [System.Diagnostics.Process]::Start($info)
        $out = $process.StandardOutput.ReadToEndAsync()
        $err = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(30000)) { try { $process.Kill() } catch {}; return $null }
        $first = (($out.Result + $err.Result).Trim() -split "`n")[0].Trim()
        if ($process.ExitCode -eq 0 -and $first -match '^\d+\.\d+') { return $first }
    } catch {}
    return $null
}

function Find-Claude {
    $all = @(Get-Command claude -CommandType Application -All -ErrorAction SilentlyContinue)
    $tried = @()
    $safe = @()
    $safe += $all | Where-Object { $_.Source -like '*.exe' } | ForEach-Object { $_.Source }
    foreach ($shim in $all) {
        $safe += Join-Path (Split-Path -Parent $shim.Source) 'node_modules\@anthropic-ai\claude-code\bin\claude.exe'
    }
    $safe += Join-Path $env:USERPROFILE '.local\bin\claude.exe'
    foreach ($editor in '.vscode', '.vscode-insiders', '.cursor', '.windsurf') {
        $root = Join-Path $env:USERPROFILE "$editor\extensions"
        $safe += Get-ChildItem -LiteralPath $root -Directory -Filter 'anthropic.claude-code-*' -ErrorAction SilentlyContinue |
            Sort-Object { try { [version]($_.Name -replace '^anthropic\.claude-code-([\d.]+).*$', '$1') } catch { [version]'0.0' } } -Descending |
            ForEach-Object { Join-Path $_.FullName 'resources\native-binary\claude.exe' }
    }
    foreach ($path in $safe) {
        if (-not $path -or $tried -contains $path -or -not (Test-Path -LiteralPath $path)) { continue }
        $tried += $path
        $version = Get-ClaudeVersion $path
        if ($version) { return [pscustomobject]@{ Path = $path; Safe = $true; Version = $version; Broken = $false } }
    }
    foreach ($shim in $all | Where-Object { $_.Source -notlike '*.exe' }) {
        $version = Get-ClaudeVersion $shim.Source
        if ($version) { return [pscustomobject]@{ Path = $shim.Source; Safe = $false; Version = $version; Broken = $false } }
    }
    if ($all.Count) { return [pscustomobject]@{ Path = $all[0].Source; Safe = $false; Version = ''; Broken = $true } }
    return $null
}

# One argument list as one Windows command line: quoted when it has to be, with
# backslashes doubled only where they come before a quote.
function ConvertTo-CommandLine([string[]]$ArgList) {
    $out = foreach ($arg in $ArgList) {
        if ($arg -ne '' -and $arg -notmatch '[\s"]') { $arg; continue }
        $text = '"'
        $slashes = 0
        foreach ($ch in $arg.ToCharArray()) {
            if ($ch -eq '\') { $slashes++; continue }
            if ($ch -eq '"') { $text += ('\' * ($slashes * 2 + 1)) + '"'; $slashes = 0; continue }
            $text += ('\' * $slashes) + $ch
            $slashes = 0
        }
        $text + ('\' * ($slashes * 2)) + '"'
    }
    return ($out -join ' ')
}

# Every call to Claude Code goes through here. `Where` is the folder it runs in,
# spelled exactly as given: Claude Code files a folder setting under the folder
# as it saw it, and PowerShell's own Set-Location would change the spelling.
function Invoke-Claude([string[]]$ArgList, [string]$Where = '') {
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = $script:Claude.Path
    $info.Arguments = ConvertTo-CommandLine $ArgList
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    if ($Where) { $info.WorkingDirectory = $Where } else { $info.WorkingDirectory = $env:USERPROFILE }
    $process = [System.Diagnostics.Process]::Start($info)
    $outTask = $process.StandardOutput.ReadToEndAsync()
    $errTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    return [pscustomobject]@{ Code = $process.ExitCode; Text = ($outTask.Result + $errTask.Result).Trim() }
}

# ---- folders -------------------------------------------------------------------

# The folder as the disk spells it. A path typed as c:\work\API is stored by
# Claude Code as typed, and VS Code opens C:\work\api; they must agree.
function Get-TrueCase([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
    $root = [System.IO.Path]::GetPathRoot($full)
    if ($full.Length -le $root.TrimEnd('\').Length) { return $root }
    $current = $root.ToUpper()
    foreach ($part in $full.Substring($root.Length).Split('\')) {
        if (-not $part) { continue }
        $found = @([System.IO.Directory]::GetDirectories($current, $part))
        if ($found.Count -eq 1) { $current = $found[0] } else { $current = Join-Path $current $part }
    }
    return $current
}

# Every spelling Claude Code may know this folder by. VS Code hands it the drive
# letter in lower case (c:\work) and a terminal in upper case (C:\work), and
# Claude Code keeps the two apart - so a folder is registered under both.
function Get-Spellings([string]$Path) {
    if ($Path -match '^[A-Za-z]:\\') {
        return @(($Path.Substring(0, 1).ToUpper() + $Path.Substring(1)),
                 ($Path.Substring(0, 1).ToLower() + $Path.Substring(1)))
    }
    return @($Path)
}

function Read-Ledger {
    if (-not (Test-Path -LiteralPath $Ledger)) { return @() }
    return @(Get-Content -LiteralPath $Ledger | Where-Object { $_ -match '\|' } | ForEach-Object {
        $part = $_ -split '\|', 3
        [pscustomobject]@{ Scope = $part[0]; Folder = $part[1]; Project = $part[2] }
    })
}

function Write-Ledger($entries) {
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $lines = @($entries | ForEach-Object { "$($_.Scope)|$($_.Folder)|$($_.Project)" })
    Set-Content -LiteralPath $Ledger -Value $lines -Encoding ASCII
}

function Remove-FolderRegistration([string]$Path) {
    $removed = $false
    foreach ($spelling in (Get-Spellings $Path)) {
        if (-not (Test-Path -LiteralPath $spelling)) { continue }
        if ((Invoke-Claude @('mcp', 'remove', $Name, '-s', 'local') $spelling).Code -eq 0) { $removed = $true }
    }
    return $removed
}

function Show-RemoveHelp($entries) {
    $script = Join-Path $InstallDir 'setup.ps1'
    Write-Host '  To remove it later: double-click uninstall.cmd (removes everything), or run:'
    foreach ($entry in $entries) {
        if ($entry.Scope -eq 'user') {
            Write-Host "     claude mcp remove $Name -s user" -ForegroundColor Gray
            Write-Host '        (the every-folder setting)' -ForegroundColor DarkGray
        } else {
            Write-Host "     powershell -ExecutionPolicy Bypass -File `"$script`" -RemoveFolder `"$($entry.Folder)`"" -ForegroundColor Gray
            Write-Host "        ($($entry.Folder) only)" -ForegroundColor DarkGray
        }
    }
}

# ---- starting a project --------------------------------------------------------

# The starters are written for TICVAI. For another project, TICVAI and Ticvai
# become its name as a code identifier (Greenleaf Demo -> GreenleafDemo) and
# ticvai becomes its ADAM id (greenleaf-demo), in file names and contents.
function Get-CodeName($picked) {
    if (-not $picked.name) { $words = @(($picked.id -split '[^A-Za-z0-9]+') | Where-Object { $_ }) }
    else { $words = @(($picked.name -split '[^A-Za-z0-9]+') | Where-Object { $_ }) }
    $name = ($words | ForEach-Object {
        if ($_ -ceq $_.ToUpper()) { $_ } else { $_.Substring(0, 1).ToUpper() + $_.Substring(1) }
    }) -join ''
    if (-not $name) { $name = 'App' }
    if ($name -match '^[0-9]') { $name = "App$name" }
    return $name
}

function Test-EmptyFolder([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { return $false }
    return -not (Get-ChildItem -LiteralPath $Path -Force | Select-Object -First 1)
}

$TextFiles = @('.cs', '.csproj', '.slnx', '.sln', '.json', '.http', '.md', '.ts', '.tsx', '.js', '.cjs',
    '.mjs', '.yml', '.yaml', '.props', '.targets', '.txt', '.gitignore', '.editorconfig')

function New-ProjectFolder([string]$Target, [string]$RoleName, $picked) {
    $source = Join-Path $Starters $RoleName
    if (-not (Test-Path -LiteralPath $source)) {
        Stop-Setup "The $RoleName starter is missing next to this script. Run setup.cmd from the unzipped folder, not from the installed copy."
    }
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    # -Force brings the dot-folders too: .claude and .github matter.
    Copy-Item -Path (Join-Path $source '*') -Destination $Target -Recurse -Force

    $codeName = Get-CodeName $picked
    $id = $picked.id
    if ($id -ne 'ticvai') {
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        $utf8Bom = New-Object System.Text.UTF8Encoding($true)
        foreach ($file in @(Get-ChildItem -LiteralPath $Target -Recurse -File -Force)) {
            if ($file.FullName -like '*\project-bible\*' -or $file.Name -eq 'pnpm-lock.yaml') { continue }
            if (-not ($TextFiles -contains $file.Extension.ToLower())) { continue }
            $bytes = [IO.File]::ReadAllBytes($file.FullName)
            $bom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
            $text = [IO.File]::ReadAllText($file.FullName)
            $new = $text.Replace('TICVAI', $codeName).Replace('Ticvai', $codeName).Replace('ticvai', $id)
            if ($new -cne $text) {
                if ($bom) { [IO.File]::WriteAllText($file.FullName, $new, $utf8Bom) }
                else { [IO.File]::WriteAllText($file.FullName, $new, $utf8) }
            }
        }
        # Deepest first, so a folder is renamed after what is inside it.
        $named = @(Get-ChildItem -LiteralPath $Target -Recurse -Force |
            Where-Object { $_.Name -clike '*TICVAI*' } |
            Sort-Object { $_.FullName.Length } -Descending)
        foreach ($item in $named) {
            Rename-Item -LiteralPath $item.FullName -NewName ($item.Name.Replace('TICVAI', $codeName))
        }
    }

    # The standards documents for this role, with an index Claude can start from.
    $bible = Join-Path $Target 'project-bible\setup'
    New-Item -ItemType Directory -Force -Path $bible | Out-Null
    $index = @('# Coding standards', '', "What a $RoleName developer on this project reads. CLAUDE.md says in which order.", '')
    foreach ($doc in $Roles[$RoleName].Docs) {
        $from = Join-Path $Starters "docs\$doc.md"
        if (-not (Test-Path -LiteralPath $from)) { continue }
        Copy-Item -LiteralPath $from -Destination $bible -Force
        $title = (Get-Content -LiteralPath $from -TotalCount 1) -replace '^#\s*', ''
        $index += "- [$doc]($doc.md) - $title"
    }
    Set-Content -LiteralPath (Join-Path $bible 'README.md') -Value $index -Encoding UTF8

    # A repository of its own, with the starter as its first commit, so
    # `git diff` shows exactly what was built on top of it.
    $git = Get-Command git -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($git) {
        $ErrorActionPreference = 'Continue'
        & $git.Source -C $Target init -q 2>$null | Out-Null
        & $git.Source -C $Target add -A 2>$null | Out-Null
        & $git.Source -C $Target commit -q -m "Start from the ADAM $RoleName starter" 2>$null | Out-Null
        $committed = $LASTEXITCODE -eq 0
        $ErrorActionPreference = 'Stop'
        if ($committed) { Good 'new git repository, with the starter as the first commit' }
        else { Note 'git repository created; commit the starter yourself (git has no user.name / user.email yet)' }
    } else {
        Note 'git is not installed, so this is not a repository yet'
    }
    return $codeName
}

Write-Host ''
Write-Host 'ADAM connector for Claude Code' -ForegroundColor White
$script:Claude = Find-Claude

# ---- removing ------------------------------------------------------------------
if ($Uninstall -or $RemoveFolder) {
    if (-not $script:Claude) { Stop-Setup 'Claude Code is not installed, so there is nothing registered to remove.' }
    if ($script:Claude.Broken) { Stop-Setup 'Claude Code is installed but does not start, so nothing can be removed. Reinstall it (npm install -g @anthropic-ai/claude-code) and run this again.' }
    $entries = Read-Ledger
    if ($RemoveFolder) {
        Step 'Removing ADAM from one folder'
        $target = Get-TrueCase $RemoveFolder.Trim().Trim('"')
        if (Remove-FolderRegistration $target) { Good "removed '$Name' from $target" }
        else { Note "'$Name' was not registered for $target" }
        Write-Ledger @($entries | Where-Object { -not ($_.Scope -eq 'local' -and $_.Folder -ieq $target) })
    } else {
        Step 'Removing the connector'
        foreach ($entry in ($entries | Where-Object { $_.Scope -eq 'local' })) {
            if (-not (Test-Path -LiteralPath $entry.Folder)) {
                Note "skipped $($entry.Folder) - that folder no longer exists"
                continue
            }
            if (Remove-FolderRegistration $entry.Folder) { Good "removed '$Name' from $($entry.Folder)" }
            else { Note "nothing to remove in $($entry.Folder)" }
        }
        # Removed whether or not the ledger knows about it: an older setup made one.
        if ((Invoke-Claude @('mcp', 'remove', $Name, '-s', 'user')).Code -eq 0) { Good "removed the every-folder '$Name'" }
        if (Test-Path -LiteralPath $InstallDir) {
            Remove-Item -LiteralPath $InstallDir -Recurse -Force
            Good "deleted $InstallDir"
        }
    }
    Write-Host ''
    Write-Host 'Done. Restart Claude Code for the change to show.' -ForegroundColor White
    Write-Host ''
    exit 0
}

# ---- 1. what this computer needs -----------------------------------------------
Step 'Checking this computer'

foreach ($file in ($Files + $Tools)) {
    if (-not (Test-Path -LiteralPath (Join-Path $Here $file))) {
        Stop-Setup "$file is missing next to this script. Unzip the whole folder first, then run setup.cmd from it."
    }
}

$node = Get-Command node -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $node) {
    Stop-Setup 'Node.js is not installed. Install it with:  winget install --id OpenJS.NodeJS.LTS -e   then open a new window and run setup again.'
}
$nodeVersion = (& $node.Source -v).Trim()
$major = 0
[void][int]::TryParse(($nodeVersion.TrimStart('v') -split '\.')[0], [ref]$major)
if ($major -lt 22) {
    Stop-Setup "Node.js $nodeVersion is too old - the connector needs 22 or newer. Update it with:  winget upgrade --id OpenJS.NodeJS.LTS -e"
}
Good "Node.js $nodeVersion"

if (-not $script:Claude) {
    Stop-Setup 'Claude Code is not installed. Install it with:  npm install -g @anthropic-ai/claude-code   then open a new window and run setup again.'
}
if ($script:Claude.Broken) {
    Stop-Setup ("Claude Code is installed but does not start ($($script:Claude.Path) fails - its claude.exe is missing, usually a download that was blocked). " +
        'Reinstall it with:  npm uninstall -g @anthropic-ai/claude-code   then   npm install -g @anthropic-ai/claude-code   ' +
        '(or use the native installer:  irm https://claude.ai/install.ps1 | iex ), open a new window and run setup again.')
}
Good "Claude Code $($script:Claude.Version)"

# ---- 2. who you are ------------------------------------------------------------
Step "Your ADAM account ($ViewerUrl)"

while ($Email -notmatch '^[^@\s]+@[^@\s]+\.[^@\s]+$') {
    if ($Email) { Note 'That does not look like an email address.' }
    $Email = (Read-Host '   ADAM email').Trim()
}

# Taken from the environment when it is already there, so the script can be run
# unattended; otherwise asked for, hidden, and never written to the screen.
$password = $env:ADAM_PASSWORD
if (-not $password) {
    $secure = Read-Host '   ADAM password (hidden)' -AsSecureString
    $password = (New-Object System.Net.NetworkCredential('', $secure)).Password
}
if (-not $password) { Stop-Setup 'No password was given.' }

# Only when Claude Code could not be run directly: through Command Prompt these
# characters do not arrive as typed.
if (-not $script:Claude.Safe -and $password -match '["&%^|<>!]') {
    Stop-Setup 'Your ADAM password contains one of  " & % ^ | < > !  which this Claude Code install cannot receive intact. Update Claude Code (npm install -g @anthropic-ai/claude-code), or change your ADAM password (Settings -> Password), then run setup again.'
}

# ---- 3. prove it signs in, before touching anything --------------------------
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
} catch { }

$body = @{ email = $Email; password = $password } | ConvertTo-Json -Compress
$session = $null
try {
    $null = Invoke-WebRequest -Uri "$ViewerUrl/api/auth/login" -Method Post -UseBasicParsing `
        -ContentType 'application/json' -Body $body -SessionVariable session -TimeoutSec 30
} catch {
    $status = $null
    if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
    if ($status -eq 401 -or $status -eq 400) {
        Stop-Setup "ADAM did not accept that email and password. Check them by signing in at $ViewerUrl, then run setup again."
    }
    if ($status -eq 403) {
        Stop-Setup "ADAM refused the sign-in (403) - the account may be disabled. Ask an ADAM admin."
    }
    if ($status) { Stop-Setup "ADAM answered $status to the sign-in. Try again in a minute; if it keeps happening, tell an ADAM admin." }
    Stop-Setup "Could not reach $ViewerUrl ($($_.Exception.Message)). Check your connection, then run setup again."
}
# The sign-in answers only {"ok":true}; who that was comes from asking with the
# session it set - which also proves the cookie comes back, as the connector needs.
$who = $null
try {
    $me = Invoke-WebRequest -Uri "$ViewerUrl/api/auth/me" -UseBasicParsing -WebSession $session -TimeoutSec 15
    $who = ($me.Content | ConvertFrom-Json).account
} catch { }
$shown = $Email
if ($who -and $who.name) { $shown = "$($who.name) <$Email>" }
if ($who -and $who.role) { $shown = "$shown, $($who.role)" }
Good "signed in as $shown"

# ---- 4. which ADAM project -----------------------------------------------------
# Asked with the same session, so the list is only what this account may open.
Step 'Choosing the ADAM project'
$projects = @()
try {
    $listed = Invoke-WebRequest -Uri "$ViewerUrl/api/projects" -UseBasicParsing -WebSession $session -TimeoutSec 30
    $projects = @(($listed.Content | ConvertFrom-Json).projects)
} catch { }
if ($projects.Count -eq 0) {
    Stop-Setup "Your ADAM account cannot open any project yet. Ask an ADAM admin to give you access, then run setup again."
}
$picked = $null
if ($Project) {
    $picked = $projects | Where-Object { $_.id -eq $Project } | Select-Object -First 1
    if (-not $picked) {
        Stop-Setup "There is no ADAM project '$Project' that your account can open. Yours: $(($projects | ForEach-Object { $_.id }) -join ', ')"
    }
} else {
    for ($i = 0; $i -lt $projects.Count; $i++) {
        $label = $projects[$i].name
        if (-not $label) { $label = $projects[$i].id }
        Write-Host ("     {0}. {1}  ({2})" -f ($i + 1), $label, $projects[$i].id)
    }
    while (-not $picked) {
        $answer = (Read-Host "   Enter the project number [1-$($projects.Count)]").Trim()
        $number = 0
        if ([int]::TryParse($answer, [ref]$number) -and $number -ge 1 -and $number -le $projects.Count) {
            $picked = $projects[$number - 1]
        } else {
            Note "Type a number from 1 to $($projects.Count)."
        }
    }
}
$Project = $picked.id
Good "project: $($picked.name) ($Project)"

# Not left open: this check is the only thing that session was for.
try {
    $null = Invoke-WebRequest -Uri "$ViewerUrl/api/auth/logout" -Method Post -UseBasicParsing `
        -WebSession $session -TimeoutSec 15
} catch { }

# ---- 5. backend or frontend -----------------------------------------------------
if ($Folder -ne 'all') {
    Step 'What you work on'
    if (-not $Role) {
        $names = @($Roles.Keys)
        for ($i = 0; $i -lt $names.Count; $i++) {
            Write-Host ("     {0}. {1}" -f ($i + 1), $Roles[$names[$i]].Label)
        }
        while (-not $Role) {
            $answer = (Read-Host "   Enter the number [1-$($names.Count)]").Trim()
            $number = 0
            if ([int]::TryParse($answer, [ref]$number) -and $number -ge 1 -and $number -le $names.Count) {
                $Role = $names[$number - 1]
            } else {
                Note "Type a number from 1 to $($names.Count)."
            }
        }
    }
    Good $Roles[$Role].Label
    if (-not (Get-Command $Roles[$Role].Check -ErrorAction SilentlyContinue)) {
        Note "$($Roles[$Role].Check) is not installed. The folder is still created; install it before building."
    }
}

# ---- 6. the project folder ------------------------------------------------------
Step 'The project folder'
# Created where setup was started from a terminal. Double-clicked, that is the
# unzipped adam-setup folder, which somebody will delete one day - so the
# project goes beside it instead, and beside the folder Windows' Extract All
# wraps it in, when there is one.
$unzipped = Split-Path -Parent $Here
$besideZip = Split-Path -Parent $unzipped
if ((Split-Path -Leaf $besideZip) -like 'adam-connector-setup*' -and
        @(Get-ChildItem -LiteralPath $besideZip -Force).Count -eq 1) {
    $besideZip = Split-Path -Parent $besideZip
}
$parent = $LaunchDir.TrimEnd('\')
$notHere = @($Here, $unzipped, $InstallDir, $env:USERPROFILE, $env:windir) | ForEach-Object { "$_".TrimEnd('\') }
if (-not $parent -or ($notHere -contains $parent) -or $parent.StartsWith("$env:windir\", 'OrdinalIgnoreCase') -or
        $parent -match '^[A-Za-z]:$') {
    $parent = $besideZip
}
$default = Join-Path $parent "$Project-$Role"
$create = $false
Note 'Only Claude Code sessions opened in this folder - in VS Code or a terminal - will be able to use ADAM.'
if ($Folder -ne 'all') { Note 'Press Enter to create the folder shown, or paste another path.' }
while ($true) {
    if (-not $Folder) {
        $Folder = (Read-Host "   Folder [$default]").Trim().Trim('"')
        if (-not $Folder) { $Folder = $default }
    }
    if ($Folder -eq 'all') { break }
    $Folder = [System.IO.Path]::GetFullPath($Folder).TrimEnd('\')
    if ($Folder -match '^[A-Za-z]:$') { Note 'Not a whole drive - name a folder.'; $Folder = ''; continue }
    if (Test-EmptyFolder $Folder) { $create = $true; break }
    if (-not (Test-Path -LiteralPath $Folder -PathType Container)) {
        Note "$Folder is a file."; $Folder = ''; continue
    }
    Note "$Folder already has files in it. Setup will not change them."
    $reply = (Read-Host '   Connect ADAM to it as it is? [Y/n]').Trim().ToLower()
    if ($reply -eq '' -or $reply -eq 'y' -or $reply -eq 'yes') { break }
    $Folder = ''
}
$scope = 'user'
$where = ''
if ($Folder -ne 'all') {
    if ($create) {
        $codeName = New-ProjectFolder $Folder $Role $picked
        Good "created $Folder from the $Role starter ($codeName)"
    }
    $scope = 'local'
    $where = Get-TrueCase $Folder
    if (-not $create) { Good "$where (files left as they are)" }
} else {
    Good 'every folder'
}

# ---- 7. put the connector somewhere that stays -------------------------------
Step 'Installing the connector'
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
foreach ($file in ($Files + $Tools)) {
    $from = Join-Path $Here $file
    $to = Join-Path $InstallDir $file
    # Run again from the installed copy, a file is already where it goes.
    if ($from -ine $to) { Copy-Item -LiteralPath $from -Destination $to -Force }
}
$server = Join-Path $InstallDir 'server.mjs'
Good "copied to $InstallDir"

# /update-adam, for every folder rather than only this one.
#
# **This is what makes the zip a first-install-only thing.** The command also
# ships in the project skeleton, but a developer who already has a repository
# never gets that skeleton -- so the one command that keeps a connector current
# would be missing from exactly the folders people actually work in, and the
# answer to "how do I update" would go back to being "ask for the zip again".
#
# User scope: the commands folder under the profile is read in every project.
# Written on every run so an older copy is replaced, and a failure here is a
# Note rather than a stop -- the connector is installed and working, and the
# developer can still run the one line the command wraps.
$commandDir = Join-Path $env:USERPROFILE '.claude/commands'
$commandFrom = Join-Path $Starters 'frontend/.claude/commands/update-adam.md'
if (Test-Path -LiteralPath $commandFrom) {
    try {
        New-Item -ItemType Directory -Force -Path $commandDir | Out-Null
        Copy-Item -LiteralPath $commandFrom -Destination (Join-Path $commandDir 'update-adam.md') -Force
        Good '/update-adam available in every folder'
    } catch {
        Note "could not install /update-adam: $($_.Exception.Message)"
        Note "update with: node ""$(Join-Path $InstallDir 'update.mjs')"""
    }
}

Note 'You can delete the downloaded zip now - Claude Code uses this copy, and'
Note '/update-adam keeps it current from here on.'

# ---- 8. tell Claude Code about it --------------------------------------------
Step 'Registering it with Claude Code'
# Every -e before the --: anything after it is handed to node, which ignores it.
$envArgs = @('-e', "ADAM_VIEWER_URL=$ViewerUrl", '-e', "ADAM_PROJECT=$Project")
if ($scope -eq 'local') { $envArgs += @('-e', "ADAM_WORKDIR=$where") }
$envArgs += @('-e', "ADAM_EMAIL=$Email", '-e', "ADAM_PASSWORD=$password")
$places = @('')
if ($scope -eq 'local') { $places = Get-Spellings $where }

foreach ($place in $places) {
    if ((Invoke-Claude @('mcp', 'remove', $Name, '-s', $scope) $place).Code -eq 0 -and $place -eq $places[0]) {
        Note "replacing the '$Name' connector that was already there"
    }
    $added = Invoke-Claude (@('mcp', 'add', '-s', $scope, $Name) + $envArgs + @('--', 'node', $server)) $place
    if ($added.Code -ne 0) {
        Stop-Setup "Claude Code refused the registration: $($added.Text)"
    }
    # Read back rather than trusted. `claude mcp get` prints the password, so
    # its output is checked here and never shown.
    $details = (Invoke-Claude @('mcp', 'get', $Name) $place).Text
    $envOk = ($details -match 'ADAM_EMAIL=') -and ($details -match 'ADAM_PASSWORD=') -and
             ($details -match 'ADAM_VIEWER_URL=') -and ($details -match ('ADAM_PROJECT=' + [regex]::Escape($Project)))
    $argsOk = $details -match [regex]::Escape('server.mjs')
    if (-not ($envOk -and $argsOk)) {
        Stop-Setup "The connector was registered but does not read back correctly. In that folder, run:  claude mcp get $Name   and send the output (without the password line) to an ADAM admin."
    }
}

$entries = @(Read-Ledger | Where-Object { -not ($_.Scope -eq $scope -and $_.Folder -ieq $where) })
if ($scope -eq 'local') {
    # An every-folder registration would let every other session in too, which
    # is what a folder registration is meant to prevent. An older setup made one.
    if ((Invoke-Claude @('mcp', 'remove', $Name, '-s', 'user')).Code -eq 0) {
        Note "removed the every-folder '$Name' an earlier setup made, so other folders cannot use ADAM"
    }
    $entries = @($entries | Where-Object { $_.Scope -ne 'user' })
} elseif ($scope -eq 'user' -and ((Invoke-Claude @('mcp', 'get', $Name)).Text -notmatch 'User config')) {
    Stop-Setup "A connector called '$Name' already exists outside your user settings. Remove it first with:  claude mcp remove $Name   then run setup again."
}
$entries += [pscustomobject]@{ Scope = $scope; Folder = $where; Project = $Project }
Write-Ledger $entries
if ($scope -eq 'user') { Good "registered as '$Name' for every folder, reading $Project" }
else { Good "registered as '$Name' for $where only, reading $Project" }

# ---- 9. optionally, the full test --------------------------------------------
$run = $Test
if ($run -eq 'ask') {
    Write-Host ''
    Note 'The full connection test signs in and tries all 19 tools against ADAM (about a minute).'
    Note 'If you have connected OpenProject, it also links one of your tasks to a screen or contract and removes the link again,'
    Note 'and proposes a comment on it that it never applies. Nothing in OpenProject changes.'
    $reply = (Read-Host '   Run it now? [y/N]').Trim().ToLower()
    $run = 'no'
    if ($reply -eq 'y' -or $reply -eq 'yes') { $run = 'yes' }
}
if ($run -eq 'yes') {
    Step 'Testing the connection'
    $env:ADAM_VIEWER_URL = $ViewerUrl
    $env:ADAM_PROJECT = $Project
    $env:ADAM_EMAIL = $Email
    $env:ADAM_PASSWORD = $password
    try {
        $ErrorActionPreference = 'Continue'
        & $node.Source (Join-Path $InstallDir 'mcp-check.mjs')
        $testExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = 'Stop'
        Remove-Item Env:ADAM_PASSWORD, Env:ADAM_EMAIL, Env:ADAM_VIEWER_URL, Env:ADAM_PROJECT -ErrorAction SilentlyContinue
    }
    if ($testExit -ne 0) {
        Write-Host ''
        Write-Host '   Some checks failed - the lines marked FAIL above say which. Send them to an ADAM admin.' -ForegroundColor Yellow
    }
}
$password = $null

Write-Host ''
Write-Host 'Done.' -ForegroundColor White
Write-Host ''
if ($scope -eq 'user') {
    Write-Host '  1. Restart Claude Code. Every folder can use ADAM.'
} else {
    Write-Host '  1. Open that folder and start Claude Code there - in VS Code (File > Open Folder),'
    Write-Host '     or in a terminal:' -NoNewline
    Write-Host "  cd `"$where`"; claude" -ForegroundColor Gray
    Write-Host '     Claude Code sessions in any other folder, or in a subfolder of it, cannot use ADAM.'
    if ($create -and $Role -eq 'backend') {
        Write-Host '     Build it once:' -NoNewline
        Write-Host '  dotnet test' -ForegroundColor Gray
    } elseif ($create -and $Role -eq 'frontend') {
        Write-Host '     Install it once:' -NoNewline
        Write-Host '  pnpm install' -ForegroundColor Gray
    }
    if ($create) {
        Write-Host '     CLAUDE.md, .claude\ and project-bible\setup\ tell Claude how this project works.'
        Write-Host '     Shortcuts in Claude Code:  /ticket 6046   /board   /done 6046' -ForegroundColor Gray
    }
}
Write-Host "  2. Store your OpenProject token once, so Claude can see your tickets:"
Write-Host "     $ViewerUrl/settings.html#openproject"
Write-Host '  3. Then ask Claude, for example:'
Write-Host "       What's on my board?" -ForegroundColor Gray
Write-Host '       Pull ticket 6046 into this folder and tell me what it touches.' -ForegroundColor Gray
Write-Host '       I have finished 6046 - propose closing it with a comment.' -ForegroundColor Gray
Write-Host '     Claude shows you any OpenProject change first; nothing changes until you say yes.'
Write-Host ''
Write-Host '  Another folder? Run setup from it.   Changed your ADAM password? Run setup again in each folder.'
Write-Host ''
Write-Host '  Set up now:'
foreach ($entry in (Read-Ledger)) {
    $place = 'every folder'
    if ($entry.Scope -eq 'local') { $place = $entry.Folder }
    Write-Host "     $($entry.Project)  ->  $place" -ForegroundColor Gray
}
Write-Host ''
Show-RemoveHelp (Read-Ledger)
Write-Host ''
exit 0
