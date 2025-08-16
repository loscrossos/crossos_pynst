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
python crossos_pynst.py -a [install | repair] --input [inputfile] --basedir [path where project should be installed]
```

example on Linux/Mac

```bash
python crossos_pynst.py      -a install --input comfy.cropy.txt --basedir /Users/Shared/aii/myco
```

example on Windows

```bash
python crossos_pynst.py      -a install --input comfy.cropy.txt --basedir c:\temp
```



**Commands**

* `--a [install | repair]`: 
  - install: will perform an installation (deleting the current installation!)
  - repair: will repair an existing installation safely 

* `--basedir [path]`: Target install directory  
* `--input [file]`: file containing install instructions

**Options**

* `--dry-run`: Simulate actions without making changes. Output will show which commands would normally run

  


# ROADMAP
- works: install: windows, linux, mac
- todo: write starters: ideally clickable
- todo: test rebuild
- todo: git pull on rebuild for comfy and for every node

**Upcoming Feature pipeline**
These might come but are still not in the works
- todo: data migration: safely move your models, nodes, workflows from an existing installation (e.g. Desktop install) to a new location
- todo: data separation and organisatiom: separation data from code (e.g. models are saved on a faster drive and code on the system drive)


