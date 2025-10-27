# Installation & Setup Guide

This guide covers two scenarios:
1. **New Project** - Starting from scratch in a clean folder
2. **Existing Project** - Adding orchestrator to take over an existing project

---

## Scenario 1: New Project (Clean Folder)

### Step 1: Clone the Orchestrator Repository

```bash
# Create a new directory for your project
mkdir my-new-project
cd my-new-project

# Clone the orchestrator
git clone https://github.com/CleanExpo/Drop-In-Claude-Orchestrator.git .

# Or download as ZIP and extract
```

### Step 2: Run Installation

**Windows:**
```powershell
.\scripts\install.ps1
```

**macOS/Linux:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

This copies the `.claude/` templates into your project.

### Step 3: Initialize for New Project

Tell Claude:
```
Initialize the orchestrator for a new project.

Project details:
- Name: My New Project
- Type: [e.g., Next.js Full-Stack, Python API, etc.]
- Purpose: [Brief description]
```

The orchestrator will:
1. ✅ Auto-detect project type (or ask if it's empty)
2. ✅ Guide you through setup questionnaire
3. ✅ Generate optimal configuration
4. ✅ Set up project structure
5. ✅ Create initial files if needed

### Step 4: Start Building

```
Create a Next.js project with authentication and database setup
```

---

## Scenario 2: Existing Project (Takeover)

### Step 1: Navigate to Your Existing Project

```bash
cd /path/to/your/existing/project
```

### Step 2: Clone/Download Orchestrator

**Option A: Clone into subdirectory then copy**
```bash
# Clone to temp directory
git clone https://github.com/CleanExpo/Drop-In-Claude-Orchestrator.git temp-orchestrator

# Copy scripts
cp -r temp-orchestrator/scripts .
cp -r temp-orchestrator/templates .

# Remove temp directory
rm -rf temp-orchestrator
```

**Option B: Download scripts directly**
```bash
# Download just the install script
curl -O https://raw.githubusercontent.com/CleanExpo/Drop-In-Claude-Orchestrator/master/scripts/install.sh
chmod +x install.sh
./install.sh
```

### Step 3: Run Installation (Preserves Your Files)

**Windows:**
```powershell
.\scripts\install.ps1
```

**macOS/Linux:**
```bash
./scripts/install.sh
```

**What happens:**
- ✅ Copies `.claude/` templates to your project
- ✅ **NEVER overwrites your existing files**
- ✅ Creates namespaced directories (e.g., `tests/e2e-claude/`)
- ✅ Detects your project structure

### Step 4: Context-Aware Initialization

Tell Claude:
```
Analyze my existing project and initialize the orchestrator.

Please:
1. Read my README.md to understand the project
2. Detect the project type and structure
3. Identify existing configuration files
4. Suggest optimal orchestrator configuration
5. Guide me through setup without breaking anything
```

**The orchestrator will:**
1. 📖 **Read your README.md** to understand:
   - Project purpose and goals
   - Current tech stack
   - Existing architecture
   - Team context
   - Known issues or constraints

2. 🔍 **Scan your codebase:**
   - Detect project type (Next.js, React, Python, etc.)
   - Map directory structure
   - Identify existing tests
   - Find configuration files
   - Detect dependencies

3. 🎯 **Generate takeover plan:**
   - Respect existing structure
   - Suggest safe integration points
   - Identify what NOT to touch
   - Propose guardrails

4. 📋 **Interactive questionnaire:**
   - Confirm auto-detected settings
   - Ask about team preferences
   - Define autonomy level
   - Set safety boundaries

5. ⚙️ **Generate custom configuration:**
   - Tailored to your existing project
   - Preserves your conventions
   - Adds orchestrator capabilities
   - Safe, non-breaking integration

### Step 5: Verification

```
Verify the orchestrator setup and show me:
1. What was detected about my project
2. What configuration was generated
3. What files are protected
4. Where agents can safely write
5. Suggested first task to test
```

---

## Key Differences: New vs Existing

| Aspect | New Project | Existing Project |
|--------|-------------|------------------|
| **Installation** | Clean install | Preserve existing files |
| **Detection** | Asks for project type | Auto-detects from code |
| **README** | Generates new README | Reads existing README |
| **Configuration** | Default templates | Custom based on existing |
| **Test Directory** | `tests/` | `tests/e2e-claude/` (namespaced) |
| **Git** | New .gitignore | Respects existing .gitignore |
| **Guardrails** | Standard defaults | Custom to your structure |

---

## Context-Aware Initialization Workflow

### For Existing Projects

When you say "Initialize the orchestrator for my existing project", Claude will:

#### Phase 1: Understanding Your Project

```
📖 Reading Project Context...

1. Reading README.md
   ✅ Project: "MyApp - E-commerce Platform"
   ✅ Tech Stack: Next.js 14, PostgreSQL, Stripe
   ✅ Team: 3 developers, 2 years old
   ✅ Status: Production, 10K users

2. Scanning Codebase
   ✅ Detected: Next.js Full-Stack (confidence: 94%)
   ✅ Found: 247 files, 15K lines of code
   ✅ Structure: Standard Next.js App Router
   ✅ Tests: Existing Playwright tests in tests/e2e/
   ✅ Database: Prisma with 15 models

3. Identifying Constraints
   ⚠️ Protected:
      - Existing tests/ directory
      - prisma/migrations/ (do not touch)
      - Stripe integration code
   ✅ Safe zones:
      - src/components/ (can add new)
      - src/lib/ (can add utilities)
      - docs/ (can enhance)
```

#### Phase 2: Generating Takeover Plan

```
🎯 Orchestrator Integration Plan

Based on your project, I recommend:

1. Agent Configuration:
   ✓ Enable: coder, tester, integrator
   ✓ Enable: master-fullstack (verify completeness)
   ✗ Disable: master-data (you have stable schema)

2. Test Strategy:
   ✓ Keep existing: tests/e2e/ (your Playwright tests)
   ✓ Add namespaced: tests/e2e-claude/ (orchestrator tests)
   ✓ No conflicts, both can coexist

3. Write Scope (where agents can work):
   ✓ src/components/**
   ✓ src/lib/**
   ✓ docs/**
   ✓ tests/e2e-claude/**

4. Protected Files (agents CANNOT touch):
   ✗ prisma/migrations/** (existing migrations)
   ✗ tests/e2e/** (your existing tests)
   ✗ .env* (environment variables)
   ✗ stripe-integration.ts (payment logic)

5. Integration Points:
   → New components can be added to src/components/
   → New utilities can be added to src/lib/
   → Documentation can be enhanced in docs/
   → E2E tests added in separate namespace

Proceed with this plan? (Y/n/customize):
```

#### Phase 3: Interactive Questionnaire

```
📋 Project-Specific Configuration

Q1: Team & Workflow
Your README mentions "3 developers". Confirmed?
[ ] Solo developer
[✓] Small team (2-5)
[ ] Medium team (6-20)
[ ] Large team (20+)

Q2: Autonomy Level
Given you have production users, I recommend "review_each_step"
for safety. What do you prefer?

[ ] Trusted - Fast iteration (risky for production)
[✓] Review Each Step - Safe for production (recommended)
[ ] Adaptive - Start careful, build trust

Q3: Existing Conventions
I detected you use:
- ESLint + Prettier (code style)
- Husky pre-commit hooks
- TypeScript strict mode

Should agents follow these? [Y/n]: Y

Q4: Priority Features
What should the orchestrator help with first?
[✓] Bug fixes and improvements
[✓] Test coverage expansion
[ ] New feature development
[✓] Documentation improvements
[ ] Performance optimization

Q5: Custom Constraints
Any specific rules or areas to avoid?
> Never modify Stripe integration code
> Keep existing database schema as-is
> Maintain current test structure

Noted. These will be added to guardrails.
```

#### Phase 4: Configuration Generation

```
⚙️ Generating Custom Configuration...

✅ Created: .claude/config.yaml
   - Project type: nextjs_fullstack
   - Autonomy: review_each_step
   - Write scope: Custom (safe zones only)
   - Protected: Your critical files
   - Respects: ESLint, Prettier, TypeScript rules

✅ Created: .claude/project-profile.yaml
   - Detected stack: Next.js 14, Prisma, Stripe
   - Existing tests: Preserved
   - Team context: Small team, production app
   - Constraints: Stripe & DB schema protected

✅ Updated: .gitignore
   - Added: .claude/logs/
   - Preserved: Your existing rules

✅ Namespaced: tests/e2e-claude/
   - Your tests: tests/e2e/ (untouched)
   - New tests: tests/e2e-claude/ (orchestrator)
```

#### Phase 5: Validation & Next Steps

```
✅ Orchestrator Integration Complete!

📊 Summary:
- Project analyzed: MyApp E-commerce
- Configuration: Custom for production app
- Files protected: 5 critical areas
- Safe write zones: 3 directories
- Integration: Non-breaking, namespaced

🎯 Suggested First Task (Safe Test):
"Add a utility function for date formatting in src/lib/dates.ts"

This will:
✓ Test agent can write to safe zone
✓ Verify guardrails work
✓ Confirm no existing files touched
✓ Validate integration

Ready to try? (Y/n):
```

---

## Advanced: Custom Integration Scenarios

### Scenario A: Monorepo Takeover

```
Initialize orchestrator for my monorepo.

This is a Turborepo with:
- apps/web (Next.js)
- apps/api (Express)
- packages/ui (shared components)
- packages/database (Prisma)

Please scope operations per package.
```

**Orchestrator response:**
```
✅ Monorepo detected: Turborepo

Configuration strategy:
1. Scope by workdir: Each package has own config
2. Shared policies: .claude/ at root
3. Per-package agents: .claude/apps/web/agents/
4. Global guardrails: Protect package.json, lockfiles

Proceed with monorepo setup? (Y/n):
```

### Scenario B: Legacy Codebase Takeover

```
Initialize orchestrator for a legacy project.

This is a 5-year-old codebase with:
- Mixed JS and TS
- No tests (we want to add)
- Some deprecated patterns
- Active development, can't break

Be extremely cautious.
```

**Orchestrator response:**
```
⚠️ Legacy codebase detected

Safety-first configuration:
1. Autonomy: review_each_step (MANDATORY)
2. Write scope: NEW files only initially
3. Protected: ALL existing code files
4. Strategy: Additive only (no refactoring without approval)

Initial capabilities:
✓ Add NEW test files (tests/e2e-claude/)
✓ Add NEW utility modules (lib/orchestrator-utils/)
✓ Add documentation (docs/)
✗ Modify existing code (requires explicit approval)

Proceed with maximum safety? (Y/n):
```

### Scenario C: Partially Orchestrated Project

```
This project already has some Claude configuration.

Detected:
- .claude/config.yaml (v1.0)
- Custom agents (2 agents)

Please:
1. Preserve existing config
2. Upgrade to v1.1 features
3. Add smart initialization
4. Keep custom agents

Safe upgrade path?
```

**Orchestrator response:**
```
✅ Existing orchestrator detected (v1.0)

Upgrade plan:
1. Backup current config: .claude/config.v1.0.backup
2. Merge v1.1 features:
   - Add auto-detection rules
   - Add handoff validation
   - Add initialization templates
3. Preserve your custom agents (keep as-is)
4. Maintain your existing guardrails
5. Add new capabilities without breaking changes

Upgrade to v1.1? (Y/n):
```

---

## Troubleshooting

### Issue: "Orchestrator doesn't understand my project"

**Solution:**
```
Help the orchestrator understand my project.

Here's context:
- It's a [framework] application
- Main languages: [list]
- Key dependencies: [list]
- Project structure: [describe]
- Special constraints: [list]

Please manually configure with this information.
```

### Issue: "Detection is wrong"

**Solution:**
```
The auto-detection identified my project as [wrong type],
but it's actually a [correct type].

Please override detection and configure as [correct type].
```

### Issue: "Too cautious / Too aggressive"

**Solution:**
```
Adjust orchestrator autonomy:
- Current: review_each_step
- Desired: trusted

I understand my project well and want faster iteration.
Please update .claude/config.yaml autonomy setting.
```

---

## Best Practices for Existing Project Integration

### ✅ DO

1. **Start with read-only analysis**
   ```
   Analyze my project (read-only, no changes yet)
   ```

2. **Review generated configuration before applying**
   ```
   Show me the proposed .claude/config.yaml before creating it
   ```

3. **Test with safe task first**
   ```
   Add a comment to README.md as a test
   ```

4. **Use namespaced directories**
   - Keep your tests in `tests/`
   - Add orchestrator tests in `tests/e2e-claude/`

5. **Start conservative, then relax**
   - Begin with `review_each_step`
   - Switch to `trusted` once comfortable

### ❌ DON'T

1. **Don't give full access immediately**
   - Start with restricted write scope
   - Expand gradually

2. **Don't skip README analysis**
   - Always let it read your README first
   - Provides crucial context

3. **Don't ignore existing conventions**
   - Tell it about ESLint, Prettier, style guides
   - Agents should follow your rules

4. **Don't protect too little**
   - Be explicit about critical files
   - Better safe than sorry

5. **Don't skip the test task**
   - Always test with a safe task first
   - Verify guardrails work

---

## Quick Command Reference

### New Project
```bash
# Setup
git clone https://github.com/CleanExpo/Drop-In-Claude-Orchestrator.git my-project
cd my-project
./scripts/install.sh

# Initialize
"Initialize orchestrator for new [project type] project"
```

### Existing Project
```bash
# Setup
cd existing-project
# Download and run install script
./scripts/install.sh

# Initialize (Context-Aware)
"Analyze my existing project and initialize orchestrator.
Please read README.md first, then guide me through setup."
```

### Takeover with Constraints
```
Initialize orchestrator for existing project.

Critical constraints:
- Production app with users
- Never touch: [list critical files]
- Existing tests must stay
- Follow our ESLint rules
- Start with maximum safety

Please read README.md and propose integration plan.
```

---

## Summary

**Two Paths, One Orchestrator:**

| New Project | Existing Project |
|-------------|------------------|
| Clean slate | Context-aware |
| Fast setup | Careful integration |
| Default config | Custom config |
| Full access | Restricted access |
| Generate structure | Respect structure |

**Both paths lead to:**
✅ Powerful AI-assisted development
✅ Safe guardrails
✅ Quality assurance
✅ Scalable workflows

---

**Ready to integrate? Choose your path and start!** 🚀
