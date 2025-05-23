import dearpygui.dearpygui as dpg


def create_theme():
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            # Backgrounds — dark grey
            dpg.add_theme_color(
                dpg.mvThemeCol_WindowBg, (25, 25, 25, 255)
            )  # Deep dark grey
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (35, 35, 35, 255))

            # Borders — neon pink
            dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 20, 147, 255))  # Hot pink
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 255))

            # Text — neon cyan/blue
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 255, 255))  # Bright cyan
            dpg.add_theme_color(
                dpg.mvThemeCol_TextSelectedBg, (255, 20, 147, 150)
            )  # Pink highlight

            # Buttons — neon blue/pink vibes
            dpg.add_theme_color(
                dpg.mvThemeCol_Button, (0, 255, 255, 40)
            )  # Transparent neon blue
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, (255, 20, 147, 100)
            )  # Transparent neon pink
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonActive, (0, 255, 255, 100)
            )  # Bright blue

            # Frames — matching the console tone
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBg, (50, 50, 50, 255)
            )  # Medium dark
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgHovered, (255, 20, 147, 60)
            )  # Pink glow
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgActive, (0, 255, 255, 80)
            )  # Blue glow

            # Scrollbar — style it too
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (0, 255, 255, 150))
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrabHovered, (255, 20, 147, 180)
            )
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (0, 255, 255, 255))

    return theme_id
