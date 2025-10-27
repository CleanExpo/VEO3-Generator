# Existing Project Takeover Workflow

**Purpose:** Safely integrate the orchestrator into an existing project by understanding context first.

---

## Workflow Trigger

User says one of:
- "Initialize orchestrator for my existing project"
- "Analyze my project and set up the orchestrator"
- "Add orchestrator to this project"
- "Take over this existing project with orchestrator"

---

## Phase 1: Context Discovery (Read-Only)

### Step 1.1: Read README.md

**Action:**
```
Read README.md to understand:
- Project name and description
- Purpose and goals
- Technology stack
- Team information
- Current status
- Known issues or constraints
```

**Extract:**
- Project identity (name, version, description)
- Tech stack (languages, frameworks, databases)
- Team context (size, experience level)
- Project maturity (new, established, legacy)
- Special constraints or requirements

**Example Output:**
```markdown
📖 README Analysis:

**Project:** MyApp - E-commerce Platform
**Description:** Full-stack e-commerce with Next.js and Stripe
**Tech Stack:** Next.js 14, TypeScript, PostgreSQL, Prisma, Stripe
**Team:** 3 developers, active for 2 years
**Status:** Production with 10K users
**Constraints:**
  - Stripe integration is critical (do not touch)
  - Database schema is stable (no migrations)
  - Existing test suite must be preserved
```

### Step 1.2: Scan Codebase Structure

**Action:**
```
Scan directory structure (non-invasive):
- List top-level directories
- Identify package.json, requirements.txt, etc.
- Find existing test directories
- Detect configuration files
```

**Example Output:**
```
📁 Directory Structure:

/src
  /app (Next.js App Router)
  /components (React components)
  /lib (utilities)
/prisma
  schema.prisma
  /migrations (15 files - DO NOT TOUCH)
/tests
  /e2e (existing Playwright tests)
/docs
  architecture.md
  api.md
package.json
next.config.js
.env.example
```

### Step 1.3: Auto-Detection

**Action:**
```
Run auto-detection:
- Apply detection rules from .claude/detection/project-detection-rules.yaml
- Calculate confidence score
- Identify alternatives if uncertain
```

**Example Output:**
```
🔍 Auto-Detection Results:

Detected Type: nextjs_fullstack
Confidence: 94%

Signals Found:
  ✓ next.config.js (strong)
  ✓ app/ directory (strong)
  ✓ app/api/ directory (strong)
  ✓ prisma/schema.prisma (strong)
  ✓ TypeScript (85% of code)

Alternative Interpretations:
  - nextjs_app (78% confidence)
  - react_spa (45% confidence)
```

### Step 1.4: Identify Existing Orchestration

**Action:**
```
Check if orchestrator already partially installed:
- Look for .claude/ directory
- Check for existing config files
- Identify version if present
```

**Example Output:**
```
⚠️ Partial orchestrator detected:
  - .claude/config.yaml (v1.0)
  - 2 custom agents

Recommendation: Upgrade path rather than fresh install
```

---

## Phase 2: Constraint Identification

### Step 2.1: Identify Protected Areas

**Action:**
```
Based on README and structure, identify files/directories that should be PROTECTED:

Protected by default:
  - .env*
  - node_modules/
  - .git/
  - package-lock.json, yarn.lock, pnpm-lock.yaml

Project-specific protected:
  - prisma/migrations/** (existing DB migrations)
  - tests/e2e/** (existing test suite)
  - [any mentioned in README as critical]
```

### Step 2.2: Identify Safe Zones

**Action:**
```
Identify directories where agents can safely ADD NEW files:

Safe zones:
  - src/components/** (can add new components)
  - src/lib/** (can add utilities)
  - docs/** (can enhance documentation)
  - tests/e2e-claude/** (new namespaced test directory)
```

### Step 2.3: Identify Integration Points

**Action:**
```
Suggest safe integration points:

✓ Can add new components to src/components/
✓ Can add new utilities to src/lib/
✓ Can create tests in tests/e2e-claude/
✓ Can enhance docs/ directory
✗ Should not modify prisma/migrations/
✗ Should not modify existing tests/e2e/
✗ Should not modify Stripe integration (if mentioned)
```

---

## Phase 3: Present Takeover Plan

### Step 3.1: Summary of Findings

**Present to user:**
```
🎯 Project Analysis Complete

**What I Found:**
  Project: MyApp E-commerce Platform
  Type: Next.js Full-Stack (94% confidence)
  Maturity: Production (2 years, 10K users)
  Team: Small (3 developers)

**Critical Constraints:**
  ⚠️ Stripe integration (do not touch)
  ⚠️ Database migrations (preserve as-is)
  ⚠️ Existing tests (keep separate)

**Recommended Configuration:**
  - Autonomy: review_each_step (safe for production)
  - Write Scope: New files only in safe zones
  - Protected: 5 critical areas identified
  - Namespaced: tests/e2e-claude/ for new tests

**Integration Strategy:**
  ✓ Additive only (no refactoring initially)
  ✓ Respect existing conventions
  ✓ Namespaced directories for orchestrator files
  ✓ Gradual trust building

Does this approach work for you? (Y/n/customize):
```

### Step 3.2: If User Says "Yes"

Proceed to Phase 4 (Questionnaire)

### Step 3.3: If User Says "Customize"

**Ask:**
```
What would you like to adjust?
1. Autonomy level (more/less cautious)
2. Write scope (expand/restrict)
3. Protected areas (add/remove)
4. Integration strategy
5. Other constraints

Please specify:
```

---

## Phase 4: Interactive Questionnaire

**Now that we understand the project, ask targeted questions:**

### Q1: Confirm Detection

```
📋 Project Configuration

Q1: Project Type Confirmation
Based on analysis, I detected: Next.js Full-Stack Application

Is this correct?
[✓] Yes, correct
[ ] No, it's actually: ___________
[ ] Show me alternatives
```

### Q2: Team & Workflow (Informed by README)

```
Q2: Team Context
Your README mentions "3 developers".

Current team structure:
[✓] Small team (2-5 developers) ← Suggested based on README
[ ] Solo developer
[ ] Medium team (6-20)
[ ] Large team (20+)

Development workflow:
[ ] Git Flow
[✓] Feature branches ← Detected from git branches
[ ] Trunk-based
[ ] Other: ___________
```

### Q3: Autonomy (Informed by Production Status)

```
Q3: Autonomy Level
⚠️ Your project is in production with users.

Recommended: review_each_step (safe for production)

What level of autonomy?
[ ] Trusted - Fast iteration (risky for production apps)
[✓] Review Each Step - Safe for production ← RECOMMENDED
[ ] Adaptive - Start cautious, build trust over time
```

### Q4: Respect Existing Conventions

```
Q4: Code Conventions
I detected the following in your project:

✓ ESLint configuration (.eslintrc.json)
✓ Prettier configuration (.prettierrc)
✓ TypeScript strict mode (tsconfig.json)
✓ Husky pre-commit hooks

Should agents follow these conventions?
[✓] Yes, respect all existing conventions
[ ] No, agents can use their own style
[ ] Custom rules: ___________
```

### Q5: Priority Areas

```
Q5: What Should Orchestrator Help With?
Based on your README, I see potential areas:

Priority areas (select all that apply):
[✓] Bug fixes and improvements
[✓] Test coverage expansion ← README mentions "need more tests"
[ ] New feature development
[✓] Documentation improvements
[ ] Performance optimization
[ ] Refactoring legacy code

Any specific areas to focus on? ___________
Any areas to avoid? ___________
```

### Q6: Custom Constraints

```
Q6: Additional Constraints
Are there any specific rules I should know?

From README, I noted:
  - "Stripe integration is mission-critical"
  - "Database schema is stable"

Additional constraints:
> [User can add more]
> Example: "Never modify payment processing code"
> Example: "Keep existing test structure intact"
```

### Q7: Integration Pace

```
Q7: Integration Pace
How should we integrate the orchestrator?

[✓] Cautious - Additive only, no modifications to existing code
[ ] Balanced - Can modify with approval
[ ] Aggressive - Full refactoring and optimization allowed

Given production status, "Cautious" is recommended.
```

---

## Phase 5: Configuration Generation

### Step 5.1: Generate Custom Config

**Create `.claude/config.yaml` with:**

```yaml
# Auto-generated for: MyApp E-commerce Platform
# Based on: README.md analysis + user questionnaire
# Date: 2025-10-28

project_identity:
  name: "MyApp"
  version: "2.0.0"  # From README
  description: "E-commerce platform with Next.js and Stripe"

  # From README analysis
  context:
    status: "production"
    users: "10K active users"
    team_size: 3
    years_active: 2
    critical_systems: ["stripe_integration", "payment_processing"]

project_type: nextjs_fullstack  # Auto-detected, 94% confidence

team_context:
  size: "small"
  experience_level: "senior"  # Inferred from 2 years production
  autonomy: "review_each_step"  # User selected (production safety)
  workflow: "feature_branch"  # Detected from git

# Custom guardrails based on project analysis
guardrails:
  write_scope:
    # SAFE ZONES (can add NEW files)
    - "src/components/**"
    - "src/lib/**"
    - "docs/**"
    - "tests/e2e-claude/**"  # Namespaced

  protected_files:
    # DEFAULT PROTECTION
    - ".env*"
    - "package-lock.json"
    - "pnpm-lock.yaml"

    # PROJECT-SPECIFIC PROTECTION (from README)
    - "prisma/migrations/**"  # Existing migrations
    - "tests/e2e/**"  # Existing test suite
    - "src/lib/stripe/**"  # Payment integration
    - "**/payment*.ts"  # Payment-related files

  require_tests_to_pass: true
  strict_mode: true  # Production app

  # CUSTOM: Additive-only initially
  modification_policy: "additive_only"
  # Agents can add NEW files but not MODIFY existing ones
  # User can override per-task with explicit approval

# Respect existing conventions
code_conventions:
  eslint: true  # Follow .eslintrc.json
  prettier: true  # Follow .prettierrc
  typescript_strict: true  # Follow tsconfig.json
  pre_commit_hooks: true  # Run Husky hooks

# Integration strategy
integration:
  strategy: "cautious"  # User selected
  namespaced_tests: "tests/e2e-claude/"
  preserve_existing_tests: true
  respect_existing_structure: true

# From questionnaire
priority_areas:
  - "bug_fixes"
  - "test_coverage"
  - "documentation"

custom_constraints:
  - "Never modify Stripe integration code"
  - "Database schema is stable - no migrations"
  - "Keep existing test suite separate and untouched"
```

### Step 5.2: Generate Project Profile

**Create `.claude/project-profile.yaml`:**

```yaml
# Project Profile - Auto-generated from analysis
# Source: README.md + codebase scan + questionnaire

detection_results:
  timestamp: "2025-10-28T10:30:00Z"
  method: "readme_analysis + codebase_scan"

  detected_type: "nextjs_fullstack"
  confidence: 0.94

  signals_used:
    - "README.md content analysis"
    - "next.config.js presence"
    - "app/ directory structure"
    - "prisma/schema.prisma"
    - "TypeScript 85% of codebase"

readme_analysis:
  project_name: "MyApp"
  description: "E-commerce platform with Next.js and Stripe"
  tech_stack:
    - "Next.js 14"
    - "TypeScript"
    - "PostgreSQL"
    - "Prisma"
    - "Stripe"
  team_info: "3 developers"
  status: "production"
  users: "10K active"
  constraints:
    - "Stripe integration critical"
    - "Database schema stable"

existing_structure:
  directories:
    - "src/app"
    - "src/components"
    - "src/lib"
    - "prisma"
    - "tests/e2e"
    - "docs"

  protected_areas:
    - "prisma/migrations/**"
    - "tests/e2e/**"
    - "src/lib/stripe/**"

  safe_zones:
    - "src/components/**"
    - "src/lib/**"
    - "docs/**"
    - "tests/e2e-claude/**"

integration_plan:
  approach: "additive_only"
  rationale: "Production app with users - maximum safety"
  first_task_suggestion: "Add utility function to src/lib/"
  gradual_trust_building: true
```

---

## Phase 6: Validation & Testing

### Step 6.1: Pre-Flight Checks

```
✅ Running Pre-Flight Checks...

1. Configuration valid: ✅
2. All paths exist: ✅
3. Protected files identified: ✅ (5 areas)
4. Safe zones defined: ✅ (4 directories)
5. Agent definitions present: ✅
6. No conflicts detected: ✅

Ready to activate orchestrator.
```

### Step 6.2: Suggest Safe Test Task

```
🧪 Recommended First Task (Safe Test):

"Add a date formatting utility function"

This task will:
✓ Create new file: src/lib/formatDate.ts
✓ Test write permissions in safe zone
✓ Verify guardrails work correctly
✓ Confirm existing code untouched
✓ No risk to production

Would you like to try this test task? (Y/n):
```

### Step 6.3: If User Accepts Test Task

**Execute test task with full logging:**
```
🚀 Executing Test Task...

1. Analyzing requirements... ✅
2. Checking write permissions... ✅ (src/lib/ is in write_scope)
3. Creating new file... ✅
4. Generating code... ✅
5. Running eslint... ✅ (follows your rules)
6. Running prettier... ✅ (follows your rules)
7. No existing files modified... ✅
8. Guardrails verified... ✅

✅ Test task completed successfully!

File created: src/lib/formatDate.ts
No existing files modified
All conventions followed
Guardrails working correctly

🎉 Orchestrator is ready for production use!

What would you like to build next?
```

---

## Phase 7: Handoff to User

### Final Summary

```
✅ Orchestrator Integration Complete!

📊 Configuration Summary:
  - Project: MyApp E-commerce Platform
  - Type: Next.js Full-Stack
  - Status: Production-ready integration
  - Safety: review_each_step (maximum safety)
  - Protected: 5 critical areas
  - Safe zones: 4 directories
  - Test task: ✅ Passed

📁 Files Created:
  - .claude/config.yaml (custom configuration)
  - .claude/project-profile.yaml (analysis results)
  - .claude/logs/initialization.log (full log)

🎯 What's Protected:
  ✗ prisma/migrations/** (your DB migrations)
  ✗ tests/e2e/** (your existing tests)
  ✗ src/lib/stripe/** (payment integration)
  ✗ .env* (environment variables)
  ✗ package-lock.json (lockfiles)

✅ Where Agents Can Work:
  ✓ src/components/** (add new components)
  ✓ src/lib/** (add new utilities)
  ✓ docs/** (enhance documentation)
  ✓ tests/e2e-claude/** (add new tests)

📖 Documentation Created:
  - .claude/INSTALLATION-GUIDE.md (setup reference)
  - .claude/project-profile.yaml (your project analysis)

🚀 Ready to Build!

Start with:
  "Add comprehensive tests for the checkout flow"
  "Improve documentation for the API endpoints"
  "Create a reusable modal component"

The orchestrator understands your project and will:
  ✓ Respect your existing code
  ✓ Follow your conventions
  ✓ Ask before modifying anything
  ✓ Keep production safe
```

---

## Error Handling

### If README.md doesn't exist

```
⚠️ No README.md found.

To properly integrate the orchestrator, I need to understand your project.

Options:
1. Create a basic README.md describing your project, then re-run
2. Provide project information manually via questionnaire
3. Skip context analysis (less safe, not recommended)

What would you like to do? (1/2/3):
```

### If auto-detection confidence is low

```
⚠️ Auto-detection confidence: 45%

I'm uncertain about your project type.

Detected possibilities:
  1. React SPA (45%)
  2. Next.js App (40%)
  3. Custom setup (15%)

Could you clarify what type of project this is?
> [User provides information]

Thank you! Proceeding with manual configuration...
```

### If critical conflicts detected

```
❌ Critical Conflict Detected

I found a .claude/config.yaml that conflicts with detected project type.

Existing config says: python_api
Auto-detected type: nextjs_fullstack

Options:
1. Keep existing config (skip re-initialization)
2. Override with new detection
3. Merge configurations (manual review)

What would you like to do? (1/2/3):
```

---

## Summary

**This workflow ensures:**
✅ Context-aware integration
✅ README-informed configuration
✅ Safe takeover of existing projects
✅ Respect for existing conventions
✅ Protection of critical code
✅ Gradual trust building
✅ Validation before activation

**User experience:**
1. "Initialize orchestrator for existing project"
2. Agent reads README + scans code
3. Agent presents findings and plan
4. Interactive questionnaire (context-aware)
5. Custom configuration generated
6. Safe test task to verify
7. Ready to build!

**Result:** Production-safe orchestrator integration tailored to your specific project.
