import os
import pathlib

from ue4ss_installer_gui.screens import main

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import data_structures, settings, constants, ue4ss, file_io


# make sure it allows multiple game installs of the same game, show some _1 _2 or something
# have it check the game dir not the game title for if it already exists later
# if it's not an unreal game make it show a different popup, right now it says it's already in the list


def game_dir_actually_has_unreal_game_check(game_dir_path: pathlib.Path):
    acceptable_dirs = [
        f"{file_io.SCRIPT_DIR}/Engine/Binaries",
        f"{file_io.SCRIPT_DIR}/Engine/Shared",
        f"{file_io.SCRIPT_DIR}/Engine/Shared",
    ]
    acceptable_files = [f"{file_io.SCRIPT_DIR}/Manifest_NonUFSFiles_Win64.txt"]
    for acceptable_dir in acceptable_dirs:
        if os.path.isdir(os.path.normpath(acceptable_dir)):
            return True
    for acceptable_file in acceptable_files:
        if os.path.isfile(os.path.normpath(acceptable_file)):
            return True
    init_not_an_unreal_game_popup(game_dir_path)
    from time import sleep

    sleep(0.1)
    dpg.configure_item("not_an_unreal_game_pop_up", show=True)
    return False


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
    message = " The following game directory does not contain an unreal game:"
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
        modal=True,  # this is randomly breaking it right now
        tag="game_already_exists_popup",
        no_title_bar=True,
        width=constants.window_width - 200,
        height=constants.window_height - 700,
        pos=(100, constants.y + 100),
    )
    message = " The following game already exists in the games list:"
    message_two = os.path.normpath(str(game_directory))
    dpg.add_text(message, parent="game_already_exists_popup", wrap=384)
    dpg.add_text(message_two, parent="game_already_exists_popup", wrap=384)
    dpg.add_separator(parent="game_already_exists_popup")
    dpg.add_button(
        label="Close",
        parent="game_already_exists_popup",
        width=-1,
        height=-1,
        callback=call_dismiss_pop_up_game_already_in_list,
    )


def game_already_in_list_check(game_directory: pathlib.Path) -> bool:
    # this checks currently only the games in settings, it needs to also check the autopopulated list
    game_entries = settings.get_settings().get("games", {})
    is_game_already_in_list = False
    for game_entry in game_entries:
        if os.path.normpath(game_entry["install_dir"]) == os.path.normpath(
            str(game_directory)
        ):
            is_game_already_in_list = True
            break
    if is_game_already_in_list:
        init_game_already_in_list_pop_up(game_directory)
        from time import sleep

        sleep(0.1)
        dpg.configure_item("game_already_exists_popup", show=True)
        return True
    return False


def add_manual_game_to_settings_file(game_dir_path: pathlib.Path) -> bool:
    was_valid = True
    if game_already_in_list_check(game_dir_path) == True:
        was_valid = False
    if game_dir_actually_has_unreal_game_check(game_dir_path) == False:
        was_valid = False
    if was_valid == False:
        return was_valid
    loaded_settings = settings.get_settings()
    game_entry = data_structures.GameInfo(
        install_dir=game_dir_path,
        game_title=os.path.basename(str(game_dir_path)),
        ue4ss_version=ue4ss.get_default_ue4ss_version_tag(),
        installed_files=[],
        platform=data_structures.GamePlatforms.OTHER,
    )

    new_installed_files = []
    for file in game_entry.installed_files:
        new_installed_files.append(file)

    game_entry_dict = {
        "game_title": game_entry.game_title,
        "install_dir": str(game_entry.install_dir),
        "ue4ss_version": game_entry.ue4ss_version,
        "installed_files": new_installed_files,
        "platform": game_entry.platform.name,
    }

    games_list = loaded_settings.get("games", [])
    games_list.append(game_entry_dict)
    loaded_settings["games"] = games_list

    settings.save_settings(loaded_settings)
    return was_valid


def callback_directory_selected(sender, app_data):
    if add_manual_game_to_settings_file(pathlib.Path(app_data["file_path_name"])):
        dpg.delete_item("directory_picker")
        main.add_new_game_to_games_list(os.path.basename(app_data["file_path_name"]))


def choose_directory():
    if dpg.does_item_exist("directory_picker"):
        dpg.delete_item("directory_picker")

    dpg.add_file_dialog(
        directory_selector=True,
        show=True,
        callback=callback_directory_selected,
        tag="directory_picker",
        width=constants.window_width - 80,
        height=constants.window_height - 80,
        modal=True,
    )
