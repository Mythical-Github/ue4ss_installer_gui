import dearpygui.dearpygui as dpg


def create_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            # Base Backgrounds
            dpg.add_theme_color(
                dpg.mvThemeCol_WindowBg, (15, 5, 30, 255)
            )  # Dark purple-blue
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (10, 0, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 0, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (0, 0, 0, 200))

            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 20, 147, 255))  # Neon Pink
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (130, 130, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (255, 0, 255, 80))

            # Headers
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 255, 150, 255))  # Neon Green
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderHovered, (255, 105, 180, 255)
            )  # Hot Pink
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderActive, (0, 200, 255, 255)
            )  # Jaguar Blue

            # Buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, (55, 0, 85, 255))  # Purple
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, (138, 43, 226, 255)
            )  # Bright Violet
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonActive, (0, 255, 180, 255)
            )  # Cyan Green

            # Frame
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 20, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (255, 0, 255, 100))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (0, 255, 127, 255))

            # Tabs
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (50, 0, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (255, 20, 147, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (0, 255, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (30, 0, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (55, 0, 80, 255))

            # Slider/Check
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 0, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (0, 255, 127, 255))

            # Scrollbars
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (10, 10, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (255, 0, 255, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrabHovered, (255, 105, 180, 255)
            )
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (0, 255, 150, 255))

            # Resize Grip
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (255, 0, 255, 100))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (255, 105, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (0, 255, 127, 255))

            # Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 0, 255, 80))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))

            # Title Bar & Menu
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (20, 0, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (138, 43, 226, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (10, 0, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (25, 0, 40, 255))

            # Misc
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (255, 0, 255, 100))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (255, 20, 147, 180))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (0, 255, 180, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_NavWindowingHighlight, (0, 255, 127, 255)
            )
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (0, 0, 0, 150))

            # Rounded corners
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 6)

    return theme
