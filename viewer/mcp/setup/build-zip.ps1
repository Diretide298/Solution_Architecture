<#
.SYNOPSIS
    Builds adam-connector-setup.zip - the file you hand a developer.

.DESCRIPTION
    Collects the connector (server.mjs, client.mjs, tools.mjs, mcp-check.mjs)
    and the setup scripts into one folder, stamps the build into the README,
    and zips it. The zip contains no passwords, tokens or addresses of anybody
    in particular - it is the same file for everyone.

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
$folder = Join-Path $stage 'adam-connector'
New-Item -ItemType Directory -Force -Path $folder | Out-Null

try {
    foreach ($file in 'server.mjs', 'client.mjs', 'tools.mjs', 'mcp-check.mjs') {
        Copy-Item -LiteralPath (Join-Path $Mcp $file) -Destination $folder
    }
    Copy-Item -LiteralPath (Join-Path $Here 'setup.ps1') -Destination $folder

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
    & $crlf (Join-Path $Here 'setup.cmd') (Join-Path $folder 'setup.cmd') $build
    & $crlf (Join-Path $Here 'uninstall.cmd') (Join-Path $folder 'uninstall.cmd') $build
    & $crlf (Join-Path $Here 'README.txt') (Join-Path $folder 'README.txt') $build

    # The setup script must be plain ASCII (see its header) - checked, not hoped.
    foreach ($file in Get-ChildItem -LiteralPath $folder -File) {
        if ($file.Extension -in '.ps1', '.cmd', '.txt') {
            $bytes = [IO.File]::ReadAllBytes($file.FullName)
            if ($bytes | Where-Object { $_ -gt 127 }) {
                throw "$($file.Name) contains non-ASCII characters; Windows PowerShell 5.1 would misread it."
            }
        }
    }

    if (Test-Path -LiteralPath $Out) { Remove-Item -LiteralPath $Out -Force }
    Compress-Archive -Path $folder -DestinationPath $Out
    $size = [math]::Round((Get-Item -LiteralPath $Out).Length / 1KB)
    Write-Host "built $Out ($size KB) - $build"
} finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
}
