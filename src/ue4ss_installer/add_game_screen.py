import os
import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer.constants import *  # type: ignore
from ue4ss_installer import data_structures, settings, main_screen


def add_manual_game_to_settings_file(game_dir_path: pathlib.Path):
    # check is valid dir
    # check is not already in the settings file
    loaded_settings = settings.load_settings()
    game_entry = data_structures.GameInfo(
        game_title=os.path.basename(str(game_dir_path)), 
        install_dir=game_dir_path, 
        ue4ss_version='', 
        installed_files=[], 
        platform=data_structures.GamePlatforms.OTHER
        )

    new_installed_files = []
    for file in game_entry.installed_files:
        new_installed_files.append(file)

    game_entry_dict = {
        "game_title": game_entry.game_title,
        "install_dir": str(game_entry.install_dir),
        "ue4ss_version": game_entry.ue4ss_version,  
        "installed_files": new_installed_files,
        "platform": game_entry.platform.name
    }
    
    loaded_settings['games'].append(game_entry_dict)  # type: ignore
    settings.save_settings(loaded_settings)


def callback_directory_selected(sender, app_data):
    add_manual_game_to_settings_file(pathlib.Path(app_data["file_path_name"]))
    # refresh the main scroll box on main screen
    dpg.delete_item("DirectoryPicker")
    main_screen.add_new_game_to_games_list(os.path.basename(app_data["file_path_name"]))
    

def choose_directory():
    if dpg.does_item_exist("DirectoryPicker"):
        dpg.delete_item("DirectoryPicker")

    dpg.add_file_dialog(
        directory_selector=True,
        show=True,
        callback=callback_directory_selected,
        tag="DirectoryPicker",
        width=window_width - 80,
        height=window_height - 80,
        modal=True
    )
