import dearpygui.dearpygui as dpg


def create_theme():
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            # Backgrounds — darker spooky purple
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 15, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 15, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 10, 30, 255))

            # Border — deep burnt orange
            border_orange = (200, 80, 0, 255)
            dpg.add_theme_color(dpg.mvThemeCol_Border, border_orange)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, border_orange)

            # Button — Halloween orange
            dpg.add_theme_color(dpg.mvThemeCol_Button, border_orange)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 100, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 60, 0, 255))

            # Frame background — purple tone
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (70, 35, 90, 255))

            # Text — candle yellow
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 240, 160, 255))

            # Scrollbar — orange hues
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (200, 100, 40, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrabHovered, (230, 130, 60, 255)
            )
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (180, 90, 30, 255))

    return theme_id
