# Safety & Security

Guidelines for safely using the Claude Orchestrator with appropriate permissions and protections.

## Overview

The orchestrator operates with multiple levels of safety controls:

1. **Permission Model**: What agents can and cannot do
2. **Approval Gates**: When user confirmation is required
3. **Protected Resources**: Files and operations that need extra care
4. **Audit Trail**: Logging what actions were taken

## Permission Model

### Agent Permissions

Each agent has a defined permission scope:

#### Read-Only Agents ✅
- **research**: Can only read web content
- **stuck**: Can only analyze, no writes

#### Read-Write with Approval ⚠️
- **coder**: Can read/write code files (requires approval)
- **tester**: Can read/write test files (requires approval)
- **integrator**: Can modify configurations (requires approval)
- **docs**: Can read/write documentation (requires approval)

#### High-Risk Operations 🚨
- **deployer**: Can deploy to environments (always requires approval)
- **data**: Can modify database (always requires approval)

### MCP Server Permissions

MCP servers have configured safety boundaries:

```json
{
  "safety": {
    "readOnly": true,          // Server can only read
    "requiresApproval": false, // No approval needed
    "allowWrites": false       // Writes disabled
  }
}
```

#### Filesystem MCP
```json
{
  "safety": {
    "readOnly": false,
    "requiresApproval": true,  // ⚠️ Approval for writes
    "protectedPaths": [
      ".env",
      ".env.local", 
      "**/*.key",
      "**/*.pem"
    ]
  }
}
```

#### Git MCP
```json
{
  "safety": {
    "readOnly": true,          // ✅ Read-only by default
    "requiresApproval": false,
    "allowWrites": false       // No commits/pushes
  }
}
```

#### Playwright MCP
```json
{
  "safety": {
    "readOnly": false,
    "requiresApproval": false,  // ✅ Safe for testing
    "allowedDomains": [
      "localhost",
      "127.0.0.1"
    ]
  }
}
```

## Approval Gates

### When Approval is Required

#### File Operations
- ✅ Auto-approved: Reading files
- ⚠️ Requires approval: Writing/modifying files
- 🚨 Always confirm: Deleting files

#### Command Execution
- ✅ Auto-approved: `npm test`, `npm run dev`
- ⚠️ Requires approval: `npm install`, build commands
- 🚨 Always confirm: Database migrations, deployments

#### Data Operations
- ✅ Auto-approved: Querying data
- ⚠️ Requires approval: Importing/exporting data
- 🚨 Always confirm: Bulk updates/deletes

#### Deployments
- 🚨 Always confirm: All deployment operations
- 🚨 Always confirm: Environment variable changes
- 🚨 Always confirm: Infrastructure changes

### Configuring Approval Requirements

In `config.yaml`:

```yaml
features:
  # Safety features
  requireApprovalForWrites: true    # File modifications
  requireApprovalForDeploy: true    # Deployments
  requireApprovalForData: true      # Data operations
```

Per-agent in `config.yaml`:

```yaml
agents:
  coder:
    enabled: true
    autoApprove: false  # ⚠️ Always ask before writes
    
  research:
    enabled: true
    autoApprove: true   # ✅ Safe, read-only
    
  deployer:
    enabled: true
    autoApprove: false  # 🚨 Always confirm
```

## Protected Resources

### Secrets and Credentials

**Never commit:**
```
.env
.env.local
.env.production
.env.*.local
*.key
*.pem
secrets.json
credentials.json
```

**Filesystem MCP Protection:**
```json
{
  "protectedPaths": [
    ".env",
    ".env.local",
    ".env.production",
    "config/secrets.json",
    "**/*.key",
    "**/*.pem"
  ]
}
```

These paths cannot be written to without explicit override.

### Database Access

**Protect connection strings:**
```bash
# Good: Use environment variables
DATABASE_URL=postgresql://user:pass@localhost/db

# Bad: Hardcode in code
const db = connect("postgresql://user:pass@localhost/db")
```

**Data operations safety:**
```yaml
agents:
  data:
    enabled: true
    autoApprove: false        # Always requires confirmation
    settings:
      maxRecordsPerOperation: 10000
      requireBackupBefore: true
      dryRunFirst: true
```

### Production Environments

**Deployment safety:**
```yaml
environments:
  production:
    requireApproval: true     # Always confirm
    requireTests: true        # Tests must pass
    requireReview: true       # Manual review step
    allowRollback: true       # Keep rollback option
```

**Pre-deployment checklist:**
```yaml
workflows:
  deploy:
    production:
      preChecks:
        - allTestsPass
        - stagingVerified
        - backupComplete
        - rollbackPlanDocumented
```

## Audit Trail

### Logging

All operations should be logged:

```yaml
logging:
  level: "info"
  file: ".claude/logs/orchestrator.log"
  rotation: true
  maxSize: "10MB"
  maxFiles: 5
```

**What gets logged:**
- Agent activations
- File modifications
- Command executions
- Deployment operations
- Data operations
- Approval requests and responses

**Log format:**
```
[2024-01-15 10:30:00] INFO - Orchestrator: Routing request to coder agent
[2024-01-15 10:30:01] INFO - Coder: Writing file src/components/Button.tsx
[2024-01-15 10:30:01] WARN - Filesystem: Approval required for write operation
[2024-01-15 10:30:05] INFO - User: Approved write operation
[2024-01-15 10:30:05] INFO - Coder: File written successfully
```

### Review Logs

Regularly review logs for:
- Unusual patterns
- Failed operations
- Security-related events
- Performance issues

```bash
# View recent activity
tail -f .claude/logs/orchestrator.log

# Search for errors
grep ERROR .claude/logs/orchestrator.log

# Review approval requests
grep "Approval required" .claude/logs/orchestrator.log
```

## Best Practices

### 1. Principle of Least Privilege

**Do:**
- ✅ Start with minimal permissions
- ✅ Enable agents only as needed
- ✅ Keep most MCP servers read-only
- ✅ Require approval for risky operations

**Don't:**
- ❌ Give all agents write access
- ❌ Disable approval gates
- ❌ Auto-approve deployments
- ❌ Skip logging

### 2. Environment Separation

```yaml
environments:
  development:
    permissive: true      # More freedom
    autoApprove: true     # Faster iteration
    
  staging:
    permissive: false     # More restrictions
    autoApprove: false    # Manual approval
    
  production:
    permissive: false     # Strictest
    autoApprove: false    # Always confirm
    requireReview: true   # Human review
```

### 3. Secret Management

**Use environment variables:**
```bash
# .env.example (commit this)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=your_api_key_here

# .env (DO NOT commit)
DATABASE_URL=postgresql://real_user:real_pass@prod-db:5432/prod
API_KEY=sk-real-api-key-xxxxx
```

**Load secrets safely:**
```typescript
// Good: From environment
const apiKey = process.env.API_KEY;

// Bad: Hardcoded
const apiKey = "sk-real-api-key-xxxxx";
```

### 4. Backup Before Bulk Operations

```typescript
// Data operations should backup first
async function bulkUpdate(records: any[]) {
  // 1. Create backup
  await backupDatabase();
  
  // 2. Perform operation
  try {
    await updateRecords(records);
  } catch (error) {
    // 3. Restore from backup if needed
    await restoreFromBackup();
    throw error;
  }
}
```

### 5. Test in Staging First

```yaml
workflows:
  deploy:
    steps:
      - agent: deployer
        target: staging
        description: "Deploy to staging first"
        
      - agent: tester
        description: "Verify staging deployment"
        requiredChecks:
          - healthCheckPasses
          - criticalFlowsWork
          - performanceAcceptable
          
      - agent: deployer
        target: production
        description: "Deploy to production"
        requiresApproval: true
```

## Security Checklist

### Initial Setup
- [ ] Review all agent permissions
- [ ] Configure MCP server safety settings
- [ ] Set up protected paths
- [ ] Enable logging
- [ ] Configure approval gates

### Before Each Session
- [ ] Verify current environment
- [ ] Check agent configurations
- [ ] Review protected resources
- [ ] Ensure backups are current

### During Development
- [ ] Review each approval request carefully
- [ ] Verify file changes before accepting
- [ ] Check command execution for safety
- [ ] Monitor logs for issues

### Before Deployment
- [ ] All tests pass
- [ ] Staging environment verified
- [ ] Database backup complete
- [ ] Rollback plan documented
- [ ] Team notified

### Regular Maintenance
- [ ] Review audit logs weekly
- [ ] Rotate credentials monthly
- [ ] Update dependencies regularly
- [ ] Review and update permissions

## Incident Response

### If Something Goes Wrong

#### 1. Stop Current Operations
```yaml
# Set dry-run mode
features:
  dryRun: true  # Prevents actual changes
```

#### 2. Review Logs
```bash
# Check what happened
tail -100 .claude/logs/orchestrator.log

# Look for errors
grep ERROR .claude/logs/orchestrator.log
```

#### 3. Assess Damage
- What was affected?
- Was data modified/deleted?
- Were credentials exposed?
- Did deployment fail?

#### 4. Rollback if Needed
```bash
# For deployments
./scripts/rollback.sh <previous-version>

# For database
./scripts/rollback-database.sh <backup-file>

# For Git
git revert <commit-hash>
```

#### 5. Document and Learn
- Document what happened
- Update safety measures
- Add preventive checks
- Update runbooks

## Common Pitfalls

### 1. Over-Trusting Automation
**Problem:** Blindly approving without review
**Solution:** Always read approval requests

### 2. Weak Secret Management
**Problem:** Secrets in code or logs
**Solution:** Use environment variables and secret managers

### 3. Missing Backups
**Problem:** Data loss with no recovery
**Solution:** Backup before bulk operations

### 4. Production Testing
**Problem:** Testing directly in production
**Solution:** Use staging environments

### 5. Ignoring Logs
**Problem:** Issues go unnoticed
**Solution:** Regular log review

## Additional Resources

- **MCP Security Guide**: https://modelcontextprotocol.io/security
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Secret Management**: Use tools like 1Password, AWS Secrets Manager
- **Deployment Safety**: Blue-green deployments, canary releases

---

**Remember**: Safety is not about preventing all action—it's about informed, controlled action with recovery options.
