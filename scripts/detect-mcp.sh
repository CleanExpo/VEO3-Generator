#!/bin/bash
# MCP Server Detection Script - macOS/Linux
# Discovers existing MCP servers and their configurations

set -e

echo "=== MCP Server Detection ==="
echo ""

# Check if Cline/Claude Desktop config exists
CLINE_CONFIG="$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Also check Linux paths
if [ ! -f "$CLINE_CONFIG" ]; then
    CLINE_CONFIG="$HOME/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
fi

if [ ! -f "$CLAUDE_CONFIG" ]; then
    CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
fi

MCP_FOUND=false

# Check Cline config
if [ -f "$CLINE_CONFIG" ]; then
    echo "Found Cline MCP configuration"
    echo ""
    echo "Detected servers:"
    jq -r '.mcpServers | keys[]' "$CLINE_CONFIG" 2>/dev/null | while read -r server; do
        echo "  ✓ $server (Cline)"
    done || echo "  Warning: Could not parse config"
    MCP_FOUND=true
    echo ""
fi

# Check Claude Desktop config
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "Found Claude Desktop configuration"
    echo ""
    echo "Detected servers:"
    jq -r '.mcpServers | keys[]' "$CLAUDE_CONFIG" 2>/dev/null | while read -r server; do
        echo "  ✓ $server (Claude Desktop)"
    done || echo "  Warning: Could not parse config"
    MCP_FOUND=true
    echo ""
fi

if [ "$MCP_FOUND" = false ]; then
    echo "No MCP servers detected"
    echo ""
    echo "To add MCP servers, configure them in:"
    echo "  - Cline: Settings > MCP Servers"
    echo "  - Claude Desktop: Settings > Developer > Edit Config"
    echo ""
fi

# Check against our templates
echo "Template Coverage:"
TEMPLATES=("playwright" "filesystem" "git" "browser" "jina")

for template in "${TEMPLATES[@]}"; do
    if [ -f "$CLINE_CONFIG" ]; then
        if jq -e ".mcpServers | has(\"$template\")" "$CLINE_CONFIG" >/dev/null 2>&1; then
            echo "  ✓ $template (detected)"
            continue
        fi
    fi
    if [ -f "$CLAUDE_CONFIG" ]; then
        if jq -e ".mcpServers | has(\"$template\")" "$CLAUDE_CONFIG" >/dev/null 2>&1; then
            echo "  ✓ $template (detected)"
            continue
        fi
    fi
    echo "  ○ $template (not found)"
done

echo ""
echo "Recommendation: Add missing MCP servers for full orchestrator functionality"
echo ""
