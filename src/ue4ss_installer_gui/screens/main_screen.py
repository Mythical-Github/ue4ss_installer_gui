import os
import webbrowser
import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import add_game, configure_game

from ue4ss_installer_gui import constants, settings, unreal_engine, translator

from ue4ss_installer_gui.checks import online_check


scroll_area_height = (
    constants.WINDOW_HEIGHT
    - (
        constants.HEADER_HEIGHT
        + constants.SUBHEADER_HEIGHT
        + constants.FOOTER_HEIGHT
        + constants.DIVIDER_HEIGHT
        + constants.MARGIN
    )
    - 88
)


used_game_button_strings = set()


def init_main_screen_header():
    with dpg.group(horizontal=True):
        char_width = 10
        title_width = len(constants.APP_TITLE) * char_width
        dpg.add_spacer(width=(constants.WINDOW_WIDTH - title_width) // 2)
        dpg.add_text(
            f"{translator.translator.translate('header_text')}", tag="HeaderText"
        )


def init_main_screen_sub_header():
    subheader_text = f"     {translator.translator.translate('sub_header_text')}"

    with dpg.group(horizontal=False):
        dpg.add_spacer(height=0)
        dpg.add_text(subheader_text, wrap=constants.WINDOW_WIDTH - 40)


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
    global scroll_area_height
    from ue4ss_installer_gui.checks.online_check import is_online

    if not is_online:
        scroll_area_height = scroll_area_height + 40
    with dpg.child_window(
        width=-1, height=scroll_area_height, tag="GameListScroll", autosize_x=True
    ):
        pass

    refresh_game_list_scroll_box()


def refresh_game_list_scroll_box():
    global used_game_button_strings
    used_game_button_strings.clear()
    dpg.delete_item("GameListScroll", children_only=True)

    game_titles_to_install_dirs = settings.get_game_titles_to_install_dirs()
    all_game_titles = sorted(game_titles_to_install_dirs.keys())
    print(all_game_titles)

    for game_name in all_game_titles:
        add_new_game_to_games_list(game_name, game_titles_to_install_dirs[game_name])


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
    )


def add_games_dir_to_scan_list(sender, app_data, user_data):
    games_dir = app_data["file_path_name"]
    games_dir = os.path.normpath(games_dir)

    loaded_settings = settings.get_settings()
    extra_games_dirs_to_scan = loaded_settings.get("custom_game_directories", [])

    if games_dir not in extra_games_dirs_to_scan:
        extra_games_dirs_to_scan.append(games_dir)
        loaded_settings["custom_game_directories"] = extra_games_dirs_to_scan
        settings.save_settings(loaded_settings)
        games_list_path = []
        for (
            game_path
        ) in unreal_engine.get_all_unreal_game_directories_in_directory_tree(games_dir):
            games_list_path.append(pathlib.Path(game_path))
        settings.save_settings(
            add_game.add_manual_games_to_settings_file(games_list_path)
        )
        refresh_game_list_scroll_box()


def init_main_screen_footer_section():
    with dpg.child_window(
        width=-1,
        height=constants.FOOTER_HEIGHT,
        autosize_x=True,
        autosize_y=True,
        border=False,
    ):
        with dpg.group(horizontal=True):
            dpg.add_button(
                label=translator.translator.translate(
                    "add_directory_to_scan_for_games_button_text"
                ),
                height=30,
                tag="agdb",
                width=280,
            )
            dpg.set_item_callback("agdb", callback=push_custom_games_dir_dir_selector)

            dpg.add_button(
                label=translator.translator.translate("add_game_by_game_directory"),
                height=30,
                tag="ag",
                width=280,
            )
            dpg.set_item_callback("ag", callback=add_game.choose_directory)

        dpg.add_spacer()

        with dpg.group(
            horizontal=True, tag="socials_group", show=online_check.is_online
        ):
            discord_button = dpg.add_button(
                label=translator.translator.translate("docs_button_text"),
                width=184,
                height=30,
            )
            dpg.set_item_callback(
                discord_button, lambda: webbrowser.open("https://docs.ue4ss.com/")
            )

            discord_button = dpg.add_button(
                label=translator.translator.translate("discord_button_text"),
                width=184,
                height=30,
            )
            dpg.set_item_callback(
                discord_button,
                lambda: webbrowser.open("https://discord.com/invite/7qhRGHF9Tt"),
            )

            github_button = dpg.add_button(
                label=translator.translator.translate("github_button_text"),
                width=184,
                height=30,
            )
            dpg.set_item_callback(
                github_button,
                lambda: webbrowser.open("https://github.com/UE4SS-RE/RE-UE4SS"),
            )


def push_main_screen():
    with dpg.window(
        label=translator.translator.translate("header_text"),
        tag="main_window",
        no_title_bar=True,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
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
