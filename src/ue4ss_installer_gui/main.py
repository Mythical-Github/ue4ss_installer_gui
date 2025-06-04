import os
import time

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import main_screen
from ue4ss_installer_gui import file_io, constants, settings, initialization, font
import ue4ss_installer_gui.theme_management


def remove_maximize_button(title=constants.APP_TITLE):
    if settings.is_windows():
        import ctypes

        GWL_STYLE = -16
        WS_MAXIMIZEBOX = 0x00010000
        WS_THICKFRAME = 0x00040000
        SWP_FLAGS = 0x0027

        hwnd = ctypes.windll.user32.FindWindowW(None, title)

        original_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)

        new_style = original_style & ~WS_MAXIMIZEBOX & ~WS_THICKFRAME

        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)

        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_FLAGS)


last_resize_time = 0
RESIZE_THROTTLE_SECONDS = 0.25


def on_viewport_ready(sender, app_data):
    global last_resize_time

    now = time.time()
    if now - last_resize_time < RESIZE_THROTTLE_SECONDS:
        return

    last_resize_time = now

    app_x_position = dpg.get_viewport_pos()[0]
    app_y_position = dpg.get_viewport_pos()[1]
    app_width = dpg.get_viewport_width()
    app_height = dpg.get_viewport_height()

    settings.set_app_window_properties_in_settings(
        app_width, app_height, app_x_position, app_y_position
    )

    remove_maximize_button(constants.APP_TITLE)


def main():
    initialization.init()

    if settings.is_windows():
        icon_path = os.path.normpath(
            f"{file_io.SCRIPT_DIR}/assets/images/project_main_icon.ico"
        )
    else:
        icon_path = os.path.normpath(
            f"{file_io.SCRIPT_DIR}/assets/images/project_main_icon.png"
        )
    if not os.path.isfile(icon_path):
        raise FileNotFoundError(f"Icon file not found at {icon_path}")

    dpg.create_context()

    dpg.bind_theme(ue4ss_installer_gui.theme_management.get_preferred_theme())  # type: ignore

    gui_settings = settings.get_settings_gui_section_from_settings()

    viewport_x = gui_settings.get("x", constants.X)
    viewport_y = gui_settings.get("y", constants.Y)
    viewport_width = gui_settings.get("width", constants.WINDOW_WIDTH)
    viewport_height = gui_settings.get("height", constants.WINDOW_HEIGHT)

    dpg.create_viewport(
        title=constants.APP_TITLE,
        width=viewport_width,
        height=viewport_height,
        x_pos=viewport_x,
        y_pos=viewport_y,
        resizable=False,
    )

    dpg.set_viewport_small_icon(icon_path)
    dpg.set_viewport_large_icon(icon_path)
    dpg.set_global_font_scale(settings.get_global_font_scale_from_settings())
    dpg.configure_app(auto_device=True)

    font.set_application_font()

    main_screen.push_main_app_screen()

    dpg.set_viewport_pos([viewport_x, viewport_y])
    dpg.setup_dearpygui()
    dpg.set_primary_window("main_app_screen", True)

    dpg.set_viewport_resize_callback(on_viewport_ready)

    remove_maximize_button(constants.APP_TITLE)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
