# Windows-Specific Notes

PowerShell nuances, execution policy, and Windows-specific considerations.

## Execution Policy

### Common Issue: Scripts Won't Run

When running `.\scripts\install.ps1`, you might see:

```
.\scripts\install.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

### Solution: Set Execution Policy

**Option 1: For Current Session (Safest)**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install.ps1
```

**Option 2: For Current User (Recommended)**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Option 3: Check Current Policy**
```powershell
Get-ExecutionPolicy -List
```

### Understanding Policies

- `Restricted` - No scripts allowed (default on some systems)
- `RemoteSigned` - Local scripts OK, downloaded need signature
- `Bypass` - All scripts allowed, no warnings
- `Unrestricted` - All scripts allowed, warnings for downloaded

## Path Differences

### Windows vs Unix Paths

```powershell
# Windows uses backslashes
$path = ".\scripts\install.ps1"

# Unix uses forward slashes
path="./scripts/install.sh"
```

### In Config Files

Use forward slashes (works on both):
```yaml
paths:
  app: ./src/app          # ✓ Works everywhere
  api: ./src/app/api      # ✓ Works everywhere
```

## PowerShell vs CMD

### Use PowerShell (Not CMD)

The orchestrator scripts require PowerShell:

```powershell
# ✓ PowerShell (recommended)
.\scripts\install.ps1

# ✗ CMD (won't work)
scripts\install.ps1
```

### Check PowerShell Version

```powershell
$PSVersionTable.PSVersion
```

Requires PowerShell 5.1+ (included in Windows 10/11).

## Line Endings

### Git Configuration

Ensure Git handles line endings correctly:

```bash
git config --global core.autocrlf true
```

This converts LF → CRLF on checkout, CRLF → LF on commit.

### In Your Editor

Configure VS Code:
```json
{
  "files.eol": "\n",  // Use LF everywhere
  "files.insertFinalNewline": true
}
```

## Node.js on Windows

### Installation

Download from [nodejs.org](https://nodejs.org):
- LTS version recommended
- Includes npm automatically

### Verify Installation

```powershell
node --version
npm --version
```

### Common Issues

**Issue: `node` not found**
```powershell
# Add to PATH (if needed)
$env:PATH += ";C:\Program Files\nodejs"

# Or restart terminal after install
```

**Issue: npm permissions**
```powershell
# Use current user directory for global packages
npm config set prefix "$env:APPDATA\npm"
```

## MCP Servers on Windows

### Configuration Paths

**Cline (VS Code Extension):**
```
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

**Claude Desktop:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Path Format in MCP Config

Use forward slashes or escaped backslashes:

```json
{
  "command": "node",
  "args": ["C:/path/to/server.js"]  // ✓ Works
}
```

Or:
```json
{
  "command": "node",
  "args": ["C:\\path\\to\\server.js"]  // ✓ Works (escaped)
}
```

## Environment Variables

### Setting in PowerShell

**Temporary (current session):**
```powershell
$env:DATABASE_URL = "postgresql://localhost/mydb"
```

**Permanent (user):**
```powershell
[System.Environment]::SetEnvironmentVariable(
    "DATABASE_URL",
    "postgresql://localhost/mydb",
    "User"
)
```

### Using .env Files

Install dotenv (recommended):
```powershell
npm install dotenv
```

Then in your app:
```javascript
require('dotenv').config();
```

## Running Scripts

### PowerShell Scripts

```powershell
# Run in current directory
.\scripts\install.ps1

# Run from anywhere (full path)
C:\Projects\my-app\scripts\install.ps1

# With parameters
.\scripts\install.ps1 -Force
```

### Bash Scripts (via Git Bash or WSL)

If you have Git Bash or WSL:
```bash
./scripts/install.sh
```

## File Permissions

Windows doesn't have Unix-style file permissions (`chmod`).

Scripts don't need to be marked executable - PowerShell executes `.ps1` files directly.

## Common Commands Comparison

| Task | Windows (PowerShell) | Unix (Bash) |
|------|---------------------|-------------|
| List files | `Get-ChildItem` or `ls` | `ls` |
| Copy file | `Copy-Item` or `cp` | `cp` |
| Remove file | `Remove-Item` or `rm` | `rm` |
| View file | `Get-Content` or `cat` | `cat` |
| Find text | `Select-String` | `grep` |

## VS Code on Windows

### Recommended Extensions

- PowerShell (for `.ps1` editing)
- GitLens (for Git integration)
- Cline (Claude integration)

### Integrated Terminal

Set PowerShell as default:
1. Ctrl+Shift+P
2. "Terminal: Select Default Profile"
3. Choose "PowerShell"

### Settings

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.shell.windows": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
}
```

## Troubleshooting

### Scripts Not Running

```powershell
# Check execution policy
Get-ExecutionPolicy

# Allow scripts for session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run script
.\scripts\install.ps1
```

### Path Issues

```powershell
# Use forward slashes in config
paths:
  app: ./src/app  # ✓ Works on Windows

# Or PowerShell-specific variables
$projectPath = Join-Path $PSScriptRoot ".."
```

### Node Modules Issues

```powershell
# Clean install
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Git Line Endings

```powershell
# Check current setting
git config core.autocrlf

# Set to true for Windows
git config --global core.autocrlf true

# Refresh repository
git rm --cached -r .
git reset --hard
```

## Best Practices for Windows

### 1. Use Forward Slashes

In config files and code:
```yaml
# ✓ Good - works everywhere
paths:
  app: ./src/app

# ✗ Avoid - Windows only
paths:
  app: .\src\app
```

### 2. Be Careful with `$env:PATH`

```powershell
# ✓ Good - append to PATH
$env:PATH += ";C:\new\path"

# ✗ Bad - overwrites PATH
$env:PATH = "C:\new\path"
```

### 3. Use `.env` for Secrets

```powershell
# ✓ Good - in .env file
DATABASE_URL=postgresql://...

# ✗ Bad - in PowerShell profile
$env:DATABASE_URL = "postgresql://..."
```

### 4. Consider WSL for Unix Tools

If you need Unix tools frequently, install WSL2:

```powershell
wsl --install
```

Then you can use both:
```bash
# In WSL
./scripts/install.sh

# In PowerShell  
.\scripts\install.ps1
```

## Performance Tips

### Exclude Directories from Windows Defender

Add your project directory to exclusions:

1. Windows Security → Virus & threat protection
2. Manage settings → Exclusions
3. Add folder: `C:\Projects\your-project`

This speeds up `npm install` and file operations.

### Use SSD

If possible, place projects on SSD drive for better performance with `node_modules`.

## Getting Help

If you encounter Windows-specific issues:

1. **Check execution policy first**
   ```powershell
   Get-ExecutionPolicy
   ```

2. **Try with administrator privileges**
   - Right-click PowerShell → "Run as Administrator"

3. **Check PATH**
   ```powershell
   $env:PATH -split ";"
   ```

4. **Verify Node.js works**
   ```powershell
   node --version
   npm --version
   ```

---

**Remember**: Most cross-platform issues are solved by using forward slashes and proper environment variables.
