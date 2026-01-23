# CrossOS Pynst: Iron-Clad Python Installation Manager

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** single-file Python project manager that installs, rebuilds, updates, upgrades, extends and repairs virtually any Python project with a single command.  

The ultimate setup starts here. Pynst provides a robust, scriptable solution for effortless deployment. It offers granular control over your environment, including guaranteed Python version pinning and intelligent venv management. You get advanced dependency handling with flexible file/URL installation, package filtering, and recursive repository scanning. Plus, it accelerates setup with built-in Git cloning, smart file acquisition, custom command execution, and one-step desktop shortcut creation. Install your project the right way, every time.


Whether you want to **install from scratch**, **repair an existing environment**, or **fully enhance** a complex multi-repo setup like ComfyUI, WAN2GP, or a custom AI pipeline - Pynst automates the heavy lifting while keeping your existing code and data safe.

It uses a simple plain text file with instruction commands and executes them to create the ultimate installation.



## Overview

CrossOS Pynst offers **complete environment control**, **flexible package management**, and **user-friendly setup**.


**Virtual Environment & Python Control**

* **Python Version Pinning:** Guarantee the correct runtime by strictly enforcing the $\text{Python}$ version for all virtual environments (venvs). (`PYTHON`)
* **Intelligent Venv Management:** Automatically create, manage, and optionally rebuild virtual environments at specified paths, and instantly install any local $\text{requirements.txt}$ file found within. (`SETVENV`)

**Advanced Dependency Management**

* **Flexible Requirements Handling:** Install dependencies from local files or remote $\text{URLs}$ for maximum flexibility. (`REQFILE`, `REQFILEFORCE`)
* **Direct $\text{PIP}$ Command Support:** Install specific wheels or packages directly using raw $\text{pip}$ arguments. (`PIPINST`, `XRUNCMD_PIP`)
* **Global Package Filtering (RFILTER):** Exclude unwanted packages from all installation lists instantly—ideal for dependency conflict resolution or specific build requirements. (`RFILTER`)
* **Automated Repository Scanning:** Recursively scan specified directories, update any found $\text{Git}$ repositories, and install their respective $\text{requirements.txt}$ files. (`REQSCAN`)


**Code & File Acquisition**

* **One-Step $\text{Git}$ Cloning:** Easily clone any $\text{Git}$ repository to a specific directory in your target installation. (`CLONEIT`, `XRUNCMD_GIT`)
* **Smart File Downloading:** Efficiently download files (including large assets like $\text{AI}$ models) only if they are missing or have changed in size, saving time and bandwidth. (`GETFILE`, `GETBLOB`)


**Installation Customization & User Interaction**

* **Shortcut Creation:** Instantly generate desktop icons/scripts or project-base icons/scripts to run your installed Python application. (`DESKICO`, `DESKEXE`, `HOMEICO`, `HOMEEXE`)
* **Custom Execution:** Run arbitrary $\text{Python}$ files directly within the installation process, complete with arguments. (`XRUNPYTHONFILE`)
* **User Checkpoints:** Implement mandatory pauses (`PAUSEIT`) and critical file existence checks (`HASFILE`) to ensure a smooth and verified installation path.
* **Informative Messaging:** Display custom print messages to keep users informed during long installation steps. (`PRINTIT`)



You can run it directly with:

```bash
python pynst.py [pynst-installer-file] [targetdirectory] [optional commands]
```

No installation, no dependencies, no platform issues.

---

## Features

- Easy to Use
  - Just download `pynst.py` and run it. All you need is a pynst-installer-file and a target directory.
  - The installer file defines what to install. It is a plain-text instruction file. Use one of the provided examples, check out the community or write one yourself! Everything else is automated.
- Fully Cross-OS
  - Works identically on **Windows**, **Linux**, and **macOS**. Learn once use forever!
  - Dual/multi-boot friendly: projects you install can be used across all OSes. Access the same installation from Windows, Linux and MacOS!
- Powerful Installation
  - Installs and configures full projects in one step.
  - Automatically installs the right files on the right place
  - Creates desktop or home-directory launchers automatically.
- Repair & Rebuild
  - Rebuilds or repairs broken or outdated venvs. ComfyUI broke? just repair it!
  - Works on embedded/portable installs.
  - Ensures correct Python and dependency versions. No more dependency jungle.
- Safety & Clarity
  - Colorized logging and clear status messages.
  - Dry-run mode for safe testing.
  - Backup mode for risk-free environment replacement.

---

## Quick Start

Simple example to install ComfyUI and load a full fledge workflow into it.

### Pre-requisites

You need git and python installed to run pynst. Pynst uses by default python 3.13 (it can be changed)

**Windows**

if you havent already installed them, open an administrator console and run these commands:

```
winget install --id=Python.Python.3.13 -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Git.Git -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
```

### 1. ComfyUI simple installation

An installer file defines what to install and how. Example for the simplest install of comfyUI.

Save this as `test.comfyhelloworld.inst.txt` or use the provided example in the `installers` folder:

```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
DESKICO "ComfyUI CPU" ComfyUI/main.py --cpu
```

Then run (example on windows):
```bash
python pynst.py installers/test.comfyhelloworld.inst.txt ./hellocomfy
```

This will: 

1. clone the comfyUI repository under the target directory `hellocomfy/ComfyUI`
2. automatically create a virtual environment `hellocomfy/ComfyUI/.env_win` (example on windows) while searching and installing the requirements it finds in the ComfyUI directory.
3. create a starter icon on the desktop.

Just double-click the starter icon! thats it. You have a ComfyUI installed with latest code.


### 2. Load a full fledged workflow into ComfyUI with ALL dependencies!

Now lets upgrade ComfyUI to load a workflow.








---

## Command-Line Options

```
usage: pynst.py [-h] [--revenv] [--senso] [--embedded] [--nodesktop]
                        [--dryrun] [--verbose] [--backup] [--noblob]
                        [--venvname VENVNAME] [--gitlatest]
                        [--safecheck] 
                        inputfile targetdirectory
```

**mandatory arguments**

| Argument | Description |
|-----------|--------------|
| `inputfile` | Path to instruction file (`.pynst.txt`) |
| `targetdirectory` | Target base directory for installation or repair |

**Options**

| Option | Description |
|---------|--------------|
"#"       |Arguments: any. <br> Description: comment line. this line will be ignored.
"PYTHON"  |Arguments: a float number (python version). <br> Description:  set python version to be used for venvs from now on.. Script will abort if an existing venv has another version (unless the venv shall be deleted and rebuilt). in revenv mode pynst will delete existing venvs and create a new venv with the scpecified version. on embedded python it will empty the venv and rebuild it.
"SETVENV"  |Arguments: a directory path relative to the target directory. <br> Description:  Ensures a venv exists at the path provided. Either by looking is one exists or by creating a new one. This path is also scanned for a requirements.txt file, if so then this file is installed automatically.
"REQFILE" |Arguments: a file path relative to the target directory or a remote url to a file. <br> Description:  installs a requirements file to the current venv. local or remote.
"REQFILEFORCE" |Arguments: a file path relative to the target directory or a remote url to a file. <br> Description:  installs a requirements file to the current venv. local or remote.
"PIPINST" |Arguments: a list of arguments to be passed directly to "pip install". <br> Description:  installs wheels or modules to the current venv. Can be wheel file URL (not a file path) or a pip package
"RFILTER" |Arguments: a list of words. <br> Description:  Filter out packages (from REQ* commands) from now on. Filter is reset when the command is used again with no parameters. these packages will not be installed if present on req files. can be reset by putting single command with no params. The words are filtered by looking at the start of a line until a not allowed letter appears (any letter apart from A-Z, a-z, '-' or '_'). We anchor at start (ignoring leading whitespace). Example "torch" matches: 'torch==2.1.0', 'torch ', 'torch[extra]', 'torch\t', 'torch; python_version<"3.12"'. Does NOT match 'torchaudio' or 'torchvision'.
"CLONEIT" |Arguments: an url to a repository AND a directory path relative to target. <br> Description:  clone a repo into a dir. The directory will be created if it does not exist.
"REQSCAN" |Arguments: a directory path relative to the target directory.<br>  Description:  Specifies a directory to scan for subdirectories (git repositories) with "requirements.txt" to install. git repositories found, will be updated first. Will not update code in senso mode  
"GETFILE" |Arguments: url to a file. <br> Description:  Downloads a file to a directory. Only downloads if the file does not exist or has a different size than the remote file.  
"GETBLOB" |Arguments: url to a file. <br> Description:  Downloads a file to a directory. Used for large files (e.g. models). Same as GETFILE but this command has an option to disable the downloads of this kind.
"PRINTIT" |Arguments: any number of words. <br> Description:  Prints an info message for the user to command line. e.g. when you know that the next step is going to take a long time. "the next step might take a while"
"HASFILE" |Arguments: a file path relative to the target directory. <br> Description:  Checks that a file exists. Aborts run if it fails.
"PAUSEIT" |Arguments: none. <br> Description:  Pauses the execution until user confirms   
"DESKICO" |Arguments: a python file path (relative to target dir) wiht arguments. <br> Description:  Creates a Desktop icon with a command line   
"DESKEXE" |Arguments: a python file path (relative to target dir) wiht arguments.. <br> Description:  Creates a Desktop script with a command line  
"HOMEICO" |Arguments: a python file path (relative to target dir) wiht arguments.. <br> Description:  Creates a Installdir icon with a command line   
"HOMEEXE" |Arguments: a python file path (relative to target dir) wiht arguments.. <br> Description:  Creates a installdir script with a command line   
"XRUNCMD_GIT"  | Arguments: commands to pass directly to git. <br> Description: Runs a git command directly 
"XRUNCMD_PIP" |Arguments: commands to pass directly to pip. <br> Description:  Advanced: Raw command line passed to pip.       
"XRUNPYTHONFILE" |Arguments: commands to pass directly to python. <br> Description:  Runs a python file (arguments and params allowed)   

---

## Example Use Cases

**Install ComfyUI**
```bash
python pynst.py comfy_install.pynst.txt /ai/comfy
```

**Repair an existing install by rebuilding the virtual environment**
```bash
python pynst.py comfy_install.pynst.txt /ai/comfy --revenv
```

**Update without downloading model blobs**
```bash
python pynst.py visomaster.pynst.txt /ai/visomaster --noblob
```

**Force nightly git updates**
```bash
python pynst.py comfy.pynst.txt /ai/comfy --gitlatest
```

---

## Instruction File Format

Each `.pynst.txt` file is a list of **commands**, executed sequentially.

```
[COMMAND] [PARAMETER1] [PARAMETER2] ...
```

Comments start with `#` and are ignored.



---

## Command Reference

| Command | Parameters | Description |
|----------|-------------|--------------|
| **PYTHON** | version | Use a specific Python version (e.g. `3.12`). Aborts if unavailable. |
| **SETVENV** | path | Ensures a venv exists under this relative path. Creates it if missing. If a 'requirements.txt' is found in the path, then it is installed.|
| **REQFILE** | file / URL | Installs a requirements file into the current venv (local or remote). Packages installed with this command have priority over files installed with 'SETENV' or 'REQSCAN' (force-reinstall-mode). |
| **PIPINST** | package list | Passes arguments directly to `pip install`. installs wheels or modules to the current venv. Can be wheel file URL (not a file path) or a pip package or several packages |
| **RFILTER** | word list | Filters out matching packages from requirement installs. Case-insensitive; “torch” does not match “torchaudio”. |
| **CLONEIT** | URL path | Clones a git repository into `[target]/[path]`. Installs its `requirements.txt` if present. |
| **REQSCAN** | path | Scans one directory level under `[target]/[path]` for `requirements.txt` files and installs them. |
| **GETFILE** | URL | Downloads a file if missing or size differs. |
| **GETBLOB** | URL | Same as GETFILE but optional; skipped if `--noblob` used. |
| **HASFILE** | path | Verifies that a file exists; aborts otherwise. |
| **PRINTIT** | text | Prints a custom message for the user. |
| **PAUSEIT** | - | Pauses execution until user confirms. |
| **DESKICO**, **HOMEICO** | label + command | Creates an OS-specific shortcut icon (desktop or install directory). |
| **DESKEXE**, **HOMEEXE** | label + command | Creates a `.bat` or `.sh` launcher script. |
| **XRUNGITCOMMAND** | git args | Passes raw commands directly to git. |
| **XRUNPIPCOMMAND** | pip args | Passes raw commands directly to pip. Advanced use only. |
| **XRUNPYTHONFILE** | script args | Runs a Python file directly through the venv interpreter. |
| **#** | none | Comment line. Lines beginning with `#` are ignored. |

---

## Virtual-Environment Rules

- Default Python version: **3.13**, unless changed by `PYTHON`.
- Venvs are created under the target directory:
  - `.env_win` (Windows)
  - `.env_lin` (Linux)
  - `.env_mac` (macOS)
- Embedded mode uses `python_embedded/python.exe` or equivalent.
- In `--backup` mode, an existing venv is renamed with `.bak`.
- In repair mode, corrupted entries and stale `~` folders are removed before rebuilding.

---

## Technical Notes

CrossOS Pynst is designed to be **completely self-contained**:

- Uses **only Python standard libraries** (no third-party dependencies).
- Compatible with Python ≥ 3.8 on Windows, Linux, and macOS.
- Relies solely on 2 tools (`python`, `git`).
- Fully path-safe: works with spaces and Unicode paths.
- All subprocess calls are encapsulated for cross-OS consistency.
- Default output is colorized using ANSI sequences on all supported shells.

Internally, the script:
1. Parses instruction files line-by-line.
2. Validates the environment and Python version.
3. Creates or repairs virtual environments.
4. Executes commands in sequence, respecting filters and safe modes.
5. Provides rollback (backup) when applicable.

---
 

## Summary

CrossOS Pynst is your **universal Python project installer and fixer** -  
a single file that safely automates everything from scratch setups to delicate venv repairs, across any platform.
