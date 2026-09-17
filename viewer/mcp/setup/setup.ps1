<#
.SYNOPSIS
    Connects Claude Code on this computer to ADAM.

.DESCRIPTION
    What a developer runs from the connector setup zip, usually by
    double-clicking setup.cmd beside it. It:

      1. checks that Node.js 22+ and Claude Code are installed,
      2. asks for your ADAM email and password (the password is hidden),
      3. checks that they actually sign in to ADAM - before changing anything,
      4. copies the connector to %USERPROFILE%\.adam\connector,
      5. registers it with Claude Code for every project you open,
      6. and, if you want, runs the full connection test.

    Running it again is how you update the connector or change the password.
    uninstall.cmd removes it.

    ASCII only, on purpose: Windows PowerShell 5.1 reads a script saved without
    a byte-order mark in the machine's ANSI code page, and a dash or a curly
    quote becomes a parse error on somebody else's computer.

.PARAMETER ViewerUrl
    Where ADAM is. Defaults to the live site.

.PARAMETER Email
    Your ADAM sign-in address. Asked for when not given.

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

Write-Host ''
Write-Host 'ADAM connector for Claude Code' -ForegroundColor White

# ---- uninstall ---------------------------------------------------------------
if ($Uninstall) {
    Step 'Removing the connector'
    $claude = Find-Claude
    if ($claude -and (Test-Registered $claude $Name)) {
        $gone = Invoke-Claude $claude @('mcp', 'remove', $Name, '-s', 'user')
        if ($gone.Code -eq 0) { Good "removed '$Name' from Claude Code" }
        else { Note "Claude Code would not remove '$Name' - run: claude mcp remove $Name -s user" }
    } else {
        Note "'$Name' was not registered with Claude Code"
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
# Not left open: this check is the only thing that session was for.
try {
    $null = Invoke-WebRequest -Uri "$ViewerUrl/api/auth/logout" -Method Post -UseBasicParsing `
        -WebSession $session -TimeoutSec 15
} catch { }

# ---- 4. put the connector somewhere that stays -------------------------------
Step 'Installing the connector'
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
foreach ($file in $Files) {
    Copy-Item -LiteralPath (Join-Path $Here $file) -Destination (Join-Path $InstallDir $file) -Force
}
$server = Join-Path $InstallDir 'server.mjs'
Good "copied to $InstallDir"
Note 'You can delete the downloaded zip now - Claude Code uses this copy.'

# ---- 5. tell Claude Code about it --------------------------------------------
Step 'Registering it with Claude Code'
if (Test-Registered $claude $Name) {
    $gone = Invoke-Claude $claude @('mcp', 'remove', $Name, '-s', 'user')
    if ($gone.Code -eq 0) {
        Note "replacing the '$Name' connector that was already there"
    } else {
        Stop-Setup "A connector called '$Name' already exists outside your user settings. Remove it first with:  claude mcp remove $Name   then run setup again."
    }
}

# Every -e before the --: anything after it is handed to node, which ignores it.
$added = Invoke-Claude $claude @(
    'mcp', 'add', '-s', 'user', $Name,
    '-e', "ADAM_VIEWER_URL=$ViewerUrl",
    '-e', "ADAM_EMAIL=$Email",
    '-e', "ADAM_PASSWORD=$password",
    '--', 'node', $server)
if ($added.Code -ne 0) {
    Stop-Setup "Claude Code refused the registration: $($added.Text)"
}

# Read back rather than trusted. `claude mcp get` prints the password, so its
# output is checked here and never shown.
$details = (Invoke-Claude $claude @('mcp', 'get', $Name)).Text
$envOk = ($details -match 'ADAM_EMAIL=') -and ($details -match 'ADAM_PASSWORD=') -and ($details -match 'ADAM_VIEWER_URL=')
$argsOk = $details -match [regex]::Escape('server.mjs')
if (-not ($envOk -and $argsOk)) {
    Stop-Setup "The connector was registered but does not read back correctly. Run:  claude mcp get $Name   and send the output (without the password line) to an ADAM admin."
}
Good "registered as '$Name', for every project you open"

# ---- 6. optionally, the full test --------------------------------------------
$run = $Test
if ($run -eq 'ask') {
    Write-Host ''
    Note 'The full connection test signs in and tries all 13 tools against ADAM (about a minute).'
    Note 'If you have connected OpenProject, it also links one of your tasks to a screen and removes the link again.'
    $reply = (Read-Host '   Run it now? [y/N]').Trim().ToLower()
    $run = 'no'
    if ($reply -eq 'y' -or $reply -eq 'yes') { $run = 'yes' }
}
if ($run -eq 'yes') {
    Step 'Testing the connection'
    $env:ADAM_VIEWER_URL = $ViewerUrl
    $env:ADAM_EMAIL = $Email
    $env:ADAM_PASSWORD = $password
    try {
        $ErrorActionPreference = 'Continue'
        & $node.Source (Join-Path $InstallDir 'mcp-check.mjs')
        $testExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = 'Stop'
        Remove-Item Env:ADAM_PASSWORD, Env:ADAM_EMAIL, Env:ADAM_VIEWER_URL -ErrorAction SilentlyContinue
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
Write-Host '  1. Restart Claude Code (or start a new session).'
Write-Host "  2. Ask it:  What's on my board?"
Write-Host "  3. To see your OpenProject work too, store your token at:"
Write-Host "     $ViewerUrl/settings.html#openproject"
Write-Host ''
Write-Host '  Changed your ADAM password? Run setup again.   To remove: uninstall.cmd'
Write-Host ''
exit 0
