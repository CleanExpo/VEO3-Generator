# Playwright Detection Script - Windows
# Checks if Playwright is installed and configured

$ErrorActionPreference = "Stop"

Write-Host "=== Playwright Detection ===" -ForegroundColor Cyan
Write-Host ""

# Check for Playwright installation
$playwrightInstalled = $false
$playwrightConfig = $null

# Check npm global
try {
    $npmList = npm list -g playwright 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Playwright installed globally" -ForegroundColor Green
        $playwrightInstalled = $true
    }
} catch {}

# Check local project
if (Test-Path "package.json") {
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    
    if ($packageJson.dependencies.playwright -or $packageJson.devDependencies.playwright -or 
        $packageJson.dependencies."@playwright/test" -or $packageJson.devDependencies."@playwright/test") {
        Write-Host "✓ Playwright installed in project" -ForegroundColor Green
        $playwrightInstalled = $true
    }
}

# Check for config file
$configFiles = @(
    "playwright.config.ts",
    "playwright.config.js",
    "playwright.config.mjs"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found config: $file" -ForegroundColor Green
        $playwrightConfig = $file
        break
    }
}

# Check for tests
$testDirs = @("tests", "e2e", "test")
$hasTests = $false

foreach ($dir in $testDirs) {
    if (Test-Path $dir) {
        $testFiles = Get-ChildItem -Path $dir -Filter "*.spec.*" -Recurse -ErrorAction SilentlyContinue
        if ($testFiles) {
            Write-Host "✓ Found test files in $dir" -ForegroundColor Green
            $hasTests = $true
            break
        }
    }
}

# Summary
Write-Host ""
Write-Host "Status Summary:" -ForegroundColor Cyan

if (!$playwrightInstalled) {
    Write-Host "  ✗ Playwright not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install Playwright:" -ForegroundColor Yellow
    Write-Host "  npm install -D @playwright/test"
    Write-Host "  npx playwright install"
} else {
    Write-Host "  ✓ Playwright installed" -ForegroundColor Green
}

if (!$playwrightConfig) {
    Write-Host "  ✗ No Playwright config found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Initialize Playwright:" -ForegroundColor Yellow
    Write-Host "  npx playwright init"
} else {
    Write-Host "  ✓ Playwright configured" -ForegroundColor Green
}

if (!$hasTests) {
    Write-Host "  ○ No test files found" -ForegroundColor Gray
} else {
    Write-Host "  ✓ Test files present" -ForegroundColor Green
}

Write-Host ""

# Check MCP integration
if (Test-Path ".claude/mcp/playwright.config.json") {
    Write-Host "✓ Playwright MCP configured for orchestrator" -ForegroundColor Green
} else {
    Write-Host "○ Playwright MCP not yet configured" -ForegroundColor Gray
    Write-Host "  Run install.ps1 to add MCP configuration" -ForegroundColor Cyan
}

Write-Host ""
