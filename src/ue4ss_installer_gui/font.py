import os

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings


def set_application_font():
    if settings.get_use_custom_font_from_settings():
        font_path = settings.get_custom_font_path_from_settings()
    else:
        font_path = 0

    font_tag = f"{font_path}_font"

    font_path_str = str(font_path) if isinstance(font_path, str) else None
    normalized_path = os.path.normpath(font_path_str) if font_path_str else None

    if normalized_path and os.path.exists(normalized_path):
        if not dpg.does_item_exist(font_tag):
            with dpg.font_registry():
                dpg.add_font(normalized_path, 14, tag=font_tag)
            print(f'font_tag generated: "{font_tag}"')
        dpg.bind_font(font_tag)
    else:
        dpg.bind_font(0)
