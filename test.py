import os
import subprocess
from pathlib import Path

def force_git_pull_on_repository(directory: str) -> bool:
    """
    Checks if a directory is a Git repository and ensures it is in a state to run 'git pull' on main or master.
    If not, attempts to put it in a pullable state (e.g., switch to main/master, stash changes).
    
    Args:
        directory (str): Path to the directory to check.
        
    Returns:
        bool: True if the repository is ready and git pull succeeds, False otherwise.
    """
    # Convert directory to Path object and ensure it exists
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"Error: {directory} is not a valid directory")
        return False

    # Change to the directory
    original_dir = os.getcwd()
    try:
        os.chdir(dir_path)

        # Check if it's a Git repository
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True
        )
        if result.returncode != 0 or result.stdout.strip() != "true":
            print(f"Error: {directory} is not a Git repository")
            return False
        print("is git dir!")
        # Check current branch or detached HEAD state
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True
        )
        current_branch = result.stdout.strip() if result.returncode == 0 else None

        # Determine target branch (try main, then master)
        target_branch = None
        result = subprocess.run(
            ["git", "fetch", "--all"],
            capture_output=True, text=True
        )

        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True, text=True
        )
        remote_branches = result.stdout.splitlines()
        if "origin/main" in [b.strip() for b in remote_branches]:
            target_branch = "main"
        elif "origin/master" in [b.strip() for b in remote_branches]:
            target_branch = "master"
        else:
            print("Error: Neither main nor master branch found in remote")
            return False

        # If not on the target branch or in detached HEAD, switch to it
        if current_branch != target_branch:
            if current_branch is None:  # Detached HEAD
                print(f"Switching from detached HEAD to {target_branch}")
            else:
                print(f"Switching from {current_branch} to {target_branch}")
            
            # Check for local branch existence
            result = subprocess.run(
                ["git", "branch", "--list", target_branch],
                capture_output=True, text=True
            )
            if target_branch not in result.stdout:
                # Create local branch tracking remote
                result = subprocess.run(
                    ["git", "checkout", "-b", target_branch, f"origin/{target_branch}"],
                    capture_output=True, text=True
                )
            else:
                result = subprocess.run(
                    ["git", "checkout", target_branch],
                    capture_output=True, text=True
                )
            
            if result.returncode != 0:
                print(f"Error switching to {target_branch}: {result.stderr}")
                return False

        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            print("Uncommitted changes detected, stashing them")
            result = subprocess.run(
                ["git", "stash", "push", "-m", "Auto-stash for git pull"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error stashing changes: {result.stderr}")
                return False

        # Ensure branch is tracking remote
        result = subprocess.run(
            ["git", "branch", "--set-upstream-to", f"origin/{target_branch}", target_branch],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error setting upstream to origin/{target_branch}: {result.stderr}")
            return False

        # Perform git pull
        print(f"Running git pull on {target_branch}")
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error during git pull: {result.stderr}")
            return False

        print(f"Successfully pulled latest changes on {target_branch}")
        return True

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False
    finally:
        # Restore original working directory
        os.chdir(original_dir)

# Example usage
if __name__ == "__main__":
    test_dir = "d:/gh_test/ComfyUI_windows_portable3/ComfyUI"  # Replace with actual path
    success = force_git_pull_on_repository(test_dir)
    print(f"Git pull {'succeeded' if success else 'failed'}")