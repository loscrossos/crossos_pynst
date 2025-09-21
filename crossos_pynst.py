#!/usr/bin/env python3

"""
#TODO
DONE: criticalfilecheck.
TODO: warnfilecheck
TODO: 


FILECHECK crit ComfyUI/myfile "this does not seem to be a Comfy installation"
FILECHECK warn ComfyUI/main.py  "Not having this file will slowdown your processes"

FILECRITX
FILEWARNX






UseCases:
-Install repository
-repair repository
-install plugins
-install files
-verify installation integrity
-update installation code


ComfyUI.
Fully automatically, safely and fail proof perform these tasks with one single command:
-Install a fully configured (ALL accelerators!) ComnfyUI with start shortcut on your desktop from zero. 
-repair broken installation by rebuilding venv and updating code
-add plugins to an existing installation
-install any workflow (automatic collection and installation of workflow, plugins, models)

All this while:
-not needing any admin rights!
-not needing to disabl or override any security mechanisms of your OS

"""


"""
i need a python function that takes a string and uses the first letters of the frst 2 words (if only one word only the first 2 letters) to create a ico or png file with the letters as a logo.  (the format "png" or "ico" shall be given as a param)
e.g. if the input is "test command" then the letters are "te co".
make the letters rounded and nice. not blocky. 
only need A-Z (uppercase) and digits 0-9,
The ico or png dimensions is 256x256.
the program shall run on windows, linux and macos and shall not have any dependencies: only standard library.

any questions before coding?
"""

#***START***
#SHORTCUTMAKER

import os
import sys
from pathlib import Path
def get_desktop_directory() -> Path:
    """
    Returns the path to the user's desktop directory across different operating systems.
    Returns:
        Path: Path object pointing to the desktop directory
    """
    home = Path.home()
    if sys.platform == 'win32':
        # Windows
        desktop = home / 'Desktop'
        # On some Windows versions, the desktop might be localized
        if not desktop.exists():
            # Try getting it from environment variables
            desktop = Path(os.environ.get('USERPROFILE')) / 'Desktop'
    elif sys.platform == 'darwin':
        # macOS
        desktop = home / 'Desktop'
    else:
        # Linux and other UNIX-like systems
        # Try XDG user dirs first
        xdg_config = home / '.config' / 'user-dirs.dirs'
        if xdg_config.exists():
            try:
                with open(xdg_config, 'r') as f:
                    for line in f:
                        if line.startswith('XDG_DESKTOP_DIR'):
                            # Extract path, remove quotes and $HOME
                            path = line.split('=')[1].strip().strip('"')
                            path = path.replace('$HOME', str(home))
                            desktop = Path(path)
                            break
            except (IOError, IndexError):
                pass
        # Fallback if XDG method fails
        if 'desktop' not in locals():
            desktop = home / 'Desktop'
            # Some Linux systems might use lowercase 'desktop'
            if not desktop.exists():
                desktop = home / 'desktop'
    return desktop

###################################
import os
import sys
import tempfile
import subprocess
def create_shortcut_windows(app_name: str , python_command: str , icon_path: str , shortcut_path: str , working_dir: str ):
    """
    Create a clickable Windows .lnk shortcut.
    :param shortcut_path: Path to the shortcut file (.lnk)
    :param target: Command or executable to run
    :param icon_path: Optional path to .ico file
    :param working_dir: Optional working directory for the shortcut
    """
    shortcut_path=f"{shortcut_path}/{app_name}.lnk"
    #shortcut_path = os.path.expanduser(shortcut_path)
    icon_path = os.path.expanduser(icon_path) if icon_path else ""
    working_dir = os.path.expanduser(working_dir) if working_dir else ""
    # Ensure directory exists
    os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
    # Create a temporary VBScript to generate the shortcut
    vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\\Windows\\System32\\cmd.exe"
oLink.Arguments = "/K {python_command}"
oLink.WorkingDirectory = "{working_dir or os.path.dirname(python_command)}"
{"oLink.IconLocation = \"" + icon_path + "\"" if icon_path else ""}
oLink.Save
'''
    with tempfile.NamedTemporaryFile("w", suffix=".vbs", delete=False) as vbs_file:
        vbs_file.write(vbs_content)
        temp_vbs_path = vbs_file.name
    # Run the VBScript silently
    subprocess.run(["cscript", "//NoLogo", temp_vbs_path], check=True)
    # Remove the temporary VBScript
    os.remove(temp_vbs_path)
###############################################################
"""
for macos: i need a python script that creates a clickable file on the desktop (which runs a command i provide) and assigns an icon to it. it can be app bundle or  .command. its important that i dont want to install any dependencies for python. the icon format will be png. so any conversion if necessary should be in the script. existing files can be overwritten. the command to be run will be a python script  as in "python myfile.py"
"""
import os
import shutil
import subprocess
from pathlib import Path
def create_shortcut_mac(app_name: str , python_command: str , icon_path: str , shortcut_path: str , working_dir: str ):
    # === PATHS ===
    targetdir=Path(shortcut_path)
    app_path = targetdir / f"{app_name}.app"
    contents_path = app_path / "Contents"
    macos_path = contents_path / "MacOS"
    resources_path = contents_path / "Resources"
    icns_path = resources_path / "icon.icns"
    # === CLEAN EXISTING ===
    if app_path.exists():
        shutil.rmtree(app_path)
    # === CREATE FOLDER STRUCTURE ===
    macos_path.mkdir(parents=True)
    resources_path.mkdir()
    # === CREATE EXECUTABLE SCRIPT (open in Terminal) ===
    executable_path = macos_path / app_name
    with open(executable_path, "w") as f:
        f.write(f"""#!/bin/bash
    osascript -e 'tell application "Terminal" to do script "cd \\"{working_dir}\\"; {python_command}"'
    """)
    os.chmod(executable_path, 0o755)
    # === CONVERT PNG TO ICNS ===
    # Create temporary iconset
    iconset_path = resources_path / "icon.iconset"
    if iconset_path.exists():
        shutil.rmtree(iconset_path)
    iconset_path.mkdir()
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        png_resized = iconset_path / f"icon_{size}x{size}.png"
        subprocess.run(
            ["sips", "-z", str(size), str(size), icon_path, "--out", str(png_resized)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    # Convert to ICNS
    subprocess.run(["iconutil", "-c", "icns", str(iconset_path), "-o", str(icns_path)])
    shutil.rmtree(iconset_path)
    # === CREATE Info.plist ===
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CFBundleExecutable</key>
        <string>{app_name}</string>
        <key>CFBundleIconFile</key>
        <string>icon.icns</string>
        <key>CFBundleIdentifier</key>
        <string>com.user.{app_name}</string>
        <key>CFBundleName</key>
        <string>{app_name}</string>
        <key>CFBundleVersion</key>
        <string>1.0</string>
        <key>CFBundlePackageType</key>
        <string>APPL</string>
    </dict>
    </plist>
    """

    with open(contents_path / "Info.plist", "w") as f:
        f.write(plist_content)

 
###############################################################
import os
import stat
import sys
def create_shortcut_linux(app_name: str , python_command: str , icon_path: str , shortcut_path: str , working_dir: str ):
    icon_path = os.path.expanduser(icon_path)
    f_content=f"""
    #!/usr/bin/env xdg-open
    [Desktop Entry]
    Exec=/bin/bash -c '{python_command}'
    Name={app_name}
    Type=Application
    Terminal=true
    Icon={icon_path}
    Path={working_dir}
    """
    starter_extension=".desktop"
    f_name=f"{shortcut_path}{os.sep}{app_name}{starter_extension}"
    filename = os.path.expanduser(f_name)
    # Write the content to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f_content)
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

##############



def crossos_make_shortcut(app_name, exec_line,  installpath, env_path, onDesktop=False, working_dir: str=None):
    """
    app_name: name of the shortcut. e.g. "ComfyUI CPU Mode"
    exec_line: python file to be called. include the folder from the installdir: e.g. ComfyUI/main.py
    installpath: path where the main installation takes place,
    env_path: path to the virtenv. used to build the calling command
    """
    
    env_bin_folder="bin"
    icon_ext="png"
    if sys.platform.startswith("win"):
        env_bin_folder="scripts"
        icon_ext="ico"


    param_env_path=env_path
    icon_path=f"{installpath}{os.sep}{app_name}_icon.{icon_ext}"

    param_app_name = f"{app_name}"            # Name of the app
    param_python_command = exec_line
    param_icon_path = icon_path  # Path to your PNG icon
    param_targetshortcut_path=installpath
    if onDesktop:
        param_targetshortcut_path=str(get_desktop_directory())

    param_working_dir=working_dir
    #crossos_make_icon(app_name, '#FFFFFF', '#0066CC', placement='sbs', size=256,  path=icon_path)

    crossos_make_icon_artsy(text=app_name, outfile=icon_path)

    if sys.platform.startswith("win"):
        create_shortcut_windows(app_name=param_app_name , python_command=param_python_command , icon_path=param_icon_path , shortcut_path=param_targetshortcut_path , working_dir=param_working_dir )
    if sys.platform.startswith("darwin"):
        create_shortcut_mac(app_name=param_app_name , python_command=param_python_command , icon_path=param_icon_path , shortcut_path=param_targetshortcut_path , working_dir=param_working_dir )
    if sys.platform.startswith("linux"):
        create_shortcut_linux(app_name=param_app_name , python_command=param_python_command , icon_path=param_icon_path , shortcut_path=param_targetshortcut_path , working_dir=param_working_dir )

#SHORTCUTMAKER
##***END***







































#***START***
###***ICONMAKER ***START***



#####ENGINE1 Blocky and pixely+++++++++++++
import struct, zlib
# Simple 8x8 rounded block font (A-Z, uppercase only)
FONT = {
    'A': ["00111100",
          "01000010",
          "10000001",
          "10000001",
          "11111111",
          "10000001",
          "10000001",
          "00000000"],
    'B': ["11111100",
          "10000010",
          "10000010",
          "11111100",
          "10000010",
          "10000010",
          "11111100",
          "00000000"],
    'C': ["00111110",
          "01000001",
          "10000000",
          "10000000",
          "10000000",
          "10000000",
          "01000001",
          "00111110"],
    'D': ["11111000",
          "10000100",
          "10000010",
          "10000010",
          "10000010",
          "10000100",
          "11111000",
          "00000000"],
    'E': ["11111111",
          "10000000",
          "10000000",
          "11111110",
          "10000000",
          "10000000",
          "11111111",
          "00000000"],
    'F': ["11111111",
          "10000000",
          "10000000",
          "11111110",
          "10000000",
          "10000000",
          "10000000",
          "00000000"],
    'G': ["00111110",
          "01000001",
          "10000000",
          "10000000",
          "10001111",
          "10000001",
          "01000001",
          "00111110"],
    'H': ["10000001",
          "10000001",
          "10000001",
          "11111111",
          "10000001",
          "10000001",
          "10000001",
          "00000000"],
    'I': ["11111111",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "11111111",
          "00000000"],
    'J': ["00011111",
          "00000100",
          "00000100",
          "00000100",
          "10000100",
          "01000100",
          "00111000",
          "00000000"],
    'K': ["10000010",
          "10000100",
          "10001000",
          "11110000",
          "10001000",
          "10000100",
          "10000010",
          "00000000"],
    'L': ["10000000",
          "10000000",
          "10000000",
          "10000000",
          "10000000",
          "10000000",
          "11111111",
          "00000000"],
    'M': ["10000001",
          "11000011",
          "10100101",
          "10011001",
          "10000001",
          "10000001",
          "10000001",
          "00000000"],
    'N': ["10000001",
          "11000001",
          "10100001",
          "10010001",
          "10001001",
          "10000101",
          "10000011",
          "00000000"],
    'O': ["00111100",
          "01000010",
          "10000001",
          "10000001",
          "10000001",
          "10000001",
          "01000010",
          "00111100"],
    'P': ["11111100",
          "10000010",
          "10000010",
          "11111100",
          "10000000",
          "10000000",
          "10000000",
          "00000000"],
    'Q': ["00111100",
          "01000010",
          "10000001",
          "10000001",
          "10000001",
          "10001001",
          "01000010",
          "00111101"],
    'R': ["11111100",
          "10000010",
          "10000010",
          "11111100",
          "10001000",
          "10000100",
          "10000010",
          "00000000"],
    'S': ["01111110",
          "10000001",
          "10000000",
          "01111100",
          "00000010",
          "10000001",
          "01111110",
          "00000000"],
    'T': ["11111111",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "00000000"],
    'U': ["10000001",
          "10000001",
          "10000001",
          "10000001",
          "10000001",
          "10000001",
          "01000010",
          "00111100"],
    'V': ["10000001",
          "10000001",
          "10000001",
          "10000001",
          "01000010",
          "01000010",
          "00100100",
          "00011000"],
    'W': ["10000001",
          "10000001",
          "10000001",
          "10000001",
          "10011001",
          "10100101",
          "11000011",
          "10000001"],
    'X': ["10000001",
          "01000010",
          "00100100",
          "00011000",
          "00100100",
          "01000010",
          "10000001",
          "00000000"],
    'Y': ["10000001",
          "01000010",
          "00100100",
          "00011000",
          "00011000",
          "00011000",
          "00011000",
          "00000000"],
    'Z': ["11111111",
          "00000010",
          "00000100",
          "00001000",
          "00010000",
          "00100000",
          "11111111",
          "00000000"]
}

def hex_to_rgba(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 6:
        r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
        return (r, g, b, 255)
    elif len(hex_str) == 8:
        r, g, b, a = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16), int(hex_str[6:8], 16)
        return (r, g, b, a)
    else:
        raise ValueError("Invalid hex color")




def render_letter(letter, fg, bg, scale):
    grid = FONT.get(letter.upper(), FONT['C'])
    w, h = len(grid[0]), len(grid)
    img = [[bg for _ in range(w * scale)] for _ in range(h * scale)]
    radius = scale * 0.3
    for gy, row in enumerate(grid):
        for gx, cell in enumerate(row):
            if cell == '1':
                for sy in range(scale):
                    for sx in range(scale):
                        px = gx * scale + sx
                        py = gy * scale + sy
                        img[py][px] = fg
    return img

def combine_letters(l1, l2, fg, bg, size, mode):
    if mode == 'sbs':
        letter_width = size // 2
        scale = letter_width // 8
    else:
        scale = size // 8
    img1 = render_letter(l1, fg, bg, scale)
    img2 = render_letter(l2, fg, bg, scale)
    h, w = len(img1), len(img1[0])
    canvas = [[bg for _ in range(size)] for _ in range(size)]
    if mode == 'sbs':
        off_y = (size - h) // 2
        off_x1 = (letter_width - w) // 2
        off_x2 = letter_width + (letter_width - w) // 2
        for y in range(h):
            for x in range(w):
                canvas[off_y + y][off_x1 + x] = img1[y][x]
                canvas[off_y + y][off_x2 + x] = img2[y][x]
    else:
        off_y = (size - h) // 2
        off_x = (size - w) // 2
        for y in range(h):
            for x in range(w):
                if img1[y][x] != bg:
                    canvas[off_y + y][off_x + x] = img1[y][x]
                if img2[y][x] != bg:
                    canvas[off_y + y][off_x + x] = img2[y][x]
    return canvas

def write_png(path, pixels):
    height, width = len(pixels), len(pixels[0])
    raw_data = b''.join(b'\x00' + b''.join(struct.pack('BBBB', *px) for px in row) for row in pixels)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw_data, 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

def make_icon(path, base_pixels):
    sizes = [256, 128, 64, 32, 16]
    images = []
    for s in sizes:
        factor = len(base_pixels) // s
        small = [[base_pixels[y*factor][x*factor] for x in range(s)] for y in range(s)]
        raw_data = b''.join(b'\x00' + b''.join(struct.pack('BBBB', *px) for px in row) for row in small)
        def chunk(tag, data):
            return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
        png_data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack(">IIBBBBB", s, s, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw_data, 9)) + chunk(b'IEND', b'')
        images.append(png_data)
    ico = struct.pack('<HHH', 0, 1, len(images))
    offset = 6 + len(images) * 16
    for i, img in enumerate(images):
        w = h = sizes[i] if sizes[i] < 256 else 0
        ico += struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, len(img), offset)
        offset += len(img)
    for img in images:
        ico += img
    with open(path, 'wb') as f:
        f.write(ico)



# Global defaults
DEFAULT_FIRST = "X"
DEFAULT_SECOND = "Y"
def get_two_letters(input_str):
    global DEFAULT_FIRST, DEFAULT_SECOND
    if not isinstance(input_str, str):
        input_str = str(input_str or "")
    
    input_str = input_str.strip()    
    # Empty - defaults
    if not input_str:
        return DEFAULT_FIRST, DEFAULT_SECOND
    # Manual split into words (alphabetic chunks, unicode-aware)
    words = []
    current = []
    for ch in input_str:
        if ch.isalpha():  # True for accented and non-Latin letters too
            current.append(ch)
        else:
            if current:
                words.append("".join(current))
                current = []
    if current:
        words.append("".join(current))
    # Pick letters based on rules
    if len(words) >= 2:
        return words[0][0].upper(), words[1][0].upper()
    elif len(words) == 1:
        if len(words[0]) >= 2:
            return words[0][0].upper(), words[0][1].upper()
        else:
            return words[0][0].upper(), DEFAULT_SECOND
    else:
        return DEFAULT_FIRST, DEFAULT_SECOND

def crossos_make_icon(word, fg_hex, bg_hex, placement='sbs', size=256, path='logo'):
    
    l1, l2 = get_two_letters(word)
    fmt=path[-3:]
    fg, bg = hex_to_rgba(fg_hex), hex_to_rgba(bg_hex)
    pixels = combine_letters(l1, l2, fg, bg, size, placement)
    if fmt == 'png':
        write_png(f"{path}", pixels)
    elif fmt == 'ico':
        make_icon(f"{path}", pixels)
    else:
        raise ValueError("Format must be 'png' or 'ico'")


###***END***  #####ENGINE1 Blocky and pixely+++++++++++++






























#####ENGINE2 better+++++++++++++



#!/usr/bin/env python3
# Pure-stdlib logo generator with anti-aliased vector strokes.
# - Accepts a string, extracts first 2 letters of first 2 words (or first 2 of one word)
# - Renders smooth, geometric stroke letters (A–Z, 0–9) at 256x256
# - Saves as PNG or ICO (PNG-in-ICO) with configurable colors
#
# No external dependencies. Works on Windows, Linux, macOS.

from pathlib import Path
import math
import struct
import zlib


# --------------------------
# Utilities
# --------------------------

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def lerp(a, b, t):
    return a + (b - a) * t


def length(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def downsample_mask(mask_hi, w_hi, h_hi, ss):
    """Average ss x ss blocks from grayscale hi-res mask into low-res mask."""
    w_lo, h_lo = w_hi // ss, h_hi // ss
    mask_lo = [0.0] * (w_lo * h_lo)
    inv = 1.0 / (ss * ss)
    for y in range(h_lo):
        for x in range(w_lo):
            s = 0.0
            y0 = y * ss
            x0 = x * ss
            for yy in range(y0, y0 + ss):
                i = yy * w_hi + x0
                s += sum(mask_hi[i:i + ss])
            mask_lo[y * w_lo + x] = s * inv
    return mask_lo, w_lo, h_lo


def compose_rgba_over(bg, fg, alpha):  # colors are (r,g,b,a) 0..255, alpha is 0..1 (from mask)
    a_fg = (fg[3] / 255.0) * alpha
    a_bg = bg[3] / 255.0
    a_out = a_fg + a_bg * (1 - a_fg)
    if a_out == 0:
        return (0, 0, 0, 0)
    r = int((fg[0] * a_fg + bg[0] * a_bg * (1 - a_fg)) / a_out + 0.5)
    g = int((fg[1] * a_fg + bg[1] * a_bg * (1 - a_fg)) / a_out + 0.5)
    b = int((fg[2] * a_fg + bg[2] * a_bg * (1 - a_fg)) / a_out + 0.5)
    a = int(a_out * 255 + 0.5)
    return (r, g, b, a)


def encode_png(rgba_bytes, w, h):
    """Minimal PNG encoder for RGBA data."""
    stride = w * 4
    # Prepend filter 0 to each scanline
    raw = b"".join(b"\x00" + rgba_bytes[y * stride:(y + 1) * stride] for y in range(h))
    comp = zlib.compress(raw)
    def chunk(typ, data):
        return struct.pack("!I", len(data)) + typ + data + struct.pack("!I", zlib.crc32(typ + data) & 0xffffffff)
    ihdr = struct.pack("!2I5B", w, h, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")


def write_png_or_ico(png_bytes, outfile: Path, size):
    suf = outfile.suffix.lower()
    if suf == ".png":
        outfile.write_bytes(png_bytes)
    elif suf == ".ico":
        # Write ICO with a single PNG entry (supported since Vista/Win7+)
        header = struct.pack("<3H", 0, 1, 1)  # reserved=0, type=1(icon), count=1
        width = size if size < 256 else 0
        height = size if size < 256 else 0
        png_size = len(png_bytes)
        offset = 6 + 16  # header + single dir entry
        entry = struct.pack("<BBBBHHII",
                            width, height,
                            0, 0,      # colors, reserved
                            1, 32,     # planes, bitcount
                            png_size, offset)
        outfile.write_bytes(header + entry + png_bytes)
    else:
        raise ValueError("Output file must end with .png or .ico")


# --------------------------
# Stroke-based vector font
# --------------------------
# Each glyph defined by:
#   {
#     "w": advance width (relative, ~1.0),
#     "strokes": [(x1,y1,x2,y2), ...] in normalized glyph space [0..1]
#   }
# Coordinates follow a geometric, mono-line sans-serif style.
# Digits included. All uppercase.

def G(w, segs):  # helper to build glyph dict
    return {"w": w, "strokes": segs}

GLYPHS = {}

# Basic geometric helpers for consistency
MARGIN_X = 0.10
MARGIN_Y = 0.10
LEFT = MARGIN_X
RIGHT = 1.0 - MARGIN_X
TOP = MARGIN_Y
BOTTOM = 1.0 - MARGIN_Y
MID_X = 0.5
MID_Y = 0.5
BAR_HI = MID_Y - 0.02
BAR_LO = MID_Y + 0.02

# A
GLYPHS["A"] = G(1.0, [
    (LEFT, BOTTOM, MID_X, TOP),
    (RIGHT, BOTTOM, MID_X, TOP),
    (LEFT + 0.14, MID_Y, RIGHT - 0.14, MID_Y),
])

# B (angular bowls)
GLYPHS["B"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT - 0.1, TOP + 0.15),
    (RIGHT - 0.1, TOP + 0.15, LEFT, MID_Y),
    (LEFT, MID_Y, RIGHT - 0.1, MID_Y + 0.15),
    (RIGHT - 0.1, MID_Y + 0.15, LEFT, BOTTOM),
])

# C
GLYPHS["C"] = G(1.0, [
    (RIGHT, TOP + 0.1, LEFT + 0.15, TOP),
    (LEFT + 0.15, TOP, LEFT, MID_Y),
    (LEFT, MID_Y, LEFT + 0.15, BOTTOM),
    (LEFT + 0.15, BOTTOM, RIGHT, BOTTOM - 0.1),
])

# D
GLYPHS["D"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT - 0.1, MID_Y - 0.2),
    (RIGHT - 0.1, MID_Y - 0.2, RIGHT - 0.1, MID_Y + 0.2),
    (RIGHT - 0.1, MID_Y + 0.2, LEFT, BOTTOM),
])

# E
GLYPHS["E"] = G(0.95, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT, TOP),
    (LEFT, MID_Y, RIGHT - 0.15, MID_Y),
    (LEFT, BOTTOM, RIGHT, BOTTOM),
])

# F
GLYPHS["F"] = G(0.95, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT, TOP),
    (LEFT, MID_Y, RIGHT - 0.2, MID_Y),
])

# G
GLYPHS["G"] = G(1.0, [
    (RIGHT - 0.05, TOP + 0.12, LEFT + 0.15, TOP),
    (LEFT + 0.15, TOP, LEFT, MID_Y),
    (LEFT, MID_Y, LEFT + 0.15, BOTTOM),
    (LEFT + 0.15, BOTTOM, RIGHT, BOTTOM - 0.1),
    (RIGHT, BOTTOM - 0.1, RIGHT, MID_Y + 0.05),
    (RIGHT, MID_Y + 0.05, MID_X + 0.05, MID_Y + 0.05),
])

# H
GLYPHS["H"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM),
    (RIGHT, TOP, RIGHT, BOTTOM),
    (LEFT, MID_Y, RIGHT, MID_Y),
])

# I
GLYPHS["I"] = G(0.7, [
    (MID_X, TOP, MID_X, BOTTOM),
    (LEFT, TOP, RIGHT, TOP),
    (LEFT, BOTTOM, RIGHT, BOTTOM),
])

# J
GLYPHS["J"] = G(1.0, [
    (RIGHT - 0.2, TOP, RIGHT - 0.2, BOTTOM - 0.1),
    (RIGHT - 0.2, BOTTOM - 0.1, RIGHT - 0.5, BOTTOM),
    (RIGHT - 0.5, BOTTOM, LEFT + 0.15, BOTTOM - 0.1),
])

# K
GLYPHS["K"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM),
    (RIGHT, TOP, LEFT + 0.1, MID_Y),
    (LEFT + 0.1, MID_Y, RIGHT, BOTTOM),
])

# L
GLYPHS["L"] = G(0.9, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, BOTTOM, RIGHT, BOTTOM),
])

# M
GLYPHS["M"] = G(1.1, [
    (LEFT, BOTTOM, LEFT, TOP),
    (LEFT, TOP, MID_X, MID_Y),
    (MID_X, MID_Y, RIGHT, TOP),
    (RIGHT, TOP, RIGHT, BOTTOM),
])

# O
GLYPHS["O"] = G(1.0, [
    (LEFT + 0.1, MID_Y, LEFT + 0.2, TOP + 0.1),
    (LEFT + 0.2, TOP + 0.1, MID_X, TOP),
    (MID_X, TOP, RIGHT - 0.2, TOP + 0.1),
    (RIGHT - 0.2, TOP + 0.1, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, RIGHT - 0.2, BOTTOM - 0.1),
    (RIGHT - 0.2, BOTTOM - 0.1, MID_X, BOTTOM),
    (MID_X, BOTTOM, LEFT + 0.2, BOTTOM - 0.1),
    (LEFT + 0.2, BOTTOM - 0.1, LEFT + 0.1, MID_Y),
])

# P
GLYPHS["P"] = G(0.95, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT - 0.1, TOP),
    (RIGHT - 0.1, TOP, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, LEFT, MID_Y),
])

# Q
GLYPHS["Q"] = G(1.0, GLYPHS["O"]["strokes"] + [
    (MID_X + 0.05, MID_Y + 0.05, RIGHT, BOTTOM),
])

# R
GLYPHS["R"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM),
    (LEFT, TOP, RIGHT - 0.1, TOP),
    (RIGHT - 0.1, TOP, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, LEFT, MID_Y),
    (LEFT + 0.2, MID_Y, RIGHT, BOTTOM),
])

# S
GLYPHS["S"] = G(1.0, [
    (RIGHT - 0.05, TOP + 0.15, MID_X, TOP),
    (MID_X, TOP, LEFT + 0.05, TOP + 0.15),
    (LEFT + 0.05, TOP + 0.15, LEFT + 0.15, MID_Y - 0.05),
    (LEFT + 0.15, MID_Y - 0.05, RIGHT - 0.15, MID_Y + 0.05),
    (RIGHT - 0.15, MID_Y + 0.05, RIGHT - 0.05, BOTTOM - 0.15),
    (RIGHT - 0.05, BOTTOM - 0.15, MID_X, BOTTOM),
    (MID_X, BOTTOM, LEFT + 0.05, BOTTOM - 0.15),
])

# T
GLYPHS["T"] = G(1.0, [
    (LEFT, TOP, RIGHT, TOP),
    (MID_X, TOP, MID_X, BOTTOM),
])

# U
GLYPHS["U"] = G(1.0, [
    (LEFT, TOP, LEFT, BOTTOM - 0.15),
    (LEFT, BOTTOM - 0.15, MID_X, BOTTOM),
    (MID_X, BOTTOM, RIGHT, BOTTOM - 0.15),
    (RIGHT, BOTTOM - 0.15, RIGHT, TOP),
])

# V
GLYPHS["V"] = G(1.0, [
    (LEFT, TOP, MID_X, BOTTOM),
    (MID_X, BOTTOM, RIGHT, TOP),
])

# W
GLYPHS["W"] = G(1.2, [
    (LEFT, TOP, LEFT + 0.25, BOTTOM),
    (LEFT + 0.25, BOTTOM, MID_X, TOP),
    (MID_X, TOP, RIGHT - 0.25, BOTTOM),
    (RIGHT - 0.25, BOTTOM, RIGHT, TOP),
])

# X
GLYPHS["X"] = G(1.0, [
    (LEFT, TOP, RIGHT, BOTTOM),
    (RIGHT, TOP, LEFT, BOTTOM),
])

# Y
GLYPHS["Y"] = G(1.0, [
    (LEFT, TOP, MID_X, MID_Y),
    (RIGHT, TOP, MID_X, MID_Y),
    (MID_X, MID_Y, MID_X, BOTTOM),
])

# Z
GLYPHS["Z"] = G(1.0, [
    (LEFT, TOP, RIGHT, TOP),
    (RIGHT, TOP, LEFT, BOTTOM),
    (LEFT, BOTTOM, RIGHT, BOTTOM),
])

# Digits 0–9 (geometric)
GLYPHS["0"] = G(1.0, GLYPHS["O"]["strokes"])
GLYPHS["1"] = G(0.8, [
    (MID_X, TOP, MID_X, BOTTOM),
    (MID_X - 0.2, TOP + 0.2, MID_X, TOP),
])
GLYPHS["2"] = G(1.0, [
    (LEFT + 0.05, TOP + 0.15, MID_X, TOP),
    (MID_X, TOP, RIGHT - 0.05, TOP + 0.15),
    (RIGHT - 0.05, TOP + 0.15, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, LEFT + 0.1, BOTTOM),
    (LEFT + 0.1, BOTTOM, RIGHT, BOTTOM),
])
GLYPHS["3"] = G(1.0, [
    (LEFT + 0.05, TOP + 0.15, MID_X, TOP),
    (MID_X, TOP, RIGHT - 0.05, TOP + 0.15),
    (RIGHT - 0.05, TOP + 0.15, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, MID_X, MID_Y),
    (MID_X, MID_Y, RIGHT - 0.1, MID_Y + 0.01),
    (RIGHT - 0.1, MID_Y + 0.01, RIGHT - 0.05, BOTTOM - 0.15),
    (RIGHT - 0.05, BOTTOM - 0.15, MID_X, BOTTOM),
    (MID_X, BOTTOM, LEFT + 0.05, BOTTOM - 0.15),
])
GLYPHS["4"] = G(1.0, [
    (RIGHT - 0.2, TOP, RIGHT - 0.2, BOTTOM),
    (LEFT, MID_Y, RIGHT - 0.2, MID_Y),
    (LEFT, MID_Y, RIGHT - 0.5, TOP),
])
GLYPHS["5"] = G(1.0, [
    (RIGHT, TOP, LEFT, TOP),
    (LEFT, TOP, LEFT, MID_Y),
    (LEFT, MID_Y, RIGHT - 0.05, MID_Y),
    (RIGHT - 0.05, MID_Y, RIGHT, BOTTOM - 0.15),
    (RIGHT, BOTTOM - 0.15, MID_X, BOTTOM),
    (MID_X, BOTTOM, LEFT + 0.1, BOTTOM - 0.15),
])
GLYPHS["6"] = G(1.0, [
    (RIGHT - 0.05, TOP + 0.15, MID_X, TOP),
    (MID_X, TOP, LEFT + 0.1, TOP + 0.2),
    (LEFT + 0.1, TOP + 0.2, LEFT, MID_Y + 0.05),
    (LEFT, MID_Y + 0.05, LEFT + 0.15, BOTTOM),
    (LEFT + 0.15, BOTTOM, MID_X, BOTTOM),
    (MID_X, BOTTOM, RIGHT - 0.05, BOTTOM - 0.15),
    (RIGHT - 0.05, BOTTOM - 0.15, RIGHT - 0.1, MID_Y),
    (RIGHT - 0.1, MID_Y, LEFT + 0.1, MID_Y),
])
GLYPHS["7"] = G(1.0, [
    (LEFT, TOP, RIGHT, TOP),
    (RIGHT, TOP, LEFT + 0.2, BOTTOM),
])
GLYPHS["8"] = G(1.0, [
    (MID_X, MID_Y, LEFT + 0.1, TOP + 0.2),
    (LEFT + 0.1, TOP + 0.2, MID_X, TOP),
    (MID_X, TOP, RIGHT - 0.1, TOP + 0.2),
    (RIGHT - 0.1, TOP + 0.2, MID_X, MID_Y),
    (MID_X, MID_Y, LEFT + 0.15, BOTTOM - 0.2),
    (LEFT + 0.15, BOTTOM - 0.2, MID_X, BOTTOM),
    (MID_X, BOTTOM, RIGHT - 0.15, BOTTOM - 0.2),
    (RIGHT - 0.15, BOTTOM - 0.2, MID_X, MID_Y),
])
GLYPHS["9"] = G(1.0, [
    (LEFT + 0.05, BOTTOM - 0.15, MID_X, BOTTOM),
    (MID_X, BOTTOM, RIGHT - 0.1, BOTTOM - 0.2),
    (RIGHT - 0.1, BOTTOM - 0.2, RIGHT, MID_Y - 0.05),
    (RIGHT, MID_Y - 0.05, RIGHT - 0.15, TOP),
    (RIGHT - 0.15, TOP, MID_X, TOP),
    (MID_X, TOP, LEFT + 0.05, TOP + 0.15),
    (LEFT + 0.05, TOP + 0.15, LEFT + 0.1, MID_Y),
    (LEFT + 0.1, MID_Y, RIGHT - 0.1, MID_Y),
])


# --------------------------
# Stroke rendering (supersampled, anti-aliased)
# --------------------------

def draw_disk(mask, w, h, cx, cy, r):
    """Draw a filled disk (antialiased via supersampling done later)."""
    x0 = int(math.floor(cx - r))
    x1 = int(math.ceil (cx + r))
    y0 = int(math.floor(cy - r))
    y1 = int(math.ceil (cy + r))
    r2 = r * r
    for y in range(y0, y1 + 1):
        if y < 0 or y >= h:
            continue
        dy = y - cy
        dx_max2 = r2 - dy * dy
        if dx_max2 < 0:
            continue
        dx_max = math.sqrt(dx_max2)
        x_start = int(math.floor(cx - dx_max))
        x_end   = int(math.ceil (cx + dx_max))
        base = y * w
        for x in range(x_start, x_end + 1):
            if 0 <= x < w:
                mask[base + x] = 1.0  # binary coverage; AA comes from downsample


def draw_thick_segment(mask, w, h, x1, y1, x2, y2, radius):
    """Draw a thick line segment by splatting overlapping disks along the path."""
    seg_len = math.hypot(x2 - x1, y2 - y1)
    if seg_len == 0:
        draw_disk(mask, w, h, x1, y1, radius)
        return
    # step at about radius/2 for solid coverage
    step = max(1.0, radius * 0.5)
    n = int(seg_len / step) + 1
    for i in range(n + 1):
        t = i / n
        cx = lerp(x1, x2, t)
        cy = lerp(y1, y2, t)
        draw_disk(mask, w, h, cx, cy, radius)


def render_glyphs_to_mask(letters, size, stroke_px=22, spacing=0.12, ss=4):
    """
    Render the given letters (string with A-Z 0-9 and spaces) to a hi-res grayscale mask (0..1),
    using supersampling for antialiasing.
    """
    reduction_factor_for_second_letter=0.6
    # Supersampled canvas
    W = size * ss
    H = size * ss
    mask = [0.0] * (W * H)

    # Layout: normalize glyph height to 1.0 box; scale to fit into vertical bounds
    # Leave uniform paddings
    pad = 0.12  # normalized padding around
    box_h = 1.0 - 2 * pad
    # Compute total advance width
    advances = []
    total_w = 0.0
    for ch in letters:
        if ch == " ":
            adv = 0.35  # space width
        else:
            g = GLYPHS.get(ch)
            if not g:
                continue
            adv = g["w"]
        advances.append((ch, adv))
        total_w += adv
        total_w += spacing if ch != " " else spacing * 0.6
    if advances:
        total_w -= spacing  # no trailing spacing

    # Scale so that glyphs fit horizontally with padding
    scale = (1.0 - 2 * pad) / max(1e-6, total_w)
    # Convert normalized coords to pixels
    def NX(x): return (pad + x) * scale * size * ss
    def NY(y): return (pad + y) * box_h * size * ss

    # Baseline and centering vertically
    # Our glyphs use [0..1] y; map TOP~pad to BOTTOM~(1-pad)
    y_offset = (H - box_h * size * ss) * 0.5

    # Stroke radius in hi-res pixels
    radius = stroke_px * ss / 2.0

    # Draw each glyph
    x_cursor = (W - total_w * scale * size * ss) * 0.5
    for ch, adv in advances:
        if ch == " ":
            x_cursor += adv * scale * size * ss + spacing * 0.6 * scale * size * ss
            #reset radius after a space
            radius = stroke_px * ss / 2.0
            continue
        g = GLYPHS.get(ch)
        if not g:
            x_cursor += spacing * scale * size * ss
            continue
        for (x1, y1, x2, y2) in g["strokes"]:
            X1 = x_cursor + NX(x1) - NX(0)
            X2 = x_cursor + NX(x2) - NX(0)
            Y1 = y_offset + NY(y1)
            Y2 = y_offset + NY(y2)
            draw_thick_segment(mask, W, H, X1, Y1, X2, Y2, radius)
        x_cursor += g["w"] * scale * size * ss + spacing * scale * size * ss
        #reduce radius for the second letter
        radius = (stroke_px*reduction_factor_for_second_letter) * ss / 2.0
    return mask, W, H


# --------------------------
# Text handling & main API
# --------------------------

def extract_logo_letters(text: str) -> str:
    words = [w for w in text.strip().split() if w]
    if not words:
        return "AA"  # fallback
    if len(words) >= 2:
        s = words[0][:2] + " " + words[1][:2]
    else:
        s = words[0][:2]
    return s.upper()


def crossos_make_icon_artsy(text: str,
              outfile: str,
              size: int = 256,
              fg=(0, 0, 0, 255),
              bg=(255, 255, 255, 255),
              stroke_px: int = 22,
              supersample: int = 10):
    """
    Create a 256x256 logo with stroke-rendered letters (A-Z, 0-9).
    - text: input string; we use first 2 letters of first 2 words (or first 2 of one word)
    - outfile: path ending in .png or .ico
    - size: output size (default 256)
    - fg, bg: RGBA tuples (0..255)
    - stroke_px: stroke thickness in output pixels (approximate)
    - supersample: supersampling factor for antialiasing (4 is good)
    """
    letters = extract_logo_letters(text)
    # Render supersampled mask
    mask_hi, W, H = render_glyphs_to_mask(letters, size=size, stroke_px=stroke_px, spacing=0.19, ss=supersample)
    # Downsample to final mask
    mask, w, h = downsample_mask(mask_hi, W, H, supersample)
    # Compose RGBA
    out = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            a = clamp(mask[y * w + x], 0.0, 1.0)
            r, g, b, a_out = compose_rgba_over(bg, fg, a)
            i = (y * w + x) * 4
            out[i + 0] = r
            out[i + 1] = g
            out[i + 2] = b
            out[i + 3] = a_out
    # Encode PNG
    png_bytes = encode_png(bytes(out), w, h)
    # Save as PNG or ICO
    write_png_or_ico(png_bytes, Path(outfile), size)

#crossos_make_icon_artsy(text="Tester Comfy Install", outfile="mylogo.ico")
















#####END ENGINE2 Blocky and pixely+++++++++++++

















































































































































# -*- coding: utf-8 -*-

"""
 
A single-file, cross-platform (Windows/Linux/macOS) installer/repairer for Python repositories
driven by a .txt instruction file.

- No external packages required (stdlib only).
- Modes:
  * install
  * repair (with --embedded for embedded/portable distributions)

Implements commands (case-insensitive) from the .txt, in order:
  - PYTHON <version>
  - RFILTER <pkg1> <pkg2> ...
  - REQFILE <path-or-URL>
  - GITCLONE|GITCLON <url> <path_suffix>
  - REQSCAN <path_suffix>
  - STARTER <label or "label with spaces"> <args...>

See the user’s spec for full semantics.
"""

import argparse
import os
import sys
import subprocess
import shutil
import tempfile
import urllib.request
import platform
import re
from pathlib import Path



# ========= Global defaults & flags =========
APP_NAME="Pynst"

#main modes of operation

STARTOPTION_MODE_SENSOINSTALL="sensoinstall"
STARTOPTION_MODE_INSTALL="install"
STARTOPTION_MODE_REBUILD="rebuild"
STARTOPTION_INPUTFILE="inputfile"
STARTOPTION_INPUTDIR="targetdirectory"
STARTOPTION_EMBEDDED="embedded"
STARTOPTION_NODESKTOP="nodesktop"
STARTOPTION_DRYRUN="dryrun"
STARTOPTION_VERBOSE="verbose"
STARTOPTION_BACKUP="backup"
STARTOPTION_NOBLOB="noblob"
STARTOPTION_VENVNAME="venvname"
STARTOPTION_FORCELATESTPULL="forcegitlatest"
STARTOPTION_SHOWOP="debugopt"

    
DEFAULT_PYTHON_VERSION = "3.13"
COMFYUI_PYTHON_EMBEDDED_FOLDER_NAME="python_embedded"
COMFYUI_PYTHON_EMBEDDED_FOLDER_NAME_FALLBACK="python_embeded"

DEFAULT_VENV_NAME_MAC=".env_mac"
DEFAULT_VENV_NAME_WINDOWS=".env_win"
DEFAULT_VENV_NAME_LINUX=".env_lin"
DEFAULT_REQUIREMENTS_FILENAME="requirements.txt"

STARTER_NO_DESKTOP = False
DRYRUN = False
VERBOSE = False
BACKUP = False
GLOBAL_OPTION_FORCE_REINSTALL =False 


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

COLOR_TASK = GREEN     
COLOR_SUBTASK = BLUE
COLOR_SUBSUBTASK = DARKCYAN
COLOR_ERROR = RED
COLOR_END = "\033[0m"


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


TOKEN_PRINT_PREFIX="Info: "

# ========= Utility logging =========
def log_task(msg: str):
    print(f"{COLOR_TASK}{msg}{COLOR_END}")

def log_subsubtask(msg: str):
    print(f"{COLOR_SUBSUBTASK}{msg}{COLOR_END}")
def log_subtask(msg: str):
    print(f"{COLOR_SUBTASK}{msg}{COLOR_END}")


def log_error(msg: str):
    print(f"{COLOR_ERROR}{msg}{COLOR_END}")

def abort(msg: str, code: int = 1):
    log_error(msg)
    sys.exit(code)



import io
def run_cmd(cmd, cwd=None, task_description=None) -> int:
    """
    Run a command with optional output suppression.
    Returns the process return code.
    """
    if task_description is not None:
        log_subsubtask(f"Executing task: {task_description}")
        
    if DRYRUN:
        log_subsubtask(f"[DRYRUN] Would run: {' '.join(map(str, cmd))} (cwd={cwd or os.getcwd()})")
        return 0
    
    if VERBOSE:
        return subprocess.call(cmd, cwd=cwd )
    else:
# Silent run with forced ASCII environment to handle Unicode issues
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "ascii:replace"  # Force ASCII, replace invalid chars
        env["LANG"] = "C"  # Set locale to C to avoid Unicode issues
        try:
            p = subprocess.run(
                cmd,
                cwd=cwd,
                stdout=subprocess.DEVNULL,  # Discard output
                stderr=subprocess.DEVNULL,  # Discard errors
                env=env  # Use modified environment
            )
            return p.returncode
        except Exception:
            # Fallback to basic run if environment tweak fails
            p = subprocess.run(
                cmd,
                cwd=cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return p.returncode

def is_valid_version_format(version: str) -> bool:
    """
    Validates if a string is formatted like a software version number.
    Examples: '3', '3.22', '3.22.22'
    
    Args:
        version (str): The string to validate
        
    Returns:
        bool: True if the string is a valid version number format, False otherwise
    """
    # Check if string is empty or contains non-numeric/non-dot characters
    if not version or not all(c.isdigit() or c == '.' for c in version):
        return False
    
    # Split by dots
    parts = version.split('.')
    
    # Check if there's at least one part and no empty parts
    if not parts or '' in parts:
        return False
        
    # Check if all parts are numeric
    try:
        return all(part.isdigit() for part in parts)
    except ValueError:
        return False


def ensure_utf8(path: Path):
    """
    Ensure a text file is UTF-8 encoded. If not, re-save with replacement characters.
    """
    raw = path.read_bytes()
    try:
        raw.decode("utf-8")
        return
    except UnicodeDecodeError:
        text = raw.decode(errors="replace")
        path.write_text(text, encoding="utf-8")

def which(exe: str) -> str | None:
    return shutil.which(exe)

def require_tool(exe: str, how_to: str):
    """
    Confirm a tool exists in PATH; otherwise abort with hint.
    """
    if which(exe) is None:
        abort(f"Required tool '{exe}' not found in PATH. {how_to}")



import sys

def validate_file(path, allowed_keywords, limited_keywords):
    """
    Validate a text file against keyword rules.
    
    Args:
        path (str): Path to the text file.
        allowed_keywords (set[str]): All keywords that are valid as line starters.
        limited_keywords (dict[str, int]): Keywords with usage limits.
                                           Example: {"ONCE_ONLY": 1, "TEN_TIMES": 10}
    """
    counts = {k: 0 for k in limited_keywords}

    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue  # skip empty lines if allowed (remove this if not allowed)
            
            first_word = stripped.split()[0]

            # Rule 1: line must start with allowed keyword
            if first_word not in allowed_keywords:
                log_subsubtask(f"FilePrecheck: on Inputfile Error at line {lineno}: '{first_word}' is not an allowed keyword (is not in allowed list for this version).")
                sys.exit(1)

            # Rule 2: count restricted keywords
            if first_word in limited_keywords:
                counts[first_word] += 1
                if counts[first_word] > limited_keywords[first_word]:
                    log_subsubtask(f"FilePrecheck:  on Inputfile: Error at line {lineno}: '{first_word}' "
                          f"exceeds allowed limit ({limited_keywords[first_word]}).")
                    sys.exit(1)


# ========= Python / venv helpers =========
def python_cmd_for_version(version: str) -> list[str]:
    """
    Construct the command to invoke the specified Python version (system Python, not venv).
    Windows: py -3.12
    Linux/macOS: python3.12
    """
    system = platform.system().lower()
    if system == "windows":
        return ["py", f"-{version}"]
    else:
        return [f"python{version if version.startswith('3.') else '3.' + version.split('.')[-1]}"]


import subprocess
import re
import os

def check_python_version(exec_path: str, desired_version: str) -> bool:
    """
    Check if the Python executable at exec_path matches the desired version.
    
    Args:
        exec_path (str): Path to the Python executable
        desired_version (str): Desired version (e.g., '3', '3.12', '3.12.1')
    
    Returns:
        bool: True if version matches, False otherwise
    
    Raises:
        FileNotFoundError: If the executable path doesn't exist
        PermissionError: If the executable cannot be run
        RuntimeError: If version cannot be determined
    """
    # Validate executable path
    if not os.path.isfile(exec_path):
        abort(f"Python executable not found at: {exec_path}")
    
    # Ensure executable is accessible
    if not os.access(exec_path, os.X_OK):
        abort(f"No executable permissions for: {exec_path}")
    
    try:
        # Run python --version command
        result = subprocess.run(
            [exec_path, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract version from output (stdout or stderr)
        output = result.stdout or result.stderr
        version_match = re.search(r"Python (\d+(?:\.\d+)*)", output)
        
        if not version_match:
            abort("Could not determine Python version")
        
        actual_version = version_match.group(1)
        
        # Escape desired_version for regex and replace dots with literal dots
        desired_version_escaped = re.escape(desired_version)
        
        # Create regex pattern to match desired version
        pattern = f"^{desired_version_escaped}(?:\\.\\d+)*$"
        
        # Check if actual version matches the desired version pattern
        result_matches=bool(re.match(pattern, actual_version))
        if result_matches==False:
            log_subsubtask(f"Version does not match: need '{desired_version}' but got '{actual_version}'")
        return result_matches
    
    except subprocess.CalledProcessError:
        abort(f"Failed to execute {exec_path} --version")
    except Exception as e:
        abort(f"Error checking Python version: {str(e)}")
    
    

def check_system_python_version_available(version: str):
    cmd = python_cmd_for_version(version) + ["--version"]
    try:
        rc = run_cmd(cmd=cmd,task_description=f"checking availability of system python version: {version}")
        if rc != 0:
                abort(f"Python {version} not available on this system. Please install it and try again.")
    except Exception as e:
        abort(f"Python {version} not available on this system. Please install it and try again.")

def ensure_venv_exists(venv_path: Path, venv_python_exec: str, required_python_version: str=None, do_backup: bool=False, operation_mode=None, embedded_mode=False, path_for_requirementstxt=None, current_filters: list[str]=None ):
    """
    ensure a venv exists:
    if venv exists based on OP_mode: 
        -if backup mode
            -do backup (embedded copy, non embedded rename)
        -if sensoinstall:
            -do nothing
        elif install:
            -upgrade pip
        elif rebuild:
            -embedded 
                -empty venv
            -non embeded
                -delete and recreate
            -upgrade pip
    if venv does not exist:
        -if embedded:
            -error
        else:
            -create one
"""

    #ENSURE A VENV EXISTS
    #PRE-Existing VENV
    if venv_path.exists():
        log_subsubtask("Found a venv at the location")
        

        #precheck
        if operation_mode==STARTOPTION_MODE_SENSOINSTALL or operation_mode == STARTOPTION_MODE_INSTALL:
            if os.path.exists(venv_python_exec)==False:
                abort(f"Python executable does not exist or corrupted. Maybe run in rebuild mode to fix: {venv_python_exec}")
        
        
        #First: HANDLE BACKUP
        if do_backup:
            bak = unique_bak_name(venv_path)
            if DRYRUN:
                log_subsubtask(f"[DRYRUN] Would backup existing venv '{venv_path}' -> '{bak}'")
            else:
                log_subsubtask(f"Backing up existing venv to: {bak}")
                if embedded_mode:
                    shutil.copytree(venv_path, bak)
                else:
                    venv_path.rename(bak)

        #now handle existing venv
        if operation_mode==STARTOPTION_MODE_SENSOINSTALL:
            log_subsubtask("Will use existing venv but will not upgrade it due to extra safe settings")
            return
        if operation_mode==STARTOPTION_MODE_INSTALL:
            log_subsubtask("Will use existing venv and upgrade it to latest pip")
            pip_upgrade_pip(venv_python_exec)
            return
        if operation_mode==STARTOPTION_MODE_REBUILD:
            if embedded_mode:
                log_subsubtask("Will empty embedded venv to rebuild it")
                # empty venv
                uninstall_all_packages(venv_python_exec)
                # Verify empty
                if not is_venv_empty(venv_python_exec):
                    abort("Embedded environment is not empty after uninstalling all packages. Aborting.")
                if path_for_requirementstxt is not None:
                    pip_install_requirements_file(python_exec=venv_python_exec, req_file=path_for_requirementstxt, current_filters=current_filters, fail_label=str(path_for_requirementstxt))
                return
            else:
                #delete venv
                if DRYRUN:
                    log_subsubtask(f"[DRYRUN] Would delete existing venv: {venv_path}")
                else:
                    log_subsubtask(f"Deleting existing venv to rebuild it")
                    shutil.rmtree(venv_path, ignore_errors=True)
                
    #at this point there is no venv.
    if required_python_version is None:
        log_subsubtask(f"setting Python version to {APP_NAME}-default: {required_python_version}")
        required_python_version = DEFAULT_PYTHON_VERSION
        check_system_python_version_available(required_python_version)

    # Create new venv
    cmd = python_cmd_for_version(required_python_version) + ["-m", "venv", str(venv_path)]
    rc = run_cmd(cmd=cmd, task_description=f"creating new venv: {venv_path}")
    if rc != 0:
        abort(f"Failed to create virtual environment at {venv_path}")
    
    #upgrade pip
    pip_upgrade_pip(venv_python_exec)

    #install requirements
    if path_for_requirementstxt is not None:
        pip_install_requirements_file(python_exec=venv_python_exec, req_file=path_for_requirementstxt, current_filters=current_filters, fail_label=str(path_for_requirementstxt))

    log_subsubtask(f"Created virtual environment: {venv_path}")




def get_theoretic_venv_python_executable(venv_path: Path) -> str:
    system = platform.system().lower()
    if system == "windows":
        return str(venv_path / "Scripts" / "python.exe")
    else:
        return str(venv_path / "bin" / "python")

def is_venv_empty(python_exec: str) -> bool:
    """
    True if 'pip freeze' returns zero packages.
    """
    if DRYRUN:
        # In dry-run, pretend it's empty to let flow proceed without side-effects.
        log_subsubtask("[DRYRUN] Assuming environment is empty for checks.")
        return True
    try:
        out = subprocess.check_output([python_exec, "-m", "pip", "freeze"], stderr=subprocess.STDOUT)
        lines = [l.strip() for l in out.decode("utf-8", errors="replace").splitlines() if l.strip()]
        return len(lines) == 0
    except Exception:
        return False

def uninstall_all_packages(python_exec: str):
    """
    Uninstall all installed packages from the environment represented by python_exec.
    """
    log_subtask("Uninstalling all packages from current environment (pip freeze -> pip uninstall -y) ...")
    if DRYRUN:
        log_subsubtask("[DRYRUN] Would run 'pip freeze' and uninstall all packages.")
        return
    try:
        out = subprocess.check_output([python_exec, "-m", "pip", "freeze"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        abort("Failed to query installed packages via 'pip freeze'.")

    pkgs = [l.strip() for l in out.decode("utf-8", errors="replace").splitlines() if l.strip()]
    if not pkgs:
        log_subsubtask("No packages installed.")
        return
    # Write to temp file to avoid command-line length limits
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as tf:
        for p in pkgs:
            tf.write(p + "\n")
        temp_list = tf.name
    try:
        rc = run_cmd(cmd=[python_exec, "-m", "pip", "uninstall", "-y", "-r", temp_list], task_description="uninstalling packages")
        if rc != 0:
            abort("Failed to uninstall some packages.")
    finally:
        try:
            os.remove(temp_list)
        except OSError:
            pass

# ========= Requirements filtering & installation =========
def compile_rfilter_pattern(filters: list[str]) -> re.Pattern | None:
    """
    Build a case-insensitive regex that matches lines starting with any filtered package
    name followed by whitespace or a NON alphabetic symbol (not A-Z, a-z, '-' or '_').
    We anchor at start (ignoring leading whitespace).
    Example matches: 'torch==2.1.0', 'torch ', 'torch[extra]', 'torch\t', 'torch; python_version<"3.12"'
    Does NOT match 'torchaudio' when 'torch' is filtered.
    """
    if not filters:
        return None
    # Escape and join names; allow optional leading whitespace before name.
    name_alt = "|".join(re.escape(x) for x in filters)
    # Start-of-line (after optional whitespace), then one of names, then lookahead for
    # whitespace OR a char that is NOT in [A-Za-z_-]
    pat = rf"^\s*(?:{name_alt})(?=\s|[^A-Za-z_-])"
    return re.compile(pat, re.IGNORECASE)

def apply_rfilter_to_file(src_path: Path, filters: list[str]) -> Path:
    """
    If filters present, create a filtered temp requirements file and return its path.
    Otherwise return src_path.
    """
    if not filters:
        return src_path
    pat = compile_rfilter_pattern(filters)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    os.close(tmp_fd)
    tmp = Path(tmp_path)
    src_path = Path(src_path)
    with src_path.open("r", encoding="utf-8", errors="replace") as src, tmp.open("w", encoding="utf-8") as dst:
        for line in src:
            # Preserve comments and blank lines as-is unless they match (they won't)
            if pat and pat.search(line):
                continue
            dst.write(line)
    return tmp

def download_to_temp(url: str) -> Path:
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    os.close(tmp_fd)
    p = Path(tmp_path)
    log_subsubtask(f"Downloading to tempfile: {p}")
    if DRYRUN:
        log_subsubtask("[DRYRUN] Skipping actual download.")
        # Create an empty file to keep flow consistent
        p.write_text("", encoding="utf-8")
        return p
    urllib.request.urlretrieve(url, p)
    return p



def pip_upgrade_pip(python_exec: str):
    """
    Install requirements from a (possibly remote) file with RFILTER applied.
    """
    #not effective
    #run_cmd(cmd=[python_exec, "-m", "pip", "ensurepip", "--upgrade"],task_description="upgrading pip")
    #python.exe -m pip install --upgrade pip
    run_cmd(cmd=[python_exec, "-m", "pip", "install",   "--upgrade", "pip"],task_description="upgrading pip")

def pip_install_requirements_file(python_exec: str, req_file: Path, current_filters: list[str], fail_label: str, force_reinstall=False):
    """
    Install requirements from a (possibly remote) file with RFILTER applied.
    """
   
    if not os.path.exists(req_file):
        abort(f"Requirements file not found: {req_file}")
    filtered = apply_rfilter_to_file(req_file, current_filters)
    
    message_append=""
    if current_filters:
       message_append=f"(package filter applied and installing as temp file)" 
    #pip install --upgrade --force-reinstall --no-warn-script-location -r requirements.txt
    cmd=[python_exec, "-m", "pip", "install", "--upgrade"]
    
    if force_reinstall:
        cmd.extend([ "--force-reinstall"])
    cmd.extend(["--no-warn-script-location", "-r", str(filtered)])
    
    rc = run_cmd(cmd, task_description=f"Installing requirements from file{message_append}: {req_file}" )
    if rc != 0:
        abort(f"Failed to install requirements from: {fail_label}")

def pip_run_pip_install(python_exec: str, pip_command: list[str], fail_label: str="Pip command failed"):
    """
    run a command through pip install.
    """       
    if DRYRUN:
        log_subsubtask(f"[DRYRUN] Would run: pip install {" ".join(pip_command)}")
    else:
        log_subsubtask(f"Running pip command: pip install {" ".join(pip_command)}")
        rc = run_cmd(cmd=[python_exec, "-m", "pip", "install" ] + pip_command)
        if rc != 0:
            abort(f"Failed to run pip command: {fail_label}")


def pip_run_command(python_exec: str, pip_command: list[str], fail_label: str="Pip command failed"):
    """
    run a command through pip.
    """       
    rc = run_cmd(cmd=[python_exec, "-m", "pip" ]+pip_command,task_description=f"Running command: pip {" ".join(pip_command)}")
    if rc != 0:
        abort(f"Failed to run pip command: {fail_label}")



# ========= Git helpers =========

def extract_project_name(url):
    # Remove trailing '/' if any
    url = url.rstrip('/')    
    # Remove '.git' if present at the end
    if url.endswith('.git'):
        url = url[:-4]    
    # Split by '/' and take the last part
    project_name = url.split('/')[-1]
    return project_name

import os, shutil, stat
from pathlib import Path

def _force_remove_readonly(func, path, excinfo):
    """Clear readonly flag and reattempt removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_dir_force(target: Path):
    if DRYRUN:
        log_subsubtask(f"[DRYRUN] Would remove existing directory before clone: {target}")
    else:
        if target.exists():
            if target.is_file() or target.is_symlink():
                target.unlink()
            else:
                shutil.rmtree(target, onerror=_force_remove_readonly)


def do_git_clone(url: str, target: Path, operating_mode=None, force_gitpull_mode=False):
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if GLOBAL_OPTION_FORCE_REINSTALL:
            remove_dir_force(target)
        else:
            log_subsubtask(f"Repository already exists. Not cloning...")
            if operating_mode==STARTOPTION_MODE_INSTALL or operating_mode==STARTOPTION_MODE_REBUILD:
                log_subsubtask("Repository: updating code")
                do_git_pull(repo_path=target, operating_mode=operating_mode, force_gitpull_mode=force_gitpull_mode)
            return

    rc = run_cmd(cmd=["git", "clone", url, str(target)],cwd=str(target.parent),task_description="Cloning repo...")
    if rc != 0:
        abort(f"Git clone failed for {url}")
    log_subsubtask(f"Cloned to: {target}")



def do_git_pull( repo_path: Path, operating_mode=None, force_gitpull_mode=False):
    """
    Perform a git pull on a directory
    """     
    if not repo_path.exists():
        abort(f"Directory to perform git pull not found: {repo_path}")

    if operating_mode==STARTOPTION_MODE_REBUILD:
        try:
            rc = run_cmd(cmd=["git", "restore", "." ],cwd=repo_path, task_description="Resetting repository due to rebuild mode")
            if rc != 0:
                log_subsubtask(f"Warning: 'Git restore .' failed. Repo could be broken or conflicting changes (force remove might be needed): {repo_path}. Ignore this if no further ERROR appears!")
        except Exception as e:
                abort(f"Warning(exception): 'Git restore .' failed. Repo could be broken or conflicting changes (try adding argument '--{STARTOPTION_FORCELATESTPULL}'): {repo_path}.")
    rc = run_cmd(cmd=["git", "pull"], cwd=repo_path, task_description=f"Updating git repository: {repo_path}")
    if rc != 0:
        if force_gitpull_mode==True:
            if operating_mode==STARTOPTION_MODE_INSTALL or operating_mode==STARTOPTION_MODE_REBUILD:
                log_subtask("git pull failed, trying force-pull")
                if do_force_git_pull_on_repository(repo_path):
                    log_subsubtask("Repository was succesfully force-updated!")
                    return
            if operating_mode==STARTOPTION_MODE_SENSOINSTALL:
                log_subtask("Forcemode was cancelled by extra safe install mode")            
        abort(f"Failed to update repository (broken or not a repo) (try adding argument '--{STARTOPTION_FORCELATESTPULL}'): {str(repo_path)}")
        

def do_git_command(target: Path, params):

    rc = run_cmd(cmd=["git"]+ params,cwd=str(target),task_description="running git command...")
    if rc != 0:
        abort(f"Git command failed for {target}")
 

import os
import subprocess
from pathlib import Path

def do_force_git_pull_on_repository(directory: str) -> bool:
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
        abort(f"Force-pull: Fatal Error: {directory} is not a valid directory")
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
        log_subsubtask("Force-pull: Git directory detected. attempting to move code version to 'nightly'")
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
                log_subsubtask(f"Force-pull: Switching from detached HEAD to {target_branch}")
            else:
                log_subsubtask(f"Force-pull: Switching from {current_branch} to {target_branch}")
            
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
                abort(f"Force-pull:Fatal error: Repo might be broken. Error switching to {target_branch}: {result.stderr}")
                return False

        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            log_subsubtask(f"Force-pull: Uncommitted changes detected, stashing them")
            result = subprocess.run(
                ["git", "stash", "push", "-m", "Auto-stash for git pull"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                abort(f"Force-pull:Fatal error: Error stashing changes: {result.stderr}")
                return False

        # Ensure branch is tracking remote
        result = subprocess.run(
            ["git", "branch", "--set-upstream-to", f"origin/{target_branch}", target_branch],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            abort(f"Force-pull:Fatal error: Error setting upstream to origin/{target_branch}: {result.stderr}")
            return False

        # Perform git pull
        log_subsubtask(f"Force-pull: Running git pull on {target_branch}")
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            abort(f"Force-pull:Fatal Error: Error during git pull: {result.stderr}")
            return False

        log_subsubtask(f"Force-pull: Successfully pulled latest changes on {target_branch}")
        return True

    except Exception as e:
        abort(f"Force-pull:Fatal error: Unexpected error: {str(e)}")
        return False
    finally:
        # Restore original working directory
        os.chdir(original_dir)




def task_print(text_tokens):
    text = " ".join([quote_arg(x) for x in text_tokens])
    print(f"{COLOR_SUBSUBTASK}{TOKEN_PRINT_PREFIX}{COLOR_END}{text}")
 
def task_pause():
    """
    Pause execution until the user presses Enter to continue
    or Ctrl+C to abort. Works on Windows, Linux, and macOS.
    """
    try:
        input("Press Enter to continue or Ctrl+C to abort... ")
    except KeyboardInterrupt:
        abort("\nAborted by user.")
        raise  # re-raise so caller can handle it if needed


# ========= Download helpers =========

import urllib.request

def get_file_size(url: str, verbose: bool = False):
    """
    Returns the file size from server as (size_in_bytes, human_readable_str).
    If Content-Length is missing, returns (None, None).
    """
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req) as response:
            length = response.getheader("Content-Length")

        if length is None:
            if verbose:
                log_subsubtask(f"Server did not provide Content-Length for {url}")
            return None, None

        size_bytes = int(length)
        size_str = human_readable_size(size_bytes)
        return size_bytes, size_str

    except Exception as e:
        if verbose:
            log_subsubtask(f"Error fetching file size for {url}: {e}")
        return None, None


def human_readable_size(num_bytes: int) -> str:
    """Convert bytes into human-readable string with appropriate unit."""
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0 or unit == "TB":
            return f"{num_bytes:.2f} {unit}" if unit != "bytes" else f"{num_bytes} {unit}"
        num_bytes /= 1024.0



import os
import urllib.request
import sys

def check_if_file_is_aready_downloaded(url: str, filepath: str, verbose=False) -> bool:
    """
    Check if the file at 'filepath' exists and is complete compared to the file size on the server.
    Returns True if the file exists and matches the server size, else False.
    """
    try:
        # Send a HEAD request
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req) as response:
            length = response.getheader("Content-Length")
        
        if length is None:
            # Can't determine size from server
            if verbose:
                log_subsubtask(f"file does not exist on server: {url}")
            return os.path.exists(filepath)
        
        expected_size = int(length)
        if os.path.exists(filepath):
            actual_size = os.path.getsize(filepath)
            if actual_size != expected_size:
                log_subsubtask(f"Size on server different than file size! Server Size: {expected_size}. actual size {actual_size}")
            return actual_size == expected_size
        else:
            return False
    except Exception as e:
        log_subsubtask(f"check_file error: {e}")
        return False

import sys
import urllib.request

def human_readable_size(num_bytes: int) -> str:
    """Convert bytes into human-readable string with appropriate unit."""
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0 or unit == "TB":
            return f"{num_bytes:.2f} {unit}" if unit != "bytes" else f"{num_bytes} {unit}"
        num_bytes /= 1024.0

def download_file_old(url: str, filepath: str, show_progress: bool = False):
    """
    Download the file from 'url' into 'filepath'.
    If show_progress is True, displays a progress bar with human-readable file size.
    """

    total_human = None  # will be set once we know total size

    def progress(block_num, block_size, total_size):
        nonlocal total_human
        if not show_progress:
            return
        if total_size > 0 and total_human is None:
            total_human = human_readable_size(total_size)

        downloaded = block_num * block_size
        percent = downloaded * 100 / total_size if total_size > 0 else 0
        percent = min(100, percent)
        bar_len = 50
        filled_len = int(bar_len * percent // 100)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        downloaded_human = human_readable_size(min(downloaded, total_size))
        sys.stdout.write(f"\r[{bar}] {percent:6.2f}% ({downloaded_human} / {total_human})      ")
        sys.stdout.flush()
        if downloaded >= total_size:
            print()  # newline after completion

    try:
        urllib.request.urlretrieve(url, filepath, reporthook=progress)
    except Exception as e:
        abort(f"download_file error: {e}")


def download_file(url: str, filepath: str, show_progress: bool = False):
    """
    Download the file from 'url' into 'filepath'.
    Decodes %20 etc. in the local filename, but leaves the URL untouched.
    If show_progress is True, displays a progress bar with human-readable file size.
    """
    total_human = None  # will be set once we know total size

    def progress(block_num, block_size, total_size):
        nonlocal total_human
        if not show_progress:
            return
        if total_size > 0 and total_human is None:
            total_human = human_readable_size(total_size)

        downloaded = block_num * block_size
        percent = downloaded * 100 / total_size if total_size > 0 else 0
        percent = min(100, percent)
        bar_len = 50
        filled_len = int(bar_len * percent // 100)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        downloaded_human = human_readable_size(min(downloaded, total_size))
        sys.stdout.write(f"\r[{bar}] {percent:6.2f}% ({downloaded_human} / {total_human})")
        sys.stdout.flush()
        if downloaded >= total_size:
            print()  # newline after completion

    try:
        # decode the filename part only
        dirpath, fname = os.path.split(filepath)
        fname = urllib.parse.unquote(fname)
        filepath_decoded = os.path.join(dirpath, fname)

        urllib.request.urlretrieve(url, filepath_decoded, reporthook=progress)
        return filepath_decoded
    except Exception as e:
        abort(f"download_file error: {e}")
        return None

#url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/wan2.2-i2v-rapid-aio-example.json"
#path = "d:/resources/"
#download_only_if_not_existent(url, path, verbose=False, show_progress=True)



from urllib.parse import urlparse
import os

def download_only_if_not_existent(url, directory_target_path, verbose=False, show_progress=True):
    # Ensure target directory exists
    os.makedirs(directory_target_path, exist_ok=True)

    # Extract filename from URL
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(directory_target_path, filename)

    if check_if_file_is_aready_downloaded(url, filepath, verbose=True):
        log_subsubtask(f"File already exists and is complete: {filepath}")
    else:
        download_file(url, filepath, show_progress=True)


 
# ========= Starter helpers =========
def crossos_make_starter_script(basedir: Path, venv_py: str, label: str, cmd_line: list[str], working_dir: str):
    """
    Create .bat/.sh starter scripts that launch the given command with the venv python.
    Resolve any relative path to absolute under basedir if it exists there.
    """
    if STARTER_NO_DESKTOP:
        log_subsubtask("STARTER creation skipped due to --nodesktop.")
        return

    system = platform.system().lower()
    script_name = f"{label}{'.bat' if system == 'windows' else '.sh'}"
    script_path = basedir / script_name

    if system == "windows":
        content = f"cd {working_dir}\r\n" + cmd_line + "\r\n"
    else:
        content = "#!/usr/bin/env bash\n" +f"cd {working_dir}\n" + cmd_line + "\n"

    if DRYRUN:
        log_subsubtask(f"[DRYRUN] Would create starter: {script_path}")
        return

    script_path.write_text(content, encoding="utf-8")
    if system != "windows":
        os.chmod(script_path, 0o755)
    log_subsubtask(f"Created starter shortcut: {script_path}")

def quote_arg(s: str) -> str:
    if platform.system().lower() == "windows":
        # Basic quoting for Windows cmd
        if " " in s or "\t" in s or '"' in s:
            return f'"{s.replace("\"", "\\\"")}"'
        return s
    else:
        # POSIX shell quoting
        if re.search(r"\s|'|\"", s):
            return "'" + s.replace("'", "'\"'\"'") + "'"
        return s

# ========= REQSCAN helpers =========
def scan_requirements_one_level(root: Path) -> list[Path]:
    """
    Find requirements.txt files exactly one level below root (i.e., in each direct subdir).
    Also include root/requirements.txt if present (useful).
    """
    results: list[Path] = []
    if root.is_dir():
        root_req = root / DEFAULT_REQUIREMENTS_FILENAME
        if root_req.is_file():
            results.append(root_req)
        for entry in root.iterdir():
            if entry.is_dir():
                p = entry / DEFAULT_REQUIREMENTS_FILENAME
                if p.is_file():
                    results.append(p)
    return results

# ========= Backup helpers =========
def unique_bak_name(p: Path) -> Path:
    base = Path(str(p) + ".bak")
    if not base.exists():
        return base
    i = 1
    while True:
        candidate = Path(str(p) + f".bak{i}")
        if not candidate.exists():
            return candidate
        i += 1
 

# ========= Parsing ifile =========
def parse_inputfile(inputfile_path: Path) -> list[tuple[str, list[str]]]:
    """
    Returns a list of (COMMAND_UPPER, [params...]) preserving order.
    Supports quoted labels/params with spaces.
    Ignores blank lines and lines starting with '#'.
    """
    ensure_utf8(inputfile_path)
    commands: list[tuple[str, list[str]]] = []
    token_re = re.compile(r'"[^"]*"|\S+')
    for raw in inputfile_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = token_re.findall(line)
        parts = [p[1:-1] if p.startswith('"') and p.endswith('"') else p for p in parts]
        cmd = parts[0].upper()
        params = parts[1:]
        commands.append((cmd, params))
    return commands




from pathlib import Path
import re

def get_dir_name(path: Path, root_fallback: str = "ROOT") -> str:
    """
    Returns the name of the directory for the given path.
    - If path is root (C: or /), returns root_fallback.
    - Ensures the name is alphanumeric, underscores, or dashes.
    Works on Windows, Linux, macOS.
    """
    path = path.resolve()

    # Handle root directories
    if path == path.anchor:
        return root_fallback

    name = path.name
    # Keep only alphanumeric, underscore, dash
    clean_name = re.sub(r'[^0-9A-Za-z_-]', '', name)

    # If nothing left after cleaning, use fallback
    return clean_name if clean_name else root_fallback


 

import os
def assert_file_exists(path: str):
    """
    Check if the given path exists (file or directory).
    If not, prints an error message.
    """
    if os.path.exists(path):
        return True
    else:
        abort(f"CONFIRM: Fatal Error: required path does not exist. Check failed. -> {path}")
        return False




def get_exec_variables(in_python_embedded_mode:bool=False,in_custom_venv_name:str=None, in_basedir:Path=None, required_venv_path:str=None ):
    #GET PYTHON TO BE USED DEPENDING ON PORTABLE OR NORMAL INSTALL
    if in_python_embedded_mode:
        log_subtask("Running in embedded mode. Will check if paths exist")
        current_venv_name=COMFYUI_PYTHON_EMBEDDED_FOLDER_NAME
        is_embedded_present=False
        if in_custom_venv_name is not None:
            current_venv_name = in_custom_venv_name
            embedded_dir = in_basedir / current_venv_name
            is_embedded_present = embedded_dir.is_dir()
        else:
            embedded_dir = in_basedir / current_venv_name
            is_embedded_present = embedded_dir.is_dir()
            if is_embedded_present == False:
                current_venv_name=COMFYUI_PYTHON_EMBEDDED_FOLDER_NAME_FALLBACK
                embedded_dir = in_basedir / current_venv_name
                is_embedded_present = embedded_dir.is_dir()

        if not is_embedded_present:
            abort(f"Venv not found! this is not a portable or manual installation. Missing: {embedded_dir}")
        else:
            log_subsubtask(f"embedded mode: found embedded dir at: {current_venv_name}")

        # Use embedded python executable (best effort cross-platform)
        python_exec = str(embedded_dir / ("python.exe" if platform.system().lower() == "windows" else "python"))
        log_subsubtask(f"attempting to search for {python_exec}")
        if not (Path(python_exec).exists()):
            # Fallback to 'python3' inside embedded_dir if present; else abort
            alt = str(embedded_dir / "python3")
            log_subsubtask(f"failed. attempting to search for {alt}")
            if not Path(alt).exists():
                abort(f"Directory exists but embedded Python executable not found in {embedded_dir}.")
            python_exec = alt

        # requirements installs will proceed using this python_exec
        venv_name=current_venv_name
        venv_python_exec = python_exec
        venv_path = embedded_dir
    else:
        #normal mode: non-embedded 
        # OS-specific venv name
        system = platform.system().lower()
        temp_venv_name = {
            "windows":  DEFAULT_VENV_NAME_WINDOWS,
            "linux":    DEFAULT_VENV_NAME_LINUX,
            "darwin":   DEFAULT_VENV_NAME_MAC
        }.get(system, ".env")
        if in_custom_venv_name is not None:
            temp_venv_name=in_custom_venv_name
        temp_venv_path = in_basedir / required_venv_path / temp_venv_name
        temp_venv_python_exec = get_theoretic_venv_python_executable(venv_path=temp_venv_path)
        
        venv_name= temp_venv_name
        venv_python_exec =  temp_venv_python_exec
        venv_path =  temp_venv_path
        
    return venv_name, venv_python_exec, venv_path

def check_that_file_exists_or_abort(file_path, file_description=None):
    
    file_desc="requested file"
    if file_description is not None:
        file_desc=file_description
    
    if DRYRUN:
        log_subsubtask(f"[DRYRUN] Would run: an existece check for {file_desc}: {file_path}")
    else:
        if os.path.exists(file_path)==False:
            abort(f"{file_desc}. Missing: {file_path}")


# ========= MAIN PROCESS =========
def process_input_script(in_commands: list[tuple[str, list[str]]], 
                         in_basedir: Path, 
                         in_python_embedded_mode: bool,  
                         noblob_mode=False,
                         force_gitpull_mode=False, 
                         in_custom_venv_name=None, 
                         in_operation_mode=STARTOPTION_MODE_REBUILD):
    # Ensure git available (not strictly required for repair flow, but keep parity)
    require_tool("git", "Please install Git and ensure it is on your PATH.")


    venv_path=None
    venv_python_exec=None
    venv_name=None


       
       
    # Build/rebuild a new venv with the requested/implicit Python version
    # Determine PYTHON version from commands (default 3.12 if absent)
    required_python_version = None

    #pre-check to see that all required versions in the input are present

    #pre-set the theoretical paths to a venv on the basedir. for embeddedd check existence
    venv_name, venv_python_exec, venv_path = get_exec_variables(in_python_embedded_mode=in_python_embedded_mode,in_custom_venv_name=in_custom_venv_name, in_basedir=in_basedir, required_venv_path="." )

    #TODO: DEcision if a venv is ensured made in any case. or novenv must be provided.
    #idea: per. default no venv is created but assumeed. on use of functions var are checked for None
    
    for cmd, params in in_commands:
        if cmd == CMD_PYTHON:
            required_python_version = params[0]
            log_task(f"Pre-Check:{cmd}: Pre-checking that version is valid and exists in system: {required_python_version}")
            if is_valid_version_format(required_python_version)==False:
                abort(f"Provided version is invalid or not properly formatted: {required_python_version}")
            log_task(f"{cmd}: This pynst requires a python version of: {required_python_version}. Will check for it.")
            if in_python_embedded_mode:
                log_subsubtask("Embedded mode: checking version of embedded python")     
                if check_python_version(venv_python_exec, required_python_version)==False:
                    abort(f"Embedded Python version does not match to needed version! You can solve it by creating a new venv in normal mode (need to have pyhon {required_python_version} installed on your system)") 
            else:
                log_subsubtask(f"checking if System has python{required_python_version} installed")
                check_system_python_version_available(required_python_version)
            break
        


     
    
    log_subtask(f"Processing Input file")
    # Now process commands permitted in REPAIR mode: PYTHON (already handled), RFILTER, REQFILE, STARTER, REQSCAN
    rfilters: list[str] = []
    # Collect REQSCAN paths (process them after REQFILEs or as they appear? Spec: executed in order they appear. We'll execute in order.)
    for cmd, params in in_commands:
        if cmd == CMD_PAUSE:
            task_pause()
        elif cmd == CMD_PRINT:
            task_print(params)
        elif cmd == CMD_PYTHON:
            required_python_version = params[0]
            log_task(f"{cmd}: setting version to be used as: {required_python_version}")
            continue
        elif cmd == CMD_SETVENV:
            required_venv_path = params[0]
            log_task(f"{cmd}: Ensuring existence of venv at path {required_venv_path}")

            venv_name, venv_python_exec, venv_path = get_exec_variables(in_python_embedded_mode=in_python_embedded_mode,in_custom_venv_name=in_custom_venv_name, in_basedir=in_basedir, required_venv_path=required_venv_path )
            
            path_to_req_file=None            
            req_temp_path= in_basedir / required_venv_path / DEFAULT_REQUIREMENTS_FILENAME
            if os.path.exists(req_temp_path):
                path_to_req_file= str(req_temp_path)
                log_subsubtask(f"{DEFAULT_REQUIREMENTS_FILENAME} found.")
                        
            ensure_venv_exists(venv_path=venv_path,venv_python_exec=venv_python_exec, required_python_version=required_python_version, do_backup=BACKUP,embedded_mode=in_python_embedded_mode, operation_mode=in_operation_mode,current_filters=rfilters,path_for_requirementstxt=path_to_req_file)

            check_that_file_exists_or_abort(venv_python_exec,"python executable")

        elif cmd == CMD_RFILTER:
            rfilters = params[:]
            if len(params) == 0:
                log_task(f"{cmd} Filters cleared! {rfilters}")
            else:
                log_task(f"{cmd} filters set: {', '.join(rfilters)}")

        elif cmd == CMD_PIPREQFILE:
            req_file_to_install = params[0]
            log_task(f"{cmd} installing: {req_file_to_install}")
            
            check_that_file_exists_or_abort(venv_python_exec,"python executable")
            
            
            if re.match(r"^https?://", req_file_to_install, re.I):
                req_file_to_install = download_to_temp(req_file_to_install)
            else:
                req_file_to_install=(in_basedir / req_file_to_install) if not Path(req_file_to_install).is_file() else Path(req_file_to_install)
            #TODO decide if force reinstall: for now yes
            pip_install_requirements_file(python_exec=venv_python_exec, req_file=req_file_to_install,current_filters= rfilters, fail_label=req_file_to_install,force_reinstall=True)

        elif cmd == CMD_REQSCAN:
            log_task(f"{cmd} searching for requirements in: {in_basedir / params[0]} (depth=1)")
            #TODO: maybe its more efficient to collect all reqscans and copy all reqfiles and concatenate them into once command as in: pip install -r fiole1.txt -r file2.txt -r file3.txt
            check_that_file_exists_or_abort(venv_python_exec,"python executable")
            # Search one level below basedir/suffix for requirements.txt (plus root-of-suffix)
            scan_root = (in_basedir / params[0]).resolve()
            if not scan_root.exists():
                log_subsubtask(f"{cmd} path does not exist, skipping: {scan_root}")
                continue
            reqs = scan_requirements_one_level(scan_root)
            if not reqs:
                log_subsubtask(f"No {DEFAULT_REQUIREMENTS_FILENAME} files found at the specified depth.")
            for req in reqs:
                path = Path(req)
                git_dir=path.parent
                log_subtask(f"{cmd} Repository found: {git_dir}")
                do_git_pull(git_dir, operating_mode=in_operation_mode, force_gitpull_mode=force_gitpull_mode)
                pip_install_requirements_file(python_exec=venv_python_exec, req_file=req, current_filters=rfilters, fail_label=str(req))
                
        elif  cmd == CMD_SHORTCUT_BASE_ICON or cmd == CMD_SHORTCUT_DESK_ICON or cmd == CMD_SHORTCUT_BASE_SCRIPT or cmd == CMD_SHORTCUT_DESK_SCRIPT :
            log_task(f"{cmd}: creating start shortcuts")
            if not params:
                abort(f"{cmd} requires parameters.")
            check_that_file_exists_or_abort(venv_python_exec,"python executable")
            #the first param is the shortcut name
            shortcut_name = params[0]
            #the params follow
            actual_params = params[1:]
            fill_gap=" "
            base_name=get_dir_name(in_basedir)
            shortcut_name= f"{shortcut_name}{fill_gap}{base_name}{fill_gap}{venv_name}"

            exec_working_dir, full_exec_line, main_executable_file, executable_as_list = get_executable_line_and_dir(in_basedir, venv_python_exec, actual_params) 
            
            if cmd == CMD_SHORTCUT_BASE_SCRIPT:
                crossos_make_starter_script(in_basedir, venv_python_exec, shortcut_name, full_exec_line, working_dir=exec_working_dir)
            elif cmd == CMD_SHORTCUT_BASE_ICON:
                if DRYRUN:
                    log_subsubtask(f"DRY_RUN: would create a homedir shortcut file: '{shortcut_name}' venv: '{venv_path}', basedir: '{in_basedir}'. Exec line: '{full_exec_line}'")
                else:
                    crossos_make_shortcut(app_name=shortcut_name, exec_line=full_exec_line, installpath=in_basedir,env_path=venv_path, onDesktop=False, working_dir=exec_working_dir)
            elif cmd == CMD_SHORTCUT_DESK_ICON:
                if DRYRUN:
                    log_subsubtask(f"DRY_RUN: would create a Desktop shortcut file: '{shortcut_name}' venv: '{venv_path}', basedir: '{in_basedir}'. Exec line: '{full_exec_line}'")
                else:
                    crossos_make_shortcut(app_name=shortcut_name, exec_line=full_exec_line, installpath=in_basedir,env_path=venv_path, onDesktop=True, working_dir=exec_working_dir)

            log_subsubtask(f"{cmd} Created Starter Shortcut: '{shortcut_name}'")
        elif cmd == CMD_EXEC:
            if not params:
                abort(f"{cmd} requires parameters.")
            log_task(f"{cmd}: will execute python command: {' '.join(params)}")
            check_that_file_exists_or_abort(venv_python_exec,"python executable")
            exec_working_dir, full_exec_line, main_executable_file, params_as_list = get_executable_line_and_dir(in_basedir, venv_python_exec, params)
            log_subsubtask(f"Full command line: '{full_exec_line}', CWD='{exec_working_dir}'")
            exec_command= [venv_python_exec] +  [main_executable_file] + params_as_list 
            rc = run_cmd(cmd = exec_command, cwd = exec_working_dir, task_description="executing command")
            if rc != 0:
                abort(f"Failed to exec command: {str(exec_command)}")
            
        elif cmd in (CMD_GITCLONE, CMD_GITCLONE_ALIAS1):
            if len(params) != 2:
                abort(f"{cmd} requires exactly 2 parameters: <url> <path_suffix>")
            url, suffix = params
            log_task(f"{cmd} cloning: {url}")
                        
            target = (in_basedir / suffix).resolve()
            target = target / extract_project_name(url)
            do_git_clone(url=url, target=target,operating_mode=in_operation_mode, force_gitpull_mode=force_gitpull_mode)
            
        elif cmd == CMD_GETFILE or cmd==CMD_GETBLOB:
            if len(params) != 2:
                abort(f"{cmd} requires exactly 2 parameters: <url> <path_suffix>")
            url, suffix = params
            log_task(f"{cmd}: retrieving file: {url}")
            
            targetdir = (in_basedir / suffix).resolve()
            if noblob_mode and cmd==CMD_GETBLOB:
                log_subsubtask(f"{cmd}: no-blob mode. ignoring download")    
                continue
            if DRYRUN:
                log_subsubtask(f"DRYRUM: {cmd}: would download {url}")
            else:
                log_subsubtask(f"{cmd} Storing file to: {targetdir}")
                #url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/wan2.2-i2v-rapid-aio-example.json"
                #path = "d:/resources/"
                download_only_if_not_existent(url=url, directory_target_path=targetdir, verbose=VERBOSE, show_progress=True)
                
        elif cmd ==CMD_PIPEXEC:
            if len(params) < 1:
                abort(f"{cmd} requires at least one parameter")
            log_task(f"{cmd}: executing pip command: {" ".join(params)}")
            check_that_file_exists_or_abort(venv_python_exec,"python executable")            
            pip_run_command(venv_python_exec, pip_command= params)

        elif cmd ==CMD_PIPREQPACKAGE:
            if len(params) < 1:
                abort(f"{cmd} requires at least one parameter")
            log_task(f"{cmd}: installing pip packages: {" ".join(params)}")
            check_that_file_exists_or_abort(venv_python_exec,"python executable")
            pip_run_pip_install(venv_python_exec, pip_command= params)

        elif cmd == CMD_COMMENTEDOUT_LINE:
            continue
        elif cmd == CMD_CONFIRM_FILE_OR_ABORT:
            path_to_confirm = params[0]
            log_task(f"{cmd}: Checking for file existence: {str(path_to_confirm)}")
            
            target = (in_basedir / path_to_confirm).resolve()
            assert_file_exists(target)
            
        elif cmd ==CMD_XRUNGITCOMMAND:
            git_command_path = params[0]
            #the params follow
            git_command_params = params[1:]
            git_command_target = (in_basedir / git_command_path).resolve()
            assert_file_exists(git_command_target)
            
            log_task(f"{cmd}: executing git command on: {git_command_path}")
            
            do_git_command(target=Path(git_command_target), params=git_command_params)

        else:
            abort(f"Unknown command in inputfile: {cmd}")




def get_executable_line_and_dir(basedir, venv_python, params):
    single_exec_params = params[1:]
    main_executable_file=None
    main_executable_temp= basedir / params[0]
    if main_executable_temp.exists():
        main_executable_file = str(main_executable_temp)
    else:
        abort(f"Python file not found: {main_executable_temp}")

    params_as_list = []
    for i, a in enumerate(single_exec_params):
        #if a.startswith("./") or a.startswith(".\\") or "/" in a or "\\" in a:
        params_as_list.append(a)
    exec_working_dir= str(Path(main_executable_file).parent)
    full_exec_line = " ".join([quote_arg(venv_python)] +[main_executable_file]+ [quote_arg(x) for x in params_as_list])

    return exec_working_dir,full_exec_line, main_executable_file, params_as_list
    


import os
def is_file(path):
    """
    Check if the given path is an existing file.
    Args: path (str): The path to check
    Returns:  bool: True if path exists and is a file, False otherwise
    """
    return os.path.exists(path) and os.path.isfile(path)

def is_directory(path):
    """
    Check if the given path is an existing directory.
    Args:  path (str): The path to check
    Returns:  bool: True if path exists and is a directory, False otherwise
    """
    return os.path.exists(path) and os.path.isdir(path)




# ========= Helper =========
def printargs(args):
    """Print all parsed arguments with their values."""
    for k, v in vars(args).items():
        print(f"{k}: {v}")




# ========= Main =========
def main():
    global STARTER_NO_DESKTOP, DRYRUN, VERBOSE, BACKUP
    

    

    parser = argparse.ArgumentParser(description="Install or repair a Python project based on a instruction file.", epilog="Have fun!")
    parser.add_argument(f"--{STARTOPTION_MODE_REBUILD}", action="store_true",help=f"rebuilds the venv from zero")
    parser.add_argument(f"--{STARTOPTION_MODE_SENSOINSTALL}",action="store_true", help=f"adds extra care not to change/replace any existing code or file and only add new elements.")


    
    parser.add_argument(STARTOPTION_INPUTFILE,  help="Path to inputfile (will be coerced to UTF-8 if needed)")
    parser.add_argument(STARTOPTION_INPUTDIR,  help="Base directory for install/repair")

    parser.add_argument(f"--{STARTOPTION_EMBEDDED}", action="store_true", help="(repair only) Treat installation as portable with 'python_embedded' folder")
    parser.add_argument(f"--{STARTOPTION_NODESKTOP}", action="store_true", help="Do not create STARTER scripts")
    parser.add_argument(f"--{STARTOPTION_DRYRUN}", action="store_true", help="Simulate actions without changing files or installing")
    parser.add_argument(f"--{STARTOPTION_VERBOSE}", action="store_true",help="Show subprocess output")
    parser.add_argument(f"--{STARTOPTION_BACKUP}", action="store_true", help="Backup existing venv (or copy python_embedded) instead of deleting/replacing")
    parser.add_argument(f"--{STARTOPTION_NOBLOB}", action="store_true",help="Enable Filedownloads. This can consume high band width and is disabled by default")
    parser.add_argument(f"--{STARTOPTION_VENVNAME}",type=str,default=None,help="Name of the custom virtual environment")
    parser.add_argument(f"--{STARTOPTION_FORCELATESTPULL}", action="store_true",help="Force repository code to the newest version on the main/master branch (sometimes calles 'nightly')")
    parser.add_argument(f"--{STARTOPTION_SHOWOP}", action="store_true",help="Show input options and quit")
    args = parser.parse_args()

    if  getattr(args, STARTOPTION_SHOWOP):
        printargs(args=args)
        abort("end")

    STARTER_NO_DESKTOP = getattr(args, STARTOPTION_NODESKTOP)
    DRYRUN = getattr(args, STARTOPTION_DRYRUN)
    VERBOSE = getattr(args, STARTOPTION_VERBOSE)
    BACKUP = getattr(args, STARTOPTION_BACKUP)

    inputfile_path = Path(getattr(args, STARTOPTION_INPUTFILE)).expanduser().resolve()
    installdir = Path(getattr(args, STARTOPTION_INPUTDIR)).expanduser().resolve()

    # Basic validations for compatibility
    if not inputfile_path.is_file():
        abort(f"PRE_CHECK: input file not found: {inputfile_path}")
    if not installdir.is_dir():
        abort(f"PRE_CHECK: Input directory not found: {installdir}")
        
    allowed_keys={
        CMD_PYTHON,
        CMD_SETVENV,
        CMD_PIPREQFILE,
        CMD_PIPREQPACKAGE,
        CMD_PIPEXEC,
        CMD_RFILTER,
        CMD_GITCLONE,
        CMD_GITCLONE_ALIAS1,
        CMD_REQSCAN,
        CMD_GETFILE,
        CMD_GETBLOB,
        CMD_PRINT,
        CMD_PAUSE,
        CMD_SHORTCUT_DESK_ICON  ,
        CMD_SHORTCUT_DESK_SCRIPT,
        CMD_SHORTCUT_BASE_ICON  ,
        CMD_SHORTCUT_BASE_SCRIPT,
        CMD_COMMENTEDOUT_LINE,
        CMD_CONFIRM_FILE_OR_ABORT,
        CMD_EXEC,
        CMD_XRUNGITCOMMAND
        }
    restricted_keys={CMD_PYTHON: 1, CMD_PAUSE: 10}
    validate_file(inputfile_path,allowed_keywords=allowed_keys,limited_keywords=restricted_keys)
    
    
    
    fileget_text=""
    if getattr(args, STARTOPTION_NOBLOB):
        fileget_text="(Large File Download disabled)"
    log_task(f"=== STARTING CROSSOS PYNST {fileget_text} ===")
    if not installdir.exists():
        if DRYRUN:
            log_subsubtask(f"[DRYRUN] Would create base directory: {installdir}")
        else:
            log_subsubtask(f"Creating base directory: {installdir}")
            installdir.mkdir(parents=True, exist_ok=True)




    # Parse instructions
    commands = parse_inputfile(inputfile_path)
    if not commands:
        abort("No commands found in inputfile.")

    # Confirm git availability early (install requires, repair may ignore clones but still good to check)
    require_tool("git", "Install Git from https://git-scm.com/ and ensure it's on PATH.")

    operation_mode=STARTOPTION_MODE_INSTALL

    if args.mode==STARTOPTION_MODE_SENSOINSTALL:
        operation_mode=STARTOPTION_MODE_SENSOINSTALL
    elif args.mode==STARTOPTION_MODE_INSTALL:
        operation_mode=STARTOPTION_MODE_INSTALL
    elif args.mode==STARTOPTION_MODE_REBUILD:
        operation_mode=STARTOPTION_MODE_REBUILD
    
    
    
    
    log_task(f"=== CrossOS {APP_NAME}: START ===")
    process_input_script(
        in_commands=commands, 
        in_basedir= installdir, 
        in_python_embedded_mode= getattr(args, STARTOPTION_EMBEDDED), 
        in_custom_venv_name=getattr(args, STARTOPTION_VENVNAME), 
        noblob_mode=getattr(args, STARTOPTION_NOBLOB), 
        in_operation_mode=operation_mode, 
        force_gitpull_mode=getattr(args, STARTOPTION_FORCELATESTPULL))
    log_task(f"=== CrossOS {APP_NAME}: END ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        abort("Aborted by user (Ctrl+C).", code=130)
