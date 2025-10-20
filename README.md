# Drop-In Claude Orchestrator

A production-ready orchestration framework for Claude/Cline that coordinates specialized AI agents to handle complex development tasks with safety guardrails and clear workflows.

## Overview

The Drop-In Claude Orchestrator provides structured AI-assisted development through:

- **Specialized Agents** - Focused roles (coder, tester, research, devops, etc.)
- **Smart Routing** - Automatic task delegation to appropriate agents
- **Safety Guardrails** - Protected files, write scopes, test gates
- **Master Coordinators** - Fullstack verification, deployment safety, documentation
- **MCP Integration** - Playwright, filesystem, git, and more
- **Flexible Autonomy** - Trusted or review-each-step modes

## Quick Start

### One Command Install

**Windows:**
```powershell
cd your-project
.\scripts\install.ps1
```

**macOS/Linux:**
```bash
cd your-project
./scripts/install.sh
```

This copies orchestrator templates to `.claude/` in your project.

### Configure

```bash
cp .claude/config.example.yaml .claude/config.yaml
```

Edit to match your project:
```yaml
project_type: nextjs_fullstack
autonomy: trusted
```

### First Task

```
@research - Find best practices for authentication in Next.js
```

## Key Features

### 🎯 Specialized Agents

**Core Agents:**
- **coder** - Full-stack implementation (FE/BE/API/packages)
- **tester** - Playwright E2E + acceptance validation
- **research** - Web/doc research with Jina/Browser MCP
- **integrator** - Merges outputs, resolves conflicts
- **stuck** - Dead-end detection, escalation with A/B/C choices

**Master Agents (Coordinators):**
- **master-fullstack** - "No piece missing" verification specialist
- **master-devops** - CI/CD with deployment guardrails
- **master-docs** - README/ADR/CHANGELOG generation
- **master-data** - Seeds, fixtures, data integrity

### 🔒 Safety First

```yaml
guardrails:
  write_scope: ["src/**", "app/**", "docs/**"]
  protected_files: [".env*", "infra/**", "Dockerfile"]
  require_tests_to_pass: true
```

- Write scope restrictions
- Protected file approval gates
- Test-gated progression
- Dry-run for risky operations

### 🔧 MCP Auto-Discovery

Detection scripts find your existing setup:
```bash
./scripts/detect-mcp.sh        # Find configured MCP servers
./scripts/detect-playwright.sh  # Check test setup
```

Auto-configuration:
```yaml
mcp:
  playwright: auto  # Enables if installed
  jina: auto        # Enables if API key present
```

### 📋 Clear Handoffs

JSON contracts between agents:
```json
{
  "from_agent": "coder",
  "to_agent": "tester",
  "context": { "files_modified": [...], "next_steps": [...] },
  "requirements": { "must_test": [...], "must_verify": [...] }
}
```

## Project Structure

```
dropin-claude-orchestrator/
├── scripts/
│   ├── install.ps1              # Windows installation
│   ├── install.sh               # macOS/Linux installation
│   ├── update.ps1/sh            # Safe updates
│   ├── detect-mcp.ps1/sh        # MCP discovery
│   └── detect-playwright.ps1/sh # Test setup check
├── templates/.claude/
│   ├── claude.md                # Orchestrator routing
│   ├── config.example.yaml      # Configuration template
│   ├── agents/
│   │   ├── coder.md
│   │   ├── tester.md
│   │   ├── research.md
│   │   ├── integrator.md
│   │   ├── stuck.md
│   │   ├── master-fullstack.md
│   │   ├── master-devops.md
│   │   ├── master-docs.md
│   │   └── master-data.md
│   ├── mcp/
│   │   ├── playwright.config.json
│   │   ├── fs.config.json
│   │   ├── git.config.json
│   │   ├── browser.config.json
│   │   └── jina.config.json
│   └── policies/
│       ├── guardrails.md        # Safety rules
│       └── handoffs.md          # Agent contracts
├── docs/
│   ├── getting-started.md       # Quick setup guide
│   ├── rationale.md             # Architecture decisions
│   ├── safety.md                # Security guidelines
│   ├── customizing.md           # Extension guide
│   └── windows-notes.md         # Windows-specific help
├── ci/
│   └── quality.yml              # GitHub Actions (disabled by default)
├── LICENSE
└── README.md
```

## Usage Examples

### Feature Development

```
Request: "Add search functionality with autocomplete"

Orchestrator workflow:
1. @research - Find search implementation patterns
2. @coder - Implement API + frontend
3. @tester - Create E2E tests
4. @integrator - Wire everything together
5. @master-fullstack - Verify completeness
6. @master-docs - Update documentation

Result: Complete, tested, documented feature
```

### Bug Fix

```
Request: "API timing out on large datasets"

Orchestrator workflow:
1. @research - Investigate timeout patterns
2. @stuck - Recognize performance bottleneck
3. @coder - Implement pagination
4. @tester - Add load tests
5. @master-fullstack - Verify fix

Result: Root cause fixed with regression prevention
```

### Deployment

```
Request: "Deploy v2.0 to production"

Orchestrator workflow:
1. @tester - Run full test suite
2. @master-devops - Deploy to staging
3. @tester - Verify staging
4. @master-devops - Production deploy (with approval)
5. @master-docs - Update CHANGELOG

Result: Zero-downtime production deployment
```

## Configuration

### Project Types

```yaml
project_type: nextjs_fullstack   # or: api_only, wordpress, python_api
```

### Autonomy Modes

```yaml
autonomy: trusted                # Fast iteration, agent decisions
autonomy: review_each_step       # Manual approval for writes
```

### Feature Toggles

```yaml
features:
  research: true    # Web research capability
  tests: true       # Test generation
  docs: true        # Auto-documentation
  devops: true      # CI/CD workflows
```

### Guardrails

```yaml
guardrails:
  write_scope:
    - "src/**"
    - "app/**"
    - "docs/**"
  protected_files:
    - ".env*"
    - "infra/**"
    - "Dockerfile"
  require_tests_to_pass: true
```

## Workflows

### Built-In Workflows

**Feature Workflow:**
```yaml
steps:
  - research: Gather context
  - coder: Implement
  - tester: Validate
  - integrator: Connect
  - master-fullstack: Verify
```

**Bugfix Workflow:**
```yaml
steps:
  - research: Investigate
  - stuck: Pattern match
  - coder: Fix
  - tester: Regression test
```

**Deploy Workflow:**
```yaml
steps:
  - tester: Full suite
  - master-devops: Deploy with gates
```

## Documentation

- **[Getting Started](docs/getting-started.md)** - One command setup
- **[Rationale](docs/rationale.md)** - Why this architecture
- **[Safety & Security](docs/safety.md)** - Security guidelines
- **[Customizing](docs/customizing.md)** - Extend the orchestrator
- **[Windows Notes](docs/windows-notes.md)** - Windows-specific help

## Requirements

- **Claude Desktop** or **Cline VS Code Extension**
- **Node.js** 18+ (for MCP servers)
- **Git** (recommended)
- **Playwright** (optional, for E2E testing)

## Detection & Setup

### Check Your Environment

```bash
# Detect MCP servers
./scripts/detect-mcp.sh

# Check Playwright setup
./scripts/detect-playwright.sh
```

### Update Orchestrator

```bash
# Safe update (preserves your config)
./scripts/update.sh
```

## Best Practices

### 1. Start Small
```
"Add a button component with loading state"
```

### 2. Be Specific
- ❌ "Improve the app"
- ✅ "Add input validation to the signup form"

### 3. Use Workflows
```
"Follow feature workflow to add user profiles"
```

### 4. Trust the Process
Let agents complete → hand off → verify → proceed

### 5. Review Handoffs
Check agent-to-agent context transfers

## Advanced Features

### Custom Agents

Create domain-specific agents:
```markdown
# .claude/agents/security.md
You perform security audits...
```

Enable in config:
```yaml
agents:
  security:
    enabled: true
    definition: ".claude/agents/security.md"
```

### Custom MCP Servers

Add new capabilities:
```json
// .claude/mcp/custom.config.json
{
  "name": "custom",
  "command": "npx",
  "args": ["-y", "@custom/mcp-server"]
}
```

### CI Integration

Enable automated testing:
```yaml
ci:
  enabled: true
```

Or ask:
```
Enable CI workflows for this project
```

## Troubleshooting

### Scripts Won't Run (Windows)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install.ps1
```

### Orchestrator Not Responding
```bash
# Verify structure
ls -la .claude/

# Check config
cat .claude/config.yaml
```

### MCP Servers Not Found
```bash
./scripts/detect-mcp.sh
```

Add in IDE settings:
- **Cline**: Settings > MCP Servers
- **Claude Desktop**: Settings > Developer > Edit Config

## Contributing

Contributions welcome! Areas of interest:

- Additional agent definitions
- Stack-specific presets
- MCP server configurations
- Workflow templates
- Documentation improvements

## Roadmap

### v1.0 (Current)
- ✅ Core + Master agents
- ✅ MCP integration
- ✅ Safety guardrails
- ✅ Detection scripts
- ✅ Comprehensive docs

### v1.1 (Planned)
- [ ] Additional project type presets
- [ ] Enhanced CI templates
- [ ] Agent performance metrics
- [ ] Community agent library

### v2.0 (Future)
- [ ] Visual workflow designer
- [ ] Team collaboration features
- [ ] Cloud orchestration
- [ ] Advanced analytics

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **Anthropic/Claude** - AI platform
- **Cline** - VS Code extension
- **MCP Community** - Protocol ecosystem

---

**Drop in. Build faster. Deploy safely.**

Start with: `./scripts/install.sh`
