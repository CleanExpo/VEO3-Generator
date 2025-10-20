# Getting Started

One command to install, then start building.

## Quick Install

### Windows
```powershell
cd your-project
.\scripts\install.ps1
```

### macOS/Linux
```bash
cd your-project
./scripts/install.sh
```

This copies orchestrator templates to `.claude/` in your project.

## First Configuration

1. **Copy example config:**
   ```bash
   cp .claude/config.example.yaml .claude/config.yaml
   ```

2. **Set your project type:**
   ```yaml
   project_type: nextjs_fullstack   # or api_only, wordpress, etc.
   autonomy: trusted                # or review_each_step
   ```

3. **Configure paths for your project:**
   ```yaml
   paths:
     app: ./src/app
     api: ./src/app/api
     e2e: ./tests/e2e-claude
   ```

4. **Set guardrails:**
   ```yaml
   guardrails:
     write_scope:
       - "src/**"
       - "app/**"
       - "docs/**"
     protected_files:
       - ".env*"
       - "infra/**"
   ```

## Verify Setup

Run detection scripts to check your environment:

```bash
# Check MCP servers
./scripts/detect-mcp.sh

# Check Playwright
./scripts/detect-playwright.sh
```

## First Task

Start with a simple request to test the orchestrator:

```
@research - Find best practices for input validation in Next.js
```

The orchestrator will:
1. Route to research agent
2. Gather information
3. Present findings
4. Ready for next step

## Common First Tasks

### Set Up Testing
```
Set up Playwright for E2E testing in this Next.js project
```

The orchestrator will:
- @research - Find Playwright setup guide
- @coder - Install and configure Playwright
- @tester - Create sample test
- @integrator - Wire into npm scripts

### Add a Feature
```
Add user authentication with Google OAuth
```

The orchestrator will:
- @research - OAuth best practices
- @coder - Implement auth endpoints
- @tester - Create auth tests
- @integrator - Connect to frontend
- @master-fullstack - Verify completeness

### Fix a Bug
```
API endpoint /api/users is timing out under load
```

The orchestrator will:
- @research - Investigate performance patterns
- @stuck - Analyze known solutions
- @coder - Implement optimization
- @tester - Add performance tests

## Understanding Agents

### Core Agents (Always Available)
- **coder** - Writes code (frontend, backend, API)
- **tester** - Creates and runs tests
- **research** - Gathers information
- **integrator** - Connects pieces together
- **stuck** - Recognizes patterns, escalates blockers

### Master Agents (Coordinators)
- **master-fullstack** - "No piece missing" verification
- **master-devops** - Deployment with guardrails
- **master-docs** - Documentation generation
- **master-data** - Data operations (optional)

## Autonomy Modes

### Trusted Mode
```yaml
autonomy: trusted
```
- Agents make decisions automatically
- File writes proceed with confidence
- Faster iteration
- Best for: Experienced teams, trusted environments

### Review Each Step
```yaml
autonomy: review_each_step
```
- Agent asks before each write operation
- More control, slower pace
- Best for: Learning, critical projects, production changes

## Feature Toggles

Enable/disable capabilities:

```yaml
features:
  research: true    # Web/doc research
  tests: true       # Test generation
  docs: true        # Auto documentation
  devops: true      # CI/CD workflows
```

## MCP Configuration

### Auto Mode (Recommended)
```yaml
mcp:
  playwright: auto    # Enables if installed
  jina: auto          # Enables if API key present
```

### Force On/Off
```yaml
mcp:
  playwright: force_on   # Always try to use
  browser: force_off     # Never use
```

## Guardrails

### Write Scope
Define where agents can write:
```yaml
guardrails:
  write_scope:
    - "src/**"
    - "app/**"
    - "docs/**"
```

### Protected Files
Require approval for these:
```yaml
guardrails:
  protected_files:
    - ".env*"
    - "Dockerfile"
    - "infra/**"
```

### Test Gates
Block progression if tests fail:
```yaml
guardrails:
  require_tests_to_pass: true
```

## CI Integration

The orchestrator includes CI workflows:

```yaml
ci:
  installed: true     # Files present in .github/workflows
  enabled: false      # You control when to enable
```

To enable:
```
Enable CI workflows for automated testing
```

Or manually:
```yaml
ci:
  enabled: true
```

## Tips for Success

### 1. Start Small
Begin with simple tasks to learn agent interactions:
- "Add a button component"
- "Create an API endpoint for health checks"
- "Set up Prettier configuration"

### 2. Be Specific
Clear requests get better results:
- ❌ "Improve the UI"
- ✅ "Add loading states to all buttons in the dashboard"

### 3. Use Workflows
Leverage built-in workflows:
- "Follow feature workflow to add search"
- "Use bugfix workflow for payment timeout"

### 4. Trust the Process
Let agents complete their work:
- Research gathers context
- Coder implements
- Tester validates
- Integrator connects
- Master-fullstack verifies

### 5. Review Handoffs
Agents hand off context between each other. Review these to understand progress.

## Troubleshooting

### Orchestrator Not Responding
```bash
# Verify .claude directory exists
ls -la .claude/

# Check config syntax
cat .claude/config.yaml
```

### Agent Not Activating
```yaml
# Ensure agent is enabled
agents:
  coder:
    enabled: true
```

### MCP Servers Not Found
```bash
# Run detection
./scripts/detect-mcp.sh

# Add servers in IDE settings
# Cline: Settings > MCP Servers
# Claude Desktop: Settings > Developer > Edit Config
```

### Tests Not Running
```bash
# Check Playwright installation
./scripts/detect-playwright.sh

# Install if needed
npm install -D @playwright/test
npx playwright install
```

## Next Steps

Once set up:

1. **Read the docs:**
   - [Rationale](rationale.md) - Why this architecture
   - [Safety](safety.md) - Security guidelines
   - [Customizing](customizing.md) - Extend the orchestrator

2. **Try a workflow:**
   ```
   Follow the feature workflow to add user profile editing
   ```

3. **Create your first agent:**
   ```
   Help me create a custom security agent for OWASP checks
   ```

4. **Set up CI:**
   ```
   Enable and configure CI workflows for this project
   ```

## Getting Help

- **Check logs:** `.claude/logs/orchestrator.log`
- **Run detection:** `./scripts/detect-mcp.sh`
- **Review config:** `.claude/config.yaml`
- **Ask the orchestrator:** "Explain how the orchestrator routes tasks"

---

**You're ready!** Start with a simple task and let the orchestrator coordinate the work.
