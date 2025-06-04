import os
import pathlib
import webbrowser
from typing import Callable, Any

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import (
    add_game,
    configure_game,
    main_ue4ss_screen,
    main_settings_screen,
    scanning_for_games,
)

from ue4ss_installer_gui import (
    constants,
    settings,
    translator,
    auto_align,
    unreal_engine,
    grid,
)

from ue4ss_installer_gui.checks import online_check


def get_footer_height() -> int:
    if online_check.is_online:
        FOOTER_HEIGHT = 20
    else:
        FOOTER_HEIGHT = 40
    return FOOTER_HEIGHT


scroll_area_height = (
    constants.WINDOW_HEIGHT
    - (
        constants.HEADER_HEIGHT
        + constants.SUBHEADER_HEIGHT
        + get_footer_height()
        + constants.DIVIDER_HEIGHT
        + constants.MARGIN
    )
    - 98
)


used_game_button_strings = set()


def init_main_screen_header():
    with dpg.group():
        auto_align.add_centered_text(
            f"{translator.translator.translate('header_text')}",
            auto_align.AlignmentType.HORIZONTAL,
            tag="HeaderText",
        )


def init_main_screen_sub_header():
    with dpg.group():
        auto_align.add_centered_text(
            f"{translator.translator.translate('sub_header_text')}",
            auto_align.AlignmentType.HORIZONTAL,
            tag="SubHeaderText",
        )


def game_button_clicked_callback(sender, app_data, user_data):
    configure_game.push_configure_game_screen(
        sender, app_data, user_data=pathlib.Path(user_data)
    )


def add_new_game_to_games_list(game_name: str, game_directory: str):
    global used_game_button_strings
    base_name = game_name
    count = 1

    while game_name in used_game_button_strings:
        count += 1
        game_name = f"{base_name} #{count}"

    used_game_button_strings.add(game_name)

    with dpg.group(horizontal=True, parent="GameListScroll"):
        dpg.add_button(
            label=game_name,
            tag=f"{game_name}_button",
            width=-1,
            height=28,
            user_data=game_directory,
            callback=game_button_clicked_callback,
        )
    dpg.add_spacer(height=6, parent="GameListScroll")


def init_main_screen_game_list_scroll_box():
    scroll_area_height = (
        constants.WINDOW_HEIGHT
        - (
            constants.HEADER_HEIGHT
            + constants.SUBHEADER_HEIGHT
            + get_footer_height()
            + constants.DIVIDER_HEIGHT
            + constants.MARGIN
        )
        - 98
    )

    if not online_check.is_online:
        scroll_area_height = scroll_area_height + 20
    with dpg.child_window(
        width=-1, height=scroll_area_height, tag="GameListScroll", autosize_x=True
    ):
        pass

    refresh_game_list_scroll_box()


def refresh_game_list_scroll_box():
    global used_game_button_strings
    used_game_button_strings.clear()
    dpg.delete_item("GameListScroll", children_only=True)

    install_dirs_to_game_titles = settings.get_install_dirs_to_game_titles()

    sorted_items = sorted(
        install_dirs_to_game_titles.items(), key=lambda item: item[1].lower()
    )

    for install_dir, game_title in sorted_items:
        add_new_game_to_games_list(game_title, install_dir)


def push_custom_games_dir_dir_selector(sender, app_data, user_data):
    if dpg.does_item_exist("directory_picker"):
        dpg.delete_item("directory_picker")

    dpg.add_file_dialog(
        directory_selector=True,
        show=True,
        callback=add_games_dir_to_scan_list,
        tag="directory_picker",
        width=constants.WINDOW_WIDTH - 80,
        height=constants.WINDOW_HEIGHT - 80,
        modal=True,
        user_data=user_data,
        cancel_callback=main_ue4ss_screen.push_main_screen,
    )


def add_custom_game_directory(games_dir):
    loaded_settings = settings.get_settings()
    extra_games_dirs_to_scan = settings.get_custom_game_directories()
    extra_games_dirs_to_scan.append(games_dir)
    loaded_settings["custom_game_directories"] = extra_games_dirs_to_scan
    settings.save_settings(loaded_settings)
    games_list_path = []
    for game_path in unreal_engine.get_all_unreal_game_directories_in_directory_tree(
        games_dir
    ):
        games_list_path.append(pathlib.Path(game_path))
    settings.save_settings(
        scanning_for_games.add_manual_games_to_settings_file(games_list_path)
    )


def add_games_dir_to_scan_list(sender, app_data, user_data):
    games_dir = os.path.normpath(app_data["file_path_name"])

    if games_dir not in settings.get_custom_game_directories():
        add_custom_game_directory(games_dir)
        refresh_game_list_scroll_box()


def push_settings_screen():
    main_settings_screen.push_main_settings_screen()


def init_main_screen_footer_section():
    with dpg.child_window(
        width=-1,
        autosize_x=True,
        height=72,
        border=False,
    ):
        directory_buttons: dict[str, dict[Callable[..., Any], dict[str, Any]]] = {
            "button_1": {
                dpg.add_button: {
                    "label": translator.translator.translate(
                        "add_directory_to_scan_for_games_button_text"
                    ),
                    "width": -1,
                    "height": 28,
                    "callback": push_custom_games_dir_dir_selector,
                }
            },
            "button_2": {
                dpg.add_button: {
                    "label": translator.translator.translate(
                        "add_game_by_game_directory"
                    ),
                    "width": -1,
                    "height": 28,
                    "callback": add_game.choose_directory,
                }
            },
        }

        grid.add_spaced_item_grid(directory_buttons)

        dpg.add_spacer(height=-1)

        social_buttons: dict[str, dict[Callable[..., Any], dict[str, Any]]] = {}

        if online_check.is_online:
            social_buttons = {
                "docs_button": {
                    dpg.add_button: {
                        "label": translator.translator.translate("docs_button_text"),
                        "width": -1,
                        "height": 28,
                        "callback": lambda: webbrowser.open("https://docs.ue4ss.com/"),
                    }
                },
                "discord_button": {
                    dpg.add_button: {
                        "label": translator.translator.translate("discord_button_text"),
                        "width": -1,
                        "height": 28,
                        "callback": lambda: webbrowser.open(
                            "https://discord.com/invite/7qhRGHF9Tt"
                        ),
                    }
                },
                "github_button": {
                    dpg.add_button: {
                        "label": translator.translator.translate("github_button_text"),
                        "width": -1,
                        "height": 28,
                        "callback": lambda: webbrowser.open(
                            "https://github.com/UE4SS-RE/RE-UE4SS"
                        ),
                    }
                },
                "settings_button": {
                    dpg.add_button: {
                        "label": "Settings",
                        "width": -1,
                        "height": 28,
                        "callback": push_settings_screen,
                    }
                },
            }
            grid.add_spaced_item_grid(social_buttons, max_rows=1)
        else:
            dpg.add_button(
                label="Settings", width=-1, height=28, callback=push_settings_screen
            )


def push_main_screen():
    if dpg.does_item_exist("main_window"):
        dpg.delete_item("main_window")
    with dpg.window(
        label=translator.translator.translate("header_text"),
        tag="main_window",
        no_title_bar=True,
        width=constants.WINDOW_WIDTH - 18,
        height=constants.WINDOW_HEIGHT - 47,
        no_move=True,
        no_resize=True,
        no_open_over_existing_popup=False,
    ):
        offset = 0
        if settings.is_linux():
            offset = 12
        dpg.add_spacer(height=10 + offset)
        init_main_screen_header()
        dpg.add_spacer(height=6 + offset)
        init_main_screen_sub_header()
        dpg.add_spacer(height=10 + offset)
        init_main_screen_game_list_scroll_box()
        dpg.add_spacer(height=8 + offset)
        init_main_screen_footer_section()
