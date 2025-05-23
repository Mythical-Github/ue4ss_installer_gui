import dearpygui.dearpygui as dpg


def create_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            # Text
            dpg.add_theme_color(
                dpg.mvThemeCol_Text, (248, 248, 242, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TextDisabled,
                (98, 114, 164, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TextSelectedBg,
                (68, 71, 90, 255),
                category=dpg.mvThemeCat_Core,
            )

            # Window
            dpg.add_theme_color(
                dpg.mvThemeCol_WindowBg, (40, 42, 54, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ChildBg, (40, 42, 54, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_PopupBg, (40, 42, 54, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ModalWindowDimBg,
                (40, 42, 54, 150),
                category=dpg.mvThemeCat_Core,
            )

            # Headers
            dpg.add_theme_color(
                dpg.mvThemeCol_Header,
                (255, 184, 108, 255),
                category=dpg.mvThemeCat_Core,
            )  # Orange
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderHovered,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderActive,
                (189, 147, 249, 255),
                category=dpg.mvThemeCat_Core,
            )  # Purple

            # Buttons
            dpg.add_theme_color(
                dpg.mvThemeCol_Button, (68, 71, 90, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered,
                (139, 233, 253, 255),
                category=dpg.mvThemeCat_Core,
            )  # Cyan
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonActive,
                (80, 250, 123, 255),
                category=dpg.mvThemeCat_Core,
            )  # Green

            # Frame
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBg, (68, 71, 90, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgHovered,
                (189, 147, 249, 255),
                category=dpg.mvThemeCat_Core,
            )  # Purple
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgActive,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink

            # Tabs
            dpg.add_theme_color(
                dpg.mvThemeCol_Tab, (68, 71, 90, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TabHovered,
                (139, 233, 253, 255),
                category=dpg.mvThemeCat_Core,
            )  # Cyan
            dpg.add_theme_color(
                dpg.mvThemeCol_TabActive,
                (255, 184, 108, 255),
                category=dpg.mvThemeCat_Core,
            )  # Orange
            dpg.add_theme_color(
                dpg.mvThemeCol_TabUnfocused,
                (50, 54, 66, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TabUnfocusedActive,
                (68, 71, 90, 255),
                category=dpg.mvThemeCat_Core,
            )

            # Separator
            dpg.add_theme_color(
                dpg.mvThemeCol_Separator,
                (98, 114, 164, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_SeparatorHovered,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink
            dpg.add_theme_color(
                dpg.mvThemeCol_SeparatorActive,
                (255, 184, 108, 255),
                category=dpg.mvThemeCat_Core,
            )  # Orange

            # Resize grip
            dpg.add_theme_color(
                dpg.mvThemeCol_ResizeGrip,
                (68, 71, 90, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ResizeGripHovered,
                (189, 147, 249, 255),
                category=dpg.mvThemeCat_Core,
            )  # Purple
            dpg.add_theme_color(
                dpg.mvThemeCol_ResizeGripActive,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink

            # Scrollbar
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarBg,
                (40, 42, 54, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrab,
                (98, 114, 164, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrabHovered,
                (189, 147, 249, 255),
                category=dpg.mvThemeCat_Core,
            )  # Purple
            dpg.add_theme_color(
                dpg.mvThemeCol_ScrollbarGrabActive,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink

            # Check mark and Slider
            dpg.add_theme_color(
                dpg.mvThemeCol_CheckMark,
                (80, 250, 123, 255),
                category=dpg.mvThemeCat_Core,
            )  # Green
            dpg.add_theme_color(
                dpg.mvThemeCol_SliderGrab,
                (255, 184, 108, 255),
                category=dpg.mvThemeCat_Core,
            )  # Orange
            dpg.add_theme_color(
                dpg.mvThemeCol_SliderGrabActive,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink

            # Title and menubar
            dpg.add_theme_color(
                dpg.mvThemeCol_TitleBg, (68, 71, 90, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TitleBgActive,
                (98, 114, 164, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_TitleBgCollapsed,
                (40, 42, 54, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_MenuBarBg,
                (68, 71, 90, 255),
                category=dpg.mvThemeCat_Core,
            )

            # Borders and shadows
            dpg.add_theme_color(
                dpg.mvThemeCol_Border, (98, 114, 164, 255), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core
            )

            # Other UI elements
            dpg.add_theme_color(
                dpg.mvThemeCol_DockingPreview,
                (189, 147, 249, 100),
                category=dpg.mvThemeCat_Core,
            )  # Purple
            dpg.add_theme_color(
                dpg.mvThemeCol_DockingEmptyBg,
                (40, 42, 54, 255),
                category=dpg.mvThemeCat_Core,
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_DragDropTarget,
                (255, 121, 198, 255),
                category=dpg.mvThemeCat_Core,
            )  # Pink
            dpg.add_theme_color(
                dpg.mvThemeCol_NavHighlight,
                (255, 184, 108, 255),
                category=dpg.mvThemeCat_Core,
            )  # Orange
            dpg.add_theme_color(
                dpg.mvThemeCol_NavWindowingHighlight,
                (80, 250, 123, 255),
                category=dpg.mvThemeCat_Core,
            )  # Green
            dpg.add_theme_color(
                dpg.mvThemeCol_NavWindowingDimBg,
                (40, 42, 54, 150),
                category=dpg.mvThemeCat_Core,
            )

            # Styles
            dpg.add_theme_style(dpg.mvStyleVar_Alpha, 1.0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(
                dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_ChildRounding, 4, category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_PopupRounding, 3, category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_TabRounding, 3, category=dpg.mvThemeCat_Core
            )

    return theme
