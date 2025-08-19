#!/usr/bin/env python3

"""
#TODO
-criticalfilecheck.
-warnfilecheck


FILECHECK warn ComfyUI/myfile
FILECHECK crit ComfyUI/main.py

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
    crossos_make_icon(app_name, '#FFFFFF', '#0066CC', placement='sbs', size=256,  path=icon_path)

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

####FANCY C MAKER------------------------------


##Create windows Ico start----
import struct
from typing import DefaultDict

def create_c_png(path="c_icon.png"):
    import zlib
    size = 256
    bg = (0, 102, 204)     # blue background RGB
    fg = (255, 255, 255)   # white letter C RGB

    # Generate raw image data (RGBA scanlines with filter type 0)
    def pixel(x, y):
        cx, cy = size//2, size//2
        radius = size * 0.4
        thickness = size * 0.18
        dx, dy = x - cx, y - cy
        dist = (dx*dx + dy*dy)**0.5
        # Same "C" shape logic
        if (radius - thickness < dist < radius and
            (dx < radius * 0.3 or dy > radius * 0.7 or dy < -radius * 0.7)):
            return fg
        else:
            return bg

    raw_data = bytearray()
    for y in range(size):
        raw_data.append(0)  # no filter for this scanline
        for x in range(size):
            r, g, b = pixel(x, y)
            raw_data.extend([r, g, b, 255])  # opaque alpha

    def png_chunk(chunk_type, data):
        chunk = chunk_type + data
        import zlib
        return (len(data).to_bytes(4,'big') + chunk + zlib.crc32(chunk).to_bytes(4,'big'))

    # PNG signature
    png = bytearray(b'\x89PNG\r\n\x1a\n')

    # IHDR chunk
    ihdr = (
        size.to_bytes(4,'big') + size.to_bytes(4,'big') +
        b'\x08' +    # bit depth 8
        b'\x06' +    # color type 6 = RGBA
        b'\x00' +    # compression
        b'\x00' +    # filter
        b'\x00'      # interlace
    )
    png += png_chunk(b'IHDR', ihdr)

    # IDAT chunk (compressed image data)
    png += png_chunk(b'IDAT', zlib.compress(raw_data))

    # IEND chunk
    png += png_chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(png)
 

def create_c_ico(path="c_icon.ico"):
    size = 256
    bg_color = (4, 42, 54, 55)  # Blue background (RGBA)
    fg_color = (255, 255, 255, 255)  # White letter C (RGBA)

    # Create pixel array (BGRA order)
    pixels = bytearray(size * size * 4)
    cx, cy = size // 2, size // 2
    radius = int(size * 0.4)
    thickness = int(size * 0.18)
    for y in range(size):
        for x in range(size):
            i = (y * size + x) * 4
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            # Draw "C": an arc with a gap on right side
            if (radius - thickness < dist < radius and
                (dx < radius * 0.3 or dy > radius * 0.7 or dy < -radius * 0.7)):
                pixels[i:i+4] = fg_color[::-1]  # BGRA
            else:
                pixels[i:i+4] = bg_color[::-1]  # BGRA

    ico = bytearray()
    # ICONDIR header: Reserved, Type (1=icon), Count
    ico.extend(struct.pack('<HHH', 0, 1, 1))
    # ICONDIRENTRY:
    # Width, Height, ColorCount, Reserved, Planes, BitCount, SizeInBytes, ImageOffset
    ico.extend(struct.pack('<BBBBHHII',
        size % 256, size % 256, 0, 0, 1, 32,
        size * size * 4 + 40 + size * size // 8,  # Size of image data + header + mask
        6 + 16  # Offset to image data: ICONDIR(6) + ICONDIRENTRY(16)
    ))

    # BITMAPINFOHEADER: size=40, width, height*2 (XOR+AND masks), planes, bitcount, compression, sizeimage, xppm, yppm, clrused, clrimportant
    ico.extend(struct.pack('<IIIHHIIIIII',
        40, size, size * 2, 1, 32, 0,
        size * size * 4, 0, 0, 0, 0
    ))

    # Pixel data: BMP stores bottom-up
    for y in range(size-1, -1, -1):
        start = y * size * 4
        end = (y + 1) * size * 4
        ico.extend(pixels[start:end])

    # AND mask (1 bit per pixel; all zero = no transparency)
    ico.extend(b'\x00' * (size * size // 8))

    with open(path, 'wb') as f:
        f.write(ico)




###FANC YC MAKER END---------------------------




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


###***END***



























































# -*- coding: utf-8 -*-

"""
 
A single-file, cross-platform (Windows/Linux/macOS) installer/repairer for Python repositories
driven by a .txt instruction file.

- No external packages required (stdlib only).
- Modes:
  * install
  * repair (with --repairportable for embedded/portable distributions)

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
DEFAULT_PYTHON_VERSION = "3.12"

STARTER_NO_DESKTOP = False
DRYRUN = False
VERBOSE = False
BACKUP = False

COLOR_TASK = "\033[32m"     # Dark green for main tasks
COLOR_SUBTASK = "\033[94m"  # Blue for subtasks
COLOR_ERROR = "\033[91m"    # Red for errors
COLOR_END = "\033[0m"

CMD_PYTHON="PYTHON"
CMD_REQFILE="REQFILE"
CMD_RFILTER="RFILTER"
CMD_GITCLONE="GITCLON"
CMD_GITCLONE_ALIAS1="GITCLONE"
CMD_REQSCAN="REQSCAN"
CMD_FILEGET="FILEGET"
CMD_PRINT="NOTEOUT"

CMD_PAUSE="PAUSE"

CMD_DESK_ICON_SHORTCUT  ="DESKICO"
CMD_DESK_SCRIPT_SHORTCUT="DESKEXE"
CMD_BASE_ICON_SHORTCUT  ="HOMEICO"
CMD_BASE_SCRIPT_SHORTCUT="HOMEEXE"


TOKEN_PRINT_PREFIX="Info: "

# ========= Utility logging =========
def log_task(msg: str):
    print(f"{COLOR_TASK}{msg}{COLOR_END}")

def log_subtask(msg: str):
    print(f"{COLOR_SUBTASK}{msg}{COLOR_END}")

def log_error(msg: str):
    print(f"{COLOR_ERROR}{msg}{COLOR_END}")

def abort(msg: str, code: int = 1):
    log_error(msg)
    sys.exit(code)

def run_cmd(cmd, cwd=None) -> int:
    """
    Run a command with optional output suppression.
    Returns the process return code.
    """
    if DRYRUN:
        log_subtask(f"[DRYRUN] Would run: {' '.join(map(str, cmd))} (cwd={cwd or os.getcwd()})")
        return 0
    if VERBOSE:
        return subprocess.call(cmd, cwd=cwd)
    else:
        with subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
            return p.returncode

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
                log_subtask(f"FilePrecheck: on Inputfile Error at line {lineno}: '{first_word}' is not an allowed keyword.")
                sys.exit(1)

            # Rule 2: count restricted keywords
            if first_word in limited_keywords:
                counts[first_word] += 1
                if counts[first_word] > limited_keywords[first_word]:
                    log_subtask(f"FilePrecheck:  on Inputfile: Error at line {lineno}: '{first_word}' "
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

def check_python_version_available(version: str):
    cmd = python_cmd_for_version(version) + ["--version"]
    rc = run_cmd(cmd)
    if rc != 0:
        abort(f"Python {version} not available on this system. Please install it and try again.")

def create_or_replace_venv(venv_path: Path, version: str, do_backup: bool):
    """
    Create a new venv at venv_path using the specified Python version.
    If venv_path exists:
      - if BACKUP: rename to .bak (unique suffix)
      - else: delete it
    """
    if venv_path.exists():
        if do_backup:
            bak = unique_bak_name(venv_path)
            if DRYRUN:
                log_subtask(f"[DRYRUN] Would move existing venv '{venv_path}' -> '{bak}'")
            else:
                log_subtask(f"Backing up existing venv to: {bak}")
                venv_path.rename(bak)
        else:
            if DRYRUN:
                log_subtask(f"[DRYRUN] Would delete existing venv: {venv_path}")
            else:
                log_subtask(f"Deleting existing venv: {venv_path}")
                shutil.rmtree(venv_path, ignore_errors=True)

    # Create new venv
    cmd = python_cmd_for_version(version) + ["-m", "venv", str(venv_path)]
    rc = run_cmd(cmd)
    if rc != 0:
        abort(f"Failed to create virtual environment at {venv_path}")
    log_subtask(f"Created virtual environment: {venv_path}")

    # Ensure pip present and up-to-date
    vpy = get_venv_python(venv_path)
    run_cmd([vpy, "-m", "ensurepip", "--upgrade"])
    #run_cmd([vpy, "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"])

def get_venv_python(venv_path: Path) -> str:
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
        log_subtask("[DRYRUN] Assuming environment is empty for checks.")
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
    log_task("Uninstalling all packages from current environment (pip freeze -> pip uninstall -y) ...")
    if DRYRUN:
        log_subtask("[DRYRUN] Would run 'pip freeze' and uninstall all packages.")
        return
    try:
        out = subprocess.check_output([python_exec, "-m", "pip", "freeze"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        abort("Failed to query installed packages via 'pip freeze'.")

    pkgs = [l.strip() for l in out.decode("utf-8", errors="replace").splitlines() if l.strip()]
    if not pkgs:
        log_subtask("No packages installed.")
        return
    # Write to temp file to avoid command-line length limits
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as tf:
        for p in pkgs:
            tf.write(p + "\n")
        temp_list = tf.name
    try:
        rc = run_cmd([python_exec, "-m", "pip", "uninstall", "-y", "-r", temp_list])
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
    log_subtask(f"Downloading {url} -> {p}")
    if DRYRUN:
        log_subtask("[DRYRUN] Skipping actual download.")
        # Create an empty file to keep flow consistent
        p.write_text("", encoding="utf-8")
        return p
    urllib.request.urlretrieve(url, p)
    return p

def do_git_pull( repo_path: Path):
    """
    Perform a git pull on a directory
    """     
    if not repo_path.exists():
        abort(f"Directory to perform git pull not found: {repo_path}")
    if DRYRUN:
        log_subtask(f"[DRYRUN] Would update repository: git pull (cwd: {repo_path})")
    else:
        rc = run_cmd(["git", "pull"], repo_path)
        if rc != 0:
            abort(f"Failed to update repository (broken or not a repo) from: {str(repo_path)}")
    log_subtask(f"Updated git repository: {repo_path}")


def pip_install_requirements(python_exec: str, req_file: Path, current_filters: list[str], fail_label: str):
    """
    Install requirements from a (possibly remote) file with RFILTER applied.
    """
    src = req_file
    if not src.exists():
        abort(f"Requirements file not found: {src}")
    filtered = apply_rfilter_to_file(src, current_filters)
    
    message_append=""
    if current_filters:
       message_append=f"(package filter applied and installing as temp file)" 
    log_subtask(f"Installing requirements from file{message_append}: {req_file}")
    rc = run_cmd([python_exec, "-m", "pip", "install", "-r", str(filtered)])
    if rc != 0:
        abort(f"Failed to install requirements from: {fail_label}")

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

def git_clone(url: str, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        # If exists, assume it's the expected repo already — remove it to re-clone.
        if DRYRUN:
            log_subtask(f"[DRYRUN] Would remove existing directory before clone: {target}")
        else:
            shutil.rmtree(target, ignore_errors=True)
    rc = run_cmd(["git", "clone", url, str(target)])
    if rc != 0:
        abort(f"Git clone failed for {url}")
    log_subtask(f"Cloned to: {target}")


def task_print(text_tokens):
    text = " ".join([quote_arg(x) for x in text_tokens])
    print(f"{COLOR_SUBTASK}{TOKEN_PRINT_PREFIX}{COLOR_END}{text}")
 
def task_pause():
    """
    Pause execution until the user presses Enter to continue
    or Ctrl+C to abort. Works on Windows, Linux, and macOS.
    """
    try:
        input("Press Enter to continue or Ctrl+C to abort... ")
    except KeyboardInterrupt:
        print("\nAborted by user.")
        raise  # re-raise so caller can handle it if needed


# ========= Download helpers =========
import subprocess
import os
from urllib.parse import urlparse
def download_with_wget(url: str, dest_dir: str, quiet: bool = True) -> str:
    """
    Downloads a file from `url` into `dest_dir` using wget.
    Works on Windows, Linux, and macOS (requires wget installed).
    
    Args:
        url (str): The URL of the file to download.
        dest_dir (str): The destination directory.
        quiet (bool): If True, suppress wget output (default False).
    
    Returns:
        str: The full path of the downloaded file.
    """
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    # Extract filename from URL
    filename = os.path.basename(urlparse(url).path)
    if not filename:  # if URL ends with /, fallback
        filename = "downloaded_file"
    dest_path = os.path.join(dest_dir, filename)
    # Build wget command
    cmd = ["wget", url, "-O", dest_path]
    if quiet:
        cmd.insert(1, "-q")  # insert -q after wget
    # Run wget
    subprocess.run(cmd, check=True)
    return dest_path


# ========= Starter helpers =========
def make_starter(basedir: Path, venv_py: str, label: str, cmd_line: list[str], working_dir: str):
    """
    Create .bat/.sh starter scripts that launch the given command with the venv python.
    Resolve any relative path to absolute under basedir if it exists there.
    """
    if STARTER_NO_DESKTOP:
        log_subtask("STARTER creation skipped due to --nodesktop.")
        return

    system = platform.system().lower()
    script_name = f"{label}{'.bat' if system == 'windows' else '.sh'}"
    script_path = basedir / script_name

    if system == "windows":
        content = f"cd {working_dir}\r\n" + cmd_line + "\r\n"
    else:
        content = "#!/usr/bin/env bash\n" +f"cd {working_dir}\n" + cmd_line + "\n"

    if DRYRUN:
        log_subtask(f"[DRYRUN] Would create starter: {script_path}")
        return

    script_path.write_text(content, encoding="utf-8")
    if system != "windows":
        os.chmod(script_path, 0o755)
    log_subtask(f"Created starter shortcut: {script_path}")

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
        root_req = root / "requirements.txt"
        if root_req.is_file():
            results.append(root_req)
        for entry in root.iterdir():
            if entry.is_dir():
                p = entry / "requirements.txt"
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

def backup_embedded_folder(embedded_dir: Path):
    """
    Copy python_embedded to python_embedded.bak (or .bakN if exists).
    """
    bak = unique_bak_name(embedded_dir)
    if DRYRUN:
        log_subtask(f"[DRYRUN] Would copy '{embedded_dir}' -> '{bak}'")
        return
    log_subtask(f"Creating backup of embedded Python at: {bak}")
    shutil.copytree(embedded_dir, bak)

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

# ========= Mode: INSTALL =========
def do_install(commands: list[tuple[str, list[str]]], basedir: Path, fileget_mode=False):
    # Ensure git available
    require_tool("git", "Please install Git and ensure it is on your PATH.")

    # State
    python_version = DEFAULT_PYTHON_VERSION

    # First pass: allow PYTHON to set version before venv creation if it's the first command,
    # but spec says PYTHON can only occur once and is the version to use. If absent, use default.
    for cmd, params in commands:
        if cmd == CMD_PYTHON:
            python_version = params[0]
            break

    # Strictly check Python version available
    check_python_version_available(python_version)
    # Execute commands in order
    for cmd, params in commands:
        if cmd == CMD_PAUSE:
            task_pause()
            
        elif cmd == CMD_PRINT:
            
            
            task_print(params)
        
        elif cmd == CMD_PYTHON:
            # Already handled; validate only occurrence
            continue
        elif cmd == CMD_RFILTER:
            continue
        elif cmd == CMD_REQFILE:
            continue
        elif cmd in (CMD_GITCLONE, CMD_GITCLONE_ALIAS1):
            if len(params) != 2:
                abort(f"{cmd} requires exactly 2 parameters: <url> <path_suffix>")
            url, suffix = params
            target = (basedir / suffix).resolve()
            target = target / extract_project_name(url)
            log_task(f"{cmd} cloning: {url}")
            git_clone(url, target)

        elif cmd == CMD_BASE_ICON_SHORTCUT or cmd == CMD_DESK_ICON_SHORTCUT or cmd == CMD_BASE_SCRIPT_SHORTCUT or cmd == CMD_DESK_SCRIPT_SHORTCUT :
            continue
        elif cmd == CMD_REQSCAN:
            continue
 
        elif cmd == CMD_FILEGET:
            continue
            
            
        else:
            abort(f"Unknown command in inputfile: {cmd}")
 
    do_repair(commands=commands, basedir= basedir, repairportable= False, fileget_mode=fileget_mode, install_mode=True)
     




# ========= Mode: REPAIR =========
def do_repair(commands: list[tuple[str, list[str]]], basedir: Path, repairportable: bool,  fileget_mode=False,install_mode=False):
    # Ensure git available (not strictly required for repair flow, but keep parity)
    require_tool("git", "Please install Git and ensure it is on your PATH.")

    embedded_dir = basedir / "python_embedded"
    is_embedded_present = embedded_dir.is_dir()
    venv_path=""
    # Validate portable/manual selection
    if repairportable:
        if not is_embedded_present:
            abort("this is not a portable or manual installation")
        # Use embedded python executable (best effort cross-platform)
        python_exec = str(embedded_dir / ("python.exe" if platform.system().lower() == "windows" else "python"))
        if not (Path(python_exec).exists()):
            # Fallback to 'python3' inside embedded_dir if present; else abort
            alt = str(embedded_dir / "python3")
            if not Path(alt).exists():
                abort("Embedded Python executable not found in 'python_embedded'.")
            python_exec = alt

        # Optional backup of python_embedded
        if BACKUP:
            backup_embedded_folder(embedded_dir)

        # Uninstall all packages in embedded environment
        uninstall_all_packages(python_exec)

        # Verify empty
        if not is_venv_empty(python_exec):
            abort("Embedded environment is not empty after uninstall. Aborting.")

        # requirements installs will proceed using this python_exec
        venv_python = python_exec
        venv_path=embedded_dir

    else:
        if is_embedded_present:
            # The presence of python_embedded suggests it's a portable install; user should pass --repairportable
            abort("this is not a portable or manual installation")
        # Build/rebuild a new venv with the requested/implicit Python version
        # Determine PYTHON version from commands (default 3.12 if absent)
        python_version = DEFAULT_PYTHON_VERSION
        for cmd, params in commands:
            if cmd == CMD_PYTHON:
                python_version = params[0]
                break
        check_python_version_available(python_version)

        # OS-specific venv name
        system = platform.system().lower()
        venv_name = {
            "windows": ".env_windows",
            "linux": ".env_linux",
            "darwin": ".env_macos"
        }.get(system, ".env")
        venv_path = basedir / venv_name

        # Backup or delete existing venv dir if present
        log_task(f"Building venv for Python {python_version}")
        create_or_replace_venv(venv_path, python_version, BACKUP)
        venv_python = get_venv_python(venv_path)
    # Now process commands permitted in REPAIR mode: PYTHON (already handled), RFILTER, REQFILE, STARTER, REQSCAN
    rfilters: list[str] = []
    # Collect REQSCAN paths (process them after REQFILEs or as they appear? Spec: executed in order they appear. We'll execute in order.)
    for cmd, params in commands:
        
        if cmd == CMD_PAUSE:
            if install_mode:
                continue
            task_pause()
            
        elif cmd == CMD_PRINT:
            if install_mode:
                continue
            task_print()
        elif cmd == CMD_PYTHON:
            continue
        elif cmd == CMD_RFILTER:
            rfilters = params[:]
            log_task(f"{cmd} set: {', '.join(rfilters)}")
        elif cmd == CMD_REQFILE:
            src = params[0]
            log_task(f"{cmd} installing: {src}")
            if re.match(r"^https?://", src, re.I):
                temp = download_to_temp(src)
                pip_install_requirements(venv_python, temp, rfilters, src)
            else:
                pip_install_requirements(venv_python, (basedir / src) if not Path(src).is_file() else Path(src), rfilters, src)
        elif cmd == CMD_REQSCAN:
            # Search one level below basedir/suffix for requirements.txt (plus root-of-suffix)
            scan_root = (basedir / params[0]).resolve()
            if not scan_root.exists():
                log_subtask(f"{cmd} path does not exist, skipping: {scan_root}")
                continue
            log_task(f"{cmd} searching for requirements in: {scan_root} (depth=1)")
            reqs = scan_requirements_one_level(scan_root)
            if not reqs:
                log_subtask("No requirements.txt files found at the specified depth.")
            for req in reqs:
                
                path = Path(req)
                git_dir=path.parent
                log_subtask(f"{cmd} Repository found. Installing: {git_dir}")
                
                do_git_pull(git_dir)
                pip_install_requirements(venv_python, req, rfilters, str(req))
        elif  cmd == CMD_BASE_ICON_SHORTCUT or cmd == CMD_DESK_ICON_SHORTCUT or cmd == CMD_BASE_SCRIPT_SHORTCUT or cmd == CMD_DESK_SCRIPT_SHORTCUT :
            
            
            
            
            if not params:
                abort(f"{cmd} requires parameters.")

            shortcut_name = params[0]
            single_exec_params = params[1:]
            main_executable_file=""
            resolved = []
            for i, a in enumerate(single_exec_params):
                main_executable_file = basedir / a
                if a.startswith("./") or a.startswith(".\\") or "/" in a or "\\" in a:
                    # Looks like a path - resolve if it exists
                    if main_executable_file.exists():
                        resolved.append(str(main_executable_file))
                    else:
                        resolved.append(a)
                else:
                    # Non-path-ish argument
                    resolved.append(a)           
            exec_working_dir= str(Path(main_executable_file).parent)
            full_exec_line = " ".join([quote_arg(venv_python)] + [quote_arg(x) for x in resolved]) 
           
            if cmd == CMD_BASE_SCRIPT_SHORTCUT:
                make_starter(basedir, venv_python, shortcut_name, full_exec_line, working_dir=exec_working_dir)


 
            
            elif cmd == CMD_BASE_ICON_SHORTCUT:
                if DRYRUN:
                    print(f"DRY_RUN: would create a homedir shortcut {shortcut_name}.venv: {venv_path}, basedir: {basedir}. Exex line: {full_exec_line}")
                else:
                    crossos_make_shortcut(app_name=shortcut_name, exec_line=full_exec_line, installpath=basedir,env_path=venv_path, onDesktop=False, working_dir=exec_working_dir)
            elif cmd == CMD_DESK_ICON_SHORTCUT:
                if DRYRUN:
                    log_subtask(f"DRY_RUN: would create a Desktop shortcut {shortcut_name}.venv: {venv_path}, basedir: {basedir}. Exex line: {full_exec_line}")
                else:
                    crossos_make_shortcut(app_name=shortcut_name, exec_line=full_exec_line, installpath=basedir,env_path=venv_path, onDesktop=True, working_dir=exec_working_dir)

            log_subtask(f"{cmd} Created Starter Shortcut: {shortcut_name}")
        elif cmd in (CMD_GITCLONE, CMD_GITCLONE_ALIAS1):
            continue
        
        elif cmd == CMD_FILEGET:
            if len(params) != 2:
                abort(f"{cmd} requires exactly 2 parameters: <url> <path_suffix>")
            url, suffix = params
            targetdir = (basedir / suffix).resolve()
            quietmode= not VERBOSE
            
            log_task(f"{cmd} Retrieving file: {url}")
            if fileget_mode==False:
                log_subtask(f"{cmd} Fileget option not present. ignoring download")    
                continue


            if DRYRUN:
                print(f"DRYRUM: {cmd}: would download {url}")
            else:
                log_subtask(f"{cmd} Storing file to: {targetdir}")
                download_with_wget(url=url,dest_dir=targetdir, quiet=quietmode)
            
            
        else:
            abort(f"Unknown command in inputfile: {cmd}")
    










# ========= Main =========
def main():
    global STARTER_NO_DESKTOP, DRYRUN, VERBOSE, BACKUP

    parser = argparse.ArgumentParser(
        description="Install or repair a Python project based on a instruction file."
    )
    parser.add_argument("-a", dest="mode", choices=["install", "repair"], required=True,
                        help="Main mode: install or repair")
    parser.add_argument("--input", required=True, help="Path to inputfile (will be coerced to UTF-8 if needed)")
    parser.add_argument("--dir", required=True, help="Base directory for install/repair")
    parser.add_argument("--repairportable", action="store_true",
                        help="(repair only) Treat installation as portable with 'python_embedded' folder")
    parser.add_argument("--nodesktop", action="store_true",
                        help="Do not create STARTER scripts")
    parser.add_argument("--dryrun", action="store_true",
                        help="Simulate actions without changing files or installing")
    parser.add_argument("--verbose", action="store_true",
                        help="Show subprocess output")
    parser.add_argument("--backup", action="store_true",
                        help="Backup existing venv (or copy python_embedded) instead of deleting/replacing")
    parser.add_argument("--fileget", action="store_true",
                        help="Enable Filedownloads. This can consume high band width and is disabled by default")
    args = parser.parse_args()

    STARTER_NO_DESKTOP = args.nodesktop
    DRYRUN = args.dryrun
    VERBOSE = args.verbose
    BACKUP = args.backup

    inputfile_path = Path(args.input).expanduser().resolve()
    installdir = Path(args.dir).expanduser().resolve()

    # Basic validations
    if not inputfile_path.is_file():
        abort(f"inputfile file not found: {inputfile_path}")

    allowed_keys={CMD_PYTHON,
        CMD_REQFILE,
        CMD_RFILTER,
        CMD_GITCLONE,
        CMD_GITCLONE_ALIAS1,
        CMD_REQSCAN,
        CMD_FILEGET,
        CMD_PRINT,
        CMD_PAUSE,
        CMD_DESK_ICON_SHORTCUT  ,
        CMD_DESK_SCRIPT_SHORTCUT,
        CMD_BASE_ICON_SHORTCUT  ,
        CMD_BASE_SCRIPT_SHORTCUT}
    restricted_keys={CMD_PYTHON: 1, CMD_PAUSE: 10}
    validate_file(inputfile_path,allowed_keywords=allowed_keys,limited_keywords=restricted_keys)
    
    fileget_text=""
    if args.fileget:
        fileget_text="(File Download enabled)"
    log_task(f"=== STARTING CROSSOS PYNST {fileget_text} ===")
    if not installdir.exists():
        if DRYRUN:
            log_subtask(f"[DRYRUN] Would create base directory: {installdir}")
        else:
            log_subtask(f"Creating base directory: {installdir}")
            installdir.mkdir(parents=True, exist_ok=True)

    # Parse instructions
    commands = parse_inputfile(inputfile_path)
    if not commands:
        abort("No commands found in inputfile.")

    # Confirm git availability early (install requires, repair may ignore clones but still good to check)
    require_tool("git", "Install Git from https://git-scm.com/ and ensure it's on PATH.")

    if args.mode == "install":
        log_task("=== INSTALL MODE ===")
        do_install(commands=commands, basedir=installdir, fileget_mode=args.fileget)
        log_subtask("--- INSTALL COMPLETED ---")
    else:
        log_task("=== REPAIR MODE ===")
        do_repair(commands=commands, basedir= installdir, repairportable= args.repairportable, fileget_mode=args.fileget)
        log_subtask("--- REPAIR COMPLETED ---")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        abort("Aborted by user (Ctrl+C).", code=130)
