# Customizing the Orchestrator

How to extend and adapt the orchestrator to your specific needs.

## Customization Levels

The orchestrator can be customized at four levels:

1. **Configuration**: Adjust settings without code changes
2. **Agent Modification**: Customize existing agents
3. **New Agents**: Create domain-specific agents
4. **MCP Extension**: Add new tools and capabilities

## 1. Configuration Customization

### Basic Configuration

Edit `.claude/config.yaml`:

```yaml
# Adjust for your project
project:
  name: "My SaaS Platform"
  version: "2.1.0"
  
# Enable/disable agents
agents:
  coder:
    enabled: true
    autoApprove: false  # Change based on trust level
    
# Configure your stack
stack:
  preset: "nextjs"
  custom:
    languages: [TypeScript]
    frameworks: [Next.js, FastAPI]
    databases: [PostgreSQL, Redis]
```

### Workflow Customization

Add custom workflows:

```yaml
workflows:
  # Custom: Security audit workflow
  security_audit:
    steps:
      - agent: research
        description: "Check for known vulnerabilities"
      - agent: coder
        description: "Run security scanners"
      - agent: docs
        description: "Document findings"
        
  # Custom: Performance optimization
  performance:
    steps:
      - agent: research
        description: "Identify bottlenecks"
      - agent: coder
        description: "Implement optimizations"
      - agent: tester
        description: "Benchmark improvements"
```

## 2. Agent Modification

### Customizing Existing Agents

Copy an agent file and modify:

```bash
cd .claude/agents
cp coder.md coder.custom.md
```

Edit `coder.custom.md`:

```markdown
# Agent: Coder (Custom)

## Custom Coding Standards

### Company Style Guide
- Use 2 spaces for indentation
- Always use TypeScript strict mode
- Prefer functional components
- Use Tailwind for styling

### Architecture Patterns
```typescript
// Feature-first structure
src/
  features/
    auth/
      api/
      components/
      hooks/
      types/
      index.ts
```

### Custom Commit Format
```
<type>(<ticket>): <description>

<body>

Refs: PROJ-123
```
```

Update `config.yaml` to use it:

```yaml
agents:
  coder:
    enabled: true
    customDefinition: ".claude/agents/coder.custom.md"
```

### Example: Custom Testing Agent

Create `.claude/agents/tester.custom.md`:

```markdown
# Agent: Tester (Custom)

## Custom Test Requirements

### Test Coverage Requirements
- Minimum 80% line coverage
- 100% coverage for business logic
- All API endpoints must have tests

### Custom Test Structure
```typescript
describe('FeatureName', () => {
  describe('happy paths', () => {
    // Tests for normal operation
  });
  
  describe('edge cases', () => {
    // Tests for boundary conditions
  });
  
  describe('error handling', () => {
    // Tests for failure scenarios
  });
});
```

### Performance Tests Required
- All API endpoints must respond < 200ms
- Database queries must complete < 50ms
- Page loads must complete < 2s
```

## 3. Creating New Agents

### When to Create a New Agent

Create a new agent when you have:
- **Repeated specialized tasks** that don't fit existing agents
- **Domain-specific knowledge** not covered
- **Tool requirements** unique to your workflow
- **Compliance needs** (security audits, accessibility checks)

### Agent Template

Create `.claude/agents/your-agent.md`:

```markdown
# Agent: [Agent Name]

## Responsibilities

[What this agent does]

## When to Use

[Scenarios where this agent should be activated]

## Tools & Resources

[MCP servers, APIs, or tools this agent uses]

## Patterns & Examples

### Pattern 1: [Pattern Name]

**When:**
[Situation]

**How:**
```
[Example code or process]
```

**Result:**
[Expected outcome]

## Handoff Format

When complete, hand off to:

```markdown
@[next-agent]
## [What was done]
[Details]

## [What's needed]
[Next steps]
```

## Best Practices

[Guidelines specific to this agent]

---

**Remember**: [Key principle for this agent]
```

### Example: Security Agent

`.claude/agents/security.md`:

```markdown
# Agent: Security

You perform security audits and vulnerability assessments.

## Responsibilities

- Scan for security vulnerabilities
- Review authentication/authorization
- Check for common security issues (SQL injection, XSS, etc.)
- Validate input handling
- Review secret management

## When to Use

- Before production deployments
- After adding authentication features
- When integrating third-party services
- During security audit requests

## Tools & Resources

- npm audit / yarn audit
- OWASP guidelines
- Security headers checker
- Dependency vulnerability databases

## Audit Process

### 1. Dependency Scan
```bash
npm audit
npm audit fix
```

### 2. Code Review

Check for:
```typescript
// SQL Injection
❌ db.query(`SELECT * FROM users WHERE id = ${userId}`)
✅ db.query('SELECT * FROM users WHERE id = ?', [userId])

// XSS
❌ element.innerHTML = userInput
✅ element.textContent = userInput

// Secrets
❌ const apiKey = "sk-actual-key"
✅ const apiKey = process.env.API_KEY
```

### 3. Authentication Review

Verify:
- Password hashing (bcrypt, argon2)
- Session management
- CSRF protection
- Rate limiting

### 4. Authorization Review

Check:
- Role-based access control
- Resource ownership validation
- API endpoint protection

## Security Report Format

```markdown
## Security Audit Report

### Vulnerabilities Found

#### High Priority
- [ ] Issue 1: Description
  - Impact: [description]
  - Fix: [recommendation]

#### Medium Priority
- [ ] Issue 2: Description

#### Low Priority
- [ ] Issue 3: Description

### Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

### Compliance

- [ ] OWASP Top 10 checked
- [ ] Authentication secure
- [ ] Secrets properly managed
- [ ] Input validation present
```

## Handoff Format

```markdown
@coder
## Security Issues Found
[List of issues]

## Fixes Required
[Specific changes needed]

@deployer
## Security Clearance
- [ ] All critical issues resolved
- [ ] Security headers configured
- [ ] Secrets properly managed
Ready for deployment
```
```

Enable in `config.yaml`:

```yaml
agents:
  security:
    enabled: true
    definition: ".claude/agents/security.md"
    autoApprove: true  # Read-only analysis
```

## 4. MCP Extension

### Adding New MCP Servers

#### Example: Slack MCP

Create `.claude/mcp/slack.config.json`:

```json
{
  "name": "slack",
  "description": "Slack MCP for team notifications",
  "command": "npx",
  "args": ["-y", "@slack/mcp-server"],
  "env": {
    "SLACK_BOT_TOKEN": "",
    "SLACK_CHANNEL_ID": ""
  },
  "settings": {
    "defaultChannel": "#dev-notifications"
  },
  "capabilities": {
    "send_messages": true,
    "read_messages": false,
    "manage_channels": false
  },
  "safety": {
    "readOnly": false,
    "requiresApproval": true,
    "rateLimit": 10
  }
}
```

Enable in `config.yaml`:

```yaml
mcp:
  slack:
    enabled: true
    config: "./mcp/slack.config.json"
```

#### Example: Database MCP

Create `.claude/mcp/database.config.json`:

```json
{
  "name": "database",
  "description": "Direct database access for data agent",
  "command": "npx",
  "args": ["-y", "@prisma/mcp-server"],
  "env": {
    "DATABASE_URL": ""
  },
  "settings": {
    "readonly": true,
    "maxQueryTime": 5000
  },
  "capabilities": {
    "query": true,
    "migrations": false,
    "schema_access": true
  },
  "safety": {
    "readOnly": true,
    "requiresApproval": false
  }
}
```

### Custom MCP Server

You can also create completely custom MCP servers. See the [MCP documentation](https://modelcontextprotocol.io) for details.

## Example Customizations

### Example 1: Monorepo Support

`.claude/agents/coder.monorepo.md`:

```markdown
# Agent: Coder (Monorepo)

## Monorepo Structure

```
my-monorepo/
  packages/
    web/          # Next.js frontend
    api/          # Express backend
    shared/       # Shared utilities
  apps/
    admin/        # Admin dashboard
    mobile/       # React Native app
```

## Package-Specific Commands

```bash
# Web package
npm run dev --workspace=web

# API package
npm run dev --workspace=api

# All packages
npm run build --workspaces
```

## Import Patterns

```typescript
// Cross-package imports
import { Button } from '@myapp/shared/ui';
import { api } from '@myapp/api-client';
```
```

### Example 2: Compliance Agent

`.claude/agents/compliance.md`:

```markdown
# Agent: Compliance

## Responsibilities

- GDPR compliance checks
- Accessibility (WCAG) validation
- License compliance
- Data retention policies

## GDPR Checklist

- [ ] Privacy policy present
- [ ] Cookie consent implemented
- [ ] Data export functionality
- [ ] Data deletion functionality
- [ ] Audit logging enabled

## Accessibility Checks

```bash
# Run automated checks
npm run a11y-test

# Manual checks
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast sufficient
- [ ] Alt text on images
```
```

### Example 3: Stack-Specific Configuration

#### For Python/Django Projects

`.claude/config.yaml`:

```yaml
stack:
  preset: "python"
  custom:
    languages: [Python]
    framework: Django
    testing: Pytest
    linting: [Ruff, Black]
    
agents:
  coder:
    settings:
      pythonVersion: "3.11"
      useTypeHints: true
      formatter: "black"
```

#### For Go Projects

`.claude/config.yaml`:

```yaml
stack:
  preset: "go"
  custom:
    languages: [Go]
    framework: "Standard Library"
    testing: "testing package"
    
agents:
  coder:
    settings:
      goVersion: "1.21"
      useModules: true
      linter: "golangci-lint"
```

## Best Practices for Customization

### 1. Start Small
- Begin with configuration changes
- Test with existing agents
- Add custom agents only when needed
- Extend MCP capabilities last

### 2. Document Everything
```markdown
# .claude/CUSTOMIZATIONS.md

## Custom Agents
- security: Performs security audits before deployment
- compliance: Checks GDPR and accessibility

## Modified Agents
- coder: Added company coding standards
- tester: Increased coverage requirements to 80%

## Custom MCP Servers
- slack: Team notifications
- database: Direct DB access for data agent

## Custom Workflows
- security_audit: Pre-deployment security checks
- performance: Performance optimization workflow
```

### 3. Version Control

Commit to Git:
```
.claude/
  agents/
    *.md              ✅ Commit
  mcp/
    *.config.json     ✅ Commit
  config.example.yaml ✅ Commit
  config.yaml         ❌ Don't commit (may have secrets)
```

### 4. Share with Team

```bash
# Other developers can adopt your setup
git clone <repo>
cd project
./scripts/install.sh
```

### 5. Iterate Based on Usage

Track what works:
```markdown
# .claude/usage-notes.md

## What Works Well
- Security agent catches issues early
- Custom coder standards improve consistency

## What Needs Improvement
- Deployment agent too cautious
- Need better test coverage reporting

## Future Additions
- Performance profiling agent
- Design review agent
```

## Troubleshooting Customizations

### Agent Not Activating

**Problem**: Custom agent isn't being used

**Check**:
1. Is it enabled in config.yaml?
2. Is the file path correct?
3. Does the orchestrator know about it?

**Solution**:
```yaml
# config.yaml
agents:
  custom_agent:
    enabled: true
    definition: ".claude/agents/custom.md"
```

### MCP Server Not Working

**Problem**: MCP server not connecting

**Check**:
1. Is the package installed?
2. Are environment variables set?
3. Is it enabled in config?

**Debug**:
```bash
# Test MCP server directly
npx @modelcontextprotocol/server-test ./mcp/custom.config.json
```

### Configuration Not Applied

**Problem**: Changes to config.yaml not taking effect

**Solution**:
1. Restart Claude/Cline
2. Check YAML syntax (use a validator)
3. Check for typos in keys

## Community Contributions

### Share Your Custom Agents

If you create useful agents, consider sharing:

1. Create a gist or repo
2. Document the use case
3. Include example config
4. Share with community

### Use Community Agents

Browse shared agents:
- GitHub topic: `claude-orchestrator-agent`
- Community forum
- Discord server

## Migration Guide

### Upgrading from V1 to V2

If the orchestrator structure changes:

```bash
# Backup current setup
cp -r .claude .claude.backup

# Run update script
./scripts/update.sh

# Review changes
diff .claude .claude.backup

# Migrate custom configurations
# (Manual review and merge)
```

## Summary

Customization paths:

**Simple**: Edit config.yaml
**Moderate**: Customize existing agents  
**Advanced**: Create new agents
**Expert**: Build custom MCP servers

Start simple, add complexity as needed. The orchestrator grows with your project.

---

**Remember**: The goal is better collaboration with AI, not perfect customization. Customize when it adds clear value, not for its own sake.
