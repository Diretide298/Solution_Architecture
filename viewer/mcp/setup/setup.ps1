<#
.SYNOPSIS
    Connects Claude Code on this computer to ADAM.

.DESCRIPTION
    What a developer runs from the connector setup zip, usually by
    double-clicking setup.cmd beside it. It:

      1. checks that Node.js 22+ and Claude Code are installed,
      2. asks for your ADAM email and password (the password is hidden),
      3. checks that they actually sign in to ADAM - before changing anything,
      4. lists the ADAM projects you can open and asks which one to use,
      5. asks which folder that is for - one code folder, or every folder,
      6. copies the connector to %USERPROFILE%\.adam\connector,
      7. registers it with Claude Code for that folder (or for all of them),
      8. and, if you want, runs the full connection test.

    Run it once per folder to give each folder its own ADAM project: a folder
    setting wins over the every-folder one. Running it again for the same
    folder replaces that folder's setting. uninstall.cmd removes all of them.

    ASCII only, on purpose: Windows PowerShell 5.1 reads a script saved without
    a byte-order mark in the machine's ANSI code page, and a dash or a curly
    quote becomes a parse error on somebody else's computer.

.PARAMETER ViewerUrl
    Where ADAM is. Defaults to the live site.

.PARAMETER Email
    Your ADAM sign-in address. Asked for when not given.

.PARAMETER Project
    The ADAM project id (for example ticvai). Asked for when not given.

.PARAMETER Folder
    The code folder this is for. "all" means every folder. Asked for when not given.

.PARAMETER Test
    ask (default), yes or no - whether to run the full connection test at the end.

.PARAMETER Uninstall
    Remove the connector from Claude Code and delete the installed files.

.PARAMETER Name
    The name Claude Code knows the connector by. Leave it as adam.

.PARAMETER InstallDir
    Where the connector files go. Leave it as the default.

.EXAMPLE
    .\setup.ps1

.EXAMPLE
    .\setup.ps1 -Uninstall
#>
param(
    [string]$ViewerUrl = 'https://adam.ainfinite.ai',
    [string]$Email = '',
    [string]$Project = '',
    [string]$Folder = '',
    [ValidateSet('ask', 'yes', 'no')]
    [string]$Test = 'ask',
    [switch]$Uninstall,
    [string]$Name = 'adam',
    [string]$InstallDir = (Join-Path $env:USERPROFILE '.adam\connector')
)

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Files = @('server.mjs', 'client.mjs', 'tools.mjs', 'mcp-check.mjs')
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

# `claude` in PowerShell is usually npm's claude.ps1 wrapper, and PowerShell
# drops a bare `--` on its way into a script - which breaks `claude mcp add`.
# Asking for an Application skips the wrapper and finds claude.cmd or
# claude.exe, which receive every argument as given.
function Find-Claude {
    $found = Get-Command claude -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) { return $found.Source }
    return $null
}

# Every call to claude goes through here, for two reasons.
#
# Windows PowerShell turns anything a program writes to stderr into an error
# record, and under $ErrorActionPreference = 'Stop' the first one ends the
# script. Claude writes ordinary answers there ("No MCP server found"), so
# these calls run with errors as plain text instead.
#
# And the arguments go in as one array. Passed loose through a function, a bare
# `--` is eaten by PowerShell's own parameter binding - the same fault as the
# claude.ps1 wrapper. Splatted to a program as an array, it arrives intact.
function Invoke-Claude([string]$Exe, [string[]]$ArgList) {
    $ErrorActionPreference = 'Continue'
    $lines = & $Exe @ArgList 2>&1 | ForEach-Object { "$_" }
    return [pscustomobject]@{ Code = $LASTEXITCODE; Text = ($lines -join "`n") }
}

function Test-Registered([string]$claude, [string]$serverName) {
    return ((Invoke-Claude $claude @('mcp', 'get', $serverName)).Code -eq 0)
}

# A folder registration is stored by Claude Code against the folder it was made
# in, so adding, reading and removing one all have to run from inside it.
function Invoke-ClaudeIn([string]$Where, [string]$Exe, [string[]]$ArgList) {
    if (-not $Where) { return (Invoke-Claude $Exe $ArgList) }
    Push-Location -LiteralPath $Where
    try { return (Invoke-Claude $Exe $ArgList) } finally { Pop-Location }
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

function Show-RemoveHelp($entries) {
    Write-Host '  To remove it from Claude Code later, double-click uninstall.cmd, or run:'
    foreach ($entry in $entries) {
        if ($entry.Scope -eq 'user') {
            Write-Host "     claude mcp remove $Name -s user" -ForegroundColor Gray
            Write-Host '        (every folder)' -ForegroundColor DarkGray
        } else {
            Write-Host "     cd `"$($entry.Folder)`"; claude mcp remove $Name -s local" -ForegroundColor Gray
            Write-Host '        (that folder only)' -ForegroundColor DarkGray
        }
    }
}

Write-Host ''
Write-Host 'ADAM connector for Claude Code' -ForegroundColor White

# ---- uninstall ---------------------------------------------------------------
if ($Uninstall) {
    Step 'Removing the connector'
    $claude = Find-Claude
    if (-not $claude) {
        Note 'Claude Code is not installed, so there is nothing registered to remove.'
    } else {
        # Every folder setup registered, then the every-folder one - which is
        # removed whether or not the ledger knows about it.
        foreach ($entry in (Read-Ledger | Where-Object { $_.Scope -eq 'local' })) {
            if (-not (Test-Path -LiteralPath $entry.Folder)) {
                Note "skipped $($entry.Folder) - that folder no longer exists"
                continue
            }
            $gone = Invoke-ClaudeIn $entry.Folder $claude @('mcp', 'remove', $Name, '-s', 'local')
            if ($gone.Code -eq 0) { Good "removed '$Name' from $($entry.Folder)" }
            else { Note "nothing to remove in $($entry.Folder)" }
        }
        $gone = Invoke-Claude $claude @('mcp', 'remove', $Name, '-s', 'user')
        if ($gone.Code -eq 0) { Good "removed the every-folder '$Name'" }
        if (Test-Registered $claude $Name) {
            Note "'$Name' is still registered for this folder. Remove it with:  claude mcp remove $Name"
        }
    }
    if (Test-Path -LiteralPath $InstallDir) {
        Remove-Item -LiteralPath $InstallDir -Recurse -Force
        Good "deleted $InstallDir"
    }
    Write-Host ''
    Write-Host 'Done. Restart Claude Code for the change to show.' -ForegroundColor White
    Write-Host ''
    exit 0
}

# ---- 1. what this computer needs -----------------------------------------------
Step 'Checking this computer'

foreach ($file in $Files) {
    if (-not (Test-Path -LiteralPath (Join-Path $Here $file))) {
        Stop-Setup "$file is missing next to this script. Unzip the whole folder first, then run setup.cmd from inside it."
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

$claude = Find-Claude
if (-not $claude) {
    Stop-Setup 'Claude Code is not installed. Install it with:  npm install -g @anthropic-ai/claude-code   then open a new window and run setup again.'
}
$claudeVersion = ((Invoke-Claude $claude @('--version')).Text -split "`n")[0]
Good "Claude Code $claudeVersion"

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

# Windows PowerShell 5.1 does not escape a double quote inside an argument it
# passes to a program, so a password containing one arrives cut in two and the
# registration fails. A trailing backslash can swallow the closing quote the
# same way. Refused here, with the reason, rather than failing further on.
if ($password.Contains('"')) {
    Stop-Setup 'Your ADAM password contains a double quote ("), which Windows PowerShell cannot pass on intact. Change your ADAM password to one without quotes (Settings -> Password), then run setup again.'
}
if ($password.EndsWith('\')) {
    Stop-Setup 'Your ADAM password ends with a backslash (\), which Windows PowerShell cannot pass on intact. Change your ADAM password (Settings -> Password), then run setup again.'
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

# ---- 5. which folder ------------------------------------------------------------
Step 'Choosing the folder'
Note 'Claude Code uses this project when you start it in the folder you give here.'
Note 'Paste the path of your code folder, or press Enter to use it in every folder.'
while ($true) {
    if (-not $Folder) {
        $Folder = (Read-Host '   Folder (Enter = every folder)').Trim().Trim('"')
        if (-not $Folder) { $Folder = 'all' }
    }
    if ($Folder -eq 'all') { break }
    if (Test-Path -LiteralPath $Folder -PathType Container) {
        $Folder = (Resolve-Path -LiteralPath $Folder).ProviderPath.TrimEnd('\')
        break
    }
    Note "There is no folder at $Folder."
    $Folder = ''
}
$scope = 'user'
$where = ''
if ($Folder -ne 'all') { $scope = 'local'; $where = $Folder }
if ($scope -eq 'user') { Good 'every folder' } else { Good $Folder }

# ---- 6. put the connector somewhere that stays -------------------------------
Step 'Installing the connector'
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
foreach ($file in $Files) {
    Copy-Item -LiteralPath (Join-Path $Here $file) -Destination (Join-Path $InstallDir $file) -Force
}
$server = Join-Path $InstallDir 'server.mjs'
Good "copied to $InstallDir"
Note 'You can delete the downloaded zip now - Claude Code uses this copy.'

# ---- 7. tell Claude Code about it --------------------------------------------
Step 'Registering it with Claude Code'
# Only the entry at this scope is replaced. A folder entry wins over the
# every-folder one, so the two can hold different projects side by side.
$gone = Invoke-ClaudeIn $where $claude @('mcp', 'remove', $Name, '-s', $scope)
if ($gone.Code -eq 0) { Note "replacing the '$Name' connector that was already there" }
if ($scope -eq 'user' -and (Test-Registered $claude $Name)) {
    Stop-Setup "A connector called '$Name' already exists outside your user settings. Remove it first with:  claude mcp remove $Name   then run setup again."
}

# Every -e before the --: anything after it is handed to node, which ignores it.
# A folder registration also names the folder, which is where adam_pull writes
# .adam/ when Claude does not say.
$addArgs = @('mcp', 'add', '-s', $scope, $Name,
    '-e', "ADAM_VIEWER_URL=$ViewerUrl",
    '-e', "ADAM_PROJECT=$Project")
if ($scope -eq 'local') { $addArgs += @('-e', "ADAM_WORKDIR=$where") }
$addArgs += @('-e', "ADAM_EMAIL=$Email", '-e', "ADAM_PASSWORD=$password", '--', 'node', $server)
$added = Invoke-ClaudeIn $where $claude $addArgs
if ($added.Code -ne 0) {
    Stop-Setup "Claude Code refused the registration: $($added.Text)"
}

# Read back rather than trusted. `claude mcp get` prints the password, so its
# output is checked here and never shown.
$details = (Invoke-ClaudeIn $where $claude @('mcp', 'get', $Name)).Text
$envOk = ($details -match 'ADAM_EMAIL=') -and ($details -match 'ADAM_PASSWORD=') -and
         ($details -match 'ADAM_VIEWER_URL=') -and ($details -match ('ADAM_PROJECT=' + [regex]::Escape($Project)))
$argsOk = $details -match [regex]::Escape('server.mjs')
if (-not ($envOk -and $argsOk)) {
    Stop-Setup "The connector was registered but does not read back correctly. Run:  claude mcp get $Name   and send the output (without the password line) to an ADAM admin."
}
$entries = @(Read-Ledger | Where-Object { -not ($_.Scope -eq $scope -and $_.Folder -eq $where) })
$entries += [pscustomobject]@{ Scope = $scope; Folder = $where; Project = $Project }
Write-Ledger $entries
if ($scope -eq 'user') { Good "registered as '$Name' for every folder, reading $Project" }
else { Good "registered as '$Name' for $where, reading $Project" }

# ---- 8. optionally, the full test --------------------------------------------
$run = $Test
if ($run -eq 'ask') {
    Write-Host ''
    Note 'The full connection test signs in and tries all 16 tools against ADAM (about a minute).'
    Note 'If you have connected OpenProject, it also links one of your tasks to a screen and removes the link again,'
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
    Write-Host '  1. Restart Claude Code (or start a new session).'
} else {
    Write-Host '  1. Start Claude Code in that folder:'
    Write-Host "     cd `"$where`"; claude" -ForegroundColor Gray
}
Write-Host "  2. Store your OpenProject token once, so Claude can see your tickets:"
Write-Host "     $ViewerUrl/settings.html#openproject"
Write-Host '  3. Then ask Claude, for example:'
Write-Host "       What's on my board?" -ForegroundColor Gray
Write-Host '       Pull ticket 6046 into this folder and tell me what it touches.' -ForegroundColor Gray
Write-Host '       I have finished 6046 - propose closing it with a comment.' -ForegroundColor Gray
Write-Host '     Claude shows you any OpenProject change first; nothing changes until you say yes.'
Write-Host ''
Write-Host '  Another folder or project? Run setup again.   Changed your ADAM password? Run setup again.'
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
