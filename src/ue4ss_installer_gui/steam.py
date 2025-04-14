import os
import pathlib

from ue4ss_installer_gui import file_io


def get_all_steam_game_directories() -> list[pathlib.Path]:
    steam_directories = []
    for drive_letter in file_io.get_all_drive_letter_paths():
        if drive_letter == "C":
            steam_directory = os.path.normpath(
                f"{drive_letter}Program Files (x86)/Steam/steamapps/common"
            )
        else:
            steam_directory = os.path.normpath(
                f"{drive_letter}SteamLibrary/steamapps/common"
            )
        if os.path.isdir(steam_directory):
            steam_directories.append(steam_directory)
    return steam_directories
