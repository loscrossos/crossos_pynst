# Pynst Tutorial - Install the Perfect ComfyUI

**Linux/MacOS Users:** All examples use a Windows path `d:\temp\mytestcomfy`. For Linux or macOS, the command is exactly the same, just use a Unix path e.g., `/Users/Shared/mycomfy`.

## Overview

Pynst is a powerful tool to securely install, manage, and repair your ComfyUI setup. It can also fully install workflows (the workflow file AND the models and the right dependencies). This all depends on an installer file (which is a plain text file with instructions). The definition file can be provided by someone, or you can easily define one yourself!

In this tutorial, we will learn how to build a perfect ComfyUI installation file that can be used with Pynst. It will be a full-fledged ComfyUI installation with the latest code, all accelerators installed, some of the best plugins pre-installed, and some nice icons on the desktop to just click and start! Then we will see how we can use it to manage a new installation or your existing installation.

To use an installation file, all you need to run is:

```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt [your target directory]
```

For example on Windows:

```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt d:\temp\mytestcomfy
```

This command does the following:
- Calls Python to run the installer.
- **First parameter**: The pynst-installer file to use. We use `installers/comfy_installer_rtx_full.pynst.txt`.
- **Second parameter**: The target directory where the project will be installed.

**IMPORTANT: Target Directory**
Pynst always installs into a directory that contains all files and repositories. If the target project directory is `mytestcomfy`, all files Pynst creates will be placed under it (e.g., `d:\temp\mytestcomfy\ComfyUI`).

---

## Pre-requisites

On an OS level, you need **Git** and **Python 3.8+** installed.

**Recommended: The Easy Way**
If you want to save time and avoid manual configuration, I highly recommend using the **CrossOS Auto-Setup** tool. It is free, open-source, and automatically installs everything you need (Git, Python, Visual C++ runtimes, etc.) for AI projects on Windows, Mac, or Linux.

Check out the project: [https://github.com/loscrossos/crossos_setup](https://github.com/loscrossos/crossos_setup)

---

**The Manual Way**
If you prefer to install things yourself:

**Windows**
Open an administrator console and run these commands:
```powershell
winget install --id=Python.Python.3.13 -e --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Git.Git -e --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Microsoft.VCRedist.2015+.x64 -e --silent --accept-package-agreements --accept-source-agreements --scope machine
```

**MacOS**
Use brew:
```bash
brew install git python@3.13
```

---

## Building the Installer File

Let's build a pynstaller that installs a brand new ComfyUI preloaded with accelerators and plugins!

### 1. Installing the Repo
The most basic setup is to clone the repository and create a virtual environment.

```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
```

- `CLONEIT`: Clones ComfyUI to the target directory (`.`). If it exists, it updates it.
- `SETVENV`: Ensures a venv exists inside `ComfyUI`. If `requirements.txt` is found, it installs it automatically.

### 2. Securing the Installation
We add a check to ensure the repository was correctly installed.

```bash
HASFILE ComfyUI/main.py
```
This ensures that running with `--safecheck` later will abort if the file is not found, preventing accidental overwrites of wrong directories.

### 3. Installing Accelerators
ComfyUI comes by default with no accelerators installed. We use `REQFILE` to install a specific requirements file for NVIDIA RTX cards.

```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV .
PRINTIT This step may take some time depending on your connection.
REQFILE https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt
REQSCAN .
```

### 4. Adding Custom Nodes (Plugins)
We can clone plugins directly into `ComfyUI/custom_nodes`.

```bash
CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

# Install requirements for ALL plugins found
REQSCAN ComfyUI/custom_nodes
```
`REQSCAN` is powerful: it finds ANY repository in that folder, updates it, and installs its `requirements.txt`.

### 5. Adding Starter Icons
We want clickable desktop icons. Pynst creates platform-native icons automatically.

```bash
HOMEEXE "ComfyUI_cpu" ComfyUI/main.py --cpu --auto-launch 
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
DESKICO "ComfyUI CPU Mode" ComfyUI/main.py --cpu  --auto-launch 
```
*   `DESKICO`: Desktop Icon
*   `HOMEEXE`: Script in the installation folder

### The Final File

```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV .
PRINTIT This step may take some time depending on your connection.
REQFILE https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt
REQSCAN .

CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

REQSCAN ComfyUI/custom_nodes
HOMEEXE "ComfyUI_cpu" ComfyUI/main.py --cpu --auto-launch 
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
DESKICO "ComfyUI CPU Mode" ComfyUI/main.py --cpu  --auto-launch 
```

---

## Managing Your Installation

### Repair an existing install
If your venv is broken, rebuild it from scratch:
```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt /ai/comfy --revenv
```

### Update Portable (Embedded) ComfyUI
Convert a portable install to a bleeding-edge version:
```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt /ai/comfy_portable --revenv --gitlatest
```

### Install Workflows & Models
You can automate model downloading too!

```bash
# Download workflow
GETFILE https://example.com/my_workflow.json ComfyUI/user/default/workflows

# Download models (Skipped if --noblob is used)
GETBLOB https://huggingface.co/some/model.safetensors ComfyUI/models/checkpoints

# Install required custom node
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes
REQSCAN ComfyUI/custom_nodes
```

### Safe Updates ("Senso" Mode)
Update plugins or add files without touching the core code or removing anything.
```bash
python pynst.py installers/comfy_installer.txt /ai/comfy --senso
```