import os
import pathlib

from ue4ss_installer_gui.screens import main_screen
from ue4ss_installer_gui import translator

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import (
    data_structures,
    settings,
    constants,
    ue4ss,
    unreal_engine,
)


def game_dir_actually_has_unreal_game_check(game_dir_path: pathlib.Path):
    if not unreal_engine.does_directory_contain_unreal_game(game_dir_path):
        if settings.has_inited_settings:
            init_not_an_unreal_game_popup(game_dir_path)
            dpg.split_frame()
            dpg.configure_item("not_an_unreal_game_pop_up", show=True)
        return False
    return True


def call_dismiss_pop_up_game_already_in_list():
    dpg.delete_item("game_already_exists_popup")


def call_dismiss_pop_up_not_unreal_game():
    dpg.delete_item("not_an_unreal_game_pop_up")


def init_not_an_unreal_game_popup(game_directory: pathlib.Path):
    if dpg.does_item_exist("not_an_unreal_game_pop_up"):
        dpg.delete_item("not_an_unreal_game_pop_up")
    dpg.add_window(
        modal=True,
        tag="not_an_unreal_game_pop_up",
        no_title_bar=True,
        min_size=[100, 140],
    )
    message = translator.translator.translate(
        "invalid_game_directory_selected_error_text"
    )
    message_two = os.path.normpath(str(game_directory))
    dpg.add_text(message, parent="not_an_unreal_game_pop_up", wrap=384)
    dpg.add_text(message_two, parent="not_an_unreal_game_pop_up", wrap=384)
    dpg.add_separator(parent="not_an_unreal_game_pop_up")
    dpg.add_button(
        label="Close",
        parent="not_an_unreal_game_pop_up",
        width=-1,
        height=-1,
        callback=call_dismiss_pop_up_not_unreal_game,
    )


def init_game_already_in_list_pop_up(game_directory: pathlib.Path):
    dpg.add_window(
        modal=True,
        tag="game_already_exists_popup",
        no_title_bar=True,
        width=constants.WINDOW_WIDTH - 200,
        height=constants.WINDOW_HEIGHT - 700,
        pos=(100, constants.Y + 100),
    )
    message = translator.translator.translate("game_already_exists_in_list_error")
    message_two = os.path.normpath(str(game_directory))
    dpg.add_text(message, parent="game_already_exists_popup", wrap=384)
    dpg.add_text(message_two, parent="game_already_exists_popup", wrap=384)
    dpg.add_separator(parent="game_already_exists_popup")
    dpg.add_button(
        label=translator.translator.translate("close_button_text"),
        parent="game_already_exists_popup",
        width=-1,
        height=-1,
        callback=call_dismiss_pop_up_game_already_in_list,
    )


def game_already_in_list_check(game_directory: pathlib.Path) -> bool:
    game_entries = settings.get_settings().get("games", [])
    normalized_new_game = os.path.normcase(os.path.normpath(str(game_directory)))

    for game_entry in game_entries:
        existing_game = os.path.normcase(os.path.normpath(game_entry["install_dir"]))
        print(f"existing game: {existing_game}")
        print(f"normalized new game: {normalized_new_game}")
        if existing_game == normalized_new_game:
            if settings.has_inited_settings:
                init_game_already_in_list_pop_up(game_directory)
                dpg.split_frame()
                dpg.configure_item("game_already_exists_popup", show=True)
            print("true was in")
            return True
    print("false was not in")
    return False


def game_already_in_list_check_multi(
    game_directory: pathlib.Path, input_settings
) -> bool:
    game_entries = input_settings.get("games", [])
    normalized_new_game = os.path.normcase(os.path.normpath(str(game_directory)))

    for game_entry in game_entries:
        existing_game = os.path.normcase(os.path.normpath(game_entry["install_dir"]))
        if existing_game == normalized_new_game:
            if settings.has_inited_settings:
                init_game_already_in_list_pop_up(game_directory)
                dpg.split_frame()
                dpg.configure_item("game_already_exists_popup", show=True)
            print("true was in")
            return True
    print("false was not in")
    return False


def add_manual_games_to_settings_file(game_dir_paths: list[pathlib.Path]) -> dict:
    bool_list = []
    loaded_settings = settings.get_settings()
    for game_dir_path in game_dir_paths:
        if not os.path.isdir(game_dir_path):
            bool_list.append(False)
            continue

        was_valid = True

        if game_already_in_list_check_multi(game_dir_path, loaded_settings):
            was_valid = False
        if not game_dir_actually_has_unreal_game_check(game_dir_path):
            was_valid = False

        bool_list.append(was_valid)

        if not was_valid:
            continue

        game_entry = data_structures.GameInfo(
            install_dir=game_dir_path,
            game_title=os.path.basename(str(game_dir_path)),
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
            "install_dir": str(game_entry.install_dir),
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


def callback_directory_selected(sender, app_data):
    game_directory = pathlib.Path(app_data["file_path_name"])
    game_name = os.path.basename(game_directory)
    if add_manual_game_to_settings_file(game_directory):
        main_screen.add_new_game_to_games_list(
            constants.GAME_PATHS_TO_DISPLAY_NAMES.get(game_name, game_name),
            str(game_directory),
        )
        main_screen.refresh_game_list_scroll_box()


def choose_directory():
    if dpg.does_item_exist("directory_picker"):
        dpg.delete_item("directory_picker")

    dpg.add_file_dialog(
        directory_selector=True,
        show=True,
        callback=callback_directory_selected,
        tag="directory_picker",
        width=constants.WINDOW_WIDTH - 80,
        height=constants.WINDOW_HEIGHT - 80,
        modal=True,
    )


def add_manual_game_to_settings_file(game_dir_path: pathlib.Path) -> bool:
    if not os.path.isdir(game_dir_path):
        return False
    was_valid = True
    if game_already_in_list_check(game_dir_path):
        was_valid = False
    if not game_dir_actually_has_unreal_game_check(game_dir_path):
        was_valid = False
    if not was_valid:
        return was_valid
    loaded_settings = settings.get_settings()
    game_entry = data_structures.GameInfo(
        install_dir=game_dir_path,
        game_title=os.path.basename(str(game_dir_path)),
        ue4ss_version=ue4ss.get_default_ue4ss_version_tag(),
        platform=data_structures.GamePlatforms.OTHER,
        last_installed_version="",
        using_developer_version=False,
        show_pre_releases=False,
        using_portable_version=False,
        using_keep_mods_and_settings=False,
        installed_files=[],
    )

    new_installed_files = []
    for file in game_entry.installed_files:
        new_installed_files.append(file)

    game_entry_dict = {
        "install_dir": str(game_entry.install_dir),
        "game_title": game_entry.game_title,
        "ue4ss_version": game_entry.ue4ss_version,
        "platform": game_entry.platform.value,
        "using_developer_version": game_entry.using_developer_version,
        "show_pre_releases": game_entry.show_pre_releases,
        "using_keep_mods_and_settings": game_entry.using_keep_mods_and_settings,
        "installed_files": new_installed_files,
    }

    games_list = loaded_settings.get("games", [])
    games_list.append(game_entry_dict)
    loaded_settings["games"] = games_list

    settings.save_settings(loaded_settings)
    return was_valid
