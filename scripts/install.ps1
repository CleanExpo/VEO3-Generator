# Claude Orchestrator Installation Script - Windows
# Idempotent copy-in with discovery, diff reporting, smart merging, and safety

param(
  [switch]$Force,
  [switch]$SkipDetection,
  [switch]$DryRun,
  [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$host.ui.RawUI.WindowTitle = "Claude Orchestrator Installer"

Write-Host "=== Claude Orchestrator Installer (Windows) ===" -ForegroundColor Cyan

# ExecutionPolicy helper (session-only)
try {
  $currentPolicy = Get-ExecutionPolicy -Scope Process
  if ($currentPolicy -eq "Undefined") {
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  }
} catch {
  Write-Host "⚠ Unable to adjust ExecutionPolicy for this session. You may need to run PowerShell as Administrator." -ForegroundColor Yellow
}

# Paths
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot    = Split-Path -Parent $ScriptDir
$TemplateDir = Join-Path $RepoRoot "templates\.claude"
$TargetDir   = ".\.claude"
$DiffDir     = "$TargetDir\_install-diff"
$LogPath     = Join-Path $DiffDir "install.log"

# Logging helper
function Write-Log {
  param([string]$Message)
  if (!(Test-Path $DiffDir)) { New-Item -ItemType Directory -Path $DiffDir | Out-Null }
  ("[{0}] {1}" -f (Get-Date -Format "u"), $Message) | Out-File $LogPath -Append -Encoding utf8
  if ($Verbose) { Write-Host "• $Message" -ForegroundColor DarkGray }
}

Write-Host "`nChecking prerequisites..." -ForegroundColor Yellow

# PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5) {
  Write-Host "✗ PowerShell 5.0+ required" -ForegroundColor Red
  exit 1
} else {
  Write-Host "✓ PowerShell $($PSVersionTable.PSVersion)" -ForegroundColor Green
}

# Node.js (optional but recommended)
try {
  $nodeVersion = node --version 2>$null
  Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
  Write-Host "⚠ Node.js not found - MCP servers and Playwright may not work" -ForegroundColor Yellow
  Write-Host "  Install from: https://nodejs.org" -ForegroundColor Gray
}

Write-Host ""

# Detect Playwright (namespaced, never overwrite)
function Detect-Playwright {
  $has = $false
  if (Test-Path "package.json") {
    try {
      $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
      $has = ($pkg.dependencies.playwright -or $pkg.devDependencies.playwright `
           -or $pkg.dependencies."@playwright/test" -or $pkg.devDependencies."@playwright/test")
    } catch { $has = $false }
  }
  return $has
}

# Discover MCP servers by scanning .claude/mcp + common paths
function Discover-MCP {
  $servers = @()
  $candidateDirs = @(".\.claude\mcp", ".\mcp", ".\config\mcp")
  foreach ($dir in $candidateDirs) {
    if (Test-Path $dir) {
      Get-ChildItem -Path $dir -Filter *.json -File -Recurse | ForEach-Object {
        try {
          $json = Get-Content $_.FullName -Raw | ConvertFrom-Json
          $name = if ($json.name) { $json.name } else { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) }
          $servers += @{ name=$name; path=$_.FullName }
        } catch { }
      }
    }
  }
  return $servers | Sort-Object -Property name -Unique
}

# Append/refresh MCP registry block between markers in claude.md
function Update-RegistryBlock {
  param([string]$ClaudePath, [array]$Servers)
  if (!(Test-Path $ClaudePath)) { return }

  $content = Get-Content $ClaudePath -Raw
  $begin = "# BEGIN-AUTO-REGISTRY"
  $end   = "# END-AUTO-REGISTRY"

  $lines = @()
  $lines += ""
  $lines += $begin
  $lines += "# Auto-generated agent & MCP registry - do not edit between markers"
  $lines += "# Agents:"
  $lines += "# - @coder, @tester, @research, @integrator, @stuck"
  $lines += "# - @master-fullstack, @master-devops, @master-docs, @master-data"
  $lines += "# MCP Servers:"
  foreach ($s in $Servers) { $lines += "# - $($s.name) -> $($s.path)" }
  $lines += $end
  $block = ($lines -join "`r`n")

  if ($content -notmatch [regex]::Escape($begin)) {
    $content = $content + "`r`n" + $block + "`r`n"
  } else {
    $pattern = "(?s)$([regex]::Escape($begin)).*?$([regex]::Escape($end))"
    $content = [regex]::Replace($content, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block })
  }

  if (-not $DryRun) {
    $content | Set-Content $ClaudePath -Encoding utf8
  }
  Write-Log "Updated registry block in claude.md"
}

# Smart copy with .new + .diff (idempotent)
function Copy-SmartFile {
  param(
    [string]$Source,
    [string]$Target,
    [string]$RelPath,
    [switch]$SkipIfPlaywright
  )

  # Skip overwriting Playwright core config/tests if user already has Playwright
  if ($SkipIfPlaywright -and (Detect-Playwright)) {
    # Only allow namespaced E2E templates to be added, not core config files
    $isCore = $RelPath -match "(?i)playwright\.config\.(js|ts|mjs|cjs)$" -or $RelPath -match "(?i)^tests[\\/](e2e|playwright)[\\/]"
    if ($isCore) {
      Write-Host "  ↷ $RelPath (Playwright detected; core preserved)" -ForegroundColor Cyan
      Write-Log "Skipped Playwright core: $RelPath"
      return "skipped"
    }
  }

  $targetExists = Test-Path $Target
  if ($DryRun) {
    $action = if ($targetExists) { "compare" } else { "create" }
    Write-Host "  (dry-run) $action $RelPath" -ForegroundColor DarkGray
    Write-Log "(dry-run) $action $RelPath"
    return (if ($targetExists) { "same" } else { "created" })
  }

  if (!$targetExists) {
    $targetParent = Split-Path -Parent $Target
    if (!(Test-Path $targetParent)) { New-Item -ItemType Directory -Path $targetParent -Force | Out-Null }
    Copy-Item $Source $Target
    Write-Host "  + $RelPath" -ForegroundColor Green
    Write-Log "Created $RelPath"
    return "created"
  } else {
    $newFile = "$Target.new"
    Copy-Item $Source $newFile

    $diffFile = Join-Path $DiffDir "$RelPath.diff"
    $diffParent = Split-Path -Parent $diffFile
    if (!(Test-Path $diffParent)) { New-Item -ItemType Directory -Path $diffParent -Force | Out-Null }

    $sourceContent = Get-Content $Source -Raw
    $targetContent = Get-Content $Target -Raw

    if ($sourceContent -ne $targetContent) {
      "=== $RelPath ===" | Out-File $diffFile -Encoding utf8
      "<<< YOUR VERSION" | Out-File $diffFile -Append -Encoding utf8
      $targetContent | Out-File $diffFile -Append -Encoding utf8
      "===" | Out-File $diffFile -Append -Encoding utf8
      ">>> NEW VERSION" | Out-File $diffFile -Append -Encoding utf8
      $sourceContent | Out-File $diffFile -Append -Encoding utf8
      Write-Host "  ≠ $RelPath (see .new & diff)" -ForegroundColor Yellow
      Write-Log "Differs $RelPath"
      return "differs"
    } else {
      Remove-Item $newFile -Force
      Write-Host "  = $RelPath" -ForegroundColor Gray
      Write-Log "Same $RelPath"
      return "same"
    }
  }
}

$IsNewInstall = !(Test-Path $TargetDir)
if ($IsNewInstall) {
  Write-Host "NEW INSTALLATION → $TargetDir" -ForegroundColor Green
} else {
  Write-Host "EXISTING INSTALLATION → updating $TargetDir (preserving your files)" -ForegroundColor Yellow
}

if (!($DryRun) -and !(Test-Path $TargetDir)) { New-Item -ItemType Directory -Path $TargetDir | Out-Null }
if (!$IsNewInstall) {
  if (!($DryRun)) {
    if (Test-Path $DiffDir) { Remove-Item -Recurse -Force $DiffDir }
    New-Item -ItemType Directory -Path $DiffDir | Out-Null
  }
}

Write-Host "`nDetecting environment..." -ForegroundColor Yellow
$HasPlaywright = Detect-Playwright
$McpServers    = @()
if (!$SkipDetection) { $McpServers = Discover-MCP }

Write-Host ("• Playwright: " + ($(if ($HasPlaywright) { "present" } else { "not found" })))
if ($McpServers.Count -gt 0) {
  Write-Host ("• MCP servers: " + ($McpServers.name -join ", "))
} else {
  Write-Host "• MCP servers: none discovered"
}

Write-Host "`nCopying files..." -ForegroundColor Yellow
$stats = @{created=0; differs=0; same=0; skipped=0}

Get-ChildItem -Path $TemplateDir -Recurse -File | ForEach-Object {
  $relPath   = $_.FullName.Substring($TemplateDir.Length + 1)
  $targetPath= Join-Path $TargetDir $relPath

  $skipPlay = $relPath -match "(?i)playwright"
  $result = Copy-SmartFile -Source $_.FullName -Target $targetPath -RelPath $relPath -SkipIfPlaywright:$skipPlay
  if ($stats.ContainsKey($result)) { $stats[$result]++ }
}

# Update registry block with discovered MCP
$claudeMdPath = Join-Path $TargetDir "claude.md"
Update-RegistryBlock -ClaudePath $claudeMdPath -Servers $McpServers

Write-Host "`n=== Installation Summary ===" -ForegroundColor Cyan
Write-Host ("Created : {0}" -f $stats.created) -ForegroundColor Green
Write-Host ("Updated : {0}" -f $stats.differs) -ForegroundColor Yellow
Write-Host ("Same    : {0}" -f $stats.same) -ForegroundColor Gray
Write-Host ("Skipped : {0}" -f $stats.skipped) -ForegroundColor Cyan
Write-Host ("Log     : {0}" -f $LogPath) -ForegroundColor Gray

if ($stats.differs -gt 0) {
  Write-Host "`nReview changes:" -ForegroundColor Yellow
  Write-Host "  - .claude\*.new (side-by-side)" -ForegroundColor Gray
  Write-Host "  - $DiffDir\*.diff" -ForegroundColor Gray
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
if ($IsNewInstall) {
  Write-Host "1) Copy example config:" -ForegroundColor White
  Write-Host "   Copy-Item .claude\config.example.yaml .claude\config.yaml" -ForegroundColor Gray
} else {
  Write-Host "1) Review updated files (.new & .diff) then merge desired changes" -ForegroundColor White
}
Write-Host "2) Start using the orchestrator (@research / @coder / @tester ...)" -ForegroundColor White

# Offer Playwright install (safe)
if (!$HasPlaywright -and !$SkipDetection -and -not $DryRun) {
  $response = Read-Host "Playwright not detected. Install now? (y/N)"
  if ($response -match '^[Yy]$') {
    Write-Host "`nInstalling Playwright..." -ForegroundColor Yellow
    npm install -D @playwright/test
    npx playwright install
    Write-Host "✓ Playwright installed" -ForegroundColor Green
  }
}

Write-Host "`n✓ Installation complete!" -ForegroundColor Green
