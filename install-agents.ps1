# Install Claude SEO Master Skills into one or more AI coding agents (Windows).
#
#   powershell -ExecutionPolicy Bypass -File install-agents.ps1 -Tool claude,codex,cursor,antigravity,kiro
#   powershell -ExecutionPolicy Bypass -File install-agents.ps1 -Tool all
#   powershell -ExecutionPolicy Bypass -File install-agents.ps1 -Tool cursor -Project C:\code\my-site
#
# Same layout as install-agents.sh: one shared runtime in $HOME\.seo-master and
# a copy of the skills in each tool's skills folder. On Windows the skills call
# the runtime with "python ...\runtime.py" because PowerShell cannot run the
# bash launcher directly.
param(
    [Parameter(Mandatory = $true)][string[]]$Tool,
    [string]$Project = "",
    [switch]$NoSetup
)
$ErrorActionPreference = 'Stop'
$Src = Split-Path -Parent $MyInvocation.MyCommand.Path
$HomeDir = if ($env:SEO_MASTER_HOME) { $env:SEO_MASTER_HOME } else { Join-Path $HOME '.seo-master' }
# -File passes "codex,cursor" as one string, so split on commas too.
$Tool = @($Tool | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
if ($Tool -contains 'all') { $Tool = @('claude', 'codex', 'cursor', 'antigravity', 'kiro') }

function Get-SkillsDir([string]$Name) {
    if ($Project) {
        $map = @{ claude = '.claude'; codex = '.codex'; cursor = '.cursor'; antigravity = '.agent'; kiro = '.kiro'; agents = '.agents' }
        if (-not $map.ContainsKey($Name)) { throw "Unknown tool: $Name" }
        return Join-Path (Join-Path $Project $map[$Name]) 'skills'
    }
    $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
    $map = @{
        claude = Join-Path $HOME '.claude'; codex = $codexHome; cursor = Join-Path $HOME '.cursor'
        antigravity = Join-Path $HOME '.gemini\antigravity'; kiro = Join-Path $HOME '.kiro'; agents = Join-Path $HOME '.agents'
    }
    if (-not $map.ContainsKey($Name)) { throw "Unknown tool: $Name (use claude, codex, cursor, antigravity, kiro, agents, all)" }
    return Join-Path $map[$Name] 'skills'
}

Write-Host ">> Installing shared runtime into $HomeDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $HomeDir | Out-Null
foreach ($item in 'scripts', 'schema', 'data', 'skills', 'extensions', 'hooks', '.claude-plugin', 'requirements.txt', 'pyproject.toml', 'LICENSE') {
    $p = Join-Path $Src $item
    if (Test-Path $p) { Copy-Item -Recurse -Force $p $HomeDir }
}

$rt = if ($HomeDir.StartsWith($HOME)) { '$HOME' + $HomeDir.Substring($HOME.Length).Replace('\', '/') } else { $HomeDir.Replace('\', '/') }
$launcher = 'python "' + $rt + '/scripts/runtime.py"'

function Convert-Text([string]$Text) {
    $Text = $Text.Replace('"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo"', $launcher)
    return $Text.Replace('${CLAUDE_PLUGIN_ROOT}', $rt)
}

foreach ($t in $Tool) {
    $dest = Get-SkillsDir $t
    Write-Host ">> $t" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    $count = 0
    foreach ($skill in Get-ChildItem -Directory (Join-Path $Src 'skills')) {
        $target = Join-Path $dest $skill.Name
        if (Test-Path $target) { Remove-Item -Recurse -Force $target }
        Copy-Item -Recurse $skill.FullName $target
        foreach ($md in Get-ChildItem -Recurse -File -Filter *.md $target) {
            $text = [IO.File]::ReadAllText($md.FullName)
            [IO.File]::WriteAllText($md.FullName, (Convert-Text $text), (New-Object Text.UTF8Encoding($false)))
        }
        $count++
    }
    Write-Host "   $count skills -> $dest"
    if ($t -eq 'claude') {
        $agents = Join-Path (Split-Path -Parent $dest) 'agents'
        New-Item -ItemType Directory -Force -Path $agents | Out-Null
        foreach ($a in Get-ChildItem -File -Filter *.md (Join-Path $Src 'agents')) {
            $text = [IO.File]::ReadAllText($a.FullName)
            [IO.File]::WriteAllText((Join-Path $agents $a.Name), (Convert-Text $text), (New-Object Text.UTF8Encoding($false)))
        }
        Write-Host "   agents -> $agents"
    }
}

if (-not $NoSetup) {
Write-Host ">> Preparing the Python runtime (one time, about 2 minutes)" -ForegroundColor Yellow
& python (Join-Path $HomeDir 'scripts\runtime.py') setup
if ($LASTEXITCODE -ne 0) { Write-Host "   Runtime setup did not finish. Run later: python `"$HomeDir\scripts\runtime.py`" setup" -ForegroundColor Red }
}

Write-Host ""
Write-Host "Done. Restart the tool, then ask it: Run an SEO audit of https://yoursite.com" -ForegroundColor Green
Write-Host "In Claude Code you can also type:    /seo audit https://yoursite.com"
Write-Host "Each audit writes SEO-Report.pdf and FIX-PROMPTS.md into <domain>-audit/."
