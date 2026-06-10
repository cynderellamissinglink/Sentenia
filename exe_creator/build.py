import os
import shutil
import subprocess
from pathlib import Path

# Change to the script's directory
os.chdir(Path(__file__).parent)

# Move UP one level to the root folder where NetScan.py lives
ROOT_DIR = Path(__file__).parent.parent
os.chdir(ROOT_DIR)

APP_NAME = "NetScan"
EXE_PATH = os.path.join("dist", f"{APP_NAME}.exe")

# 1. Kill the app if it's currently running (prevents "Permission Denied" errors)
if os.name == "nt":  # Windows
    subprocess.run(["taskkill", "/F", "/IM", f"{APP_NAME}.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Explicitly delete the old EXE if it exists
if os.path.exists(EXE_PATH):
    try:
        os.remove(EXE_PATH)
        print(f"Removed old executable: {EXE_PATH}")
    except PermissionError:
        print(f"Warning: Could not delete {EXE_PATH}. It might be open or running.")

# 3. Clean old builds and folders
for folder in ["build", "dist"]:
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except PermissionError:
            # If rmtree fails because the folder is locked, we try to keep going
            pass

# Remove old spec file from root (if exists)
spec_file = f"{APP_NAME}.spec"
if os.path.exists(spec_file):
    os.remove(spec_file)

# PyInstaller command - now NetScan.py is in the current (root) directory
cmd = [
    "python",
    "-m",
    "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", APP_NAME,
    "--icon", "assets/images/icon.png",  # Now assets is in the root folder
    "--add-data", "assets;assets",
    "NetScan.py"  # Now this exists in the root folder
]

subprocess.run(cmd)

print("\nBuild complete.")
print(f"EXE location: {os.path.join(ROOT_DIR, 'dist', f'{APP_NAME}.exe')}")