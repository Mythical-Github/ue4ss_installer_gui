import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import file_io


def cancel_text_edit_callback(sender, app_data, user_data):
    user_data["finished_callback"]()


def save_text_edit_callback(sender, app_data, user_data):
    text_value = dpg.get_value("text_editor_input")
    file_io.save_content_to_file(content=text_value, file_path=user_data["file_path"])
    user_data["finished_callback"]()


def push_text_editor_screen(sender, app_data, user_data):
    if dpg.does_item_exist("text_editor_screen"):
        dpg.delete_item("text_editor_screen")

    with dpg.window(
        tag="text_editor_screen",
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
            default_value=file_io.get_contents_of_file(user_data["file_path"]),
            multiline=True,
            width=-1,
            height=340,
        )

        dpg.add_spacer()

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Cancel",
                width=250,
                height=28,
                callback=cancel_text_edit_callback,
                user_data=user_data,
            )
            dpg.add_button(
                label="Save",
                width=250,
                height=28,
                callback=save_text_edit_callback,
                user_data=user_data,
            )
