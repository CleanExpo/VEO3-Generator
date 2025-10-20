# Claude Orchestrator Installation Script - Windows
# Idempotent copy-in with discovery, diff reporting, and smart merging

param(
    [switch]$Force,
    [switch]$SkipDetection
)

$ErrorActionPreference = "Stop"

Write-Host "=== Claude Orchestrator Installer ===" -ForegroundColor Cyan
Write-Host ""

# Get script directory and template source
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path (Split-Path -Parent $ScriptDir) "templates\.claude"
$TargetDir = ".\.claude"
$DiffDir = "$TargetDir\_install-diff"

# Validate prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "✗ PowerShell 5.0+ required" -ForegroundColor Red
    exit 1
}
Write-Host "✓ PowerShell $($PSVersionTable.PSVersion)" -ForegroundColor Green

# Check Node.js
try {
    $nodeVersion = node --version 2>$null
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Node.js not found - MCP servers may not work" -ForegroundColor Yellow
    Write-Host "  Install from: https://nodejs.org" -ForegroundColor Gray
}

Write-Host ""

# Run detection (unless skipped)
$HasPlaywright = $false
$McpServers = @()

if (!$SkipDetection) {
    Write-Host "Running environment detection..." -ForegroundColor Yellow
    Write-Host ""
    
    # Detect Playwright
    if (Test-Path "$ScriptDir\detect-playwright.ps1") {
        & "$ScriptDir\detect-playwright.ps1" | Out-Null
        
        # Check if Playwright is installed
        if (Test-Path "package.json") {
            $pkg = Get-Content "package.json" | ConvertFrom-Json
            $HasPlaywright = ($pkg.dependencies.playwright -or 
                            $pkg.devDependencies.playwright -or
                            $pkg.dependencies."@playwright/test" -or
                            $pkg.devDependencies."@playwright/test")
        }
    }
    
    # Detect MCP servers
    if (Test-Path "$ScriptDir\detect-mcp.ps1") {
        & "$ScriptDir\detect-mcp.ps1" | Out-Null
    }
    
    Write-Host ""
}

# Determine installation mode
$IsNewInstall = !(Test-Path $TargetDir)

if ($IsNewInstall) {
    Write-Host "NEW INSTALLATION" -ForegroundColor Green
    Write-Host "Installing orchestrator to $TargetDir" -ForegroundColor Cyan
} else {
    Write-Host "EXISTING INSTALLATION" -ForegroundColor Yellow
    Write-Host "Updating $TargetDir (preserving your files)" -ForegroundColor Cyan
}

Write-Host ""

# Create target directory if needed
if (!(Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir | Out-Null
}

# Create diff directory for updates
if (!$IsNewInstall) {
    if (Test-Path $DiffDir) {
        Remove-Item -Recurse -Force $DiffDir
    }
    New-Item -ItemType Directory -Path $DiffDir | Out-Null
}

# Copy function with smart handling
function Copy-SmartFile {
    param(
        [string]$Source,
        [string]$Target,
        [string]$RelPath
    )
    
    $targetExists = Test-Path $Target
    
    if (!$targetExists) {
        # File doesn't exist - copy it
        $targetParent = Split-Path -Parent $Target
        if (!(Test-Path $targetParent)) {
            New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
        }
        Copy-Item $Source $Target
        Write-Host "  + $RelPath" -ForegroundColor Green
        return "created"
    } else {
        # File exists - create .new and diff
        $newFile = "$Target.new"
        Copy-Item $Source $newFile
        
        # Generate diff
        $diffFile = Join-Path $DiffDir "$RelPath.diff"
        $diffParent = Split-Path -Parent $diffFile
        if (!(Test-Path $diffParent)) {
            New-Item -ItemType Directory -Path $diffParent -Force | Out-Null
        }
        
        $sourceContent = Get-Content $Source -Raw
        $targetContent = Get-Content $Target -Raw
        
        if ($sourceContent -ne $targetContent) {
            "=== $RelPath ===" | Out-File $diffFile
            "<<< YOUR VERSION" | Out-File $diffFile -Append
            $targetContent | Out-File $diffFile -Append
            "===" | Out-File $diffFile -Append
            ">>> NEW VERSION" | Out-File $diffFile -Append
            $sourceContent | Out-File $diffFile -Append
            
            Write-Host "  ≠ $RelPath (see .new file and diff)" -ForegroundColor Yellow
            return "differs"
        } else {
            Remove-Item $newFile
            Write-Host "  = $RelPath" -ForegroundColor Gray
            return "same"
        }
    }
}

# Copy files
Write-Host "Copying files..." -ForegroundColor Yellow
$stats = @{created=0; differs=0; same=0; skipped=0}

Get-ChildItem -Path $TemplateDir -Recurse -File | ForEach-Object {
    $relPath = $_.FullName.Substring($TemplateDir.Length + 1)
    $targetPath = Join-Path $TargetDir $relPath
    
    # Skip Playwright files if detected
    if ($HasPlaywright -and $relPath -like "*playwright*") {
        Write-Host "  ↷ $relPath (Playwright detected, skipping)" -ForegroundColor Cyan
        $stats.skipped++
        return
    }
    
    $result = Copy-SmartFile -Source $_.FullName -Target $targetPath -RelPath $relPath
    $stats[$result]++
}

Write-Host ""

# Handle claude.md agent registry
$claudeMdPath = Join-Path $TargetDir "claude.md"
if (Test-Path $claudeMdPath) {
    Write-Host "Updating agent registry in claude.md..." -ForegroundColor Yellow
    
    $content = Get-Content $claudeMdPath -Raw
    
    # Check if registry markers exist
    if ($content -notmatch "# BEGIN-AUTO-REGISTRY") {
        # Add registry section
        $registry = @"

# BEGIN-AUTO-REGISTRY
# Auto-generated agent registry - do not edit between markers
# Available agents:
# - @coder - Full-stack implementation
# - @tester - Playwright E2E + validation
# - @research - Web/doc research
# - @integrator - Merge outputs, resolve conflicts
# - @stuck - Pattern recognition, escalation
# - @master-fullstack - Completeness verification
# - @master-devops - CI/CD with guardrails
# - @master-docs - Documentation generation
# - @master-data - Data operations
# END-AUTO-REGISTRY
"@
        $content += $registry
        $content | Set-Content $claudeMdPath
        Write-Host "  ✓ Added agent registry" -ForegroundColor Green
    } else {
        Write-Host "  = Registry already present" -ForegroundColor Gray
    }
}

Write-Host ""

# Report results
Write-Host "=== Installation Summary ===" -ForegroundColor Cyan
Write-Host "Created:  $($stats.created) files" -ForegroundColor Green
Write-Host "Updated:  $($stats.differs) files (see .new and diffs)" -ForegroundColor Yellow
Write-Host "Same:     $($stats.same) files" -ForegroundColor Gray
Write-Host "Skipped:  $($stats.skipped) files" -ForegroundColor Cyan

if ($stats.differs -gt 0) {
    Write-Host ""
    Write-Host "Review changes in:" -ForegroundColor Yellow
    Write-Host "  - .new files in .claude/" -ForegroundColor Gray
    Write-Host "  - Diffs in .claude/_install-diff/" -ForegroundColor Gray
}

Write-Host ""

# Next steps
Write-Host "=== Next Steps ===" -ForegroundColor Cyan

if ($IsNewInstall) {
    Write-Host "1. Copy example config:" -ForegroundColor White
    Write-Host "   Copy-Item .claude\config.example.yaml .claude\config.yaml" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Edit configuration:" -ForegroundColor White
    Write-Host "   - Set project_type (nextjs_fullstack, api_only, etc.)" -ForegroundColor Gray
    Write-Host "   - Configure paths for your project" -ForegroundColor Gray
    Write-Host "   - Set autonomy mode (trusted or review_each_step)" -ForegroundColor Gray
} else {
    Write-Host "1. Review updated files (.new and diffs)" -ForegroundColor White
    Write-Host "2. Merge changes you want to keep" -ForegroundColor White
    Write-Host "3. Remove .new files when done" -ForegroundColor White
}

Write-Host ""
Write-Host "3. Start using the orchestrator:" -ForegroundColor White
Write-Host "   @research - Find best practices for [topic]" -ForegroundColor Gray

Write-Host ""

# Offer Playwright installation
if (!$HasPlaywright -and !$SkipDetection) {
    $response = Read-Host "Playwright not detected. Install now? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host ""
        Write-Host "Installing Playwright..." -ForegroundColor Yellow
        npm install -D @playwright/test
        npx playwright install
        Write-Host "✓ Playwright installed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
