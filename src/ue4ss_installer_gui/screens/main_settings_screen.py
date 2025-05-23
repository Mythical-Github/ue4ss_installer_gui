import os
import sys
import subprocess

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings
import ue4ss_installer_gui.theme_management


def open_settings_file_in_default_text_editor(sender, app_data, user_data):
    settings_path = settings.SETTINGS_FILE

    if not os.path.isfile(settings_path):
        print(f"Settings file does not exist: {settings_path}")
        return

    try:
        if sys.platform.startswith('win'):
            os.startfile(settings_path)
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', settings_path])
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', settings_path])
        else:
            print("Unsupported OS.")
    except Exception as e:
        print(f"Failed to open settings file: {e}")


def toggle_force_offline_mode_in_settings_file(sender, app_data, user_data):
    loaded_settings = settings.get_settings()
    gui_settings = loaded_settings.get('GUI', {})
    gui_settings['use_force_offline_mode'] = app_data
    loaded_settings['GUI'] = gui_settings
    settings.save_settings(loaded_settings)


def get_system_font_path():
    import platform
    system = platform.system()
    if system == "Windows":
        return os.path.normpath("C:/Windows/Fonts/arial.ttf")
    elif system == "Linux":
        possible_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
        for path in possible_paths:
            if os.path.isfile(path):
                return path
    return None


def toggle_use_custom_font_in_settings_file(sender, app_data, user_data):
    # this needs to set the actual default font later on toggle off
    # this needs to toggle disabling the group containing the font path and font change button
    loaded_settings = settings.get_settings()
    gui_settings = loaded_settings.get('GUI', {})
    gui_settings['use_custom_font'] = app_data
    loaded_settings['GUI'] = gui_settings
    settings.save_settings(loaded_settings)

    if app_data:
        font_path = settings.get_settings().get("GUI", {}).get("custom_font_path", "")
    else:
        font_path = get_system_font_path()

    if dpg.does_item_exist("font_reg"):
        dpg.delete_item("font_reg")

    if font_path and os.path.exists(font_path):
        with dpg.font_registry(tag='font_reg'):
            with dpg.font(font_path, 14) as custom_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(custom_font)
    


def add_centered_text(text, parent):
    char_width = 7.25
    available_width = 498

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=center_x)
        dpg.add_text(text)


def close_main_settings_menu():
    dpg.delete_item("main_settings_screen")


def theme_selected(sender, app_data, user_data):
    loaded_settings = settings.get_settings() or {}
    gui_settings = loaded_settings.setdefault('GUI', {})
    gui_settings['preferred_theme'] = app_data or 'default'
    settings.save_settings(loaded_settings)
    dpg.bind_theme(ue4ss_installer_gui.theme_management.get_theme_from_theme_name(app_data or 'default'))


def push_main_settings_screen():
    if dpg.does_item_exist("main_settings_screen"):
        dpg.delete_item("main_settings_screen")

    with dpg.window(
        tag="main_settings_screen",
        no_title_bar=True,
        no_open_over_existing_popup=False,
        min_size=[524, 400],
        max_size=[524, 999],
        autosize=True,
        modal=True,
        no_move=True,
        no_resize=True,
    ):
        add_centered_text('Settings', parent='main_settings_screen')

        dpg.add_separator()
        dpg.add_spacer(height=2)
        
    
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                callback=toggle_use_custom_font_in_settings_file, 
                default_value=settings.get_settings().get('GUI', {}).get('use_custom_font', False)
            )
            dpg.add_text('Use custom font')
        with dpg.group(enabled=False, tag='font_holder'):
            dpg.add_text(default_value=f'Font path: {settings.get_settings().get("GUI", {}).get("custom_font_path", "")}')
            dpg.add_button(label='Change font path', width=-1, height=28)

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_checkbox()
            dpg.add_text('Use language override')

        with dpg.group(horizontal=True, enabled=False):
            items = ['test', 'test_two', 'test_three']
            dpg.add_text(default_value='Language override')
            dpg.add_combo(items=items, width=-1)

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_checkbox(default_value=True)
            dpg.add_text('Use automatic game detection scanning')

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True):
            dpg.add_checkbox(callback=toggle_force_offline_mode_in_settings_file, default_value=settings.get_settings().get('GUI', {}).get('use_force_offline_mode', False))
            dpg.add_text('Force offline mode (requires restart)')

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)


        with dpg.group(horizontal=True):
            after_default_items = sorted(theme_name for theme_name in ue4ss_installer_gui.theme_management.theme_labels_to_themes if theme_name != 'default')
            after_default_items.insert(0, 'default')
            dpg.add_text(default_value='Theme')
            dpg.add_combo(
                items=after_default_items, 
                width=-1, 
                default_value=ue4ss_installer_gui.theme_management.get_preferred_theme_name(), 
                callback=theme_selected
            )

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=2)

        with dpg.group(horizontal=True, tag='test', horizontal_spacing=7):
            dpg.add_button(label='Edit settings file', width=250, height=28)
            dpg.add_button(label='Open settings file', width=250, height=28, callback=open_settings_file_in_default_text_editor)

        dpg.add_spacer(height=2)
        dpg.add_separator()
        dpg.add_spacer(height=0)

        dpg.add_button(label='Close', height=28, width=-1, callback=close_main_settings_menu)
