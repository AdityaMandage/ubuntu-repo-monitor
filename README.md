# Ubuntu Repository Monitor

A simple system to continuously monitor Ubuntu Noble (24.04 LTS) repository updates by tracking the `Packages.gz` file timestamps.

## What it does

- 🔍 **Monitors** three Ubuntu Noble repositories:
  - `noble/main` - Main packages (original release)
  - `noble-updates` - Package updates 
  - `noble-security` - Security updates

- 📊 **Tracks** when the `Packages.gz` files are modified
- 📝 **Logs** all changes with timestamps
- 🚨 **Detects** new updates automatically
- 💾 **Stores** state to avoid duplicate notifications

## Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **That's it!** No cloud services needed - runs locally.

## Usage

### Option 1: Use PowerShell Menu (Recommended for Windows)
```powershell
.\Run-Monitor.ps1
```

### Option 2: Use Batch File
```cmd
run_monitor.bat
```

### Option 3: Direct Python Commands

**Single check:**
```bash
python ubuntu_repo_monitor.py --once
```

**Continuous monitoring (30-minute intervals):**
```bash
python ubuntu_repo_monitor.py 30
```

**Custom interval (e.g., every 15 minutes):**
```bash
python ubuntu_repo_monitor.py 15
```

## Log Files

The system creates these files in the `logs/` directory:

- **`update_summary.log`** - Master log with all updates
- **`noble-main_updates.log`** - Main repository changes
- **`noble-updates_updates.log`** - Updates repository changes  
- **`noble-security_updates.log`** - Security repository changes
- **`last_state.json`** - Tracks last known timestamps (don't delete!)

## Free Continuous Monitoring Solutions

Since you want to avoid cloud costs, here are free ways to keep it running:

### 1. **Windows Task Scheduler** (Recommended)
- Create a scheduled task to run every 30 minutes
- Use: `python ubuntu_repo_monitor.py --once`
- More reliable than keeping a process running 24/7

### 2. **Keep Process Running**
- Run: `python ubuntu_repo_monitor.py 30`
- Keep your computer on
- Process will run continuously until stopped

### 3. **GitHub Actions** (Free tier)
- Set up the script to run on GitHub's servers
- 2000 minutes/month free
- Runs in the cloud but costs nothing

### 4. **Raspberry Pi / Old Computer**
- Install on a low-power device
- Let it run 24/7
- Very low electricity cost

## Log Format

**Individual repository logs:**
```
[2025-08-09 10:23:17 UTC] 🆕 UPDATE DETECTED! Packages.gz modified: 2025-08-09 08:38 UTC
[2025-08-09 10:53:17 UTC] 📊 Check: Packages.gz last modified: 2025-08-09 08:38 UTC
```

**Summary log:**
```
[2025-08-09 10:23:17 UTC] noble-updates: UPDATE - Packages.gz modified at 2025-08-09 08:38 UTC
[2025-08-09 11:15:32 UTC] noble-security: UPDATE - Packages.gz modified at 2025-08-09 11:14 UTC
```

## Analyzing Update Frequency

After running for a while, you can analyze the logs to see:
- How often each repository gets updated
- Which repository is most active (usually `noble-security`)
- Update patterns (business hours, weekdays vs weekends)
- Time between security updates

## Troubleshooting

**Python not found?**
- Make sure Python is installed and in your PATH
- Try `python3` instead of `python`

**Network errors?**
- Check internet connection
- Ubuntu servers might be temporarily down

**Permission errors?**
- Make sure you can write to the current directory
- The script creates a `logs/` folder automatically

## Customization

Want to monitor different repositories? Edit the `repos` dictionary in `ubuntu_repo_monitor.py`:

```python
self.repos = {
    'focal-main': 'https://archive.ubuntu.com/ubuntu/dists/focal/main/binary-amd64/',
    'noble-universe': 'https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/',
    # Add more repositories...
}
```
