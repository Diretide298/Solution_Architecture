<#
.SYNOPSIS
    Connects Claude Code on this computer to ADAM, for one code folder.

.DESCRIPTION
    What a developer runs from the connector setup zip. Run it from the code
    folder whose Claude Code sessions should use ADAM:

        cd C:\work\ticvai-backend
        C:\Downloads\adam-connector\setup.cmd

    It:
      1. checks that Node.js 22+ and Claude Code are installed,
      2. asks for your ADAM email and password (the password is hidden),
      3. checks that they actually sign in to ADAM - before changing anything,
      4. lists the ADAM projects you can open and asks which one to use,
      5. asks which folder it is for - the folder it was started from by default,
      6. copies the connector to %USERPROFILE%\.adam\connector,
      7. registers it with Claude Code for that folder only,
      8. and, if you want, runs the full connection test.

    Only Claude Code sessions opened in that folder - in VS Code or a terminal -
    can use ADAM. Every folder is possible, but only when asked for ("all").
    Run it again from another folder to add that one; running it again for the
    same folder replaces that folder's setting. uninstall.cmd removes them all.

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
    The code folder this is for, or "all" for every folder. Asked for when not given.

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
    cd C:\work\ticvai-backend; C:\Downloads\adam-connector\setup.cmd

.EXAMPLE
    .\setup.ps1 -RemoveFolder C:\work\ticvai-backend

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
    [string]$RemoveFolder = '',
    [string]$Name = 'adam',
    [string]$InstallDir = (Join-Path $env:USERPROFILE '.adam\connector')
)

$ErrorActionPreference = 'Stop'
# Where setup was started from, before anything moves: the folder a developer
# ran it in is the folder they mean. Double-clicked, it is the zip's own folder,
# which is never a code folder, so then there is no default.
$LaunchDir = (Get-Location).ProviderPath
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Files = @('server.mjs', 'client.mjs', 'tools.mjs', 'mcp-check.mjs')
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
function Find-Claude {
    $all = @(Get-Command claude -CommandType Application -All -ErrorAction SilentlyContinue)
    $exe = $all | Where-Object { $_.Source -like '*.exe' } | Select-Object -First 1
    if ($exe) { return [pscustomobject]@{ Path = $exe.Source; Safe = $true } }
    foreach ($shim in $all) {
        $inner = Join-Path (Split-Path -Parent $shim.Source) 'node_modules\@anthropic-ai\claude-code\bin\claude.exe'
        if (Test-Path -LiteralPath $inner) { return [pscustomobject]@{ Path = $inner; Safe = $true } }
    }
    if ($all.Count) { return [pscustomobject]@{ Path = $all[0].Source; Safe = $false } }
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

Write-Host ''
Write-Host 'ADAM connector for Claude Code' -ForegroundColor White
$script:Claude = Find-Claude

# ---- removing ------------------------------------------------------------------
if ($Uninstall -or $RemoveFolder) {
    if (-not $script:Claude) { Stop-Setup 'Claude Code is not installed, so there is nothing registered to remove.' }
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
$claudeVersion = ((Invoke-Claude @('--version')).Text -split "`n")[0]
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

# ---- 5. which folder ------------------------------------------------------------
Step 'Choosing the folder'
# The folder setup was started from, unless that is somewhere no code lives.
$default = ''
$launch = $LaunchDir.TrimEnd('\')
$notCode = @($Here, $InstallDir, $env:USERPROFILE, $env:windir) | ForEach-Object { "$_".TrimEnd('\') }
if ($launch -and -not ($notCode -contains $launch) -and -not $launch.StartsWith("$env:windir\", 'OrdinalIgnoreCase') -and
        $launch -notmatch '^[A-Za-z]:$') {
    $default = $launch
}
Note 'Only Claude Code sessions opened in this folder - in VS Code or a terminal - will be able to use ADAM.'
if ($default) { Note 'Press Enter for the folder shown, paste another path, or type all for every folder.' }
else { Note 'Paste the path of your code folder, or type all for every folder.' }
while ($true) {
    if (-not $Folder) {
        if ($default) {
            $Folder = (Read-Host "   Folder [$default]").Trim().Trim('"')
            if (-not $Folder) { $Folder = $default }
        } else {
            $Folder = (Read-Host '   Folder').Trim().Trim('"')
            if (-not $Folder) { continue }
        }
    }
    if ($Folder -eq 'all') { break }
    if (Test-Path -LiteralPath $Folder -PathType Container) {
        $Folder = Get-TrueCase $Folder
        break
    }
    Note "There is no folder at $Folder."
    $Folder = ''
}
$scope = 'user'
$where = ''
if ($Folder -ne 'all') { $scope = 'local'; $where = $Folder }
if ($scope -eq 'user') { Good 'every folder' } else { Good $where }

# ---- 6. put the connector somewhere that stays -------------------------------
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
Note 'You can delete the downloaded zip now - Claude Code uses this copy.'

# ---- 7. tell Claude Code about it --------------------------------------------
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
    Write-Host '  1. Restart Claude Code. Every folder can use ADAM.'
} else {
    Write-Host '  1. Open that folder and start Claude Code there - in VS Code (File > Open Folder),'
    Write-Host '     or in a terminal:' -NoNewline
    Write-Host "  cd `"$where`"; claude" -ForegroundColor Gray
    Write-Host '     Claude Code sessions in any other folder, or in a subfolder of it, cannot use ADAM.'
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
