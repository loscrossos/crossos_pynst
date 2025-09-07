# CrossOS Pynst: your all-in-one Iron-Clad Python Installation Manager

A **cross-platform** (Windows, Linux, macOS) single-file Python tool to install or rebuild&repair pretty much any python project!

Elements:

Mode element  |  venv                     | repo                  | code in repo          | files
---           | ---                       | ---                   | ---                   | ---
**Sensitive** | created if not existent   | cloned if not existent| untouched             | Downloaded if not existent
**Install**   | created if not existent   | cloned if not existent| code update (no reset)| Downloaded if not existent 
**Rebuild**   | deleted if exists,rebuilt | cloned if not exists  | reset and updated     | Check for integrity and redownload 



install: installs repo and files. Only installs venv, files and repos if they dont exist. Updates code of existing repos.
repair: rebuilds a venv. deletes and reinstalls repos to latest code.



commmand                              | sensitive                       | Install   | Rebuild
---                                   | ---                             |---        | ---   
CMD_COMMENTEDOUT_LINE=    "#"       #| comment                         | <- same |<- same
CMD_PYTHON=               "PYTHON"  #| set python version              | <- same |<- same
CMD_PIPREQFILE=           "REQFILE" #| install req file                | <- same |<- same
CMD_PIPREQPACKAGE=        "REQWHLS" #| install req wheel or module     | <- same |<- same
CMD_PIPEXEC=        "RAWPIPCOMMAND" #| Advanced: Raw command line passed to pip.      | <- same |<- same
CMD_RFILTER=              "RFILTER" #| Filter out packages (from files and wheel)  | <- same |<- same
CMD_GITCLONE=             "CLONEIT" #| clone a repo into a dir. no code update if it exists  | <- same but updates code | same but updates code
CMD_GITCLONE_ALIAS1=      "GITCLON" #|   | <- same |<- same
CMD_REQSCAN=              "REQSCAN" #|   | <- same |<- same
CMD_GETFILE=              "GETFILE" #|   | <- same |<- same
CMD_GETBLOB=              "GETBLOB" #|   | <- same |<- same
CMD_PRINT=                "PRINTIT" #|   | <- same |<- same
CMD_CONFIRM_FILE_OR_ABORT="CONFIRM" #|   | <- same |<- same
CMD_PAUSE=                "PAUSEIT" #|   | <- same |<- same
CMD_EXEC =                "EXECUTE" #|   | <- same |<- same
CMD_SHORTCUT_DESK_ICON  = "DESKICO" #|   | <- same |<- same
CMD_SHORTCUT_DESK_SCRIPT= "DESKEXE" #|   | <- same |<- same
CMD_SHORTCUT_BASE_ICON  = "HOMEICO" #|   | <- same |<- same
CMD_SHORTCUT_BASE_SCRIPT= "HOMEEXE" #|   | <- same |<- same



-TODO: code CMD_PIPEXEC. all arguments are fed into pip. RFILTER does not affect this command. sensoinstall does not safeguard this command.
  -TODO: issue warnin if running CMD_PIPEXEC in sensoinstall mode, also warn ifruning at all as this is advanced. disabled in settings.
-TODO: code CMD_REQPACKAGE. It has has arguments of several wheels, which are passed to "pip install". RFILTER does not affect this command.
-TODO:on CMD_GITCLONE in rebuild mode: reset it first by running: git restore 
-TODO: implement CMD_GETBLOB, a copy of CMD_GETFILE
-TODO: implement --noblob. info: CMD_GETBLOB is a copy of getfile but meant for large files which are not mandatory (like models). a switch can be provided to not load these files. 

#docu: CMD_REQSCAN command is affected by RFILTER


Install comfyUI: install
repair comfy:    repair
fully update comfy: install
Install visomaster but i want my own models: install --noblob
install a workflow: install

options:
to overwrite: --force
code: 
--gitsafe (default)
--gitlatest

provide venvname:
--venvname

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

  
### Examples


```bash
PYTHON 3.12
REQFILE https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_lite_python312torch271cu129.txt
RFILTER torch torchvision torchaudio
GITCLON https://github.com/Hillobar/Rope .
REQSCAN .
DESKICO "Hillobar Rope" Rope/Rope.py

```



# ROADMAP
- works: install: windows, linux, mac
- todo: write starters: ideally clickable
- todo: test rebuild
- todo: git pull on rebuild for comfy and for every node

**Upcoming Feature pipeline**
These might come but are still not in the works
- todo: data migration: safely move your models, nodes, workflows from an existing installation (e.g. Desktop install) to a new location
- todo: data separation and organisatiom: separation data from code (e.g. models are saved on a faster drive and code on the system drive)


