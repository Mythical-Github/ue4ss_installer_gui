import os
import pathlib
import threading

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, constants, data_structures, ue4ss
from ue4ss_installer_gui.screens import main_ue4ss_screen, add_game


def push_scanning_for_games_modal_screen():
    if dpg.does_item_exist("scanning_for_games_screen"):
        dpg.delete_item("scanning_for_games_screen")

    with dpg.window(
        tag="scanning_for_games_screen",
        no_title_bar=True,
        no_open_over_existing_popup=False,
        width=constants.WINDOW_WIDTH - 18,
        height=constants.WINDOW_HEIGHT - 47,
        no_move=True,
    ):
        dpg.add_spacer(height=300)
        dpg.add_button(label="Scanning for games...", height=28, width=-1)

    threading.Thread(target=async_init_game_scanning, daemon=True).start()


def init_game_scanning():
    games_to_add = settings.collect_games_to_add()
    games_to_remove = settings.collect_games_to_remove()

    game_directories = games_to_remove
    loaded_settings = add_manual_games_to_settings_file(games_to_add)
    updated_settings = settings.remove_game_entries_by_game_dirs(
        game_directories, loaded_settings
    )

    settings.save_settings(updated_settings)


def async_init_game_scanning():
    init_game_scanning()
    dpg.delete_item("scanning_for_games_screen")
    main_ue4ss_screen.push_main_screen()


def add_manual_games_to_settings_file(game_dir_paths: list[pathlib.Path]) -> dict:
    bool_list = []
    loaded_settings = settings.get_settings()
    for game_dir_path in game_dir_paths:
        if (
            not os.path.isdir(game_dir_path)
            or str(game_dir_path)[0] == str(game_dir_path)[0].lower()
        ):
            bool_list.append(False)
            continue

        was_valid = True

        # if game_already_in_list_check_multi(game_dir_path, loaded_settings):
        #     was_valid = False
        if not add_game.game_dir_actually_has_unreal_game_check(game_dir_path):
            was_valid = False

        bool_list.append(was_valid)

        if not was_valid:
            continue

        game_entry = data_structures.GameInfo(
            install_dir=game_dir_path,
            game_title=os.path.basename(os.path.normpath(str(game_dir_path))),
            ue4ss_version=ue4ss.get_default_ue4ss_version_tag(),
            last_installed_version="",
            platform=data_structures.GamePlatforms.OTHER,
            using_developer_version=False,
            show_pre_releases=False,
            using_portable_version=False,
            using_keep_mods_and_settings=False,
            installed_files=[],
        )

        game_entry_dict = {
            "install_dir": os.path.normpath(str(game_entry.install_dir)),
            "game_title": game_entry.game_title,
            "ue4ss_version": game_entry.ue4ss_version,
            "platform": game_entry.platform.value,
            "using_developer_version": game_entry.using_developer_version,
            "show_pre_releases": game_entry.show_pre_releases,
            "using_keep_mods_and_settings": game_entry.using_keep_mods_and_settings,
            "installed_files": [],
        }

        games_list = loaded_settings.get("games", [])
        games_list.append(game_entry_dict)
        loaded_settings["games"] = games_list

    return loaded_settings
