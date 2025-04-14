import os
import sys
from pathlib import Path

SCRIPT_DIR = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)

def get_all_drive_letter_paths() -> list[str]:
    drive_letters = []
    for drive in range(0, 26):
        drive_letter = f"{chr(drive + ord('A'))}:\\"
        if os.path.exists(drive_letter):
            drive_letters.append(drive_letter)
    return drive_letters