import os
import pathlib
import platform
import re

from ue4ss_installer_gui import file_io


def get_all_steam_game_directories() -> list[pathlib.Path]:
    steam_directories = []
    system = platform.system()

    if system == "Windows":
        for drive_letter in file_io.get_all_drive_letter_paths():
            if drive_letter.startswith("C"):
                steam_directory = os.path.normpath(
                    f"{drive_letter}Program Files (x86)/Steam/steamapps/common"
                )
            else:
                steam_directory = os.path.normpath(
                    f"{drive_letter}SteamLibrary/steamapps/common"
                )
            if os.path.isdir(steam_directory):
                steam_directories.append(steam_directory)

    else:
        steamapps_dirs = [
            os.path.expanduser("~/.steam/steam/steamapps"),
            os.path.expanduser("~/.local/share/Steam/steamapps"),
            os.path.expanduser("~/Steam/steamapps"),
            os.path.expanduser("~/snap/steam/common/.steam/steam/steamapps"),
            os.path.expanduser("~/snap/steam/current/.steam/steam/steamapps"),
        ]

        for steamapps in steamapps_dirs:
            common_path = pathlib.Path(steamapps) / "common"
            if common_path.is_dir():
                for game_dir in common_path.iterdir():
                    if game_dir.is_dir():
                        steam_directories.append(game_dir)

            vdf_path = pathlib.Path(steamapps) / "libraryfolders.vdf"
            if vdf_path.exists():
                try:
                    with open(vdf_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    matches = re.findall(r'"\d+"\s*"\s*(.*?)\s*"', content)
                    for match in matches:
                        other_common = pathlib.Path(match.strip()) / "steamapps/common"
                        if other_common.is_dir():
                            for game_dir in other_common.iterdir():
                                if game_dir.is_dir():
                                    steam_directories.append(game_dir)
                except Exception:
                    pass

    return steam_directories
