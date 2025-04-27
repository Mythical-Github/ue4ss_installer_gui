import dearpygui.dearpygui as dpg


def add_centered_text(text, parent, wrap=None):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2
    wrap_width = wrap if wrap is not None else available_width

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=max(center_x, 0))
        dpg.add_text(text, wrap=wrap_width)
