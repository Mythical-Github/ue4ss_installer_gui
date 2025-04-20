import webbrowser
import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import add_game, configure_game

from ue4ss_installer_gui import constants, settings


scroll_area_height = (
    constants.WINDOW_HEIGHT
    - (
        constants.HEADER_HEIGHT
        + constants.SUBHEADER_HEIGHT
        + constants.FOOTER_HEIGHT
        + constants.DIVIDER_HEIGHT
        + constants.MARGIN
    )
    - 60
)


used_game_button_strings = set()


def init_main_screen_header():
    with dpg.group(horizontal=True):
        char_width = 10
        title_width = len(constants.APP_TITLE) * char_width
        dpg.add_spacer(width=(constants.WINDOW_WIDTH - title_width) // 2)
        dpg.add_text(constants.APP_TITLE, tag="HeaderText")
        dpg.bind_item_font("HeaderText", "header_font")


def init_main_screen_sub_header():
    subheader_text = (
        "     To install UE4SS, choose one of the games below, or add a game manually"
    )

    with dpg.group(horizontal=False):
        dpg.add_spacer(height=0)
        dpg.add_text(subheader_text, wrap=constants.WINDOW_WIDTH - 40)


def add_new_game_button_pressed_callback(sender, app_data, user_data):
    configure_game.push_configure_game_screen(game_directory=pathlib.Path(user_data))


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
            callback=add_new_game_button_pressed_callback,
        )
    dpg.add_spacer(height=6, parent="GameListScroll")


def init_main_screen_game_list_scroll_box():
    with dpg.child_window(
        width=-1, height=scroll_area_height, tag="GameListScroll", autosize_x=True
    ):
        game_titles_to_install_dirs = settings.get_game_titles_to_install_dirs()
        all_game_titles = sorted(game_titles_to_install_dirs.keys())

        for game_name in all_game_titles:
            add_new_game_to_games_list(
                game_name, game_titles_to_install_dirs[game_name]
            )


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

            dpg.add_spacer(width=constants.WINDOW_WIDTH - (4 * 50 + 20 + 160) - 24)

            dpg.add_button(label="Add Game Manually", width=160, height=30, tag="ag")
            dpg.set_item_callback("ag", callback=add_game.choose_directory)


def push_main_screen():
    with dpg.window(
        label=constants.APP_TITLE,
        tag="main_window",
        no_title_bar=True,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
    ):
        dpg.add_spacer(height=10)
        init_main_screen_header()
        dpg.add_spacer(height=5)
        init_main_screen_sub_header()
        dpg.add_spacer(height=10)
        init_main_screen_game_list_scroll_box()
        dpg.add_spacer(height=10)
        init_main_screen_footer_section()
