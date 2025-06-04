import os
import sys
import subprocess
from typing import Callable, Any


import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import ue4ss, grid
from ue4ss_installer_gui.screens import text_editor_screen, configure_game

# there should be an edit file directly button, and a close button at the bottom
# edit directly brings up a text editor screen
# close button returns to the configure game screen for said game
# above the two above buttons, should be a section that contains a scrollbox containing key value pairs iwth comments in sections that can be edited and toggled


def open_settings_file_callback(sender, app_data, user_data):
    settings_path = str(ue4ss.get_ue4ss_settings_path(user_data))

    if not os.path.isfile(settings_path):
        print(f"Settings file does not exist: {settings_path}")
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(settings_path)
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", settings_path])
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", settings_path])
        else:
            print("Unsupported OS.")
    except Exception as e:
        print(f"Failed to open settings file: {e}")


def edit_settings_file_callback(sender, app_data, user_data):
    if isinstance(user_data, dict):
        payload = user_data
    else:
        payload = {
            "file_path": str(ue4ss.get_ue4ss_settings_path(user_data)),
            "finished_callback": push_screen,
        }

    text_editor_screen.push_text_editor_screen(sender, app_data, payload)


def cancel_edits_callback(sender, app_data, user_data):
    return


def save_edits_callback(sender, app_data, user_data):
    return


def push_screen(sender, app_data, user_data):
    screen_tag = "ue4ss_settings_configurator_screen"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)

    with dpg.window(
        tag=screen_tag,
        modal=True,
        no_title_bar=True,
        no_open_over_existing_popup=False,
        no_resize=True,
        min_size=[524, 400],
        max_size=[524, 9999],
        no_move=True,
    ):
        # settings_path = ue4ss.get_ue4ss_settings_path(user_data)
        # settings_content = file_io.get_contents_of_file(str(settings_path))
        # dpg.add_input_text(tag=f"{screen_tag}_input_text", default_value=settings_content, multiline=True, width=-1, height=340)

        grid_buttons: dict[str, dict[Callable[..., Any], dict[str, Any]]] = {
            "button_3": {
                dpg.add_button: {
                    "label": "Cancel edits",
                    "width": -1,
                    "height": 28,
                    "callback": cancel_edits_callback,
                }
            },
            "button_4": {
                dpg.add_button: {
                    "label": "Save edits",
                    "width": -1,
                    "height": 28,
                    "callback": save_edits_callback,
                }
            },
            "button_1": {
                dpg.add_button: {
                    "label": "Edit settings file",
                    "width": -1,
                    "height": 28,
                    "callback": edit_settings_file_callback,
                    "user_data": user_data,
                }
            },
            "button_2": {
                dpg.add_button: {
                    "label": "Open settings file",
                    "width": -1,
                    "height": 28,
                    "callback": open_settings_file_callback,
                    "user_data": user_data,
                }
            },
        }
        with dpg.child_window(
            width=-1, height=400, tag="ue4ss_settings_scroll", autosize_x=True
        ):
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)
            dpg.add_button(width=-1, height=28)

        grid.add_spaced_item_grid(grid_buttons)

        dpg.add_button(
            label= f"{translator.translator.translate('close_button_text')}",
            height=28,
            width=-1,
            callback=lambda: configure_game.push_configure_game_screen(
                sender, app_data, user_data
            ),
        )
