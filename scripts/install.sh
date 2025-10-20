#!/bin/bash
# Claude Orchestrator Installation Script - macOS/Linux
# Idempotent copy-in with discovery, diff reporting, and smart merging

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "$SCRIPT_DIR")/templates/.claude"
TARGET_DIR="./.claude"
DIFF_DIR="$TARGET_DIR/_install-diff"

SKIP_DETECTION=false
FORCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-detection) SKIP_DETECTION=true; shift ;;
        --force) FORCE=true; shift ;;
        *) shift ;;
    esac
done

echo "=== Claude Orchestrator Installer ==="
echo ""

# Validate prerequisites
echo "Checking prerequisites..."

# Check bash version
if [[ "${BASH_VERSION%%.*}" -lt 4 ]]; then
    echo "✗ Bash 4.0+ recommended"
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION"
else
    echo "⚠ Node.js not found - MCP servers may not work"
    echo "  Install from: https://nodejs.org"
fi

echo ""

# Run detection (unless skipped)
HAS_PLAYWRIGHT=false
MCP_SERVERS=()

if [[ "$SKIP_DETECTION" == false ]]; then
    echo "Running environment detection..."
    echo ""
    
    # Detect Playwright
    if [[ -f "$SCRIPT_DIR/detect-playwright.sh" ]]; then
        bash "$SCRIPT_DIR/detect-playwright.sh" > /dev/null 2>&1 || true
        
        # Check if Playwright is installed
        if [[ -f "package.json" ]]; then
            if grep -q "playwright\|@playwright/test" package.json; then
                HAS_PLAYWRIGHT=true
            fi
        fi
    fi
    
    # Detect MCP servers
    if [[ -f "$SCRIPT_DIR/detect-mcp.sh" ]]; then
        bash "$SCRIPT_DIR/detect-mcp.sh" > /dev/null 2>&1 || true
    fi
    
    echo ""
fi

# Determine installation mode
IS_NEW_INSTALL=true
if [[ -d "$TARGET_DIR" ]]; then
    IS_NEW_INSTALL=false
fi

if [[ "$IS_NEW_INSTALL" == true ]]; then
    echo "NEW INSTALLATION"
    echo "Installing orchestrator to $TARGET_DIR"
else
    echo "EXISTING INSTALLATION"
    echo "Updating $TARGET_DIR (preserving your files)"
fi

echo ""

# Create target directory if needed
mkdir -p "$TARGET_DIR"

# Create diff directory for updates
if [[ "$IS_NEW_INSTALL" == false ]]; then
    rm -rf "$DIFF_DIR"
    mkdir -p "$DIFF_DIR"
fi

# Copy function with smart handling
copy_smart_file() {
    local source="$1"
    local target="$2"
    local relpath="$3"
    
    if [[ ! -f "$target" ]]; then
        # File doesn't exist - copy it
        mkdir -p "$(dirname "$target")"
        cp "$source" "$target"
        echo "  + $relpath"
        echo "created"
    else
        # File exists - create .new and diff
        cp "$source" "$target.new"
        
        # Generate diff
        local difffile="$DIFF_DIR/$relpath.diff"
        mkdir -p "$(dirname "$difffile")"
        
        if ! cmp -s "$source" "$target"; then
            {
                echo "=== $relpath ==="
                echo "<<< YOUR VERSION"
                cat "$target"
                echo "==="
                echo ">>> NEW VERSION"
                cat "$source"
            } > "$difffile"
            
            echo "  ≠ $relpath (see .new file and diff)"
            echo "differs"
        else
            rm "$target.new"
            echo "  = $relpath"
            echo "same"
        fi
    fi
}

# Copy files
echo "Copying files..."

CREATED=0
DIFFERS=0
SAME=0
SKIPPED=0

while IFS= read -r -d '' file; do
    relpath="${file#$TEMPLATE_DIR/}"
    targetpath="$TARGET_DIR/$relpath"
    
    # Skip Playwright files if detected
    if [[ "$HAS_PLAYWRIGHT" == true ]] && [[ "$relpath" == *"playwright"* ]]; then
        echo "  ↷ $relpath (Playwright detected, skipping)"
        ((SKIPPED++))
        continue
    fi
    
    result=$(copy_smart_file "$file" "$targetpath" "$relpath")
    
    case "$result" in
        created) ((CREATED++)) ;;
        differs) ((DIFFERS++)) ;;
        same) ((SAME++)) ;;
    esac
done < <(find "$TEMPLATE_DIR" -type f -print0)

echo ""

# Handle claude.md agent registry
CLAUDE_MD="$TARGET_DIR/claude.md"
if [[ -f "$CLAUDE_MD" ]]; then
    echo "Updating agent registry in claude.md..."
    
    if ! grep -q "# BEGIN-AUTO-REGISTRY" "$CLAUDE_MD"; then
        # Add registry section
        cat >> "$CLAUDE_MD" << 'EOF'

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
EOF
        echo "  ✓ Added agent registry"
    else
        echo "  = Registry already present"
    fi
fi

echo ""

# Report results
echo "=== Installation Summary ==="
echo "Created:  $CREATED files"
echo "Updated:  $DIFFERS files (see .new and diffs)"
echo "Same:     $SAME files"
echo "Skipped:  $SKIPPED files"

if [[ $DIFFERS -gt 0 ]]; then
    echo ""
    echo "Review changes in:"
    echo "  - .new files in .claude/"
    echo "  - Diffs in .claude/_install-diff/"
fi

echo ""

# Next steps
echo "=== Next Steps ==="

if [[ "$IS_NEW_INSTALL" == true ]]; then
    echo "1. Copy example config:"
    echo "   cp .claude/config.example.yaml .claude/config.yaml"
    echo ""
    echo "2. Edit configuration:"
    echo "   - Set project_type (nextjs_fullstack, api_only, etc.)"
    echo "   - Configure paths for your project"
    echo "   - Set autonomy mode (trusted or review_each_step)"
else
    echo "1. Review updated files (.new and diffs)"
    echo "2. Merge changes you want to keep"
    echo "3. Remove .new files when done"
fi

echo ""
echo "3. Start using the orchestrator:"
echo "   @research - Find best practices for [topic]"

echo ""

# Offer Playwright installation
if [[ "$HAS_PLAYWRIGHT" == false ]] && [[ "$SKIP_DETECTION" == false ]]; then
    read -p "Playwright not detected. Install now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Installing Playwright..."
        npm install -D @playwright/test
        npx playwright install
        echo "✓ Playwright installed"
    fi
fi

echo ""
echo "✓ Installation complete!"
echo ""
