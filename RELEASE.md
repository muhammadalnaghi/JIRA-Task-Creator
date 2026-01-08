# Creating GitHub Releases with EXE

This guide explains how to build the EXE file and create a GitHub release.

## Prerequisites

- Windows OS (for building the EXE)
- Python 3.6+ installed
- PyInstaller: `pip install pyinstaller`
- Git installed

## Step 1: Build the EXE File

### Option A: Using the Build Script (Recommended)

1. On Windows, open Command Prompt in the repository folder
2. Run the build script:
   ```batch
   build_exe.bat
   ```
3. Wait for the build to complete (takes 2-5 minutes)
4. The EXE will be in the `dist/` folder: `dist\JiraTaskCreator.exe`

### Option B: Manual Build

```batch
pyinstaller --onefile --windowed --name "JiraTaskCreator" --clean --hidden-import=tkinter --hidden-import=requests --hidden-import=json --hidden-import=base64 --hidden-import=threading --hidden-import=importlib --noconfirm jira_task_gui.py
```

## Step 2: Create a GitHub Release

### Method 1: Using GitHub Web Interface (Easiest)

1. **Go to your repository on GitHub:**
   - Visit: https://github.com/muhammadalnaghi/jira-task-creator

2. **Click "Releases"** (right sidebar, or go to `/releases`)

3. **Click "Draft a new release"**

4. **Fill in the release details:**
   - **Tag version**: `v1.0.0` (or your version number)
   - **Release title**: `Jira Task Creator v1.0.0`
   - **Description**: 
     ```
     ## What's New
     - Initial release of Jira Task Creator GUI
     - Standalone EXE for Windows
     - No Python installation required
     
     ## Installation
     1. Download `JiraTaskCreator.exe`
     2. Place `tasks.txt` in the same folder (optional)
     3. Double-click `JiraTaskCreator.exe` to run
     
     ## Requirements
     - Windows 7 or later
     - No additional software needed (Python included in EXE)
     ```

5. **Attach the EXE file:**
   - Drag and drop `dist\JiraTaskCreator.exe` into the "Attach binaries" section
   - Or click "Attach binaries" and select the file

6. **Publish the release:**
   - Click "Publish release"

### Method 2: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
gh release create v1.0.0 dist/JiraTaskCreator.exe --title "Jira Task Creator v1.0.0" --notes "Initial release of Jira Task Creator GUI"
```

### Method 3: Using Git Tags and Manual Upload

1. **Tag the release:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Then create release on GitHub web interface** and attach the EXE

## Step 3: Verify the Release

1. Visit: https://github.com/muhammadalnaghi/jira-task-creator/releases
2. Verify the EXE file is attached
3. Test downloading the EXE
4. Update README.md with release information (optional)

## EXE File Information

- **File name**: `JiraTaskCreator.exe`
- **Size**: ~15-20 MB (includes Python runtime and all dependencies)
- **Platform**: Windows (7 or later)
- **Requirements**: None (standalone executable)

## Release Versioning

Follow semantic versioning:
- **v1.0.0** - Initial release
- **v1.0.1** - Bug fixes
- **v1.1.0** - New features
- **v2.0.0** - Major changes

## Troubleshooting

### Build fails with "Module not found"
**Solution**: Install all dependencies first:
```batch
pip install -r requirements.txt
pip install pyinstaller
```

### EXE is very large
**Solution**: This is normal. The EXE includes:
- Python interpreter
- tkinter GUI library
- requests library
- All dependencies

### Antivirus flags the EXE
**Solution**: PyInstaller EXEs sometimes trigger false positives. You can:
- Sign the EXE with a code signing certificate
- Add a note in the release about the false positive
- Users may need to allow it in their antivirus

## Updating .gitignore

The `.gitignore` already excludes:
- `dist/` folder
- `build/` folder
- `*.exe` files
- `*.spec` files

So build artifacts won't be committed to Git.

## Automated Releases (Future Enhancement)

You could set up GitHub Actions to automatically build and release on tags. Example workflow:

```yaml
# .github/workflows/release.yml
name: Build and Release

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build EXE
        run: |
          pyinstaller --onefile --windowed --name JiraTaskCreator --clean --hidden-import=tkinter --hidden-import=requests --hidden-import=json --hidden-import=base64 --hidden-import=threading --hidden-import=importlib --noconfirm jira_task_gui.py
      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: ./dist/JiraTaskCreator.exe
          asset_name: JiraTaskCreator.exe
          asset_content_type: application/octet-stream
```

