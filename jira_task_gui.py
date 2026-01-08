#!/usr/bin/env python3
"""
GUI Application for creating Jira tasks
Built with tkinter for Windows compatibility
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path

# Import required modules
import requests
import json
import base64
from typing import List, Dict, Optional

# We'll import from create_jira_tasks.py dynamically when needed
# to avoid issues with environment variables

# Default credentials (users should update these)
DEFAULT_EMAIL = "your-email@example.com"
DEFAULT_API_TOKEN = "YOUR_API_TOKEN_HERE"


class JiraTaskCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jira Task Creator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.jira_base_url = tk.StringVar(value="https://your-domain.atlassian.net")
        self.project_key = tk.StringVar(value="PROJECT")
        self.email = tk.StringVar(value=DEFAULT_EMAIL)
        self.api_token = tk.StringVar(value=DEFAULT_API_TOKEN)
        self.tasks_file = tk.StringVar(value="tasks.txt")
        self.is_creating = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Jira Task Creator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Jira Base URL
        ttk.Label(config_frame, text="Jira Base URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.jira_base_url, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Project Key
        ttk.Label(config_frame, text="Project Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_key, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Email
        ttk.Label(config_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.email, width=50).grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # API Token
        ttk.Label(config_frame, text="API Token:").grid(row=3, column=0, sticky=tk.W, pady=5)
        token_frame = ttk.Frame(config_frame)
        token_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        token_frame.columnconfigure(0, weight=1)
        
        self.token_entry = ttk.Entry(token_frame, textvariable=self.api_token, width=50, show="*")
        self.token_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        show_token_btn = ttk.Button(token_frame, text="Show", width=8,
                                   command=self.toggle_token_visibility)
        show_token_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Tasks File Section
        file_frame = ttk.LabelFrame(main_frame, text="Tasks File", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Tasks File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_path_frame = ttk.Frame(file_frame)
        file_path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        file_path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(file_path_frame, textvariable=self.tasks_file, width=40).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_path_frame, text="Browse", 
                  command=self.browse_file).grid(row=0, column=1)
        ttk.Button(file_path_frame, text="Edit", 
                  command=self.edit_file).grid(row=0, column=2, padx=(5, 0))
        
        # Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="Tasks Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, wrap=tk.WORD)
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(preview_frame, text="Refresh Preview", 
                  command=self.refresh_preview).grid(row=1, column=0, pady=(5, 0))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.create_btn = ttk.Button(button_frame, text="Create Tasks", 
                                     command=self.create_tasks, width=20)
        self.create_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Log/Output Section
        log_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD,
                                                  state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Load initial preview
        self.refresh_preview()
        
    def toggle_token_visibility(self):
        """Toggle API token visibility"""
        if self.token_entry.cget('show') == '*':
            self.token_entry.config(show='')
        else:
            self.token_entry.config(show='*')
    
    def browse_file(self):
        """Browse for tasks file"""
        filename = filedialog.askopenfilename(
            title="Select Tasks File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.tasks_file.set(filename)
            self.refresh_preview()
    
    def edit_file(self):
        """Open tasks file in default text editor"""
        file_path = self.tasks_file.get()
        if not file_path:
            messagebox.showwarning("No File", "Please select a tasks file first.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", f"File not found: {file_path}")
            return
        
        # Open file in default editor (Windows)
        if sys.platform == "win32":
            os.startfile(file_path)
        else:
            # For Linux/Mac, try to open with default editor
            import subprocess
            subprocess.run(["xdg-open", file_path])
    
    def refresh_preview(self):
        """Refresh tasks preview"""
        file_path = self.tasks_file.get()
        self.preview_text.delete(1.0, tk.END)
        
        if not file_path:
            self.preview_text.insert(tk.END, "No file selected")
            return
        
        if not os.path.exists(file_path):
            self.preview_text.insert(tk.END, f"File not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.preview_text.insert(tk.END, content)
            
            # Try to parse and show task count
            try:
                # Simple task count by counting separators
                task_count = content.count('\n---\n') + (1 if content.strip() else 0)
                parent_lines = [line for line in content.split('\n') if line.strip().upper().startswith('PARENT:')]
                subtask_count = len(parent_lines)
                if task_count > 0:
                    if subtask_count > 0:
                        regular_count = task_count - subtask_count
                        # Check for placeholder parents (PARENT-1, PARENT-2, etc.)
                        placeholder_parents = [line for line in parent_lines if 'PARENT-' in line.upper()]
                        if placeholder_parents:
                            self.status_var.set(f"Ready - {task_count} task(s) found ({regular_count} parents, {subtask_count} subtasks) - Auto-link enabled")
                        else:
                            self.status_var.set(f"Ready - {task_count} task(s) found ({regular_count} tasks, {subtask_count} subtasks)")
                    else:
                        self.status_var.set(f"Ready - {task_count} task(s) found in file")
                else:
                    self.status_var.set("Ready - No tasks found (check file format)")
            except:
                pass
        except Exception as e:
            self.preview_text.insert(tk.END, f"Error reading file: {e}")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear log output"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.jira_base_url.get():
            messagebox.showerror("Validation Error", "Jira Base URL is required")
            return False
        
        if not self.project_key.get():
            messagebox.showerror("Validation Error", "Project Key is required")
            return False
        
        if not self.email.get():
            messagebox.showerror("Validation Error", "Email is required")
            return False
        
        if not self.api_token.get():
            messagebox.showerror("Validation Error", "API Token is required")
            return False
        
        if not self.tasks_file.get():
            messagebox.showerror("Validation Error", "Tasks file is required")
            return False
        
        if not os.path.exists(self.tasks_file.get()):
            messagebox.showerror("File Error", f"Tasks file not found: {self.tasks_file.get()}")
            return False
        
        return True
    
    def create_tasks(self):
        """Create tasks in a separate thread"""
        if self.is_creating:
            messagebox.showinfo("Already Running", "Task creation is already in progress")
            return
        
        if not self.validate_inputs():
            return
        
        # Disable button
        self.create_btn.config(state=tk.DISABLED)
        self.is_creating = True
        self.status_var.set("Creating tasks...")
        
        # Run in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self._create_tasks_thread)
        thread.daemon = True
        thread.start()
    
    def _create_tasks_thread(self):
        """Create tasks in background thread"""
        try:
            # Set environment variables for the imported functions
            os.environ["JIRA_BASE_URL"] = self.jira_base_url.get()
            os.environ["JIRA_PROJECT_KEY"] = self.project_key.get()
            os.environ["JIRA_EMAIL"] = self.email.get()
            os.environ["JIRA_API_TOKEN"] = self.api_token.get()
            os.environ["TASKS_FILE"] = self.tasks_file.get()
            
            # Import here to get updated environment variables
            # Need to reload module to pick up new env vars
            import importlib
            if 'create_jira_tasks' in sys.modules:
                importlib.reload(sys.modules['create_jira_tasks'])
            
            from create_jira_tasks import (
                JIRA_BASE_URL, PROJECT_KEY, EMAIL, API_TOKEN, TASKS_FILE,
                get_user_account_id, create_jira_issue, parse_tasks_file
            )
            
            self.log("=" * 60)
            self.log("Starting task creation...")
            self.log(f"Jira URL: {JIRA_BASE_URL}")
            self.log(f"Project: {PROJECT_KEY}")
            self.log(f"Tasks file: {TASKS_FILE}")
            self.log("=" * 60)
            self.log("")
            
            # Get user account ID
            self.log(f"Getting account ID for {EMAIL}...")
            assignee_account_id = get_user_account_id(EMAIL)
            if assignee_account_id:
                self.log(f"✓ Found account ID: {assignee_account_id}\n")
            else:
                self.log("⚠ Could not find account ID. Issues will be created without assignment.\n")
            
            # Parse tasks
            self.log(f"Reading tasks from: {TASKS_FILE}")
            tasks = parse_tasks_file(TASKS_FILE)
            
            if not tasks:
                self.log("❌ No tasks found in the file!")
                return
            
            # Separate parent tasks from subtasks
            parent_tasks = []
            subtasks = []
            parent_keys_map = {}  # Maps parent_ref (1, 2, 3...) to actual issue keys
            
            for task in tasks:
                if task.get('parent_ref') is not None:
                    subtasks.append(task)
                elif task.get('parent_key'):
                    subtasks.append(task)
                else:
                    parent_tasks.append(task)
            
            self.log(f"Found {len(parent_tasks)} parent task(s) and {len(subtasks)} subtask(s) to create\n")
            
            # Create tasks
            created_issues = []
            failed_issues = []
            
            # First, create all parent tasks and store their keys
            if parent_tasks:
                self.log("=" * 60)
                self.log("Creating Parent Tasks")
                self.log("=" * 60)
                for i, task in enumerate(parent_tasks, 1):
                    self.log(f"[{i}/{len(parent_tasks)}] Creating: {task['summary']}")
                    result = create_jira_issue(task['summary'], task['description'], assignee_account_id)
                    
                    if result and 'key' in result:
                        issue_key = result['key']
                        issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
                        self.log(f"  ✓ Created: {issue_key} - {issue_url}")
                        created_issues.append(issue_key)
                        # Store the parent key by its position (1-based index)
                        parent_keys_map[i] = issue_key
                    else:
                        self.log(f"  ✗ Failed to create issue")
                        if result and 'error' in result:
                            error_info = result['error']
                            if 'error_messages' in error_info:
                                for msg in error_info['error_messages']:
                                    self.log(f"    Error: {msg}")
                            if 'errors' in error_info:
                                for key, value in error_info['errors'].items():
                                    self.log(f"    {key}: {value}")
                        failed_issues.append(task['summary'])
                    self.log("")
            
            # Then, create all subtasks using parent keys
            if subtasks:
                self.log("=" * 60)
                self.log("Creating Subtasks")
                self.log("=" * 60)
                for i, task in enumerate(subtasks, 1):
                    # Determine parent key
                    parent_key = None
                    if task.get('parent_ref') is not None:
                        # Use placeholder reference (PARENT-1, PARENT-2, etc.)
                        parent_ref = task['parent_ref']
                        parent_key = parent_keys_map.get(parent_ref)
                        if not parent_key:
                            self.log(f"[{i}/{len(subtasks)}] Creating: {task['summary']}")
                            self.log(f"  ✗ Failed: Parent task #{parent_ref} was not created successfully")
                            failed_issues.append(task['summary'])
                            self.log("")
                            continue
                    elif task.get('parent_key'):
                        # Use explicit parent key
                        parent_key = task['parent_key']
                    
                    task_type = "Subtask"
                    parent_info = f" (Parent: {parent_key})" if parent_key else ""
                    self.log(f"[{i}/{len(subtasks)}] Creating {task_type}: {task['summary']}{parent_info}")
                    
                    result = create_jira_issue(
                        task['summary'], 
                        task['description'], 
                        assignee_account_id,
                        parent_key=parent_key
                    )
                
                    if result and 'key' in result:
                        issue_key = result['key']
                        issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
                        self.log(f"  ✓ Created: {issue_key} - {issue_url}")
                        created_issues.append(issue_key)
                    else:
                        self.log(f"  ✗ Failed to create issue")
                        if result and 'error' in result:
                            error_info = result['error']
                            if 'error_messages' in error_info:
                                for msg in error_info['error_messages']:
                                    self.log(f"    Error: {msg}")
                            if 'errors' in error_info:
                                for key, value in error_info['errors'].items():
                                    self.log(f"    {key}: {value}")
                        failed_issues.append(task['summary'])
                    self.log("")
            
            # Summary
            self.log("=" * 60)
            self.log("SUMMARY")
            self.log("=" * 60)
            self.log(f"Successfully created: {len(created_issues)} issues")
            self.log(f"  - Parent tasks: {len(parent_tasks)}")
            self.log(f"  - Subtasks: {len(subtasks)}")
            if created_issues:
                self.log("\nCreated issues:")
                for key in created_issues:
                    self.log(f"  - {key}")
            
            if failed_issues:
                self.log(f"\nFailed to create: {len(failed_issues)} issues")
                for summary in failed_issues:
                    self.log(f"  - {summary}")
            
            total_tasks = len(parent_tasks) + len(subtasks)
            self.status_var.set(f"Complete - {len(created_issues)}/{total_tasks} tasks created")
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Complete",
                f"Task creation complete!\n\n"
                f"Successfully created: {len(created_issues)}/{total_tasks} tasks\n"
                f"  - Parent tasks: {len(parent_tasks)}\n"
                f"  - Subtasks: {len(subtasks)}"
            ))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log(error_msg)
            self.log(f"Error type: {type(e).__name__}")
            import traceback
            self.log(traceback.format_exc())
            self.status_var.set("Error occurred")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.create_btn.config(state=tk.NORMAL))
            self.is_creating = False


def main():
    root = tk.Tk()
    app = JiraTaskCreatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

