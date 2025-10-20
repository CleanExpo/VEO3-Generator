#!/bin/bash
# Playwright Detection Script - macOS/Linux
# Checks if Playwright is installed and configured

set -e

echo "=== Playwright Detection ==="
echo ""

PLAYWRIGHT_INSTALLED=false
PLAYWRIGHT_CONFIG=""
HAS_TESTS=false

# Check npm global
if npm list -g playwright 2>/dev/null | grep -q playwright; then
    echo "✓ Playwright installed globally"
    PLAYWRIGHT_INSTALLED=true
fi

# Check local project
if [ -f "package.json" ]; then
    if grep -q "playwright\|@playwright/test" package.json; then
        echo "✓ Playwright installed in project"
        PLAYWRIGHT_INSTALLED=true
    fi
fi

# Check for config file
for config in playwright.config.ts playwright.config.js playwright.config.mjs; do
    if [ -f "$config" ]; then
        echo "✓ Found config: $config"
        PLAYWRIGHT_CONFIG="$config"
        break
    fi
done

# Check for tests
for dir in tests e2e test; do
    if [ -d "$dir" ]; then
        if find "$dir" -name "*.spec.*" 2>/dev/null | grep -q .; then
            echo "✓ Found test files in $dir"
            HAS_TESTS=true
            break
        fi
    fi
done

# Summary
echo ""
echo "Status Summary:"

if [ "$PLAYWRIGHT_INSTALLED" = false ]; then
    echo "  ✗ Playwright not installed"
    echo ""
    echo "Install Playwright:"
    echo "  npm install -D @playwright/test"
    echo "  npx playwright install"
else
    echo "  ✓ Playwright installed"
fi

if [ -z "$PLAYWRIGHT_CONFIG" ]; then
    echo "  ✗ No Playwright config found"
    echo ""
    echo "Initialize Playwright:"
    echo "  npx playwright init"
else
    echo "  ✓ Playwright configured"
fi

if [ "$HAS_TESTS" = false ]; then
    echo "  ○ No test files found"
else
    echo "  ✓ Test files present"
fi

echo ""

# Check MCP integration
if [ -f ".claude/mcp/playwright.config.json" ]; then
    echo "✓ Playwright MCP configured for orchestrator"
else
    echo "○ Playwright MCP not yet configured"
    echo "  Run install.sh to add MCP configuration"
fi

echo ""
