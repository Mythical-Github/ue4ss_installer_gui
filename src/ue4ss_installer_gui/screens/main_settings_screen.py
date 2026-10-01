import os
import sys
import subprocess
from typing import Any, Callable

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, auto_align, font, constants, file_io, grid , translator
import ue4ss_installer_gui.theme_management
from ue4ss_installer_gui.screens import text_editor_screen


def get_valid_language_options() -> list[str]:
    specified_dir = os.path.normpath(f"{file_io.SCRIPT_DIR}/assets/localization")

    if not os.path.isdir(specified_dir):
        return []

    language_options = [
        os.path.splitext(file)[0]
        for file in os.listdir(specified_dir)
        if os.path.isfile(os.path.join(specified_dir, file))
    ]

    return language_options


def change_font_button_selected(sender, app_data, user_data):
    if dpg.does_item_exist("font_picker"):
        dpg.delete_item("font_picker")

    dpg.add_file_dialog(
        directory_selector=False,
        show=True,
        callback=save_new_font,
        cancel_callback=push_main_settings_screen,
        tag="font_picker",
        width=constants.WINDOW_WIDTH - 80,
        height=constants.WINDOW_HEIGHT - 80,
        modal=True,
        file_count=999,
        user_data=user_data,
    )
    dpg.add_file_extension(parent="font_picker", extension=".ttf")
    dpg.add_file_extension(parent="font_picker", extension=".otf")


def open_settings_file_in_default_text_editor(sender, app_data, user_data):
    settings_path = settings.SETTINGS_FILE

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


def close_main_settings_menu():
    dpg.delete_item("main_settings_screen")


def push_main_settings_screen():
    if dpg.does_item_exist("main_settings_screen"):
        dpg.delete_item("main_settings_screen")

    with dpg.window(
        tag="main_settings_screen",
        no_title_bar=True,
        no_open_over_existing_popup=False,
        min_size=[524, 340],
        max_size=[524, 9999],
        autosize=True,
        modal=True,
        no_move=True,
        no_resize=True,
    ):
        # auto_align.add_centered_text("Settings", parent="main_settings_screen")
        auto_align.add_multi_line_centered_text(
            "Settings", parent="main_settings_screen"
        )

        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_text(f"{translator.translator.translate('Global_font_scale')}")
            dpg.add_drag_float(
                default_value=settings.get_global_font_scale_from_settings(),
                speed=0.1,
                min_value=0.8,
                max_value=2,
                width=-1,
                callback=set_font_scale_and_save,
                drop_callback=set_font_scale_and_save,
                tag="global_font_scale_slider",
            )

        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                callback=toggle_using_custom_font,
                default_value=settings.get_use_custom_font_from_settings(),
            )
            dpg.add_text(f"{translator.translator.translate('Use_custom_font')}")
        with dpg.group(
            enabled=settings.get_use_custom_font_from_settings(), tag="font_holder"
        ):
            dpg.add_text(
               default_value = f"{translator.translator.translate('font_path')}{settings.get_custom_font_path_from_settings()}"
            )
            dpg.add_button(
                label=f"{translator.translator.translate('Change_font_path')}",
                width=-1,
                height=28,
                callback=change_font_button_selected,
            )

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                callback=toggle_use_language_override,
                default_value=settings.get_use_language_override_from_settings(),
            )
            dpg.add_text(f"{translator.translator.translate('Use_language_override')}")

        with dpg.group(
            horizontal=True,
            enabled=settings.get_use_language_override_from_settings(),
            tag="lang_override_group",
        ):
            dpg.add_text(default_value=f"{translator.translator.translate('Language_override')}")
            default_combo_value = settings.get_language_from_settings()
            dpg.add_combo(
                items=get_valid_language_options(),
                width=-1,
                callback=settings.language_combo_box_selection_changed,
                default_value=default_combo_value,
            )

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            default = settings.get_use_automatic_game_scanning_in_settings()
            dpg.add_checkbox(
                default_value=default,
                callback=settings.toggle_use_automatic_game_scanning_in_settings_file,
            )
            dpg.add_text(f"{translator.translator.translate('Use_automatic_game_detection_scanning')}")

        with dpg.group(horizontal=False):
            dpg.add_spacer(height=2)
            dpg.add_separator()
            dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                callback=settings.toggle_force_offline_mode_in_settings_file,
                default_value=settings.get_use_force_online_mode_in_settings(),
            )
            dpg.add_text(f"{translator.translator.translate('Force_offline_mode')}")

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            after_default_items = sorted(
                theme_name
                for theme_name in ue4ss_installer_gui.theme_management.theme_labels_to_themes
                if theme_name != settings.get_default_theme_name()
            )
            after_default_items.insert(0, settings.get_default_theme_name())
            dpg.add_text(default_value=f"{translator.translator.translate('Theme')}")
            dpg.add_combo(
                items=after_default_items,
                width=-1,
                default_value=ue4ss_installer_gui.theme_management.get_preferred_theme_name(),
                callback=theme_selected,
            )

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        screen_info = {
            "finished_callback": push_main_settings_screen,
            "file_path": settings.SETTINGS_FILE,
        }

        example_variable: dict[str, dict[Callable[..., Any], dict[str, Any]]] = {
            "button_1": {
                dpg.add_button: {
                    "label": f"{translator.translator.translate('Edit_settings_file')}",
                    "width": -1,
                    "height": 28,
                    "callback": text_editor_screen.push_text_editor_screen,
                    "user_data": screen_info,
                }
            },
            "button_2": {
                dpg.add_button: {
                    "label": f"{translator.translator.translate('Open_settings_file')}",
                    "width": -1,
                    "height": 28,
                    "callback": open_settings_file_in_default_text_editor,
                }
            },
        }

        grid.add_spaced_item_grid(example_variable)

        dpg.add_button(
            label= f"{translator.translator.translate('close_button_text')}", height=28, width=-1, callback=close_main_settings_menu
        )


def set_font_scale_and_save():
    font_scale = dpg.get_value("global_font_scale_slider")
    dpg.set_global_font_scale(font_scale)
    settings.save_global_font_scale(font_scale=font_scale)


def save_new_font(sender, app_data, user_data):
    settings.save_custom_font_path_to_settings(app_data)
    print(app_data["file_path_name"])
    font.set_application_font()
    push_main_settings_screen()


def toggle_using_custom_font(sender, app_data, user_data):
    settings.toggle_use_custom_font_in_settings_file(app_data)
    font.set_application_font()
    dpg.configure_item("font_holder", enabled=app_data)


def toggle_use_language_override(sender, app_data, user_data):
    # when setting to off set it back to the current system local if valid otherwise english
    settings.toggle_use_language_override_in_settings_file(app_data)
    dpg.configure_item("lang_override_group", enabled=app_data)


def theme_selected(sender, app_data, user_data):
    settings.change_preferred_theme_in_settings(app_data)
    dpg.bind_theme(
        ue4ss_installer_gui.theme_management.get_theme_from_theme_name(  # type: ignore
            app_data or "default"
        )
    )
