# CrossOS Pynst Manual

**CrossOS Pynst** is a single-file, cross-platform (Windows, Linux, macOS) tool designed to automate the installation, management, and repair of Python projects. It reads a simple plain-text instruction file (`.pynst.txt`) and executes it to set up environments, download files, clone repositories, and create shortcuts.

## Table of Contents

1. [Installation](#installation)
2. [Basic Concepts](#basic-concepts)
3. [CLI Usage](#cli-usage)
4. [Instruction File Reference](#instruction-file-reference)
5. [Advanced Features](#advanced-features)
   - [Embedded Python Mode](#embedded-python-mode)
   - [Repair & Rebuild](#repair--rebuild)
   - [Package Filtering](#package-filtering)
   - [Multiple Venvs](#multiple-venvs)
6. [Troubleshooting](#troubleshooting)

---

## Installation

Pynst requires no installation. It is a single Python script.

1.  **Prerequisites**:
    *   **Python 3.8+**: Must be installed and available in your system `PATH`.
    *   **Git**: Must be installed and available in your system `PATH`.
    
    > **Tip:** If you are new to this or setting up a fresh machine, use [**CrossOS Setup**](https://github.com/loscrossos/crossos_setup). It's a free, open-source tool that automatically installs Python, Git, and other necessary libraries for you on Windows, Linux, or macOS.

2.  **Get Pynst**:
    Download `pynst.py` and place it anywhere (e.g., in your project root or a utilities folder).

---

## Basic Concepts

Pynst operates on three main components:

1.  **The Installer File (`.pynst.txt`)**: A text file containing a list of commands (like `CLONEIT`, `REQFILE`, `DESKICO`) that describe the desired state of the installation.
2.  **The Target Directory**: The base folder where Pynst will install everything (repositories, virtual environments, downloaded files).
3.  **The Virtual Environment (Venv)**: Pynst automatically manages Python virtual environments within the target directory to keep dependencies isolated.

---

## CLI Usage

Run Pynst from your terminal:

```bash
python pynst.py [OPTIONS] <input_file> <target_directory>
```

### Examples

**Standard Install:**
```bash
python pynst.py installers/my_app.pynst.txt ./my_app_install
```

**Repair / Rebuild Venv:**
```bash
python pynst.py installers/my_app.pynst.txt ./my_app_install --revenv
```

**Portable/Embedded Install:**
```bash
python pynst.py installers/my_app.pynst.txt ./portable_app --embedded
```

### Options

| Option | Description |
| :--- | :--- |
| `--update` | **update**: updates all existing libraries to the newest and shinniest. |
| `--upgrade` | **force upgrade**: Force upgrade or reinstall of libraries installed by req files(stronger than update, will do a reinstall even if version is the same). |
| `--revenv` | **Rebuild Venv**: Deletes (or empties) the existing virtual environment and rebuilds it from scratch. Essential for fixing broken environments. |
| `--senso` | **Senso Mode**: "Sensitive/Conservative" installation. Only adds missing plugins/files. Does NOT update code (`git pull`) or remove existing files. Safe for updates where you don't want to touch the core. |
| `--embedded` | **Embedded Mode**: Treats the installation as a portable one using a `python_embedded` folder instead of a standard system venv. |
| `--gitlatest` | **Force Latest Git**: Forces all git repositories to the absolute latest commit on `main`/`master`, even if they are in a detached HEAD state. |
| `--safecheck` | **Safety Check**: Verify that major components (Git repos, key files) already exist before proceeding. Useful to ensure you are updating an existing install and not accidentally creating a new one or overwriting the wrong folder. |
| `--backup` | **Backup**: Backs up the existing virtual environment (renames it with a `.bak` suffix) before making changes. |
| `--venvname <name>` | **Custom Venv Name**: Use a specific name for the virtual environment folder (e.g., `venv_gpu`, `venv_cpu`) instead of the default `.env_{os}`. |
| `--noblob` | **No Blobs**: Skips commands marked as `GETBLOB`. Useful for updating code/dependencies without downloading massive model files again. |
| `--nodesktop` | **No Desktop Shortcuts**: Prevents creation of desktop icons, even if the installer file requests them. |
| `--copymode <mode>` | **Copy Mode Override**: Overrides `COPYMODE` from `.env`. Choices: `link`, `copy`. |
| `--matchmode <mode>` | **Match Mode Override**: Overrides `MATCHMODE` from `.env`. Choices: `filelistandsize`, `filelist`. |
| `--dryrun` | **Dry Run**: Simulates the execution without changing any files. Prints what would happen. |
| `--verbose` | **Verbose**: Shows full output from subprocesses (pip, git) for debugging. |

---

## Instruction File Reference

The `.pynst.txt` file is read line-by-line. Lines starting with `#` are comments.

### Core Commands

#### `PYTHON <version>`
Asserts that the system has a specific Python version available. If `--embedded` is used, checks the embedded python version.
```bash
PYTHON 3.10
```

#### `CLONEIT <url> <path> [target_dir]`
Clones a Git repository into `[TargetDir]/[path]/[target_dir]`. If `target_dir` is omitted, the default repository name is used (`[TargetDir]/[path]/[RepoName]`).
*   If the repo exists, it updates it (unless `--senso` is used).
*   If `--gitlatest` is used, it forces a checkout of the latest main/master branch.
```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
# Result: [TargetDir]/ComfyUI
CLONEIT https://github.com/comfyanonymous/ComfyUI . my_comfy
# Result: [TargetDir]/my_comfy
```

#### `CLONELF <url> <path> [target_dir]`
Same as `CLONEIT`, but designed for large repositories. It deletes the `.git` directory history after cloning to save disk space. Note that this prevents future updates via `git pull`.
*   **Smart Caching**: `CLONELF` supports Smart Caching! It can check your local cache for a directory matching the remote repository's files and link the entire directory instead of downloading it. See [Smart Downloading & Caching](#smart-downloading--caching) for details.

#### `SETVENV <path>`
Ensures a virtual environment exists at `[TargetDir]/[path]`.
*   If `requirements.txt` exists at that path, it is automatically installed.
*   Default names: `.env_win` (Windows), `.env_lin` (Linux), `.env_mac` (macOS).
```bash
SETVENV ComfyUI
```

#### `REQFILE <path_or_url>`
Installs a requirements file into the current venv using `pip`. Can be a local path (relative to TargetDir) or a remote URL.
```bash
REQFILE ComfyUI/requirements.txt
REQFILE https://example.com/extra_requirements.txt
```

#### `REQFILEFORCE <path_or_url>`
Same as `REQFILE` but forces re-installation of packages (`--force-reinstall`).

#### `PIPINST <package_list>`
Runs `pip install` directly with the provided arguments.
```bash
PIPINST numpy pandas
PIPINST torch --index-url https://download.pytorch.org/whl/cu118
```

#### `RFILTER <word1> <word2> ...`
Sets a **global filter** for requirements files. Any line in a `REQFILE` starting with these words will be ignored.
*   Useful for preventing conflicts (e.g., filtering `torch` to install a specific version later).
*   Case-insensitive. Matches the start of the package name.
*   Call without arguments to clear the filter.
```bash
RFILTER torch torchvision  # Ignore standard torch/torchvision
REQFILE requirements.txt   # install everything EXCEPT torch/torchvision
RFILTER                    # Clear filter
```

#### `REQSCAN <path>`
Scans **one level deep** inside `[TargetDir]/[path]` for subdirectories containing `requirements.txt`.
*   If a subdirectory is a Git repo, it attempts to `git pull` first.
*   Then it installs the found `requirements.txt`.
*   **Ideal for plugins/custom nodes.**
```bash
REQSCAN ComfyUI/custom_nodes
```

### File Operations

#### `GETFILE <url> <path_suffix>`
Downloads a file to `[TargetDir]/[path_suffix]`.
*   Only downloads if the file is missing or the server file size differs.
*   **Smart Caching**: Can create hardlinks instead of downloading if the file exists in your local cache. See [Smart Downloading & Caching](#smart-downloading--caching) for details.
*   If the target path is a directory (e.g., `d:/resources/`), it automatically extracts the filename from the URL.
```bash
GETFILE https://example.com/workflow.json ComfyUI/user/workflows
```

#### `GETBLOB <url> <path_suffix>`
Same as `GETFILE`, but intended for large binary files (models, weights).
*   Can be skipped by the user with the `--noblob` CLI flag.
*   Also supports Smart Caching.
```bash
GETBLOB https://huggingface.co/model.safetensors ComfyUI/models/checkpoints
```

#### `HASFILE <path>`
Verifies that `[TargetDir]/[path]` exists. Aborts if missing.
*   Used for safety checks to ensure the installation structure is valid before proceeding.
```bash
HASFILE ComfyUI/main.py
```

### Shortcuts & Execution

#### `DESKICO <Label> <Script> <Args...>`
Creates a clickable **Desktop Shortcut** (Icon) that runs a command using the installed venv.
*   **Label**: Name of the shortcut (quoted if spaces).
*   **Script**: Python script path relative to TargetDir.
*   **Args**: Arguments for the script.
```bash
DESKICO "ComfyUI GPU" ComfyUI/main.py --gpu
```
*(Also available: `DESKEXE` (script file), `HOMEICO` (icon in install dir), `HOMEEXE` (script in install dir))*

#### `XRUNPYTHONFILE <Script> <Args...>`
Runs a Python script immediately using the venv.
```bash
XRUNPYTHONFILE setup_db.py --init
```

#### `XRUNCMD_GIT <Dir> <Args...>`
Runs a raw `git` command in the specified directory (relative to TargetDir).
```bash
XRUNCMD_GIT ComfyUI checkout dev_branch
```

#### `XRUNCMD_PIP <Args...>`
Runs a raw `pip` command.
```bash
XRUNCMD_PIP uninstall -y torch
```

### Utility

#### `PRINTIT <Message...>`
Prints a message to the console.
```bash
PRINTIT "Downloading massive models, please wait..."
```

#### `PAUSEIT`
Pauses execution and waits for user confirmation (Enter).

---

## Advanced Features

### Embedded Python Mode
Use `--embedded` to manage portable installations (like ComfyUI Portable).
*   Pynst looks for a folder named `python_embedded` (or `python_embeded`) in the target directory.
*   It uses the Python executable inside that folder.
*   `--revenv` in this mode will **empty** the site-packages of the embedded python instead of deleting the folder.

### Smart Downloading & Caching
To save bandwidth and storage space, Pynst can check local directories for existing files or entire repositories before downloading them. If a file with the exact name and size is found, Pynst will create a file link (hardlink) to the target destination instead of downloading it again. For large repositories cloned via `CLONELF`, Pynst can use lightweight metadata checks (`git ls-tree`) to find a matching local directory and link (symlink/junction) the entire directory at once. These linking methods require no admin privileges in most setups.

**How to Enable:**
Create an `.env` file in the same directory as your `pynst.py` script. The feature is only activated if this file exists and contains an existing directory path.

**Configuration Variables:**
*   `BLOBREPO_XX` (e.g., `BLOBREPO_1`, `BLOBREPO_2`): Define up to 100 search directories. Pynst will search these directories (and all their subdirectories) for a matching file by name and size. For `CLONELF`, it will search for directories that exactly match the remote repository files.
    ```env
    BLOBREPO_1=D:\models
    BLOBREPO_2=F:\resources\safetensors
    ```
*   `BLOB_COLLECT_DIR` (and `BLOB_COLLECT_DIR_*`): If defined, all new file downloads and `CLONELF` repository clones will be saved to one of these directories first, and then linked to the target destination. This builds your local cache automatically. You can specify multiple cache directories by appending a suffix (e.g., `BLOB_COLLECT_DIR`, `BLOB_COLLECT_DIR_1`, `BLOB_COLLECT_DIR_2`). Pynst will automatically check the available storage space and select the first cache directory that has enough free space to store the file or repository. If no cache directory has sufficient space, Pynst will issue a warning and bypass the cache, downloading directly to the target.
    ```env
    BLOB_COLLECT_DIR=D:\pynst_cache
    BLOB_COLLECT_DIR_1=E:\overflow_cache
    ```
*   `COPYMODE`: Specifies how files and directories are transferred from the cache to the target destination. By default, Pynst uses `"link"` (hardlinks for files, symlinks/junctions for directories) to save disk space. You can set this to `"copy"` to force Pynst to always copy the files and directories instead of linking them. This is useful if your filesystem does not support links or if you prefer independent copies. Can be overridden with the `--copymode` CLI flag.
    ```env
    COPYMODE=copy
    ```
*   `MATCHMODE`: Defines the strictness for matching a local cached directory (`CLONELF`) against a remote repository's files. Can be overridden with the `--matchmode` CLI flag.
    *   `"filelistandsize"` (default): Checks that the directory has the exact same files *and* that all files match the remote sizes.
    *   `"filelist"`: Only checks if the local directory has at least the same files (same filenames) as the remote repository, ignoring sizes. This is useful when local cache files might be modified or compressed versions of the original.
    ```env
    MATCHMODE=filelist
    ```

**Technical Notes:**
*   **Storage Space Verification**: Before any download or clone operation, Pynst rigorously checks if the target file system has enough free storage space. If the target drive lacks sufficient space, the process will be safely aborted with an error message to prevent corrupted or partial installations.
*   For files, Pynst uses a `HEAD` request to verify the remote file size before downloading to ensure an exact match.
*   For repositories (`CLONELF`), Pynst uses `git clone --filter=blob:none` to fetch only the tree metadata (saving ~99.9% bandwidth) and compares it against local directories to find an exact match before linking.
*   If a file with the same name but a different size is downloaded to `BLOB_COLLECT_DIR`, Pynst automatically creates a subdirectory with a short MD5 hash derived from the URL to avoid collisions. If there are still collisions, it appends a sequential suffix (e.g., `_1`, `_2`). Repositories are stored similarly with a hash to avoid name collisions.
*   **Cross-Drive Linking Fallback**: Hardlinks generally only work when the source and destination are on the same drive. If a cross-drive link is attempted (or any other linking error occurs), Pynst will output a warning and gracefully fall back to downloading/copying the file or directory directly.

### Package Filtering
The `RFILTER` command is powerful for managing conflicting dependencies, especially with AI libraries like PyTorch.
1.  **Filter**: `RFILTER torch` or multiple words separated by spaces: `RFILTER torch torchvision numpy`.
2.  **Install**: `REQFILE requirements.txt` (skips torch)
3.  **Manual Install**: `PIPINST torch==2.1.0+cu121 ...` (installs correct version)
4.  **Clear**: `RFILTER`

### Multiple Venvs
You can maintain multiple environments for the same project using `--venvname`.
1.  Install default: `python pynst.py install.txt ./app` (Creates `.env_win`)
2.  Install CPU version: `python pynst.py install.txt ./app --venvname venv_cpu` (Creates `venv_cpu`)
3.  The `DESKICO` commands generated will be linked to the specific venv active during that run.

### Repair & Rebuild
*   **Repair**: Running Pynst on an existing directory updates repos and installs missing requirements.
*   **Rebuild**: Adding `--revenv` nukes the venv and starts fresh. This is the "Turn it off and on again" for Python environments.

### Cross-Platform Icons
Pynst generates platform-native icons with text labels generated on the fly:
*   **Windows**: `.lnk` shortcuts with `.ico` icons.
*   **macOS**: `.app` bundles with `.icns` icons.
*   **Linux**: `.desktop` entries with `.png` icons.
