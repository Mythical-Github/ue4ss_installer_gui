import threading

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, constants
from ue4ss_installer_gui.screens import main_ue4ss_screen


def add_centered_text(text, parent):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=center_x)
        dpg.add_text(text)


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


def async_init_game_scanning():
    settings.init_game_scanning()
    dpg.delete_item("scanning_for_games_screen")
    main_ue4ss_screen.push_main_screen()
