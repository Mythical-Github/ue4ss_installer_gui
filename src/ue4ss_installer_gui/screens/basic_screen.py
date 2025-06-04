import dearpygui.dearpygui as dpg


def push_text_editor_screen(sender=None, app_data=None, user_data=None):
    if dpg.does_item_exist("screen"):
        dpg.delete_item("screen")

    with dpg.window(
        tag="screen",
        modal=True,
        no_title_bar=True,
        no_open_over_existing_popup=False,
        no_resize=True,
        min_size=[524, 400],
        max_size=[524, 9999],
        no_move=True,
    ):
        dpg.add_input_text(
            tag="text_editor_input",
            default_value="default_text",
            multiline=True,
            width=-1,
            height=340,
        )

        dpg.add_spacer()

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Cancel", width=250, height=28, callback=lambda: print("Cancel")
            )
            dpg.add_button(
                label="Save", width=250, height=28, callback=lambda: print("Save")
            )
