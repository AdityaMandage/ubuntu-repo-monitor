# 📧 Free Email Notifications Setup

Get instant email alerts when Ubuntu repositories are updated - completely free!

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Gmail App Password

1. **Go to Gmail** and click your profile picture
2. **Click "Manage your Google Account"**
3. **Go to Security** → **2-Step Verification** (enable if not already)
4. **Click "App passwords"**
5. **Select "Mail"** and **"Other (Custom name)"**
6. **Type "Ubuntu Monitor"** and click **Generate**
7. **Copy the 16-character password** (save it somewhere safe)

### Step 2: Add Secrets to GitHub Repository

1. **Go to your repo**: https://github.com/AdityaMandage/ubuntu-repo-monitor
2. **Click Settings** → **Secrets and variables** → **Actions**
3. **Click "New repository secret"** and add these 3 secrets:

#### Secret 1: `EMAIL_USERNAME`
- **Name**: `EMAIL_USERNAME`
- **Value**: Your Gmail address (e.g., `youremail@gmail.com`)

#### Secret 2: `EMAIL_PASSWORD`
- **Name**: `EMAIL_PASSWORD`  
- **Value**: The 16-character app password from Step 1

#### Secret 3: `NOTIFICATION_EMAIL`
- **Name**: `NOTIFICATION_EMAIL`
- **Value**: Where you want to receive alerts (can be same as EMAIL_USERNAME)

### Step 3: That's It! 🎉

Email notifications are now active! You'll receive emails when:
- ✅ **Ubuntu repositories get updated**
- ❌ **The monitoring system encounters errors**

## 📧 What You'll Receive

### 🚨 Update Notification Email
```
Subject: 🚨 Ubuntu Repository Updates Detected!

Ubuntu Repository Updates Detected!

Time: 2025-08-09 14:30:15 UTC

Updates found in:
• noble-security: 2025-08-09 14:28 UTC
• noble-updates: 2025-08-09 14:29 UTC

View full logs: [Repository Logs]
GitHub Actions: [View Workflow Runs]

This notification was sent automatically by GitHub Actions
```

### ❌ Error Notification Email
```
Subject: ❌ Ubuntu Monitor Error

Ubuntu Repository Monitor encountered an error during execution.

Time: 2025-08-09 14:30:15 UTC
Workflow: Ubuntu Repository Monitor  
Run: 42

Please check the GitHub Actions logs for details:
https://github.com/AdityaMandage/ubuntu-repo-monitor/actions
```

## 🔧 Customization Options

### Change Email Frequency
Only get emails for specific repositories - edit `github_monitor.py`:

```python
# Only alert for security updates
if repo_name == 'noble-security' and is_new_update:
    self.updates_detected.append(f"{repo_name}: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
```

### Multiple Email Addresses
Want to notify multiple people? Change `NOTIFICATION_EMAIL` to:
```
email1@gmail.com,email2@yahoo.com,email3@outlook.com
```

### Custom Email Subject
Edit the workflow file to change:
```yaml
subject: "🚨 Ubuntu Repository Updates Detected!"
```

## 🛠️ Troubleshooting

### "Authentication failed" Error
- ✅ Make sure 2-Step Verification is enabled on Gmail
- ✅ Use App Password, not your regular Gmail password
- ✅ Double-check the EMAIL_USERNAME and EMAIL_PASSWORD secrets

### Not Receiving Emails
- ✅ Check your spam folder
- ✅ Verify the NOTIFICATION_EMAIL secret
- ✅ Make sure Gmail isn't blocking "less secure apps"

### Emails Going to Spam
Add these domains to your safe senders:
- `github.com`
- `noreply@github.com`

## 🆓 Cost Breakdown

**Completely Free!**
- ✅ Gmail app passwords: Free
- ✅ GitHub Actions email sending: Free  
- ✅ No limits on number of emails
- ✅ No monthly charges

## 🔒 Security Notes

- ✅ App passwords are safer than your main Gmail password
- ✅ GitHub secrets are encrypted and secure
- ✅ Only your repository can access these secrets
- ✅ You can revoke app passwords anytime

## 📱 Mobile Notifications

Want instant mobile alerts? 
- ✅ Enable Gmail push notifications on your phone
- ✅ Set custom notification sounds for the Ubuntu Monitor sender
- ✅ Use Gmail's VIP/Important sender features

---

**Need help?** Check your repo's Actions tab for detailed logs of email sending attempts!
