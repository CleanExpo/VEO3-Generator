# Complete Initialization Workflow

This document describes the end-to-end process for initializing the Claude Orchestrator, from first installation to first successful task.

## Table of Contents

1. [Overview](#overview)
2. [Initialization Flow](#initialization-flow)
3. [Auto-Detection Process](#auto-detection-process)
4. [Configuration Generation](#configuration-generation)
5. [Validation & Verification](#validation--verification)
6. [First Task Execution](#first-task-execution)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### Purpose

The initialization workflow ensures that the Claude Orchestrator is optimally configured for your specific project, team, and goals. It combines:

- **Auto-detection** - Automatically identifies project type and stack
- **Guided configuration** - Interactive questionnaire for preferences
- **Smart defaults** - Sensible defaults based on detection
- **Validation** - Ensures configuration is correct and complete

### Benefits

- **5-minute setup** - From zero to productive
- **Optimal configuration** - Tailored to your project
- **Safe by default** - Appropriate guardrails auto-configured
- **Easy to adjust** - Change settings anytime

---

## Initialization Flow

### High-Level Process

```
┌─────────────────────────────────────────────────────────┐
│ 1. Installation                                         │
│    - Run install script                                 │
│    - Copy templates to .claude/                         │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Auto-Detection                                       │
│    - Scan codebase                                      │
│    - Identify project type (confidence score)           │
│    - Detect technology stack                            │
│    - Map directory structure                            │
│    - Find sensitive files                               │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│ 3. User Questionnaire                                   │
│    - Confirm auto-detection results                     │
│    - Team context (size, experience)                    │
│    - Autonomy preference (critical!)                    │
│    - Safety configuration                               │
│    - Feature selection                                  │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Configuration Generation                             │
│    - Generate .claude/config.yaml                       │
│    - Create .claude/project-profile.yaml                │
│    - Configure agents                                   │
│    - Set up guardrails                                  │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Validation                                           │
│    - Verify paths exist                                 │
│    - Check agent definitions                            │
│    - Validate MCP configs                               │
│    - Test basic functionality                           │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│ 6. First Task                                           │
│    - Execute simple test task                           │
│    - Verify agent coordination                          │
│    - Confirm handoffs working                           │
└─────────────────────────────────────────────────────────┘
```

### Detailed Step-by-Step

#### Step 1: Installation

**Action:** Run the install script

**Windows:**
```powershell
.\scripts\install.ps1
```

**macOS/Linux:**
```bash
./scripts/install.sh
```

**What Happens:**
- Copies `templates/.claude/` to `.claude/` in your project
- Discovers existing MCP servers
- Detects Playwright if installed
- Creates `.claude/` directory structure

**Outputs:**
```
.claude/
├── claude.md
├── config.example.yaml
├── initialization-template.yaml  ← New!
├── QUICK-START-INITIALIZATION.md ← New!
├── agents/
├── detection/                    ← New!
│   └── project-detection-rules.yaml
├── policies/
│   ├── guardrails.md
│   ├── handoffs.md
│   └── handoff-validation.yaml   ← New!
└── mcp/
```

---

#### Step 2: Auto-Detection

**Trigger:** Say to Claude:
```
Initialize Claude Orchestrator for my project
```

**What Happens:**

1. **Scan for Package Manifests**
   - `package.json`, `requirements.txt`, `Gemfile`, etc.
   - Identifies package manager
   - Lists all dependencies

2. **Analyze Project Structure**
   - Directory tree mapping
   - File extension analysis
   - Import pattern detection

3. **Detect Configuration Files**
   - Framework configs (next.config.js, vite.config.ts, etc.)
   - Test configs
   - Build configs

4. **Identify Project Type**
   - Apply detection rules from `detection/project-detection-rules.yaml`
   - Calculate confidence scores
   - Rank possibilities

5. **Map Technology Stack**
   - Languages (TypeScript, Python, etc.)
   - Frameworks (Next.js, React, FastAPI, etc.)
   - Databases (PostgreSQL, MongoDB, etc.)
   - Testing tools (Playwright, Pytest, etc.)

6. **Find Sensitive Data**
   - `.env*` files
   - Credentials
   - API keys
   - Infrastructure code

**Output Example:**

```yaml
detection_results:
  project_type:
    detected: "nextjs_fullstack"
    confidence: 0.92
    alternatives:
      - type: "nextjs_app"
        confidence: 0.78
      - type: "react_spa"
        confidence: 0.45

  technology_stack:
    languages:
      - name: "TypeScript"
        percentage: 85
        version: "5.3.0"
      - name: "JavaScript"
        percentage: 15

    frameworks:
      - name: "Next.js"
        version: "14.0.0"
        confidence: 0.95
      - name: "React"
        version: "18.2.0"
        confidence: 0.95

    database:
      - name: "PostgreSQL"
        via: "Prisma"
        confidence: 0.90

    testing:
      - name: "Playwright"
        version: "1.40.0"
        type: "e2e"
      - name: "Vitest"
        version: "1.0.0"
        type: "unit"

    package_manager: "pnpm"

  project_structure:
    type: "nextjs_standard"
    paths:
      source: "./src"
      components: "./src/components"
      api: "./src/app/api"
      tests: "./tests"

  sensitive_files:
    - ".env.local"
    - ".env.production"
    - "prisma/migrations/**"
```

---

#### Step 3: User Questionnaire

**Trigger:** After auto-detection completes

**Interactive Prompts:**

```
═══════════════════════════════════════════════════════
CLAUDE ORCHESTRATOR INITIALIZATION
═══════════════════════════════════════════════════════

✅ Auto-Detection Complete

Detected: Next.js Full-Stack Application (92% confidence)

Stack:
  - Framework: Next.js 14 (App Router)
  - Language: TypeScript
  - Database: PostgreSQL via Prisma
  - Testing: Playwright + Vitest
  - Package Manager: pnpm

Is this correct? (Y/n/alternatives): _
```

**If user selects "Y":**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Project Identity

Project Name: my-awesome-app
Description: A full-stack application for [your purpose]

Primary Goals (select all that apply):
  [✓] Build new features
  [✓] Add test coverage
  [ ] Fix bugs
  [ ] Refactoring
  [ ] Documentation
  [ ] Deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Team Context

Team Size:
  [ ] Solo developer
  [✓] Small team (2-5)
  [ ] Medium team (6-20)
  [ ] Large team (20+)

Experience Level:
  [ ] Junior
  [ ] Mid-level
  [✓] Senior
  [ ] Mixed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Autonomy Preference ⚠️ IMPORTANT

How much autonomy should agents have?

1. TRUSTED (Recommended for experienced teams)
   ✓ Fast iteration
   ✓ Agents write within defined scope
   ✓ You review final results
   - Best for: Daily development, trusted environments

2. REVIEW EACH STEP
   ✓ Maximum control
   ✓ Approve every change
   - Slower iteration
   - Best for: Critical systems, learning phase

3. ADAPTIVE
   ✓ Starts with review
   ✓ Builds trust over time
   ✓ Balances speed and safety
   - Best for: New teams, new projects

Selection: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Safety Configuration

Risk Tolerance:
  [ ] Conservative - Maximum safety, frequent checks
  [✓] Balanced - Standard safety measures (Recommended)
  [ ] Aggressive - Minimal restrictions

Auto-detected Protected Files:
  ✓ .env.local, .env.production
  ✓ package-lock.json, pnpm-lock.yaml
  ✓ prisma/migrations/**

Add additional protected patterns? (y/N): N

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: Features & Capabilities

Select features to enable:
  [✓] Research - Web/documentation search
  [✓] Testing - E2E and unit tests
  [✓] Documentation - Auto-generate docs
  [ ] DevOps - CI/CD workflows
  [ ] Data Ops - Seeds/fixtures

Testing Coverage Target: 80%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONFIGURATION SUMMARY

Project: my-awesome-app
Type: Next.js Full-Stack
Team: Small (2-5), Senior
Autonomy: Trusted
Safety: Balanced
Features: Research, Testing, Documentation

Agents Enabled:
  ✓ coder
  ✓ tester
  ✓ research
  ✓ integrator
  ✓ stuck
  ✓ master-fullstack
  ✓ master-docs

Generate configuration? (Y/n): _
```

---

#### Step 4: Configuration Generation

**What Happens:**

1. **Generate Main Config** (`.claude/config.yaml`)
   - Project type and stack
   - Agent configuration
   - Paths and conventions
   - Safety guardrails
   - Feature flags
   - Workflow definitions

2. **Create Project Profile** (`.claude/project-profile.yaml`)
   - Detection results
   - Timestamp and metadata
   - Confidence scores
   - Signals used

3. **Configure Agents**
   - Enable/disable based on features
   - Set agent-specific configs
   - Configure handoff rules

4. **Set Up MCP Servers**
   - Configure based on detection
   - Set appropriate scopes
   - Enable/disable servers

**Generated Files:**

```
.claude/
├── config.yaml                  ← Main configuration
├── project-profile.yaml         ← Detection results
└── logs/
    └── initialization.log       ← Initialization log
```

**Example config.yaml snippet:**

```yaml
# Auto-generated by Claude Orchestrator
# Generated: 2024-01-15T10:30:00Z

project_type: nextjs_fullstack

metadata:
  name: "my-awesome-app"
  version: "1.0.0"
  initialized_at: "2024-01-15T10:30:00Z"
  detection_confidence: 0.92

team_context:
  size: "small"
  experience_level: "senior"
  autonomy: "trusted"

agents:
  coder:
    enabled: true
    definition: ".claude/agents/coder.md"
  tester:
    enabled: true
    definition: ".claude/agents/tester.md"
  # ... more agents

guardrails:
  write_scope:
    - "src/**"
    - "app/**"
    - "docs/**"
  protected_files:
    - ".env*"
    - "prisma/migrations/**"
    - "package-lock.json"
```

---

#### Step 5: Validation

**Automatic Checks:**

1. **Path Validation**
   ```
   ✓ Checking configured paths exist...
     ✓ src/
     ✓ src/components/
     ✓ src/app/api/
     ✓ tests/
   ```

2. **Agent Definition Validation**
   ```
   ✓ Checking agent definitions...
     ✓ .claude/agents/coder.md
     ✓ .claude/agents/tester.md
     ✓ .claude/agents/research.md
     ✓ .claude/agents/integrator.md
     ✓ .claude/agents/stuck.md
     ✓ .claude/agents/master-fullstack.md
     ✓ .claude/agents/master-docs.md
   ```

3. **MCP Configuration Validation**
   ```
   ✓ Checking MCP server configs...
     ✓ .claude/mcp/playwright.config.json
     ✓ .claude/mcp/fs.config.json
     ✓ .claude/mcp/git.config.json
   ```

4. **Dependency Validation**
   ```
   ✓ Checking dependencies...
     ✓ Node.js 18.x detected
     ✓ pnpm 8.x detected
     ⚠ Playwright not installed (optional)
   ```

**Validation Report:**

```
═══════════════════════════════════════════════════════
VALIDATION REPORT
═══════════════════════════════════════════════════════

Configuration: ✅ VALID

Paths: ✅ All paths exist
Agents: ✅ All definitions found
MCP: ✅ Configs valid
Dependencies: ⚠ 1 warning

Warnings:
  ⚠ Playwright not installed
    - Tester agent will use fallback smoke tests
    - Install with: pnpm add -D @playwright/test

Recommendations:
  → Install Playwright for E2E testing
  → Review .claude/config.yaml for customization
  → Read .claude/QUICK-START-INITIALIZATION.md

Ready to proceed! ✅
```

---

#### Step 6: First Task

**Test with Simple Task:**

```
Add a comment to the main page explaining what it does
```

**Expected Flow:**

```
┌─────────────────────────────────────────────────────┐
│ Orchestrator (analyzes request)                     │
│   → Simple task, single file                        │
│   → Route to: @coder only                           │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ @coder                                              │
│   1. Locates main page (src/app/page.tsx)          │
│   2. Reads file                                     │
│   3. Adds descriptive comment                       │
│   4. Writes file (within write_scope ✓)            │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ Result                                              │
│   ✅ Comment added successfully                     │
│   ✅ File: src/app/page.tsx                         │
│   ✅ No issues                                      │
└─────────────────────────────────────────────────────┘
```

**What This Tests:**
- ✅ Orchestrator routing
- ✅ Agent invocation
- ✅ File read access
- ✅ Write scope enforcement
- ✅ Basic functionality

**If Successful:**

```
✅ Initialization Complete!

Your orchestrator is ready. Try more complex tasks:
  → "Add a contact form with validation"
  → "Create E2E tests for the login flow"
  → "Research best practices for API rate limiting"

Documentation:
  → .claude/QUICK-START-INITIALIZATION.md
  → docs/getting-started.md
  → docs/customizing.md
```

---

## Auto-Detection Process

### Detection Algorithm

```python
def detect_project(codebase_path):
    """
    Multi-signal project type detection
    """
    # 1. Gather signals
    signals = {
        'files': scan_files(codebase_path),
        'packages': analyze_package_manifests(codebase_path),
        'structure': map_directory_structure(codebase_path),
        'configs': find_config_files(codebase_path),
        'imports': analyze_imports(codebase_path)
    }

    # 2. Score each project type
    scores = {}
    for project_type in PROJECT_TYPES:
        score = calculate_score(project_type, signals)
        scores[project_type] = score

    # 3. Apply confidence modifiers
    for project_type, score in scores.items():
        modifiers = get_confidence_modifiers(project_type, signals)
        scores[project_type] += sum(modifiers.values())

    # 4. Find best match
    best_match = max(scores.items(), key=lambda x: x[1])

    # 5. Get alternatives
    alternatives = [
        (type, score)
        for type, score in scores.items()
        if score >= 0.7 and type != best_match[0]
    ]

    return {
        'type': best_match[0],
        'confidence': best_match[1],
        'alternatives': alternatives,
        'signals': signals
    }
```

### Signal Weights

| Signal Type | Weight | Description |
|------------|--------|-------------|
| File Patterns | 35% | Config files, entry points |
| Package Manifest | 30% | Dependencies, scripts |
| Directory Structure | 20% | Folder organization |
| Config Files | 10% | Framework configs |
| Imports/Dependencies | 5% | Import patterns |

### Confidence Levels

| Range | Meaning | Action |
|-------|---------|--------|
| 90-100% | Very confident | Auto-apply |
| 70-89% | Confident | Ask confirmation |
| 50-69% | Uncertain | Show alternatives |
| < 50% | Cannot detect | Manual selection |

---

## Configuration Generation

### Template Resolution

```
User Preferences + Detection Results + Defaults = Final Config
```

**Priority Order:**
1. User explicit preferences (highest priority)
2. Auto-detected values
3. Smart defaults based on project type
4. System defaults (lowest priority)

### Example Resolution

```yaml
# User said: "I want trusted autonomy"
autonomy: "trusted"  # User preference wins

# Auto-detected: Next.js
project_type: "nextjs_fullstack"  # Detection result

# Not specified, use smart default for Next.js
paths:
  app: "./src/app"  # Smart default

# Not specified, use system default
logging:
  level: "info"  # System default
```

---

## Validation & Verification

### Pre-Flight Checks

Run before allowing initialization to complete:

1. **Path Existence**
   - All configured paths must exist
   - Create missing directories if safe
   - Warn if critical paths missing

2. **Agent Definitions**
   - All enabled agents must have .md files
   - Files must be readable
   - Basic syntax validation

3. **MCP Configs**
   - JSON configs must be valid
   - Required fields present
   - Commands/servers accessible

4. **Dependencies**
   - Node.js version compatible
   - Package manager available
   - Optional dependencies noted

### Validation Levels

| Level | Description | Action on Failure |
|-------|-------------|-------------------|
| CRITICAL | Must pass | Block initialization |
| ERROR | Should pass | Require confirmation |
| WARNING | Nice to have | Show warning, continue |
| INFO | Informational | Log only |

---

## First Task Execution

### Recommended First Tasks

**Level 1: Sanity Check**
```
Add a comment to the README explaining the project
```
- Tests: File reading, writing, basic routing

**Level 2: Simple Feature**
```
Add a utility function for formatting dates
```
- Tests: Code generation, file creation, scope enforcement

**Level 3: Multi-Agent**
```
Add a contact form with validation
```
- Tests: Multi-agent coordination, handoffs, testing

### Success Criteria

✅ **Initialization is successful if:**
- Configuration generated without errors
- All validations pass or warned
- First simple task completes successfully
- Agents respond and coordinate properly
- No unexpected errors or blocks

---

## Troubleshooting

### Common Issues

#### Issue: Auto-detection confidence too low

**Symptoms:**
```
⚠ Detection confidence: 45%
Cannot determine project type automatically
```

**Solutions:**
1. **Provide more context:**
   ```
   This is a Next.js 14 full-stack application with Prisma
   ```

2. **Use manual override:**
   ```
   Initialize with project type: nextjs_fullstack
   ```

3. **Check project structure:**
   - Ensure standard files present (package.json, etc.)
   - Verify frameworks installed

---

#### Issue: Validation failures

**Symptoms:**
```
❌ Path validation failed
   Path not found: ./src/components
```

**Solutions:**
1. **Create missing directories:**
   ```bash
   mkdir -p src/components
   ```

2. **Adjust paths in config:**
   Edit `.claude/config.yaml`:
   ```yaml
   paths:
     components: "./components"  # Adjust to actual path
   ```

3. **Use actual project structure:**
   ```
   Detect my actual project structure and update paths
   ```

---

#### Issue: Agents not responding

**Symptoms:**
```
@coder
(no response)
```

**Solutions:**
1. **Check agent definitions exist:**
   ```bash
   ls .claude/agents/
   ```

2. **Verify config enabled agents:**
   ```yaml
   agents:
     coder:
       enabled: true  # Must be true
   ```

3. **Restart initialization:**
   ```
   Re-initialize Claude Orchestrator with fresh configuration
   ```

---

#### Issue: Write scope violations

**Symptoms:**
```
❌ Cannot write to .env
   File is protected by guardrails
```

**Solutions:**
1. **This is correct behavior** - Protected files should not be modified

2. **If you need to modify:**
   ```
   I need to update .env, please help me do it safely
   ```

3. **Adjust guardrails if appropriate:**
   Edit `.claude/config.yaml`:
   ```yaml
   guardrails:
     protected_files:
       # Remove or comment out if needed
       # - ".env*"
   ```

---

### Getting Help

**Check Documentation:**
```
Read .claude/QUICK-START-INITIALIZATION.md
```

**Ask Claude:**
```
Help me troubleshoot my orchestrator configuration
```

**Review Logs:**
```
Check .claude/logs/initialization.log
```

**Start Over:**
```
Reset orchestrator configuration and start fresh
```

---

## Summary

### Initialization Checklist

- [x] Run install script
- [x] Trigger initialization
- [x] Review auto-detection results
- [x] Complete questionnaire
- [x] Confirm configuration
- [x] Pass validation
- [x] Execute first task
- [x] Verify success

### Next Steps

1. **Read documentation:**
   - `.claude/QUICK-START-INITIALIZATION.md`
   - `docs/getting-started.md`

2. **Try more tasks:**
   - Start with simple tasks
   - Progress to multi-agent workflows
   - Test phase gates and handoffs

3. **Customize as needed:**
   - Adjust `.claude/config.yaml`
   - Add custom agents
   - Configure workflows

4. **Monitor and improve:**
   - Review logs
   - Check metrics
   - Refine configuration

---

**You're ready to build! 🚀**

Start with:
```
Add [feature] to my project
```

The orchestrator will handle the rest.
