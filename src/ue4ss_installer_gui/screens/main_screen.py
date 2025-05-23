import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import scanning_for_games
from ue4ss_installer_gui import constants


def add_centered_text(text, parent):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=center_x)
        dpg.add_text(text)


def push_main_app_screen():
    if dpg.does_item_exist("main_app_screen"):
        dpg.delete_item("main_app_screen")

    with dpg.window(
        tag="main_app_screen",
        no_title_bar=True,
        no_open_over_existing_popup=False,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        no_move=True,
        no_resize=True,
        autosize=True
    ):
        scanning_for_games.push_scanning_for_games_modal_screen()
