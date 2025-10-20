# Claude Orchestrator Starter - Windows Update Script
# Safely re-applies orchestrator templates without overwriting customizations

param(
    [string]$TargetPath = ".",
    [switch]$SkipBackup
)

$ErrorActionPreference = "Stop"

Write-Host "=== Claude Orchestrator Starter - Update ===" -ForegroundColor Cyan
Write-Host ""

# Resolve target path
$TargetPath = Resolve-Path $TargetPath -ErrorAction SilentlyContinue
if (-not $TargetPath) {
    Write-Host "Error: Target path does not exist" -ForegroundColor Red
    exit 1
}

$ClaudeDir = Join-Path $TargetPath ".claude"
$TemplateSource = Join-Path $PSScriptRoot "..\templates\.claude"

# Check if .claude directory exists
if (-not (Test-Path $ClaudeDir)) {
    Write-Host "Error: .claude directory not found. Run install.ps1 first." -ForegroundColor Red
    exit 1
}

# Create backup
if (-not $SkipBackup) {
    $BackupDir = Join-Path $TargetPath ".claude.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Creating backup at $BackupDir" -ForegroundColor Yellow
    Copy-Item -Path $ClaudeDir -Destination $BackupDir -Recurse
    Write-Host "Backup created successfully" -ForegroundColor Green
    Write-Host ""
}

# Update only template files, preserve customizations
Write-Host "Updating orchestrator templates..." -ForegroundColor Green

# Files to always update (safe to overwrite)
$SafeToUpdate = @(
    "claude.md",
    "agents\*.md",
    "mcp\*.config.json"
)

# Files to never overwrite (user customizations)
$PreserveFiles = @(
    "config.yaml",
    "tasks.md"
)

try {
    foreach ($pattern in $SafeToUpdate) {
        $sourcePattern = Join-Path $TemplateSource $pattern
        $destPattern = Join-Path $ClaudeDir $pattern
        
        Get-ChildItem $sourcePattern -ErrorAction SilentlyContinue | ForEach-Object {
            $relativePath = $_.FullName.Substring($TemplateSource.Length + 1)
            $destPath = Join-Path $ClaudeDir $relativePath
            
            Copy-Item $_.FullName -Destination $destPath -Force
            Write-Host "  Updated: $relativePath" -ForegroundColor Gray
        }
    }
    
    # Update example files
    Copy-Item "$TemplateSource\config.example.yaml" "$ClaudeDir\config.example.yaml" -Force -ErrorAction SilentlyContinue
    Copy-Item "$TemplateSource\tasks.example.md" "$ClaudeDir\tasks.example.md" -Force -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "✓ Update complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: Your config.yaml and tasks.md were preserved." -ForegroundColor Cyan
    Write-Host "Review *.example files for new configuration options." -ForegroundColor Cyan
    
    if (-not $SkipBackup) {
        Write-Host ""
        Write-Host "Backup location: $BackupDir" -ForegroundColor Yellow
    }
    Write-Host ""
    
} catch {
    Write-Host "Error during update: $_" -ForegroundColor Red
    exit 1
}
