#!/bin/bash
# Claude Orchestrator Starter - macOS/Linux Update Script
# Safely re-applies orchestrator templates without overwriting customizations

set -e

TARGET_PATH="${1:-.}"
SKIP_BACKUP=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        *)
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

echo "=== Claude Orchestrator Starter - Update ==="
echo ""

# Resolve target path
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Target path does not exist: $TARGET_PATH"
    exit 1
fi

TARGET_PATH=$(cd "$TARGET_PATH" && pwd)
CLAUDE_DIR="$TARGET_PATH/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_SOURCE="$SCRIPT_DIR/../templates/.claude"

# Check if .claude directory exists
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Error: .claude directory not found. Run install.sh first."
    exit 1
fi

# Create backup
if [ "$SKIP_BACKUP" = false ]; then
    BACKUP_DIR="$TARGET_PATH/.claude.backup.$(date +%Y%m%d-%H%M%S)"
    echo "Creating backup at $BACKUP_DIR"
    cp -r "$CLAUDE_DIR" "$BACKUP_DIR"
    echo "Backup created successfully"
    echo ""
fi

# Update only template files, preserve customizations
echo "Updating orchestrator templates..."

# Update core orchestrator file
cp "$TEMPLATE_SOURCE/claude.md" "$CLAUDE_DIR/claude.md"
echo "  Updated: claude.md"

# Update agent definitions
if [ -d "$TEMPLATE_SOURCE/agents" ]; then
    mkdir -p "$CLAUDE_DIR/agents"
    for agent_file in "$TEMPLATE_SOURCE/agents"/*.md; do
        if [ -f "$agent_file" ]; then
            filename=$(basename "$agent_file")
            cp "$agent_file" "$CLAUDE_DIR/agents/$filename"
            echo "  Updated: agents/$filename"
        fi
    done
fi

# Update MCP configurations
if [ -d "$TEMPLATE_SOURCE/mcp" ]; then
    mkdir -p "$CLAUDE_DIR/mcp"
    for mcp_file in "$TEMPLATE_SOURCE/mcp"/*.json; do
        if [ -f "$mcp_file" ]; then
            filename=$(basename "$mcp_file")
            cp "$mcp_file" "$CLAUDE_DIR/mcp/$filename"
            echo "  Updated: mcp/$filename"
        fi
    done
fi

# Update example files
if [ -f "$TEMPLATE_SOURCE/config.example.yaml" ]; then
    cp "$TEMPLATE_SOURCE/config.example.yaml" "$CLAUDE_DIR/config.example.yaml"
fi

if [ -f "$TEMPLATE_SOURCE/tasks.example.md" ]; then
    cp "$TEMPLATE_SOURCE/tasks.example.md" "$CLAUDE_DIR/tasks.example.md"
fi

echo ""
echo "✓ Update complete!"
echo ""
echo "Note: Your config.yaml and tasks.md were preserved."
echo "Review *.example files for new configuration options."

if [ "$SKIP_BACKUP" = false ]; then
    echo ""
    echo "Backup location: $BACKUP_DIR"
fi
echo ""
