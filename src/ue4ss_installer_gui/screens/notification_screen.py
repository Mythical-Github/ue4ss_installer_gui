import pathlib
import dearpygui.dearpygui as dpg



def add_centered_text(text, parent):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=center_x)
        dpg.add_text(text)


def push_notification_screen(
    notification_text: str,
    game_directory: pathlib.Path
):
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
        height=-1
    ):
        add_centered_text(notification_text, parent="notification_modal")
        dpg.add_spacer()
        dpg.add_button(
            label="Close",
            width=-1,
            height=28,
            callback=configure_game.push_configure_game_screen,
            user_data=game_directory
        )