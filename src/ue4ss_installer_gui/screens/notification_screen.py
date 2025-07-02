import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import auto_align,translator


def push_notification_screen(notification_text: str, game_directory: pathlib.Path):
    from ue4ss_installer_gui.screens import configure_game

    if dpg.does_item_exist("notification_modal"):
        dpg.delete_item("notification_modal")

    with dpg.window(
        tag="notification_modal",
        modal=True,
        no_title_bar=True,
        min_size=[524, 1],
        no_open_over_existing_popup=False,
        no_resize=True,
        height=-1,
        no_move=True,
    ):
        auto_align.add_centered_text(notification_text, parent="notification_modal")
        dpg.add_spacer()
        dpg.add_button(
            label= f"{translator.translator.translate('close_button_text')}",
            width=-1,
            height=28,
            callback=configure_game.push_configure_game_screen,
            user_data=game_directory,
        )
