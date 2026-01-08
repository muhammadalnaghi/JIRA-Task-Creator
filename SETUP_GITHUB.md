# GitHub Setup Instructions

This document provides instructions for uploading this repository to GitHub.

## Repository Created

All sensitive data has been removed and replaced with placeholders:

- ✅ **Jira URLs**: Replaced with `https://your-domain.atlassian.net`
- ✅ **API Tokens**: Replaced with `YOUR_API_TOKEN_HERE`
- ✅ **Email addresses**: Replaced with `your-email@example.com`
- ✅ **Project Keys**: Replaced with `PROJECT`
- ✅ **Tasks file**: Contains only sample/demo tasks
- ✅ **Company names**: Removed all references

## Files Included

```
jira-task-creator/
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md              # Comprehensive documentation
├── SETUP_GITHUB.md        # This file
├── create_jira_tasks.py   # Core API functions (sanitized)
├── jira_task_gui.py       # GUI application (sanitized)
├── tasks.txt              # Sample tasks file
├── requirements.txt       # Python dependencies
├── run_gui.bat           # Windows launcher
└── install_requirements.bat  # Install script
```

## Steps to Upload to GitHub

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `jira-task-creator` (or your preferred name)
3. Description: "A Python GUI application for creating Jira tasks and subtasks via REST API"
4. Visibility: Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"

### 2. Connect Local Repository to GitHub

Run these commands in the `jira-task-creator` directory:

```bash
# Add all files
git add .

# Commit files
git commit -m "Initial commit: Jira Task Creator GUI application"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/muhammadalnaghi/jira-task-creator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: If you need to authenticate:
- Use Personal Access Token (not password)
- Or use SSH: `git@github.com:muhammadalnaghi/jira-task-creator.git`

### 3. Verify Upload

1. Visit your repository on GitHub
2. Verify all files are present
3. Check that README.md displays correctly
4. Verify sensitive data is not present

## Verification Checklist

Before pushing to GitHub, verify:

- [ ] No real Jira URLs in code
- [ ] No real API tokens in code
- [ ] No real email addresses in code
- [ ] No company-specific data in tasks.txt
- [ ] All placeholders use generic examples
- [ ] .gitignore excludes sensitive files
- [ ] README.md is complete and accurate

## Post-Upload

After uploading:

1. **Add Topics/Tags**: Add tags like `python`, `jira`, `gui`, `tkinter`, `automation`
2. **Add Description**: Update repository description if needed
3. **Enable Issues**: Enable GitHub Issues for bug reports and feature requests
4. **Add README badges**: Consider adding badges for Python version, license, etc.

## Security Notes

- ✅ All sensitive data has been removed
- ✅ Default values are placeholders only
- ✅ Users must configure their own credentials
- ✅ No hardcoded tokens or passwords
- ✅ .gitignore prevents accidental commits of sensitive files

## Next Steps

Users who clone this repository will need to:

1. Install dependencies: `pip install -r requirements.txt`
2. Configure their Jira credentials in the GUI
3. Create their own `tasks.txt` file
4. Run: `python jira_task_gui.py`

## License

This project is licensed under MIT License - see LICENSE file for details.

