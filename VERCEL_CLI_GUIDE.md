# Vercel CLI Monitoring Guide

## ✅ CLIs Installed

### Vercel CLI
- **Version**: 41.7.0
- **User**: admin-5674
- **Status**: ✅ Logged in

### GitHub CLI  
- **Version**: 2.71.0
- **User**: CleanExpo
- **Status**: ✅ Logged in

---

## 🔍 Monitor Your Deployment

### Option 1: Vercel Dashboard (Easiest)
Visit: https://vercel.com/unite-group/veo-3-generator

The dashboard shows:
- ✅ Build status (Success/Failed)
- 📊 Build logs in real-time
- 🌐 Deployment URLs
- 📈 Performance metrics

---

## 🖥️ Vercel CLI Commands

### Check Deployment Status
```bash
# List all deployments for the project
vercel ls veo-3-generator

# Get latest deployment info
vercel inspect veo-3-generator-git-master-unite-group.vercel.app

# Check logs for specific deployment
vercel logs veo-3-generator-git-master-unite-group.vercel.app
```

### Switch to Correct Team/Organization
Your deployment is under "Unite-Group" organization. Switch to it:

```bash
# List available teams
vercel teams ls

# Switch to Unite-Group team (if available)
vercel switch unite-group

# Then run commands in that context
vercel ls
```

### Real-Time Build Monitoring
```bash
# Watch logs in real-time for latest deployment
vercel logs --follow veo-3-generator

# View build logs
vercel logs veo-3-generator --build

# View function logs (API endpoints)
vercel logs veo-3-generator --output
```

### Deployment Information
```bash
# Get deployment details
vercel inspect <deployment-url>

# List recent deployments
vercel ls veo-3-generator --limit 10

# Get deployment by ID
vercel inspect <deployment-id>
```

---

## 🐙 GitHub CLI Commands

### Repository Info
```bash
# View repository details
gh repo view CleanExpo/VEO3-Generator

# View recent commits
gh repo view CleanExpo/VEO3-Generator --json defaultBranchRef --jq '.defaultBranchRef.target.history'

# Check latest commit
git log -1 --oneline
```

### Check Repository Status
```bash
# View repo with web browser
gh repo view CleanExpo/VEO3-Generator --web

# Check recent actions/workflows
gh run list --repo CleanExpo/VEO3-Generator

# Watch workflow runs
gh run watch
```

---

## 🚀 Quick Deployment Check

### Method 1: Direct URL Check
```bash
# Check if API is live
curl https://veo-3-generator-git-master-unite-group.vercel.app/

# Check health endpoint
curl https://veo-3-generator-git-master-unite-group.vercel.app/health

# Check API docs
# Visit: https://veo-3-generator-git-master-unite-group.vercel.app/docs
```

### Method 2: Vercel CLI
```bash
# Go to project directory
cd "M:\VEO3-Consistency-Generator"

# Get latest deployment URL
vercel ls veo-3-generator | head -5

# Inspect specific deployment
vercel inspect <your-deployment-url>
```

### Method 3: GitHub Webhook
```bash
# Check if Vercel GitHub integration is active
gh api repos/CleanExpo/VEO3-Generator/hooks
```

---

## 📋 Troubleshooting

### Issue: Wrong Organization/Team Context
```bash
# Your deployment is under "Unite-Group" but CLI is in "admin-cleanexpo247s-projects"

# Solution 1: Switch teams
vercel switch unite-group

# Solution 2: Use team flag
vercel ls --team unite-group

# Solution 3: Use Vercel Dashboard
# Visit: https://vercel.com/dashboard
```

### Issue: Can't Find Deployment
```bash
# List all your teams
vercel teams ls

# Switch to correct team
vercel switch <team-name>

# Then list deployments
vercel ls
```

### Issue: Need Build Logs
```bash
# Option 1: Vercel Dashboard
# Go to: https://vercel.com/unite-group/veo-3-generator
# Click on deployment → View Build Logs

# Option 2: CLI (if in correct team context)
vercel logs veo-3-generator --build
```

---

## 🎯 Recommended Workflow

1. **Check Deployment Status**
   ```bash
   curl https://veo-3-generator-git-master-unite-group.vercel.app/health
   ```

2. **View in Browser**
   - Visit: https://veo-3-generator-git-master-unite-group.vercel.app/
   - Check: https://veo-3-generator-git-master-unite-group.vercel.app/docs

3. **Monitor via Dashboard**
   - Go to: https://vercel.com/unite-group/veo-3-generator
   - View real-time logs and metrics

4. **Check Git Status**
   ```bash
   cd "M:\VEO3-Consistency-Generator"
   git status
   git log -1
   ```

---

## 📊 Current Deployment Info

**Project**: veo-3-generator  
**Organization**: Unite-Group  
**Production URL**: veo-3-generator-git-master-unite-group.vercel.app  
**Branch**: master  
**Latest Commit**: 9077eac (Add Vercel deployment support)

---

## 🔗 Useful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Project Dashboard**: https://vercel.com/unite-group/veo-3-generator
- **GitHub Repo**: https://github.com/CleanExpo/VEO3-Generator
- **API Docs**: https://veo-3-generator-git-master-unite-group.vercel.app/docs
- **Vercel CLI Docs**: https://vercel.com/docs/cli

---

## 💡 Pro Tips

1. **Auto-reload on changes**: Vercel automatically deploys on git push
2. **Preview deployments**: Every branch gets its own preview URL
3. **Environment variables**: Set in Vercel Dashboard → Settings → Environment Variables
4. **Instant rollback**: Use dashboard to rollback to previous deployment
5. **Real-time logs**: Dashboard shows logs as they happen

---

## 🆘 If Build Fails

1. Check **Vercel Dashboard** → Build Logs
2. Look for error messages
3. Common issues:
   - Missing dependencies in requirements.txt
   - Python version mismatch
   - Environment variables not set
   - Import errors

Fix and push again - Vercel will auto-rebuild!
