import os
import dearpygui.dearpygui as dpg

from ue4ss_installer import file_io, main_screen, constants, settings


def main():
    settings.init_settings()
    dpg.create_context()

    icon_path = os.path.normpath(f'{file_io.SCRIPT_DIR}/assets/images/project_main_icon.ico')
    if not os.path.isfile(icon_path):
        icon_missing_error = f"Icon file not found at {icon_path}"
        raise FileNotFoundError(icon_missing_error)

    dpg.create_viewport(title=" ", width=constants.window_width, height=constants.window_height, resizable=False)
    dpg.set_viewport_small_icon(icon_path)
    dpg.set_viewport_large_icon(icon_path)

    with dpg.font_registry():
        with dpg.font("C:/Windows/Fonts/segoeui.ttf", 20, tag="header_font"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
    main_screen.push_main_screen()
    dpg.set_viewport_pos([constants.x, constants.y])
    dpg.setup_dearpygui()
    dpg.set_primary_window("MainWindow", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
