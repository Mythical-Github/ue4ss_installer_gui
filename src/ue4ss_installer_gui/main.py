import os
import dearpygui.dearpygui as dpg

from ue4ss_installer_gui.screens import main_screen as main_screen
from ue4ss_installer_gui import file_io, constants, settings, logger, initialization, translator


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


def on_viewport_ready(sender, app_data):
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

    dpg.create_viewport(
        title=constants.APP_TITLE,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        resizable=False,
    )
    dpg.set_viewport_small_icon(icon_path)
    dpg.set_viewport_large_icon(icon_path)

    main_screen.push_main_screen()
    dpg.set_viewport_pos([constants.X, constants.Y])
    dpg.setup_dearpygui()
    dpg.set_primary_window("main_window", True)

    dpg.set_viewport_resize_callback(on_viewport_ready)

    remove_maximize_button(constants.APP_TITLE)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
