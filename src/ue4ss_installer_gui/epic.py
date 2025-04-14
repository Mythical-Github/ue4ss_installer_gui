import os
import pathlib

from ue4ss_installer_gui import file_io


def get_all_epic_games_game_directories() -> list[pathlib.Path]:
    epic_games_games_directories = []
    for drive_letter in file_io.get_all_drive_letter_paths():
        epic_games_games_directory = os.path.normpath(
            f"{drive_letter}Program Files/Epic Games"
        )
        if os.path.isdir(epic_games_games_directory):
            epic_games_games_directories.append(epic_games_games_directory)
    return epic_games_games_directories
