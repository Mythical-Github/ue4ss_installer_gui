import dearpygui.dearpygui as dpg

def create_theme():
    with dpg.theme() as theme:
        # All items (core)
        with dpg.theme_component(dpg.mvAll):
            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, (192, 202, 245, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (150, 150, 150, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (122, 162, 247, 100), category=dpg.mvThemeCat_Core)

            # Window
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (36, 40, 59, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (41, 46, 66, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (41, 46, 66, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (36, 40, 59, 150), category=dpg.mvThemeCat_Core)

            # Header (e.g., Tree, CollapsingHeader)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (122, 162, 247, 200), category=dpg.mvThemeCat_Core)

            # Buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, (59, 66, 97, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)

            # Frame (e.g., inputs, sliders)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (59, 66, 97, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (122, 162, 247, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (86, 95, 137, 100), category=dpg.mvThemeCat_Core)

            # Tabs
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (59, 66, 97, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (50, 54, 79, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (59, 66, 97, 255), category=dpg.mvThemeCat_Core)

            # Separator
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)

            # Resize grip
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (59, 66, 97, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (50, 54, 79, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)

            # Check mark and sliders
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)

            # Title and menubar
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (41, 46, 66, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (43, 51, 79, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (36, 40, 59, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (36, 40, 59, 255), category=dpg.mvThemeCat_Core)

            # Borders and shadows
            dpg.add_theme_color(dpg.mvThemeCol_Border, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

            # Misc
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (122, 162, 247, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (36, 40, 59, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (122, 162, 247, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (122, 162, 247, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (36, 40, 59, 150), category=dpg.mvThemeCat_Core)

        # Table-specific
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (86, 95, 137, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (122, 162, 247, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (122, 162, 247, 200), category=dpg.mvThemeCat_Core)

    return theme
