# **CrossOS Pynst: your all-in-one Iron-Clad Python Installation Manager**

A **cross-platform** (Windows, Linux, macOS) single-file Python tool to install or rebuild&repair pretty much any python project!

**Install**

With one command you can (fully from zero) install a fully accelerated and configured ComfyUI/WAN/LLM or any other python project so that its ready to use: it has the latest code, ALL the cool accelerators for your Nvidia Card, can have plugins included as well as the starter shortcuts on your desktop... on all OSes!

You have an existing installation that you managed to install and get running with sweat and tears and since you are afraid to change anything in fear of breaking it? well.. how would you like a fully safe and riskfree way to make it shinny and ultra hardened? 

i gotchu covered: welcome to:

**Rebuild&Repair!**

One command of your power glove and the tool will fully iron-clad your existing installation: ensures the correct Python & PyTorch versions, repairs your virtual environments (including portable mode), installs the rights accelerators and updates and repairs custom node requirements with **safety checks**. All fully safe to your existing data.

**Features**:

- **Easy to Use**: 
  - no need to install anything! download the crossos_pynst.py file and just use it!
  - you do one single command and the script takes care of everything else 
  - you can easily define installer scripts with a simple text editor and no coding knowledge... Pynst does the heavy lifting!
- **Fully CrossOS**: 
  - Script works on Windows, Linux and MacOS. What you learn here you can keep using when you move to Linux! One-fits-all!
  - The installation on a shared drive supports one single installation to be used on all OSes if you do dual/trial Boot
- **One-line installer** of your favorite project including
  - Fully updated latest version of the code.
  - Supports plugins: they are installed and ready to go
  - (Windows/Linux): fully accelerated with accelerators supported: fully automatic installation of all right accelerators: pytorch, Flash Attention, Triton, xFormers, Sage-Attention (includes full Blackwell Support)
  - creation of start shortcuts on your desktop for easy start on all OSes!
- **Rebuild&Repair** repairs your existing installation and rebuilds your virtual env without losing configs
- **Portable & manual install** modes
- **Colorized logging** for clarity

---

## Usage Manual

### 1. Installation

Clone this repo and run:

```bash
python crossos_pynst.py install [options]
```

```
python crossos_pynst.py      -a install --cropi comfy.cropy.txt --basedir /Users/Shared/aii/myco
```

**Options**

* `--dir [path]`: Target install directory (default: current directory)
* `--installname [name]`: Name for the ComfyUI installation folder (default: `comfyui`)
* `--dry-run`: Simulate actions without making changes

**Example:**

```bash
python crossos_comfyx.py install --dir c:\temp --installname mycomfyui
```

**What happens on `install`**

1. Checks system Python version & Git availability
2. Clones **ComfyUI** and **ComfyUI-Manager**
3. Creates a **venv** (`.env_windows`, `.env_linux`, `.env_macos`, or `python_embedded`)
4. Installs:

   * Accelerator requirements from
     `https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_lite_python312torch271cu129.txt`
   * ComfyUI's `requirements.txt`
   * All `requirements.txt` from `custom_nodes`

---

### 2. Rebuild Existing Environment

Run in the **home directory of an existing ComfyUI install**:

```bash
python comfyui_setup.py rebuildvenv [options]
```

**Modes:**

* **Portable:** Uses `python_embedded` inside the installation
* **Manual:** Uses system Python (e.g. `py -3.12` on Windows, `python3.12` on Linux/macOS)

**Process:**

1. Detects install mode (portable/manual)
2. Removes all installed packages from venv
3. Reinstalls accelerator requirements, ComfyUI requirements, and custom node requirements
4. Aborts on **any requirement install failure**, showing the problematic folder

---

### 3. Notes

* **No auto-installation** of Python or Git — if missing, the script aborts
* Existing installation directories are never overwritten (will abort if found)
* Portable installs keep Python inside `python_embedded`
* Safe **`.bak` renaming** of existing venvs (non-portable mode)



# ROADMAP
- works: install: windows, linux, mac
- todo: write starters: ideally clickable
- todo: test rebuild
- todo: git pull on rebuild for comfy and for every node

**Upcoming Feature pipeline**
These might come but are still not in the works
- todo: data migration: safely move your models, nodes, workflows from an existing installation (e.g. Desktop install) to a new location
- todo: data separation and organisatiom: separation data from code (e.g. models are saved on a faster drive and code on the system drive)


