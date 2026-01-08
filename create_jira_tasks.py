#!/usr/bin/env python3
"""
Script to create Jira tasks via REST API
"""

import requests
import json
import base64
import os
import sys
from typing import List, Dict, Optional

# Configuration - Can be set via environment variables or updated here
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://your-domain.atlassian.net")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "PROJECT")  # Default project key
API_TOKEN = os.getenv("JIRA_API_TOKEN", "YOUR_API_TOKEN_HERE")
EMAIL = os.getenv("JIRA_EMAIL", "your-email@example.com")  # Your Jira email address (needed for authentication)
TASKS_FILE = os.getenv("TASKS_FILE", "tasks.txt")  # Path to the tasks file

def get_auth_headers():
    """Get authentication headers for API requests"""
    if EMAIL:
        auth_string = f"{EMAIL}:{API_TOKEN}"
    else:
        auth_string = f"api_token:{API_TOKEN}"
    
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    }

def get_user_account_id(email: str) -> Optional[str]:
    """
    Get Jira user account ID from email address
    
    Args:
        email: User's email address
    
    Returns:
        Account ID if found, None otherwise
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/user/search"
    headers = get_auth_headers()
    params = {"query": email}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        users = response.json()
        
        if users and len(users) > 0:
            # Find exact email match
            for user in users:
                if user.get('emailAddress', '').lower() == email.lower():
                    return user.get('accountId')
            # If no exact match, return first result
            if users[0].get('accountId'):
                return users[0].get('accountId')
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting user account ID: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def delete_jira_issue(issue_key: str) -> bool:
    """
    Delete a Jira issue
    
    Args:
        issue_key: Issue key (e.g., PROJECT-123)
    
    Returns:
        True if successful, False otherwise
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    headers = get_auth_headers()
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error deleting issue {issue_key}: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return False

def create_jira_issue(summary: str, description: str, assignee_account_id: Optional[str] = None, issue_type: str = "Task", parent_key: Optional[str] = None) -> Dict:
    """
    Create a Jira issue using the REST API
    
    Args:
        summary: Issue summary/title
        description: Issue description
        assignee_account_id: Account ID of the assignee (optional)
        issue_type: Type of issue (default: Task)
        parent_key: Parent issue key for subtasks (e.g., "PROJECT-123") - if provided, creates a subtask
    
    Returns:
        Response from Jira API
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    headers = get_auth_headers()
    
    # If parent_key is provided, this is a subtask
    is_subtask = parent_key is not None
    
    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Sub-task" if is_subtask else issue_type
            }
        }
    }
    
    # Add parent for subtasks
    if is_subtask:
        payload["fields"]["parent"] = {
            "key": parent_key
        }
    
    # Add assignee if provided
    if assignee_account_id:
        payload["fields"]["assignee"] = {
            "accountId": assignee_account_id
        }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_details = {
            'error': str(e),
            'status_code': None,
            'response_text': None,
            'error_messages': [],
            'errors': {}
        }
        if hasattr(e, 'response') and e.response is not None:
            error_details['status_code'] = e.response.status_code
            error_details['response_text'] = e.response.text
            try:
                response_json = e.response.json()
                error_details['error_messages'] = response_json.get('errorMessages', [])
                error_details['errors'] = response_json.get('errors', {})
            except json.JSONDecodeError:
                pass
        return {'error': error_details}

def parse_tasks_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parse tasks from a text file.
    
    Format:
    - Tasks are separated by "---" on its own line
    - First line of each task is the summary
    - Following lines until the next "---" are the description
    - To create a subtask, add "PARENT: ISSUE-KEY" line before the summary
      - Use actual issue key: "PARENT: PROJECT-123"
      - Use placeholder for auto-link: "PARENT: PARENT-1" (refers to 1st parent task)
      - Use placeholder: "PARENT: PARENT-2" (refers to 2nd parent task), etc.
    - Empty lines are preserved in descriptions
    
    Args:
        file_path: Path to the tasks file
    
    Returns:
        List of task dictionaries with 'summary', 'description', and optionally 'parent_key' or 'parent_ref' keys
    """
    if not os.path.exists(file_path):
        print(f"Error: Tasks file '{file_path}' not found.")
        print(f"Please create a tasks.txt file with your tasks.")
        sys.exit(1)
    
    tasks = []
    current_task = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.rstrip('\n\r')
        
        # Check if this is a task separator
        if line.strip() == "---":
            # Save previous task if exists
            if current_task and current_task.get('summary'):
                tasks.append(current_task)
            # Start new task
            current_task = {"summary": "", "description": "", "parent_key": None, "parent_ref": None}
        else:
            # First non-empty line after separator (or start of file)
            if current_task is None:
                current_task = {"summary": "", "description": "", "parent_key": None, "parent_ref": None}
            
            # Check if this is a PARENT directive
            if line.strip().upper().startswith("PARENT:"):
                parent_value = line.strip()[7:].strip()  # Remove "PARENT:" prefix
                if parent_value:
                    # Check if it's a placeholder (PARENT-1, PARENT-2, etc.)
                    if parent_value.upper().startswith("PARENT-"):
                        try:
                            # Extract number (e.g., "PARENT-1" -> 1)
                            parent_num = int(parent_value.split('-')[1])
                            current_task["parent_ref"] = parent_num  # Store reference number
                        except (ValueError, IndexError):
                            # Invalid format, treat as actual key
                            current_task["parent_key"] = parent_value
                    else:
                        # Actual issue key
                        current_task["parent_key"] = parent_value
                continue
            
            if not current_task["summary"] and line.strip():
                # This is the summary line (skip if we already processed a PARENT line)
                if not line.strip().upper().startswith("PARENT:"):
                    current_task["summary"] = line.strip()
            elif current_task["summary"]:
                # This is part of the description
                if current_task["description"]:
                    current_task["description"] += "\n" + line
                else:
                    current_task["description"] = line
    
    # Don't forget the last task
    if current_task and current_task.get('summary'):
        tasks.append(current_task)
    
    # Clean up descriptions (remove leading/trailing whitespace)
    for task in tasks:
        task["description"] = task["description"].strip()
    
    return tasks

def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not EMAIL or EMAIL == "your-email@example.com":
        errors.append("EMAIL is not set. Please update it in the script or set JIRA_EMAIL environment variable.")
    
    if not API_TOKEN or API_TOKEN == "YOUR_API_TOKEN_HERE":
        errors.append("API_TOKEN is not set. Please update it in the script or set JIRA_API_TOKEN environment variable.")
    
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease update the configuration and try again.")
        sys.exit(1)

def main():
    """Create all Jira tasks"""
    
    # Validate configuration
    validate_config()
    
    # Get user account ID for assignment
    print(f"Getting account ID for {EMAIL}...")
    assignee_account_id = get_user_account_id(EMAIL)
    if assignee_account_id:
        print(f"  ✓ Found account ID: {assignee_account_id}\n")
    else:
        print(f"  ⚠ Could not find account ID. Issues will be created without assignment.\n")
    
    # Parse tasks from file
    print(f"Reading tasks from: {TASKS_FILE}")
    tasks = parse_tasks_file(TASKS_FILE)
    
    if not tasks:
        print("No tasks found in the file. Please add tasks to the file.")
        sys.exit(1)
    
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
    
    print(f"Found {len(parent_tasks)} parent task(s) and {len(subtasks)} subtask(s)")
    print(f"Creating tasks in Jira project {PROJECT_KEY}...")
    print(f"Jira URL: {JIRA_BASE_URL}\n")
    
    created_issues = []
    failed_issues = []
    
    # First, create all parent tasks and store their keys
    print("=" * 60)
    print("Creating Parent Tasks")
    print("=" * 60)
    for i, task in enumerate(parent_tasks, 1):
        print(f"[{i}/{len(parent_tasks)}] Creating: {task['summary']}")
        result = create_jira_issue(task['summary'], task['description'], assignee_account_id)
        
        if result and 'key' in result:
            issue_key = result['key']
            issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
            print(f"  ✓ Created: {issue_key} - {issue_url}")
            created_issues.append(issue_key)
            # Store the parent key by its position (1-based index)
            parent_keys_map[i] = issue_key
        else:
            print(f"  ✗ Failed to create issue")
            if result and 'error' in result:
                error_info = result['error']
                if 'error_messages' in error_info:
                    for msg in error_info['error_messages']:
                        print(f"    Error: {msg}")
            failed_issues.append(task['summary'])
        print()
    
    # Then, create all subtasks using parent keys
    if subtasks:
        print("=" * 60)
        print("Creating Subtasks")
        print("=" * 60)
        for i, task in enumerate(subtasks, 1):
            # Determine parent key
            parent_key = None
            if task.get('parent_ref') is not None:
                # Use placeholder reference
                parent_ref = task['parent_ref']
                parent_key = parent_keys_map.get(parent_ref)
                if not parent_key:
                    print(f"[{i}/{len(subtasks)}] Creating: {task['summary']}")
                    print(f"  ✗ Failed: Parent task #{parent_ref} was not created successfully")
                    failed_issues.append(task['summary'])
                    continue
            elif task.get('parent_key'):
                # Use explicit parent key
                parent_key = task['parent_key']
            
            task_type = "Subtask" if parent_key else "Task"
            parent_info = f" (Parent: {parent_key})" if parent_key else ""
            print(f"[{i}/{len(subtasks)}] Creating {task_type}: {task['summary']}{parent_info}")
            
            result = create_jira_issue(task['summary'], task['description'], assignee_account_id, parent_key=parent_key)
        
            if result and 'key' in result:
                issue_key = result['key']
                issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
                print(f"  ✓ Created: {issue_key} - {issue_url}")
                created_issues.append(issue_key)
            else:
                print(f"  ✗ Failed to create issue")
                if result and 'error' in result:
                    error_info = result['error']
                    if 'error_messages' in error_info:
                        for msg in error_info['error_messages']:
                            print(f"    Error: {msg}")
                failed_issues.append(task['summary'])
            print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successfully created: {len(created_issues)} issues")
    print(f"  - Parent tasks: {len(parent_tasks)}")
    print(f"  - Subtasks: {len(subtasks)}")
    if created_issues:
        print("\nCreated issues:")
        for key in created_issues:
            print(f"  - {key}")
    
    if failed_issues:
        print(f"\nFailed to create: {len(failed_issues)} issues")
        for summary in failed_issues:
            print(f"  - {summary}")

if __name__ == "__main__":
    main()

