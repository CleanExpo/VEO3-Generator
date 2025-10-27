# Quick Start: Project Initialization Guide

This guide helps you initialize the Claude Orchestrator for your project with optimal configuration.

## Table of Contents

1. [New Project Setup](#new-project-setup)
2. [Existing Project Integration](#existing-project-integration)
3. [Project Description Box](#project-description-box)
4. [Auto-Detection Process](#auto-detection-process)
5. [Manual Configuration](#manual-configuration)
6. [Verification](#verification)

---

## New Project Setup

### Step 1: Initialize the Orchestrator

Start by telling Claude to initialize your project:

```
Initialize a new project with Claude Orchestrator
```

Or use the initialization template:

```
Use the initialization template to set up my project
```

###Step 2: Provide Project Description

Claude will ask you to fill out a **Project Description Box**. This helps configure the orchestrator optimally for your needs.

**Required Information:**
- Project name
- Project type (will auto-detect, but you can override)
- Primary goals (what you want to accomplish)
- Team size and experience level
- Autonomy preference (how much control you want)

**Optional but Recommended:**
- Technology stack (will auto-detect)
- Safety requirements
- Testing preferences
- Documentation needs

### Step 3: Review Auto-Detected Settings

The orchestrator will:
1. Scan your codebase
2. Detect project type and stack
3. Propose optimal configuration
4. Show you what it found

Review and confirm or adjust as needed.

### Step 4: Finalize Configuration

Once confirmed, the orchestrator will:
- Generate `.claude/config.yaml`
- Create `.claude/project-profile.yaml`
- Set up appropriate agents
- Configure safety guardrails

---

## Existing Project Integration

### For Existing Codebases

If you're integrating the orchestrator into an existing project:

```
Integrate Claude Orchestrator into my existing project
```

The orchestrator will:

1. **Detect Existing Setup**
   - Scan for frameworks and tools
   - Identify project structure
   - Find existing tests and configs

2. **Preserve Your Work**
   - Never overwrite existing files
   - Create namespaced directories (e.g., `tests/e2e-claude/`)
   - Respect existing conventions

3. **Suggest Integration Points**
   - Where to add new features
   - How to integrate with existing workflows
   - Safe scopes for agent modifications

### Quick Integration Command

```
@research - Analyze this codebase and recommend orchestrator configuration
```

This will:
- Analyze your project structure
- Recommend optimal agent configuration
- Suggest guardrails and safety settings
- Identify integration opportunities

---

## Project Description Box

### What is the Project Description Box?

It's a structured questionnaire that helps the orchestrator understand your project and configure itself optimally.

### Template

When initializing, you'll see something like this:

```yaml
╔═══════════════════════════════════════════════════════╗
║     CLAUDE ORCHESTRATOR INITIALIZATION                ║
║     Project Description & Configuration               ║
╚═══════════════════════════════════════════════════════╝

## 1. PROJECT IDENTITY

Project Name: _________________________
Version: 1.0.0
Description: __________________________________________
           __________________________________________

Primary Goals (check all that apply):
[ ] Build new features
[ ] Fix bugs and issues
[ ] Refactor/improve code
[ ] Add test coverage
[ ] Improve performance
[ ] Add documentation
[ ] Deploy to production
[ ] Other: _____________________

## 2. PROJECT TYPE & STACK

Auto-Detected: [Scanning...]

Type: Next.js Full-Stack Application
Confidence: 92%
Detected Stack:
  - Framework: Next.js 14 (App Router)
  - Language: TypeScript
  - Database: PostgreSQL with Prisma
  - Testing: Playwright + Vitest
  - Package Manager: pnpm

Is this correct? (Y/n): ___

## 3. TEAM CONTEXT

Team Size:
[ ] Solo developer
[ ] Small team (2-5)
[ ] Medium team (6-20)
[ ] Large team (20+)

Experience Level:
[ ] Junior
[ ] Mid-level
[ ] Senior
[ ] Mixed

## 4. AUTONOMY PREFERENCE ⚠️ IMPORTANT

How much autonomy should agents have?

[ ] TRUSTED (Recommended)
    Fast iteration, agents write code within scope
    You review final results

[ ] REVIEW EACH STEP
    Approve every change before writing
    Maximum control, slower iteration

[ ] ADAPTIVE
    Start with review, build trust over time
    Balances speed and safety

Selected: ___________________

## 5. SAFETY CONFIGURATION

Risk Tolerance:
[ ] Conservative - Maximum safety, frequent checks
[ ] Balanced - Standard safety measures
[ ] Aggressive - Minimal restrictions, faster iteration

Protected Files (auto-detected):
  ✓ .env*
  ✓ package-lock.json
  ✓ prisma/migrations/**

Add more? (y/N): ___

## 6. CAPABILITIES

Enable these features:
[✓] Research - Web/documentation search
[✓] Testing - E2E and unit tests
[✓] Documentation - Auto-generate docs
[ ] DevOps - CI/CD workflows
[ ] Data Ops - Seeds/fixtures/migrations

## 7. TESTING PREFERENCES

Testing Level:
[ ] Extensive - Comprehensive coverage
[✓] Standard - Important paths covered
[ ] Minimal - Smoke tests only

Coverage Target: 80%

## 8. DOCUMENTATION

Documentation Strategy:
[✓] Auto-generate after changes
[ ] Manual only
[ ] None

Generate:
[✓] README.md
[✓] CHANGELOG.md
[✓] API documentation
[ ] Architecture Decision Records (ADRs)

═══════════════════════════════════════════════════════

REVIEW YOUR SELECTIONS:

Project: my-app
Type: Next.js Full-Stack
Team: Small (2-5)
Autonomy: Trusted
Safety: Balanced
Features: Research, Testing, Documentation

Confirm and generate configuration? (Y/n): ___
```

### Filling Out the Description Box

**Tips:**
1. **Be Honest About Team Size** - This affects complexity recommendations
2. **Choose Autonomy Carefully** - Start conservative, you can change later
3. **Review Auto-Detection** - It's usually accurate but verify
4. **Consider Future Needs** - Enable features you'll need soon
5. **Start Conservative on Safety** - You can relax later

---

## Auto-Detection Process

### What Gets Auto-Detected?

The orchestrator scans your project for:

1. **Project Type**
   - Framework (Next.js, React, Vue, etc.)
   - Architecture (SPA, Full-Stack, API-only, etc.)
   - Confidence level

2. **Technology Stack**
   - Programming languages
   - Frameworks and libraries
   - Database systems
   - Testing tools
   - Build tools

3. **Project Structure**
   - Directory layout
   - File naming conventions
   - Module organization
   - Import patterns

4. **Existing Configuration**
   - Git setup
   - CI/CD pipelines
   - Test configurations
   - Environment files

5. **Safety Considerations**
   - Sensitive files (.env, secrets)
   - Protected directories (infrastructure, migrations)
   - Lockfiles

### Detection Confidence Levels

- **90-100%** - Very confident, auto-applies
- **70-89%** - Confident, asks for confirmation
- **50-69%** - Uncertain, shows alternatives
- **< 50%** - Cannot detect, asks you to choose

### Example Detection Output

```
🔍 Scanning codebase...

✅ Project Type Detected
   Type: Next.js Full-Stack Application
   Confidence: 92%

   Signals Found:
   ✓ next.config.ts (strong)
   ✓ app/ directory (strong)
   ✓ app/api/ directory (strong)
   ✓ @prisma/client package (strong)
   ✓ TypeScript configuration (moderate)

📦 Technology Stack
   Languages:
   - TypeScript (85%)
   - JavaScript (15%)

   Framework: Next.js 14.0.0 (App Router)
   Database: PostgreSQL (via Prisma)
   Testing: Playwright 1.40.0, Vitest 1.0.0
   Styling: Tailwind CSS 3.3.0
   Package Manager: pnpm

📁 Project Structure
   Type: Standard Next.js structure
   Source: ./src
   Components: ./src/components
   API Routes: ./src/app/api
   Tests: ./tests

🛡️ Safety Profile
   Protected Files Detected:
   - .env.local, .env.production
   - prisma/migrations/**
   - package-lock.json, pnpm-lock.yaml

   Sensitive Patterns: 3 found
   Infrastructure Code: None detected

❓ Is this correct? (Y/n/show alternatives):
```

---

## Manual Configuration

### When to Configure Manually

Use manual configuration when:
- Auto-detection confidence is low (< 70%)
- Your project uses an unusual structure
- You have specific requirements
- You're setting up a new/empty project

### Manual Configuration Steps

#### 1. Copy the Initialization Template

```bash
# The template is already in .claude/initialization-template.yaml
# Copy it to create your config:
cp .claude/initialization-template.yaml .claude/my-project-config.yaml
```

#### 2. Fill Out Each Section

Open `.claude/my-project-config.yaml` and fill in:

**Required Sections:**
- `project_identity` - Name, description, goals
- `project_type` - Type and stack
- `team_context` - Team size, autonomy preference
- `safety_configuration` - Write scope, protected files
- `capabilities_needed` - Which features to enable

**Optional Sections:**
- `workflow_configuration` - Custom workflows
- `observability` - Logging and metrics
- `environments` - Dev/staging/production settings

#### 3. Validate Your Configuration

Tell Claude:
```
Validate my orchestrator configuration in .claude/my-project-config.yaml
```

Claude will:
- Check for required fields
- Validate paths exist
- Verify agent definitions
- Suggest improvements

#### 4. Apply the Configuration

```
Apply configuration from .claude/my-project-config.yaml
```

---

## Verification

### Verify Your Setup

After initialization, verify everything is working:

#### 1. Check Configuration

```
Show me my current orchestrator configuration
```

This displays:
- Active agents
- Enabled features
- Safety guardrails
- Project type and stack

#### 2. Run a Simple Test

Try a simple task to verify:

```
@research - Find documentation for [your main framework]
```

Or:

```
@coder - Add a comment to explain the main entry point
```

#### 3. Check Agent Status

```
List all available agents and their status
```

Should show:
- ✅ coder (enabled)
- ✅ tester (enabled)
- ✅ research (enabled)
- ✅ integrator (enabled)
- ✅ stuck (enabled)
- Plus any master agents you enabled

#### 4. Verify Safety Guardrails

```
Show me what files are protected
```

Should display:
- Write scope (where agents can write)
- Protected files (what agents cannot touch)
- Phase gates (test requirements, etc.)

### Troubleshooting

**Problem: Auto-detection not working**
```
Solution: Run manual detection:
@research - Analyze project structure and recommend configuration
```

**Problem: Agents not responding**
```
Solution: Check agent definitions exist:
ls .claude/agents/
Should see: coder.md, tester.md, research.md, etc.
```

**Problem: Configuration seems wrong**
```
Solution: Start fresh with template:
cp .claude/initialization-template.yaml .claude/config.yaml
# Then customize
```

---

## Next Steps After Initialization

### 1. Test with a Simple Task

Start with something simple:

```
Add a new utility function to help with date formatting
```

This tests:
- Agent routing (should use @coder)
- File creation (within write scope)
- Basic functionality

### 2. Try a Multi-Agent Workflow

Test coordination:

```
Add a contact form with validation and tests
```

This should trigger:
1. @research - Find best practices
2. @coder - Implement the form
3. @tester - Create E2E tests
4. @integrator - Wire everything together

### 3. Review and Adjust

After a few tasks:

```
Analyze my usage and suggest configuration improvements
```

The orchestrator will:
- Review what worked well
- Identify bottlenecks
- Suggest optimizations
- Recommend agent adjustments

### 4. Read the Docs

Explore more capabilities:
- `docs/getting-started.md` - Comprehensive guide
- `docs/customizing.md` - Advanced customization
- `.claude/policies/guardrails.md` - Safety details
- `.claude/policies/handoffs.md` - Agent coordination

---

## Quick Reference

### Common Initialization Commands

```bash
# Initialize new project
"Initialize Claude Orchestrator for my project"

# Detect and configure
"Auto-detect my project and configure the orchestrator"

# Manual setup
"Use the initialization template for manual configuration"

# Verify setup
"Verify my orchestrator configuration"

# Show status
"Show orchestrator status and enabled agents"

# Adjust configuration
"Adjust orchestrator to [preference]"
# Example: "Adjust orchestrator to be more conservative with safety"
```

### Configuration Locations

```
.claude/
├── config.yaml                    # Main configuration (generated)
├── initialization-template.yaml   # Template for manual setup
├── project-profile.yaml          # Detected project info (generated)
├── detection/
│   └── project-detection-rules.yaml  # Detection rules
├── agents/                        # Agent definitions
├── policies/                      # Safety and handoff policies
└── mcp/                          # MCP server configs
```

---

## Support

**Need Help?**

- Ask Claude: `"Help me configure the orchestrator"`
- Check docs: `docs/getting-started.md`
- Review examples: `.claude/config.example.yaml`
- Report issues: https://github.com/anthropics/claude-code/issues

**Common Questions:**

Q: Can I change configuration later?
A: Yes! Edit `.claude/config.yaml` anytime

Q: What if auto-detection is wrong?
A: Override with `manual_override` in initialization template

Q: Can I disable certain agents?
A: Yes, set `enabled: false` for any agent

Q: How do I add custom agents?
A: Create `.claude/agents/myagent.md` and enable in config

---

**Ready to start? Just say:**

```
Initialize Claude Orchestrator for my project
```

And follow the prompts! 🚀
