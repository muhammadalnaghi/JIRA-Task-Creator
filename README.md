# Jira Task Creator

A Python GUI application for creating Jira tasks and subtasks via the REST API. Built with tkinter for cross-platform compatibility.

## Features

- ✅ **GUI Interface**: User-friendly graphical interface
- ✅ **Standalone EXE**: No Python installation required (Windows)
- ✅ **Batch Creation**: Create multiple tasks from a text file
- ✅ **Parent/Subtask Support**: Automatically create and link subtasks to parent tasks
- ✅ **Auto-linking**: Use `PARENT: PARENT-1` placeholders for automatic subtask linking
- ✅ **Tasks Preview**: Preview tasks before creating them
- ✅ **Real-time Logging**: See task creation progress in real-time
- ✅ **Error Handling**: Detailed error messages for troubleshooting

## Download

**Latest Release**: [Download EXE](https://github.com/muhammadalnaghi/jira-task-creator/releases/latest)

For Windows users, you can download the standalone EXE file - no Python installation needed!

## Screenshots

The application provides a clean interface for:
- Configuring Jira connection settings
- Previewing tasks from file
- Creating tasks with real-time progress tracking

## Installation

### Option 1: Download Standalone EXE (Windows - Recommended)

1. **Download the latest release:**
   - Go to [Releases](https://github.com/muhammadalnaghi/jira-task-creator/releases/latest)
   - Download `JiraTaskCreator.exe`

2. **Run the application:**
   - Double-click `JiraTaskCreator.exe`
   - No installation or Python required!

3. **Optional**: Place `tasks.txt` in the same folder as the EXE

### Option 2: Run from Source Code

#### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python on Windows/Mac, may need installation on Linux)
- Jira API token

#### Quick Install (Windows)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or double-click `install_requirements.bat`

2. **Run the application:**
   ```bash
   python jira_task_gui.py
   ```
   Or double-click `run_gui.bat`

### Manual Install

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/muhammadalnaghi/jira-task-creator.git
   cd jira-task-creator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your settings:**
   - Edit `jira_task_gui.py` and update `DEFAULT_EMAIL` and `DEFAULT_API_TOKEN` (optional)
   - Or enter them in the GUI when running

4. **Run the application:**
   ```bash
   python jira_task_gui.py
   ```

## Configuration

### Getting Your Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label (e.g., "Task Creator")
4. Copy the token and use it in the application

### Setting Default Values (Optional)

Edit `jira_task_gui.py` and update these constants:

```python
DEFAULT_EMAIL = "your-email@example.com"
DEFAULT_API_TOKEN = "YOUR_API_TOKEN_HERE"
```

Or simply enter them in the GUI when running.

## Usage

### 1. Configure Settings

When you run the GUI:
- Enter your **Jira Base URL** (e.g., `https://your-domain.atlassian.net`)
- Enter **Project Key** (e.g., `PROJECT`)
- Enter your **Email** address
- Enter your **API Token**

### 2. Prepare Tasks File

Create or edit `tasks.txt` with your tasks (see format below).

### 3. Select Tasks File

- Click "Browse" to select `tasks.txt`
- Click "Edit" to open the file in your text editor
- Use "Refresh Preview" to see parsed tasks

### 4. Create Tasks

- Click "Create Tasks" button
- Watch progress in the Output Log
- View created issue keys and links

## Tasks File Format

Create a `tasks.txt` file with the following format:

```
Task Summary/Title
Task description line 1
Task description line 2
More description...
---
Next Task Summary
Next task description...
---
PARENT: PARENT-1
Subtask Summary
Subtask description...
---
PARENT: PARENT-1
Another Subtask Summary
Another subtask description...
---
```

### Format Rules

- **Tasks are separated by `---`** on its own line
- **First line** of each task is the summary/title
- **Following lines** until the next `---` are the description
- **Empty lines** are preserved in descriptions

### Creating Subtasks

You have two options:

#### Option 1: Auto-linking (Recommended)

Use placeholder references that automatically link to parent tasks created in the same run:

```
PARENT: PARENT-1
Subtask Title
Subtask description...
```

- `PARENT: PARENT-1` refers to the 1st parent task in the file
- `PARENT: PARENT-2` refers to the 2nd parent task
- `PARENT: PARENT-3` refers to the 3rd parent task, etc.

**How it works:**
1. Parent tasks are created first
2. Their issue keys are stored internally
3. Subtasks with `PARENT-1`, `PARENT-2`, etc. are automatically linked to the corresponding parent

#### Option 2: Direct Parent Key

Use an existing issue key:

```
PARENT: PROJECT-123
Subtask Title
Subtask description...
```

This links the subtask directly to the existing issue `PROJECT-123`.

## Examples

### Example 1: Simple Tasks

```
Implement User Authentication
Add login and logout functionality.
Implement password hashing.
---
Create User Dashboard
Design and implement the main dashboard.
Include user profile section.
---
```

### Example 2: Task with Subtasks (Auto-link)

```
Project Setup
Initialize the project structure.
Set up development environment.
---
PARENT: PARENT-1
Setup Database
Configure PostgreSQL database.
Create initial schema.
---
PARENT: PARENT-1
Setup CI/CD
Configure GitHub Actions.
Set up automated testing.
---
PARENT: PARENT-1
Setup Documentation
Create README.md.
Document API endpoints.
---
```

### Example 3: Multiple Parent Tasks with Subtasks

```
Frontend Development
Build the user interface components.
---
Backend Development
Implement REST API endpoints.
---
PARENT: PARENT-1
Frontend - Login Page
Create login form component.
Add form validation.
---
PARENT: PARENT-1
Frontend - Dashboard
Create dashboard layout.
Implement data visualization.
---
PARENT: PARENT-2
Backend - Authentication API
Implement login endpoint.
Add JWT token generation.
---
PARENT: PARENT-2
Backend - User API
Create user CRUD endpoints.
Add input validation.
---
```

## Project Structure

```
jira-task-creator/
├── jira_task_gui.py          # Main GUI application
├── create_jira_tasks.py      # Core API functions
├── tasks.txt                 # Sample tasks file
├── requirements.txt          # Python dependencies
├── run_gui.bat              # Windows launcher
├── install_requirements.bat  # Install dependencies
└── README.md                # This file
```

## Requirements

- **Python**: 3.6+
- **Dependencies**:
  - `requests` >= 2.31.0
  - `tkinter` (usually included with Python)

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
**Solution**: Install requests: `pip install requests`

### "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: 
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Should be included with Python from python.org
- **Windows**: Should be included by default

### Authentication errors
**Solution**:
- Verify your email address is correct
- Check that your API token is valid
- Ensure your account has permission to create issues in the project

### Tasks file not found
**Solution**: Use the "Browse" button to select your tasks file, or ensure `tasks.txt` is in the same directory

### Subtasks not linking
**Solution**:
- Make sure parent tasks are created successfully first
- Check that `PARENT: PARENT-X` syntax is correct (case-insensitive)
- Verify parent task indices match (1st parent = PARENT-1, 2nd = PARENT-2, etc.)

## Development

### Running from Source

```bash
python jira_task_gui.py
```

### Building EXE

To create a standalone EXE file:
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `build_exe.bat` (Windows)
3. EXE will be in `dist/` folder

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Author

**Muhammad Al-Naghi**

- GitHub: [@muhammadalnaghi](https://github.com/muhammadalnaghi)

## Acknowledgments

- Built with Python and tkinter
- Uses Jira REST API v3
- Inspired by the need for batch task creation

