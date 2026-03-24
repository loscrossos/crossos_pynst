# CrossOS Pynst: Iron-Clad Python Installation Manager

**Stop chasing installation manuals. Start using projects!**

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** Python project manager contained in a single small python file. It automates the entire lifecycle of a Python application: installation, updates, repairs, and extensions.

From simple scripts to complex AI installations like ComfyUI or WAN2GP, Pynst handles the heavy lifting for you: cloning repos, building venvs, installing dependencies, and creating desktop shortcuts. All in your hands with a single command. Every single step of what is happening defined in a simple, easily readable (or editable) text file.

Pynst is for hobbyist to pros.. To be fair: its not for the total beginner. You should know how to use the command line. but thats it.

## Why Pynst?

In the world of AI, Python projects are the gold standard but they are difficult to install for newbies and even for pros they are complex and cumbersome. There has been a new wave of "one click installers" and install managers. The problem is usually one of those: 
* **ease of use** complex instructions make it difficult to follow and if you missclick, you realize the error several steps after when you are knee deep in dependency hell.
* **Security** you need to disable security features in your OS ("hi guys welcome to my channel, the first we do is disable security, else this installer does not work...")
* **Reproducibility** That guy shares his workflow and tells you the libraries names but who do you get them from? where do these files go? why is Gamorra?
* **Transparency** Some obscure installer does *things* in the background but does not tell you what.
* **Control** even if they tell you the installer installs lots of things you might not want or from strange sources you can not see or change.
* **Dependency** you are very dependent on the author to update with new libraries or projects and can not do that yourself in an easy way.
* **Portability** the instructions only work on linux... 
* **Robustness** if something in your installation breaks there is no way to repair it
* **Flexibility** and hey i already installed Comfy with sweat and tears last year.. why cant you just repair my current installation??
* **Customization** yea that installer installs abc.. but you also want to have defghijklm! but have to do it manually afterwards... manually... what is this.... the middle ages?? i like my cofee like i like my installers: customizable and open source!

wouldnt it be great if all that was solved?


### The "Sweet Spot" of Installation
Pynst bridges the gap between fragile manual instructions, heavy setup and customization.

 Feature             | CrossOS Pynst | Docker | Bash Scripts | One-Click | Manual |
 :---                | :---:         | :---:  | :---:        | :---:     | :---:  |
 **Ease of Use**     | ✅            | ❌     | ✅           | ✅        | ❌     |
 **Security**        | ✅            | ✅     | ⚠️           | ⚠️        | ✅     |
 **Reproducibility** | ✅            | ✅     | ✅           | ✅        | ❌     |
 **Transparency**    | ✅            | ⚠️     | ⚠️           | ❌        | ✅     |
 **Control**         | ✅            | ⚠️     | ⚠️           | ❌        | ✅     |
 **Dependency**      | ✅            | ✅     | ⚠️           | ❌        | ❌     |
 **Portability**     | ✅            | ✅     | ❌           | ❌        | ❌     |
 **Robustness**      | ✅            | ✅     | ❌           | ❌        | ❌     |
 **Flexibility**     | ✅            | ⚠️     | ⚠️           | ❌        | ✅     |
 **Customization**   | ✅            | ⚠️     | ⚠️           | ❌        | ✅     |
  

---

## Installation

### Key Features
*   **Single File, Zero Dependencies**: No `pip install` required. Just grab the file and run `python pynst.py`. Everything is contained there. bring it to your friends and casually install a sophisticated comfy on any PC (Windows, Linux or Mac!)!
* **Customizable!** BYOB! Build your own installation! This is configuration-as-code in its best form. You can edit the instruction file (an easy to understand text file) with your own plugins and models and reinstall your whole comfy any time you like as often as you want! you can have one installation for daily use, another for testing new things, another for your Grandma who is coming to visit this weekend!
*   **Iron-Clad Environments**: Breaks happen. Use `--revenv` to nuke and rebuild the virtual environment instantly. It's "Have you tried turning it off and on again?" for your Python setup.
*   **Write Once, Run Anywhere**: The same instruction file works on Windows, Linux, and macOS.
*   **Native Desktop Integration**: Automatically generates clickable **native Desktop Icons** for your projects. They feel like a native app but simply deleting the icon and install dir wipes everything.. no system installation!
*   **Smart Dependency Management**:
    *   **`REQSCAN`**: Recursively finds and installs `requirements.txt` from all sub-folders (perfect for plugin systems).
    *   **`RFILTER`**: Global package filtering to solve dependency hell (e.g., "install everything *except* Torch").
*   **Portable/Embedded Mode**: fully supports "Portable" installations (like ComfyUI Portable). Can even convert a portable install into a full system install.
*   **Smart Downloading & Local Caching**: Save bandwidth and disk space! Define local model directories (`BLOBREPO_1`, `BLOB_COLLECT_DIR`, etc.) in an `.env` file. Pynst will automatically search these directories when downloading files (like large AI models). If found, it creates a hardlink instead of downloading it again. Works seamlessly across Windows, Linux, and macOS.

---

## 🚀 Quick Start

Basically the whole principle is that the file `python pynst.py` is your all-in-one installer. 

What it installs depends on instruction files (affectionally called pynstallers). A Pynst instruction file is a simple text file with commands one after another. You can grab read-to-use examples in the `installers` folder, build your own or edit the existing ones to your liking. They are also great if you want someone to help you install software. That person can easily write a pynstaller and pass it along so you get a perfect installation from the get go. Your very own "one click installer"-maker!

Lets build a simple example!


### 1. The "Hello World" Example

Grab one of the several read-to use install scripts in the "installers" folder and use them OR save this as `install.pynst.txt`:

```bash
# Clone the repo
CLONEIT https://github.com/comfyanonymous/ComfyUI .
# Create a venv in the ComfyUI folder. Requirements are installed automatically if found on that folder.
SETVENV ComfyUI
# Create a desktop shortcut
DESKICO "ComfyUI" ComfyUI/main.py --cpu --auto-launch 
```

Now you can run It
```bash
python pynst.py install.pynst.txt ./my_app
```
**Done.** You now have a fully installed application with a desktop icon. Repeat this as many times as you like or on different locations... to remove it? just delete the icon and the folder you defined (./my_app) and its GONE!


### 2. Actual real world example

Pynst comes with batteries included! 

check out the installers folder for ready to use pynst recipes!. To install a full fledged cream of the crop ComfyUI with all accelerators for Nvidia RTX cards you can just use the provided file:

```bash
python pynst.py  installers/comfy_installer_rtx_full.pynst.txt ./my_comfy
```

Check out the [ComfyUI Pynstaller Tutorial](doc/tutorial_comfy.md) for a step-by-step explanation of what is happening there!


---

## 🛠️ Common Operations

**Update an Installation**
Run the same file again. Pynst updates code and installs new requirements automatically. Existing libraries only when really needed.
```bash
python pynst.py install.pynst.txt ./my_app
```

update new requirements and all existing libraries to the newest and shinniest:

```bash
python pynst.py install.pynst.txt ./my_app --update
```

**Repair a Broken Venv**
Something weird happening? Rebuild the environment from scratch.
```bash
python pynst.py install.pynst.txt ./my_app --revenv
```

**Safe Update ("Senso" Mode)**
Update plugins and files *without* touching or updating code.
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
| `CLONEIT <url> <path> [target_dir]` | Clone or update a git repository. If `[target_dir]` is omitted, the default repo name is used. |
| `CLONELF <url> <path> [target_dir]` | Like `CLONEIT`, but deletes the `.git` history after cloning to save space. |
| `SETVENV <path>` | Ensure a virtual environment exists (and install its requirements). |
| `REQFILE <path/url>` | Install a requirements file (local or remote). |
| `REQSCAN <path>` | Recursively find and install `requirements.txt` in subdirectories. |
| `GETFILE <url> <path>` | Download a file (smart check for existing files). |
| `DESKICO <label> <cmd>` | Create a clickable desktop shortcut. |
| `RFILTER <pkgs>` | Filter out specific packages to avoid conflicts. |

*(See the [Manual](doc/MANUAL.md) for the full list)*
