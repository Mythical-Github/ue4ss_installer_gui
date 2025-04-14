import os
import webbrowser

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import add_game_screen, steam, epic, unreal_engine, constants


scroll_area_height = (
    constants.window_height
    - (
        constants.HEADER_HEIGHT
        + constants.SUBHEADER_HEIGHT
        + constants.FOOTER_HEIGHT
        + constants.DIVIDER_HEIGHT
        + constants.MARGIN
    )
    - 60
)


def init_main_screen_header():
    with dpg.group(horizontal=True):
        title = "UE4SS Installer"
        char_width = 10
        title_width = len(title) * char_width
        dpg.add_spacer(width=(constants.window_width - title_width) // 2)
        dpg.add_text(title, tag="HeaderText")
        dpg.bind_item_font("HeaderText", "header_font")


def init_main_screen_sub_header():
    subheader_text = (
        "     To install UE4SS, choose one of the games below, or add a game manually"
    )

    with dpg.group(horizontal=False):
        dpg.add_spacer(height=0)

        dpg.add_text(subheader_text, wrap=constants.window_width - 40)


def init_main_screen_game_list_scroll_box():
    with dpg.child_window(
        width=-1, height=scroll_area_height, tag="GameListScroll", autosize_x=True
    ):
        # make sure that even games from settings files don't cause double entries from auto detected entries
        all_game_dirs = [
            game
            for dir_source in (
                steam.get_all_steam_game_directories(),
                epic.get_all_epic_games_game_directories(),
            )
            for base_dir in dir_source
            for game in unreal_engine.get_all_unreal_game_directories_in_directory_tree(
                str(base_dir)
            )
        ]

        for game_dir in all_game_dirs:
            add_new_game_to_games_list(os.path.basename(game_dir))


def init_main_screen_footer_section():
    with dpg.child_window(
        width=-1,
        height=constants.FOOTER_HEIGHT,
        autosize_x=True,
        autosize_y=True,
        border=False,
    ):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=True):
                discord_button = dpg.add_button(label="Docs", width=60, height=30)
                dpg.set_item_callback(
                    discord_button, lambda: webbrowser.open("https://docs.ue4ss.com/")
                )

                discord_button = dpg.add_button(label="Discord", width=60, height=30)
                dpg.set_item_callback(
                    discord_button,
                    lambda: webbrowser.open("https://discord.com/invite/7qhRGHF9Tt"),
                )

                github_button = dpg.add_button(label="Github", width=60, height=30)
                dpg.set_item_callback(
                    github_button,
                    lambda: webbrowser.open("https://github.com/UE4SS-RE/RE-UE4SS"),
                )

            dpg.add_spacer(width=constants.window_width - (4 * 50 + 20 + 160) - 24)

            dpg.add_button(label="Add Game Manually", width=160, height=30, tag="ag")
            dpg.set_item_callback("ag", callback=add_game_screen.choose_directory)


def push_main_screen():
    with dpg.window(
        label="UE4SS Installer",
        tag="MainWindow",
        no_title_bar=True,
        width=constants.window_width,
        height=constants.window_height,
    ):
        dpg.add_spacer(height=10)
        init_main_screen_header()
        dpg.add_spacer(height=5)
        init_main_screen_sub_header()
        dpg.add_spacer(height=10)
        init_main_screen_game_list_scroll_box()
        dpg.add_spacer(height=10)
        init_main_screen_footer_section()


def add_new_game_to_games_list(game_name: str):
    with dpg.group(horizontal=True, parent="GameListScroll"):
        dpg.add_spacer()
        dpg.add_button(label=game_name, tag=f"{game_name}_button", width=532, height=28)
        # add a game platform button here, when applicable
        # add a ue4ss version number here, when applicable
        # if a manually installed game, a button to remove it from the settings file
    dpg.add_spacer(height=6, parent="GameListScroll")
