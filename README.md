# CrossOS Pynst: your all-in-one Iron-Clad Python Installation Manager

A **cross-platform** (Windows, Linux, macOS) single-file Python tool to install or rebuild&repair pretty much any python project!



TODO: test file load if local has been changed

# Usage


```bash
python crossos_pynst.py [pynstfile] [directory]
```



on revenv: Pynst will delete stale folders from the venvs site-packages in rebuild embedded mode. Stale packages are packages orphaned after a failes install or deinstall and often start with a tilde.


todo: precheck checks if files to be downloaded are existent AND have different sizes than existent files. issue warning






Elements:

Mode element  |  venv                     | repo                  | code in repo          | files
---           | ---                       | ---                   | ---                   | ---
**senso** | created if not existent   | cloned if not existent| untouched, not updated| Downloaded if not existent
**Install**   | created if not existent   | cloned if not existent| code update (no reset)| Downloaded if not existent 
**revenv**   | deleted if exists,rebuilt | cloned if not exists  | reset and updated     | Check for integrity and redownload 



install: installs repo and files. Only installs venv, files and repos if they dont exist. Updates code of existing repos.
repair: rebuilds a venv. deletes and reinstalls repos to latest code.



commmand                              | sensitive                       | Install   | Rebuild
---                                   | ---                             |---        | ---
CMD_COMMENTEDOUT_LINE=     "#"       #| comment                                     | <- same   |<- same
CMD_PYTHON=                "PYTHON"  #| set python version to be used for venvs. Script will abort if he existing venv has another version   | <- same |<- same but will delete existing venvs and create a new venv with the scpecified version
CMD_SETVENV=               "SETVENV" #| sets the venv path to be used or created.   | <-same    | Venv to build or rebuild the venv
CMD_PIPREQFILE=            "REQINST" #| install req file                            | <- same   |<- same
CMD_PIPREQPACKAGE=         "PIPINST" #| install req wheel or module                 | <- same   |<- same
CMD_RFILTER=               "RFILTER" #| Filter out packages (from REQ* commands)    | <- same   |<- same
CMD_GITCLONE=              "CLONEIT" #| clone a repo into a dir. no code update if it exists    | <- same but updates code | same but updates code
CMD_GITCLONE_ALIAS1=       "GITCLON" #| clone a repo into a dir. no code update if it exists    | <- same but updates code | same but updates code
CMD_REQSCAN=               "REQSCAN" #| Specifies a directory to scan for subdirectories with "requirements.txt" to install. Will not update code in safe mode  | <- same but updates the repository code first|<- same but updates the repository code first
CMD_GETFILE=               "GETFILE" #| Downloads a file to a directory.  | <- same |<- same
CMD_GETBLOB=               "GETBLOB" #| Downloads a file to a directory. Used for large files (e.g. models)  | <- same |<- same
CMD_PRINT=                 "PRINTIT" #| Prints a message for the user to command line.  | <- same |<- same
CMD_CONFIRM_FILE_OR_ABORT= "HASFILE" #| Checks that a file exists. Aborts run if it fails  | <- same |<- same
CMD_PAUSE=                 "PAUSEIT" #| Pauses the execution until user confirms  | <- same |<- same
CMD_SHORTCUT_DESK_ICON  =  "DESKICO" #| Creates a Desktop icon with a command line  | <- same |<- same
CMD_SHORTCUT_DESK_SCRIPT=  "DESKEXE" #| Creates a Desktop script with a command line  | <- same |<- same
CMD_SHORTCUT_BASE_ICON  =  "HOMEICO" #| Creates a Installdir icon with a command line  | <- same |<- same
CMD_SHORTCUT_BASE_SCRIPT=  "HOMEEXE" #| Creates a installdir script with a command line  | <- same |<- same
CMD_XRUNGITCOMMAND ="XRUNGITCOMMAND"#| Runs a git command directly | <-same | <-same
CMD_PIPEXEC =       "XRUNPIPCOMMAND" #| Advanced: Raw command line passed to pip.      | <- same |<- same
CMD_EXEC =          "XRUNPYTHONFILE" #| Runs a python file (arguments and params allowed)  | <- same |<- same





code CMD_PIPEXEC. all arguments are fed into pip. RFILTER does not affect this command. sensoinstall does not safeguard this command.

TODO: issue warnin if running CMD_PIPEXEC in sensoinstall mode, also warn ifruning at all as this is advanced. disabled in settings.

forceforcegitlatest: reset git repos first by running: git restore .
  --info: 
    -a git repo where a file is changed by me but others are changed on server can be "pulled"
    -a git where a file is changed by me and the sme file on server must be restore'd before hand


--noblob. info: CMD_GETBLOB is a copy of getfile but meant for large files which are not mandatory (like models). a switch can be provided to not load these files. 

docu: CMD_REQSCAN command is affected by RFILTER

example use cases:
Install comfyUI: 
repair comfy:    
fully update comfy: 
Install visomaster but i want my own models:  --noblob
install a workflow: 



TODO: --gitrelease: forces git repos to last release tag



**Install projects**

With one command you can (fully from zero) install a fully accelerated and configured ComfyUI/WAN/LLM or any other python project so that its ready to use: it has the latest code, ALL the cool accelerators for your Nvidia Card, can have plugins included as well as the starter shortcuts on your desktop... on all OSes!

You have an existing installation that you managed to install and get running with sweat and tears and since you are afraid to change anything in fear of breaking it? well.. how would you like a fully safe and riskfree way to make it shinny and ultra hardened? 

i gotchu covered: welcome to:

**repair projects**

One command of your power glove and the tool will fully iron-clad your existing venv: ensures the correct Python & PyTorch versions, repairs your virtual environments (including portable mode), installs the rights accelerators and updates and repairs custom node requirements with **safety checks**. All fully safe to your existing data.

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
python crossos_pynst.py [inputfile] [install path where project should be installed]
```

example on Linux/Mac

```bash
python crossos_pynst.py     comfy.cropy.txt  /Users/Shared/aii/myco
```

example on Windows

```bash
python crossos_pynst.py      comfy.cropy.txt  c:\temp
```




* `[input file]`: file containing install instructions
* `[install path]`: Target install directory  




**Options**

usage: crossos_pynst.py [-h] [--revenv] [--senso] [--embedded] [--nodesktop] [--dryrun] [--verbose] [--backup] [--noblob] [--venvname VENVNAME]
                        [--forcegitlatest] [--updatemode] [--debugtest]
                        inputfile targetdirectory

Install or repair a Python project based on a instruction file.

positional arguments:
  inputfile            Path to inputfile (will be coerced to UTF-8 if needed)
  targetdirectory      Base directory for install/repair

options:
  -h, --help           show this help message and exit
  --revenv             rebuilds the venv from zero. Can be used to repair an installation with a broken venv.
  --senso              adds extra care not to change/replace any existing code or file and only add new elements.
  --embedded           Treat venv installation as portable with a 'python_embedded' folder (or name defined with custom venv option)
  --nodesktop          Do not create Dekstop shortcuts even when defined in the input file
  --dryrun             Simulated run. All actions are performed without changing files or installing anything. would-be commands are shown
  --verbose            Show full subprocess output. Good for debugging (can be long)
  --backup             Backup existing venv before deleting/replacing or changing anything (backup is the original name and a suffix on the same
                       location)
  --noblob             Disable Filedownloads marked as blobs. This can reduce band width usage but some files will be missing
  --venvname VENVNAME  Provide a custom name for the virtual environment
  --forcegitlatest     Force git repository code to the newest version on the main/master branch (sometimes calles 'nightly')
  --updatemode         Pre-Check if repositories to be cloned already exist and warn if they dont. This helps ensure an installation will be updated
                       and the target exists. Else a typo would cause a full installation besides an existing one.
  --debugtest          Show debug info and quit



 
### Examples


```bash
PYTHON 3.12
REQFILE https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_lite_python312torch271cu129.txt
RFILTER torch torchvision torchaudio
CLONEIT https://github.com/Hillobar/Rope .
REQSCAN .
DESKICO "Hillobar Rope" Rope/Rope.py

```



# ROADMAP
- works: install: windows, linux, mac
- works: write starters: ideally clickable
- works: test rebuild
- works: git pull on rebuild for comfy and for every node

**Upcoming Feature pipeline**

- Nunchaku:
https://www.reddit.com/r/StableDiffusion/comments/1n8xyc1/nunchaku_v100_officially_released/
https://nunchaku.tech/docs/nunchaku/installation/installation.html#installation-installation


https://www.reddit.com/r/StableDiffusion/comments/1nd7rvf/nunchaku_qwen_image_edit_is_out/

guide:
https://nunchaku.tech/docs/nunchaku/installation/setup_windows.html

custom node:

https://github.com/nunchaku-tech/ComfyUI-nunchaku.git



windows:
https://github.com/nunchaku-tech/nunchaku/releases/download/v1.0.0/nunchaku-1.0.0+torch2.8-cp313-cp313-win_amd64.whl

Linux 
https://github.com/nunchaku-tech/nunchaku/releases/download/v1.0.0/nunchaku-1.0.0+torch2.8-cp313-cp313-linux_x86_64.whl  ; sys_platform  == 'linux'



DONE: check if desktopmode comfy woudl work:
  -for code yes
  -for env yes.
  -not for models
