# Setup Scenarios - Quick Reference

Choose your scenario and follow the appropriate guide.

---

## 🆕 Scenario 1: New Project (Clean Start)

**When to use:**
- Starting a new project from scratch
- Empty folder
- No existing codebase

### Quick Commands

```bash
# 1. Create and enter new directory
mkdir my-new-project && cd my-new-project

# 2. Clone orchestrator
git clone https://github.com/CleanExpo/Drop-In-Claude-Orchestrator.git .

# 3. Install
./scripts/install.sh  # or install.ps1 on Windows

# 4. Initialize
# Tell Claude:
"Initialize the orchestrator for a new [Next.js/Python/React] project"
```

### What Happens
- ✅ Clean installation
- ✅ Default configuration
- ✅ Full access to all directories
- ✅ Standard project structure created
- ✅ Ready in 5 minutes

**📖 Complete Guide:** [INSTALLATION-GUIDE.md → Scenario 1](.claude/INSTALLATION-GUIDE.md#scenario-1-new-project-clean-folder)

---

## 📦 Scenario 2: Existing Project (Takeover)

**When to use:**
- You have an existing codebase
- Want to add orchestrator capabilities
- Need to preserve existing code
- Production application

### Quick Commands

```bash
# 1. Navigate to your project
cd /path/to/your/existing/project

# 2. Download and run install script
curl -O https://raw.githubusercontent.com/CleanExpo/Drop-In-Claude-Orchestrator/master/scripts/install.sh
chmod +x install.sh
./install.sh

# 3. Context-Aware Initialize
# Tell Claude:
"Analyze my existing project and initialize the orchestrator.

Please:
1. Read my README.md to understand the project
2. Detect the project type and structure
3. Identify existing configuration files
4. Suggest optimal orchestrator configuration
5. Guide me through setup without breaking anything"
```

### What Happens

**Phase 1: Context Discovery** (Read-Only)
- 📖 Reads your README.md for context
- 🔍 Scans codebase structure (non-invasive)
- 🎯 Auto-detects project type (confidence score)
- 🔎 Identifies existing orchestration (if any)

**Phase 2: Analysis**
- 🛡️ Identifies protected areas (migrations, configs, critical code)
- ✅ Identifies safe zones (where agents can add files)
- 🔗 Suggests integration points

**Phase 3: Takeover Plan**
```
🎯 Project Analysis Complete

What I Found:
  Project: YourApp
  Type: Next.js Full-Stack (94% confidence)
  Maturity: Production (2 years, 10K users)
  Team: Small (3 developers)

Critical Constraints:
  ⚠️ Payment integration (do not touch)
  ⚠️ Database migrations (preserve)
  ⚠️ Existing tests (keep separate)

Recommended Configuration:
  - Autonomy: review_each_step (safe for production)
  - Write Scope: New files only in safe zones
  - Protected: 5 critical areas
  - Namespaced: tests/e2e-claude/ for new tests

Does this approach work for you? (Y/n/customize):
```

**Phase 4: Context-Aware Questionnaire**
- ❓ Questions informed by README analysis
- ❓ Team confirmation (from README)
- ❓ Autonomy level (recommended for production)
- ❓ Respect existing conventions
- ❓ Priority areas
- ❓ Custom constraints

**Phase 5: Custom Configuration**
- ⚙️ Generates `.claude/config.yaml` (custom)
- ⚙️ Creates `.claude/project-profile.yaml` (analysis)
- ⚙️ Respects existing structure
- ⚙️ Additive-only policy

**Phase 6: Validation**
- ✅ Pre-flight checks
- ✅ Suggests safe test task
- ✅ Verifies guardrails work

**Phase 7: Ready!**
- 🎉 Complete integration summary
- 🎉 Documentation links
- 🎉 Ready to build safely

**📖 Complete Guide:** [INSTALLATION-GUIDE.md → Scenario 2](.claude/INSTALLATION-GUIDE.md#scenario-2-existing-project-takeover)

**📖 Detailed Workflow:** [existing-project-takeover.md](.claude/workflows/existing-project-takeover.md)

---

## 🔍 Key Differences

| Feature | New Project | Existing Project |
|---------|-------------|------------------|
| **Setup** | Clone → Install → Initialize | Navigate → Install → Analyze & Initialize |
| **README** | Generates new | **Reads existing first** |
| **Detection** | Asks for type | Auto-detects from code |
| **Configuration** | Default templates | **Custom based on analysis** |
| **File Protection** | Standard defaults | **Custom to your structure** |
| **Test Directory** | `tests/` | `tests/e2e-claude/` **(namespaced)** |
| **Autonomy** | Trusted | **review_each_step (production safe)** |
| **Integration** | Full access | **Additive-only initially** |
| **Guardrails** | Standard | **Project-specific** |
| **Safety Level** | Standard | **Maximum (production-safe)** |

---

## 💡 Example Commands for Existing Projects

### Basic Takeover
```
Analyze my existing project and initialize the orchestrator.
Read my README.md first, then guide me through setup.
```

### Production App Takeover
```
Initialize orchestrator for my production application.

Critical requirements:
- This app has 10K active users
- Never touch payment processing code
- Keep existing test suite separate
- Start with maximum safety (review_each_step)
- Read README.md for full context
```

### Monorepo Takeover
```
Initialize orchestrator for my monorepo.

This is a Turborepo with:
- apps/web (Next.js)
- apps/api (Express)
- packages/ui (components)

Please read README.md and scope operations per package.
```

### Legacy Codebase Takeover
```
Initialize orchestrator for a legacy codebase.

This is a 5-year-old project:
- Mixed JS and TS
- No tests (we want to add)
- Active development
- Be extremely cautious

Read README.md and use maximum safety settings.
```

---

## 🎯 What Gets Read from README.md

When you use **Scenario 2 (Existing Project)**, the orchestrator reads your README.md to understand:

### Project Identity
- Project name
- Description and purpose
- Version/status

### Technical Context
- Technology stack
- Languages and frameworks
- Databases and tools
- Dependencies

### Team Context
- Team size
- Years active
- Development status
- Users/production status

### Constraints & Requirements
- Critical systems (payment, auth, etc.)
- Known issues or limitations
- Special requirements
- Areas to avoid

### Example README Analysis

**Your README.md:**
```markdown
# MyApp - E-commerce Platform

A full-stack e-commerce solution built with Next.js and Stripe.

## Stack
- Next.js 14 with App Router
- PostgreSQL + Prisma
- Stripe for payments
- Playwright tests

## Team
3 developers, active for 2 years, 10K active users

## Important
- Stripe integration is mission-critical (do not modify)
- Database schema is stable (no new migrations)
```

**Orchestrator's Understanding:**
```
✅ Detected: Next.js Full-Stack E-commerce
✅ Team: Small (3 devs), Mature (2 years)
✅ Status: Production (10K users)
✅ Stack: Next.js 14, PostgreSQL, Prisma, Stripe
✅ Constraints:
   - Protect Stripe integration
   - No database migrations
✅ Safety Level: Maximum (production app)
```

---

## ✅ Verification Checklist

### After New Project Setup
- [ ] `.claude/` directory created
- [ ] `config.yaml` generated
- [ ] Agents available (`ls .claude/agents/`)
- [ ] Can run simple task: "Add a comment to README.md"

### After Existing Project Setup
- [ ] `.claude/` directory created (doesn't conflict with existing)
- [ ] Custom `config.yaml` generated (respects your structure)
- [ ] `project-profile.yaml` contains your analysis
- [ ] Protected files identified (check config)
- [ ] Safe zones defined (check config)
- [ ] Namespaced test directory created: `tests/e2e-claude/`
- [ ] Safe test task passed
- [ ] No existing files modified

---

## 🚨 Troubleshooting

### "Orchestrator doesn't understand my project"

**Solution:**
```
Help the orchestrator understand my project.

My README.md might not have enough detail. Here's context:
- Type: [framework] application
- Languages: [list]
- Key dependencies: [list]
- Critical systems: [list]
- Team size: [number]
- Status: [development/production]

Please manually configure with this information.
```

### "Auto-detection is wrong"

**Solution:**
```
The auto-detection identified my project as [wrong type],
but it's actually a [correct type].

Please override detection and configure as [correct type].
```

### "Too cautious / Too aggressive"

**Solution:**
```
Adjust orchestrator autonomy from review_each_step to trusted.

I understand the risks and want faster iteration.
Please update .claude/config.yaml.
```

### "README.md doesn't exist"

**Solution:**
```
I don't have a README.md yet.

Project info:
- Name: [name]
- Type: [type]
- Stack: [stack]
- Status: [status]

Please configure manually and optionally generate a README.
```

---

## 📚 Documentation Links

### Quick Start
- **[5-Minute Quick Start](.claude/QUICK-START-INITIALIZATION.md)** - Fastest path to productivity
- **[Installation Guide](.claude/INSTALLATION-GUIDE.md)** - Complete setup for both scenarios

### Workflows
- **[Initialization Workflow](.claude/INITIALIZATION-WORKFLOW.md)** - Complete initialization process
- **[Existing Project Takeover](.claude/workflows/existing-project-takeover.md)** - Detailed 7-phase workflow

### Configuration
- **[Detection Rules](.claude/detection/project-detection-rules.yaml)** - How auto-detection works
- **[Handoff Validation](.claude/policies/handoff-validation.yaml)** - Quality assurance

### Examples
- **[PTA-MVP-001 Config](.claude/projects/PTA-MVP-001-config.yaml)** - Real-world custom configuration
- **[PTA Initialization Summary](.claude/projects/PTA-INITIALIZATION-SUMMARY.md)** - Complete project example

---

## 🎉 Quick Decision Tree

```
Do you have existing code?
├─ No  → Use Scenario 1 (New Project)
│         Quick: Clone → Install → Initialize
│
└─ Yes → Use Scenario 2 (Existing Project)
          Careful: Navigate → Install → Analyze & Initialize
          Features:
          ✓ Reads your README.md first
          ✓ Custom configuration
          ✓ Respects existing code
          ✓ Production-safe
```

---

**Ready to setup? Choose your scenario and dive in!** 🚀

**Questions?** Check the [complete documentation](.claude/INSTALLATION-GUIDE.md) or ask Claude for help!
