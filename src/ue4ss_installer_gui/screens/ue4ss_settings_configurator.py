import uuid
import pathlib
import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import configure_game
from ue4ss_installer_gui.ue4ss import (
    parse_ue4ss_settings_file,
    ConfigSection,
    get_ue4ss_settings_path,
)


# finish later, localize all text in this file


def add_centered_text(text, parent):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=center_x)
        dpg.add_text(text)


def push_ue4ss_settings_configurator_screen(sender, app_data, user_data):
    if dpg.does_item_exist("ue4ss_settings_configurator_screen"):
        dpg.delete_item("ue4ss_settings_configurator_screen")

    with dpg.window(
        tag="ue4ss_settings_configurator_screen",
        modal=True,
        no_title_bar=True,
        min_size=[524, 1],
        no_open_over_existing_popup=False,
        no_resize=True,
        height=-1,
    ):
        add_centered_text(
            text="UE4SS Settings Configurator",
            parent="ue4ss_settings_configurator_screen",
        )
        dpg.add_spacer()
        dpg.add_button(
            label=get_settings_editor_toggle_value(),
            width=-1,
            height=28,
            callback=toggle_between_text_and_menu_settings_editor,
            user_data=user_data,
        )
        # add a space then horizontal here with two buttons cancel and save for the text editing of the settings file
        dpg.add_spacer()
        dpg.add_button(
            label="Close",
            width=-1,
            height=28,
            callback=configure_game.push_configure_game_screen,
            user_data=user_data,
        )


def should_show_cancel_and_save_buttons() -> bool:
    should_show_buttons = True
    return should_show_buttons


def refresh_settings_scroll_box(game_exe_directory: pathlib.Path):
    dpg.delete_item("settings_scroll_box", children_only=True)
    add_headers_entry_to_scroll_box(
        "settings_scroll_box",
        parse_ue4ss_settings_file(str(get_ue4ss_settings_path(game_exe_directory))),
    )


def toggle_between_text_and_menu_settings_editor(
    sender, app_data, game_exe_directory: pathlib.Path
):
    # add toggling here later
    refresh_settings_scroll_box(game_exe_directory)


def get_settings_editor_toggle_value() -> str:
    # swap to menu editor, swap to text editor toggle
    return "Swap to text editor"


def add_headers_entry_to_scroll_box(
    scroll_box_tag: str, settings_list: list[ConfigSection]
):
    for entry in settings_list:
        if entry.header == "":
            window_tag = f"settings_scroll_box_{str(uuid.uuid4())}"
        else:
            window_tag = f"settings_scroll_box_{entry.header}_{str(uuid.uuid4())}"
        dpg.add_child_window(parent=scroll_box_tag, tag=window_tag)
        for config_entry in entry.config_entries:
            dpg.add_text(tag=config_entry.key, parent=window_tag)
        dpg.add_spacer(parent=window_tag)


# window
#     sub window, with scrollbox, consistents of section entries, per settings header
#         each section will have the label at the top for the section
#             then a sibwindow within, that has a
