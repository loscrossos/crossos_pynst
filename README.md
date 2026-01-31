# CrossOS Pynst: Iron-Clad Python Installation Manager

**Stop chasing installation manuals. Start using projects!**

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** Python project manager contained in a single small python file. It automates the entire lifecycle of a Python application: installation, updates, repairs, and extensions.

From simple scripts to complex AI installations like ComfyUI or WAN2GP, Pynst handles the heavy lifting for you: cloning repos, building venvs, installing dependencies, and creating desktop shortcuts. All in your hands with a single command. Every single step of what is happening defined in a simple, easily readable (or editable) text file.

Pynst is for hobbyist to pros.. To be fair: its not for the total beginner. You should know how to use the command line. but thats it.

## Why Pynst?

In the world of AI, Python projects are the gold standard but they are difficult to install for newbies and even for pros they are complex and cumbersome. There has been a new wave of "one click installers" and intsall managers. The problem is usually one of those: 
* you need to disable security features in your OS ("so guys the first we do is disable security...")
* Some obscure installer does thing in the background but does not tell you what.
* even if they tell you the installer installs lots of things you might not want or from strange sources you can not see or change.
* you are very dependent on the author to update with new libraries or projects and can not do that yourself in an easy way.
* the instructions only work on linux... 
* if something breaks there is no way to repair it
* and hey i already installed Comfy with sweat and tears last year.. why cant you just repair my current installation??

wouldnt it be great if all that was solved?


### The "Sweet Spot" of Installation
Pynst bridges the gap between fragile manual instructions, heavy setup and customization.

| Method                    | Reproducible? | Cross-Platform?   | Secure/Auditable? | Expandable?  | Lightweight? |
| :---                      | :---:         | :---:             | :---:             | :---:        |:---:         |    
| **Manual Clicking**       | ❌            | ❌                | ✅                | ✅           |✅            |
| **One-Click / Managers**  | ✅            | ❌                | ⚠️ (Obscure)      | ❌           | ⚠️ (Complex)|
| **Bash / Batch Scripts**  | ✅            | ❌                | ⚠️ (Complex)      | ⚠️ (Complex) |✅           |
| **Docker**                | ✅            | ✅                | ✅                | ⚠️ (Complex) |❌           |
| **CrossOS Pynst**         | ✅            | ✅                | ✅ (Plain Text)   | ✅           |✅           |

---

## Installation

### Key Features
*   **Single File, Zero Dependencies**: No `pip install` required. Just `python pynst.py`.
*   **Indestructible Environments**: Breaks happen. Use `--revenv` to nuke and rebuild the virtual environment instantly. It's "Have you tried turning it off and on again?" for your Python setup.
*   **Write Once, Run Anywhere**: The same instruction file works on Windows, Linux, and macOS.
*   **Native Desktop Integration**: Automatically generates clickable **native Desktop Icons** for your projects. They feel like a native app but simply deleting the icon and install dir wipes everything.. no system installation!
*   **Smart Dependency Management**:
    *   **`REQSCAN`**: Recursively finds and installs `requirements.txt` from all sub-folders (perfect for plugin systems).
    *   **`RFILTER`**: Global package filtering to solve dependency hell (e.g., "install everything *except* Torch").
*   **Portable/Embedded Mode**: fully supports "Portable" installations (like ComfyUI Portable). Can even convert a portable install into a full system install.

---

## 🚀 Quick Start

### 1. The "Hello World" Example

Gran one of the several read-to use install scripts in the "installers" folder and use them OR save this as `install.pynst.txt`:

```bash
# Clone the repo
CLONEIT https://github.com/comfyanonymous/ComfyUI .

# Create the venv & install requirements
SETVENV .

# Create a desktop shortcut
DESKICO "ComfyUI" main.py
```

### 2. Run It
```bash
python pynst.py install.pynst.txt ./my_app
```
**Done.** You now have a fully installed application with a desktop icon.

---

## 🛠️ Common Operations

**Update an Installation**
Run the same file again. Pynst updates code and installs new requirements automatically.
```bash
python pynst.py install.pynst.txt ./my_app
```

**Repair a Broken Venv**
Something weird happening? Rebuild the environment from scratch.
```bash
python pynst.py install.pynst.txt ./my_app --revenv
```

**Safe Update ("Senso" Mode)**
Update plugins and files *without* touching the core code.
```bash
python pynst.py install.pynst.txt ./my_app --senso
```

---

##  Documentation

*   **[Reference Manual](doc/MANUAL.md)**: Full command list, CLI options, and advanced usage.
*   **[ComfyUI Tutorial](doc/tutorial_comfy.md)**: Step-by-step guide to installing a fully accelerated ComfyUI environment.

---

## Command Summary

| Command | Description |
| :--- | :--- |
| `CLONEIT <url> <path>` | Clone or update a git repository. |
| `SETVENV <path>` | Ensure a virtual environment exists (and install its requirements). |
| `REQFILE <path/url>` | Install a requirements file (local or remote). |
| `REQSCAN <path>` | Recursively find and install `requirements.txt` in subdirectories. |
| `GETFILE <url> <path>` | Download a file (smart check for existing files). |
| `DESKICO <label> <cmd>` | Create a clickable desktop shortcut. |
| `RFILTER <pkgs>` | Filter out specific packages to avoid conflicts. |

*(See the [Manual](doc/MANUAL.md) for the full list)*
