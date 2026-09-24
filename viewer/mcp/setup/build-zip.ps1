<#
.SYNOPSIS
    Builds adam-connector-setup.zip - the file you hand a developer.

.DESCRIPTION
    The zip opens to one folder, adam-setup\:

        adam-setup\
          setup.cmd          what the developer runs
          uninstall.cmd
          README.txt
          adam-connector\    the connector (server.mjs, client.mjs, tools.mjs,
                             mcp-check.mjs), setup.ps1, and starters\ - the
                             backend and frontend skeletons and the coding
                             standards setup copies into a new project folder

    The build is stamped into the README. The zip contains no passwords, tokens
    or addresses of anybody in particular - it is the same file for everyone.

    Rebuild it whenever anything in viewer/mcp changes, and send the new one
    round: running its setup.cmd replaces the installed copy.

    Run from anywhere:
        powershell -ExecutionPolicy Bypass -File viewer\mcp\setup\build-zip.ps1

.PARAMETER Out
    Where to write the zip. Defaults to the repository root.
#>
param(
    [string]$Out = ''
)

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path     # viewer\mcp\setup
$Mcp = Split-Path -Parent $Here                              # viewer\mcp
$Repo = Split-Path -Parent (Split-Path -Parent $Mcp)         # the repository root
if (-not $Out) { $Out = Join-Path $Repo 'adam-connector-setup.zip' }

$stage = Join-Path ([IO.Path]::GetTempPath()) ("adam-connector-" + [guid]::NewGuid().ToString('N'))
$top = Join-Path $stage 'adam-setup'
$folder = Join-Path $top 'adam-connector'
New-Item -ItemType Directory -Force -Path $folder | Out-Null

try {
    # The same six files `mcp/version.mjs` hashes, and it has to stay the same
    # six: the build id is computed from this set on both sides, so a file
    # shipped here and not listed there -- or the other way round -- makes every
    # install read as out of date forever.
    foreach ($file in 'server.mjs', 'client.mjs', 'tools.mjs', 'mcp-check.mjs',
                      'version.mjs', 'update.mjs') {
        Copy-Item -LiteralPath (Join-Path $Mcp $file) -Destination $folder
    }
    Copy-Item -LiteralPath (Join-Path $Here 'setup.ps1') -Destination $folder

    # The starters, without anything a build or an install left behind.
    $skip = '\\(bin|obj|node_modules|\.nx|dist|coverage|TestResults|\.vs)(\\|$)'
    $starters = Join-Path $Here 'starters'
    foreach ($item in Get-ChildItem -LiteralPath $starters -Recurse -Force -File) {
        $relative = $item.FullName.Substring($starters.Length)
        if ($relative -match $skip -or $item.Name -like '*.user') { continue }
        $target = Join-Path (Join-Path $folder 'starters') $relative
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $item.FullName -Destination $target
    }

    # Which build this is, so "which version do you have" has an answer.
    $commit = ''
    try { $commit = (& git -C $Repo rev-parse --short HEAD 2>$null).Trim() } catch { }
    $dirty = ''
    try {
        $changes = & git -C $Repo status --porcelain -- viewer/mcp 2>$null
        if ($changes) { $dirty = ' + uncommitted changes' }
    } catch { }
    $build = (Get-Date -Format 'yyyy-MM-dd') + $(if ($commit) { ", commit $commit$dirty" } else { '' })

    # Windows line endings for what people open in Notepad or run with cmd.
    $crlf = {
        param([string]$source, [string]$target, [string]$stamp)
        $text = [IO.File]::ReadAllText($source)
        $text = $text.Replace('{{BUILD}}', $stamp)
        $text = ($text -replace "`r`n", "`n") -replace "`n", "`r`n"
        [IO.File]::WriteAllText($target, $text, (New-Object System.Text.UTF8Encoding($false)))
    }
    # The launchers at the top, where the developer looks, and beside setup.ps1,
    # where setup copies them from when it installs itself.
    foreach ($place in $top, $folder) {
        & $crlf (Join-Path $Here 'setup.cmd') (Join-Path $place 'setup.cmd') $build
        & $crlf (Join-Path $Here 'uninstall.cmd') (Join-Path $place 'uninstall.cmd') $build
    }
    & $crlf (Join-Path $Here 'README.txt') (Join-Path $top 'README.txt') $build

    # The setup script must be plain ASCII (see its header) - checked, not hoped.
    foreach ($file in @(Get-ChildItem -LiteralPath $top -File) + @(Get-ChildItem -LiteralPath $folder -File)) {
        if ($file.Extension -in '.ps1', '.cmd', '.txt') {
            $bytes = [IO.File]::ReadAllBytes($file.FullName)
            if ($bytes | Where-Object { $_ -gt 127 }) {
                throw "$($file.Name) contains non-ASCII characters; Windows PowerShell 5.1 would misread it."
            }
        }
    }

    # Written with forward slashes and every dot-file kept, which
    # Compress-Archive on Windows PowerShell 5.1 does not promise.
    if (Test-Path -LiteralPath $Out) { Remove-Item -LiteralPath $Out -Force }
    Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::Open($Out, 'Create')
    try {
        foreach ($item in Get-ChildItem -LiteralPath $top -Recurse -Force -File) {
            $entry = 'adam-setup/' + $item.FullName.Substring($top.Length + 1).Replace('\', '/')
            [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $item.FullName, $entry, 'Optimal')
        }
    } finally {
        $zip.Dispose()
    }
    $size = [math]::Round((Get-Item -LiteralPath $Out).Length / 1KB)
    Write-Host "built $Out ($size KB) - $build"
} finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
}
