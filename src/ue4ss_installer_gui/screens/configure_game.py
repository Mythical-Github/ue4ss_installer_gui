import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, ue4ss


def dismiss_configure_game_modal():
    dpg.delete_item("configure_game_modal")


def push_configure_game_screen(game_directory: pathlib.Path):
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        str(game_directory)
    )
    if game_info:
        if dpg.does_item_exist("configure_game_modal"):
            dpg.delete_item("configure_game_modal")
        dpg.add_window(
            modal=True,
            tag="configure_game_modal",
            no_title_bar=True,
            min_size=[524, 200],
        )

        centered_game_name_text = game_info.game_title  # Get the friendly version later

        char_width = 7.25
        text_width = len(centered_game_name_text) * char_width
        available_width = 508
        center_x = int((available_width - text_width) / 2) - 2

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_spacer(width=center_x)
            dpg.add_text(centered_game_name_text)

        with dpg.group(horizontal=True, parent="configure_game_modal", width=-1):
            dpg.add_text("Game Directory:")
            dpg.add_text(str(game_info.install_dir), wrap=420)

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_text("UE4SS Version:")
            # have this default value be grabbed from the settings
            dpg.add_combo(
                items=ue4ss.ALL_TAGS, width=220, default_value=ue4ss.ALL_TAGS[0]
            )
            dpg.add_button(label="Install from zip", width=-1)

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_checkbox(default_value=False)
            dpg.add_text("Enable pre-releases")

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_checkbox(default_value=True)
            dpg.add_text("Keep mods and settings")

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_checkbox(default_value=False)
            dpg.add_text("Install developer version (when applicable)")

        with dpg.group(
            horizontal=True, tag="button_row", parent="configure_game_modal"
        ):
            # have this show based on if the settings game entry has anything under installed files
            dpg.add_button(label="Install")
            dpg.add_button(label="Reinstall", show=False)
            dpg.add_button(label="Uninstall", show=False)
        resize_install_related_buttons()

        dpg.add_separator(parent="configure_game_modal")

        dpg.add_button(
            label="Close",
            parent="configure_game_modal",
            width=-1,
            callback=dismiss_configure_game_modal,
        )


def resize_install_related_buttons():
    all_children = dpg.get_item_children("button_row", 1)  # 1 = user-created widgets
    # Filter to only children that are shown
    visible_children = [
        child
        for child in all_children  # type: ignore
        if dpg.get_item_configuration(child).get("show", True)
    ]

    button_count = len(visible_children)
    if button_count == 0:
        return

    button_width = int(524 / button_count)

    for child_id in visible_children:
        dpg.configure_item(child_id, width=button_width)


#     horizontal
#         switches between
#             reinstall/uninstall or install

# filter default things to install ticked releases download files by
#     "Dev" and "UE4SS"
#     not "Dev" and "UE4SS"
#     if not "Dev" in any "XInput"
