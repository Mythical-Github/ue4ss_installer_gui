import dearpygui.dearpygui as dpg

def create_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, (170, 180, 220, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (90, 90, 120, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (100, 130, 255, 120), category=dpg.mvThemeCat_Core)

            # Window Backgrounds - deep dark blue-purple
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (22, 25, 40, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (28, 31, 50, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (28, 31, 50, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (22, 25, 40, 180), category=dpg.mvThemeCat_Core)

            # Headers
            dpg.add_theme_color(dpg.mvThemeCol_Header, (55, 60, 90, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (100, 130, 255, 180), category=dpg.mvThemeCat_Core)

            # Buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, (40, 45, 70, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (70, 80, 120, 255), category=dpg.mvThemeCat_Core)

            # Frames (inputs, sliders)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 45, 70, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (100, 130, 255, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 80, 120, 150), category=dpg.mvThemeCat_Core)

            # Tabs
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (40, 45, 70, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (70, 80, 120, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (25, 30, 45, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (40, 45, 70, 255), category=dpg.mvThemeCat_Core)

            # Separators
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (55, 60, 90, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (25, 30, 45, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (55, 60, 90, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)

            # Check marks and sliders
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (70, 80, 120, 255), category=dpg.mvThemeCat_Core)

            # Title and menubar backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (28, 31, 50, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (38, 42, 68, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (22, 25, 40, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (22, 25, 40, 255), category=dpg.mvThemeCat_Core)

            # Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border, (55, 60, 90, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

            # Misc (drag drop, docking)
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (100, 130, 255, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (22, 25, 40, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (100, 130, 255, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (100, 130, 255, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (22, 25, 40, 180), category=dpg.mvThemeCat_Core)

            # Rounded corners
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 6)

        # Table headers
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (55, 60, 90, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (100, 130, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (100, 130, 255, 180), category=dpg.mvThemeCat_Core)


    return theme
