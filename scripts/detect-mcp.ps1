# MCP Server Detection Script - Windows
# Discovers existing MCP servers and their configurations

$ErrorActionPreference = "Stop"

Write-Host "=== MCP Server Detection ===" -ForegroundColor Cyan
Write-Host ""

# Check if Cline/Claude Desktop config exists
$clineConfig = "$env:APPDATA\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json"
$claudeConfig = "$env:APPDATA\Claude\claude_desktop_config.json"

$mcpServers = @()

# Check Cline config
if (Test-Path $clineConfig) {
    Write-Host "Found Cline MCP configuration" -ForegroundColor Green
    try {
        $config = Get-Content $clineConfig | ConvertFrom-Json
        if ($config.mcpServers) {
            $mcpServers += $config.mcpServers.PSObject.Properties | ForEach-Object {
                @{
                    Name = $_.Name
                    Source = "Cline"
                    Command = $_.Value.command
                    Args = $_.Value.args
                }
            }
        }
    } catch {
        Write-Host "  Warning: Could not parse Cline config" -ForegroundColor Yellow
    }
}

# Check Claude Desktop config
if (Test-Path $claudeConfig) {
    Write-Host "Found Claude Desktop configuration" -ForegroundColor Green
    try {
        $config = Get-Content $claudeConfig | ConvertFrom-Json
        if ($config.mcpServers) {
            $mcpServers += $config.mcpServers.PSObject.Properties | ForEach-Object {
                @{
                    Name = $_.Name
                    Source = "Claude Desktop"
                    Command = $_.Value.command
                    Args = $_.Value.args
                }
            }
        }
    } catch {
        Write-Host "  Warning: Could not parse Claude Desktop config" -ForegroundColor Yellow
    }
}

# Display results
Write-Host ""
if ($mcpServers.Count -eq 0) {
    Write-Host "No MCP servers detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To add MCP servers, configure them in:" -ForegroundColor Cyan
    Write-Host "  - Cline: Settings > MCP Servers"
    Write-Host "  - Claude Desktop: Settings > Developer > Edit Config"
} else {
    Write-Host "Detected MCP Servers:" -ForegroundColor Green
    Write-Host ""
    
    $mcpServers | ForEach-Object {
        Write-Host "  Name: $($_.Name)" -ForegroundColor White
        Write-Host "  Source: $($_.Source)" -ForegroundColor Gray
        Write-Host "  Command: $($_.Command) $($_.Args -join ' ')" -ForegroundColor Gray
        Write-Host ""
    }
    
    # Check against our templates
    $templateMcps = @("playwright", "filesystem", "git", "browser", "jina")
    Write-Host "Template Coverage:" -ForegroundColor Cyan
    foreach ($template in $templateMcps) {
        $exists = $mcpServers | Where-Object { $_.Name -like "*$template*" }
        if ($exists) {
            Write-Host "  ✓ $template (detected)" -ForegroundColor Green
        } else {
            Write-Host "  ○ $template (not found)" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "Recommendation: Add missing MCP servers for full orchestrator functionality" -ForegroundColor Cyan
Write-Host ""
