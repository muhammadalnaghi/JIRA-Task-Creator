# GitHub Authentication Setup

GitHub no longer accepts passwords for Git operations. You need to use either:

1. **Personal Access Token (PAT)** - Recommended for HTTPS
2. **SSH Keys** - Alternative method

## Method 1: Personal Access Token (Easiest)

### Step 1: Create a Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `jira-task-creator` (or any name you prefer)
4. Select expiration: Choose your preferred duration (30 days, 90 days, or no expiration)
5. **Select scopes**: At minimum, check:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if you plan to use GitHub Actions)
6. Click **"Generate token"**
7. **⚠️ IMPORTANT**: Copy the token immediately - you won't see it again!

### Step 2: Use the Token

When pushing, use your token as the password:

```bash
cd /mnt/d/WD/Jeel-RB/Atlassian/jira-task-creator

# Add and commit files
git add .
git commit -m "Initial commit: Jira Task Creator GUI application"

# Push (when prompted for password, use your token)
git push -u origin main
```

When prompted:
- **Username**: `muhammadalnaghi`
- **Password**: Paste your Personal Access Token (not your GitHub password!)

### Step 3: Save Credentials (Optional but Recommended)

To avoid entering the token every time:

```bash
# Cache credentials for 1 hour
git config --global credential.helper cache

# Or cache for longer (e.g., 24 hours = 86400 seconds)
git config --global credential.helper 'cache --timeout=86400'

# Or store permanently (less secure but convenient)
# git config --global credential.helper store
```

---

## Method 2: SSH Keys (Alternative)

### Step 1: Generate SSH Key (if you don't have one)

```bash
# Generate SSH key (use your GitHub email)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter to accept default file location
# Enter a passphrase (optional but recommended)
```

### Step 2: Add SSH Key to GitHub

```bash
# Display your public key
cat ~/.ssh/id_ed25519.pub
```

1. Copy the entire output
2. Go to GitHub: https://github.com/settings/ssh/new
3. Paste your public key
4. Give it a title: `jira-task-creator`
5. Click **"Add SSH key"**

### Step 3: Change Remote URL to SSH

```bash
cd /mnt/d/WD/Jeel-RB/Atlassian/jira-task-creator

# Change remote URL from HTTPS to SSH
git remote set-url origin git@github.com:muhammadalnaghi/jira-task-creator.git

# Test SSH connection
ssh -T git@github.com

# Push (no password needed!)
git push -u origin main
```

---

## Quick Fix for Current Issue

**Fastest solution** - Use Personal Access Token:

1. Create token: https://github.com/settings/tokens/new
2. Copy the token
3. Run:
   ```bash
   cd /mnt/d/WD/Jeel-RB/Atlassian/jira-task-creator
   git push -u origin main
   ```
4. When prompted:
   - Username: `muhammadalnaghi`
   - Password: **Paste your token** (not your GitHub password!)

---

## Troubleshooting

### "Authentication failed"
- Make sure you're using the token, not your password
- Check that the token has `repo` scope enabled
- Verify token hasn't expired

### "Permission denied"
- Verify the repository name is correct
- Check you have write access to the repository
- Make sure repository exists on GitHub

### "Repository not found"
- Create the repository on GitHub first: https://github.com/new
- Use the exact repository name: `jira-task-creator`

