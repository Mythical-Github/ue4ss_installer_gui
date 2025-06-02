import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import scanning_for_games, main_ue4ss_screen
from ue4ss_installer_gui import constants, settings


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
        autosize=True,
    ):
        if settings.get_use_automatic_game_scanning_in_settings():
            scanning_for_games.push_scanning_for_games_modal_screen()
        else:
            main_ue4ss_screen.push_main_screen()
