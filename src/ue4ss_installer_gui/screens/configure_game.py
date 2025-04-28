import pathlib
import shutil
import os
import subprocess

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, ue4ss, constants, translator, file_io
from ue4ss_installer_gui.screens import setup_screen, notification_screen
from ue4ss_installer_gui.checks import online_check


def filter_ue4sS_tag(sender, app_data, user_data):
    refresh_ue4ss_tags_combo_box(user_data=user_data)
    refresh_file_to_install_combo_box(user_data)


def filter_ue4ss_file_to_install(sender, app_data, user_data):
    refresh_ue4ss_tags_combo_box(user_data=user_data)
    refresh_file_to_install_combo_box(user_data)


def push_uninstall_successful_screen(user_data):
    notification_screen.push_notification_screen(
        translator.translator.translate("uninstall_succeeded_message_text"),
        pathlib.Path(user_data),
    )


def push_install_successful_screen(user_data):
    if isinstance(user_data, list):
        user_data = user_data[0]
    notification_screen.push_notification_screen(
        translator.translator.translate("install_succeeded_message_text"),
        pathlib.Path(user_data),
    )


def push_uninstall_failed_screen(user_data):
    notification_screen.push_notification_screen(
        translator.translator.translate("uninstall_failed_message_text"),
        pathlib.Path(user_data),
    )


def push_install_failed_screen(user_data):
    notification_screen.push_notification_screen(
        translator.translator.translate("install_failed_message_text"),
        pathlib.Path(user_data),
    )


def refresh_file_to_install_combo_box(user_data):
    filter = dpg.get_value("filter_ue4ss_file_to_install")
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        user_data
    )
    selected_tag = dpg.get_value("tags_combo_box")

    if not game_info or ue4ss.cached_repo_releases_info is None:
        return

    tag_info = next(
        (
            tag
            for tag in ue4ss.cached_repo_releases_info.tags
            if tag.tag == selected_tag
        ),
        None,
    )
    if not tag_info:
        return

    default_items = []

    for asset in tag_info.assets:
        filename = asset.file_name
        lower = filename.lower()
        is_dev = "dev" in lower

        if (game_info.using_developer_version and is_dev) or (
            not game_info.using_developer_version and not is_dev
        ):
            if lower not in ["zcustomgameconfigs.zip", "zmapgenbp.zip"]:
                default_items.append((filename, asset.created_at))

    default_items.sort(key=lambda x: x[1], reverse=True)

    sorted_filenames = [filename for filename, _ in default_items]

    filtered_filenames = [
        filename for filename in sorted_filenames if filter.lower() in filename.lower()
    ]

    if not game_info.using_developer_version:
        portable_enabled = dpg.get_value("portable_version_check_box")

        if portable_enabled:
            filtered_filenames = [
                filename for filename in filtered_filenames if "Standard" in filename
            ]
        else:
            filtered_filenames = [
                filename
                for filename in filtered_filenames
                if "Standard" not in filename
            ]

    if filtered_filenames:
        default_value = (
            game_info.last_installed_version
            if game_info.last_installed_version in filtered_filenames
            else filtered_filenames[0]
        )
        dpg.configure_item(
            "ue4ss_file_to_install_combo_box",
            items=filtered_filenames,
            default_value=default_value,
        )
    else:
        if len(sorted_filenames) > 1:
            default_value = (
                game_info.last_installed_version
                if game_info.last_installed_version in sorted_filenames
                else sorted_filenames[0]
            )
            dpg.configure_item(
                "ue4ss_file_to_install_combo_box",
                items=sorted_filenames,
                default_value=default_value,
            )
        else:
            dpg.configure_item(
                "ue4ss_file_to_install_combo_box",
                items=sorted_filenames,
                default_value="",
            )


def update_game_info_field_from_ui(
    game_directory: str, field_name: str, value, should_save: bool = True
):
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        game_directory
    )
    if game_info:
        setattr(game_info, field_name, value)
        settings.save_game_info_to_settings_file(game_info)


def on_ue4ss_version_tag_combo_box_selected(sender, app_data, user_data):
    update_game_info_field_from_ui(
        user_data, "ue4ss_version", app_data, should_save=False
    )
    refresh_file_to_install_combo_box(user_data)


def on_developer_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "using_developer_version", app_data)

    if app_data:
        dpg.set_value("portable_version_check_box", False)
        update_game_info_field_from_ui(user_data, "using_portable_version", False)

    refresh_file_to_install_combo_box(user_data)


def on_portable_version_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "using_portable_version", app_data)

    if app_data:
        dpg.set_value("developer_version_check_box", False)
        update_game_info_field_from_ui(user_data, "using_developer_version", False)

    refresh_file_to_install_combo_box(user_data)


def on_keep_mods_and_settings_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "using_keep_mods_and_settings", app_data)


def on_using_pre_releases_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "show_pre_releases", app_data)
    refresh_ue4ss_tags_combo_box(user_data=user_data)
    refresh_file_to_install_combo_box(user_data)


def install_ue4ss_through_zip(user_data):
    file_io.unzip_zip(user_data[1], get_exe_dir_from_game_dir(user_data[0]))
    all_paths_in_zip = file_io.get_paths_of_files_in_zip(user_data[1])
    update_game_info_field_from_ui(user_data[0], "installed_files", all_paths_in_zip)


def delete_all_empty_dirs_in_dir_tree(root: pathlib.Path):
    for path in sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def uninstall_ue4ss(user_data):
    if isinstance(user_data, list):
        user_data = user_data[0]
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        user_data
    )
    exe_dir = get_exe_dir_from_game_dir(user_data)
    if game_info:
        for file_to_delete in game_info.installed_files:
            file_to_delete_actual_path = os.path.normpath(f"{exe_dir}/{file_to_delete}")
            if os.path.isfile(file_to_delete_actual_path):
                os.remove(file_to_delete_actual_path)
    delete_all_empty_dirs_in_dir_tree(user_data)
    log_file_old = os.path.normpath(f"{exe_dir}/UE4SS.log")
    log_file_new = os.path.normpath(f"{exe_dir}/ue4ss/UE4SS.log")
    if os.path.isfile(log_file_old):
        os.remove(log_file_old)
    if os.path.isfile(log_file_new):
        os.remove(log_file_new)
    update_game_info_field_from_ui(user_data, "installed_files", [])


def install_ue4ss(user_data):
    ue4ss_zip_path = pathlib.Path(f"{file_io.SCRIPT_DIR}/temp/ue4ss.zip")
    file_io.unzip_zip(ue4ss_zip_path, get_exe_dir_from_game_dir(user_data))
    all_paths_in_zip = file_io.get_paths_of_files_in_zip(ue4ss_zip_path)
    update_game_info_field_from_ui(user_data, "installed_files", all_paths_in_zip)


def download_ue4ss(user_data):
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        user_data
    )
    if game_info:
        print(file_io.get_temp_dir())
        os.makedirs(str(file_io.get_temp_dir()), exist_ok=True)
        file_names_to_download_links = ue4ss.get_file_name_to_download_links_from_tag(
            game_info.ue4ss_version
        )
        download_link = file_names_to_download_links.get(
            game_info.last_installed_version
        )
        file_io.download_file(
            download_link,
            os.path.normpath(f"{str(file_io.get_temp_dir())}/ue4ss.zip"),
        )


def clean_up_temp_files(user_data):
    if isinstance(user_data, list):
        user_data = user_data[0]
    temp_dir = file_io.get_temp_dir()
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)


def push_installing_from_zip_screen(sender, app_data, user_data):
    last_installed_file = ''  # have this use provided file later
    ue4ss_version = ''  # have this use provided file later
    update_game_info_field_from_ui(
        user_data, "last_installed_version", last_installed_file
    )
    update_game_info_field_from_ui(user_data, "ue4ss_version", ue4ss_version)
    screen_tag = "installing_ue4ss_from_zip_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    game_directory = user_data
    zip_file = app_data["file_path_name"]
    print(zip_file)
    user_data = [game_directory, zip_file]
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate(
            "installing_from_zip_ue4ss_task_text"
        ),
        finished_all_steps_function=push_install_successful_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate(
                "uninstalling_old_ue4ss_files_step_text"
            ): uninstall_ue4ss,
            translator.translator.translate(
                "installing_ue4ss_step_text"
            ): install_ue4ss_through_zip,
            translator.translator.translate(
                "cleaning_up_temp_files_step_text"
            ): clean_up_temp_files,
        },
    )


def push_installing_from_zip_screen_file_selection(sender, app_data, user_data):
    if dpg.does_item_exist("zip_picker"):
        dpg.delete_item("zip_picker")

    dpg.add_file_dialog(
        directory_selector=False,
        show=True,
        callback=push_installing_from_zip_screen,
        tag="zip_picker",
        width=constants.WINDOW_WIDTH - 80,
        height=constants.WINDOW_HEIGHT - 80,
        modal=True,
        file_count=999,
        user_data=user_data,
    )
    dpg.add_file_extension(parent="zip_picker", extension=".zip")
    dpg.add_file_extension(parent="zip_picker", extension=".rar")
    dpg.add_file_extension(parent="zip_picker", extension=".7z")


def push_installing_screen(sender, app_data, user_data):
    last_installed_file = dpg.get_value("ue4ss_file_to_install_combo_box")
    ue4ss_version = dpg.get_value("tags_combo_box")
    update_game_info_field_from_ui(
        user_data, "last_installed_version", last_installed_file
    )
    update_game_info_field_from_ui(user_data, "ue4ss_version", ue4ss_version)
    screen_tag = "installing_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate("installing_ue4ss_task_text"),
        finished_all_steps_function=push_install_successful_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate(
                "uninstalling_old_ue4ss_files_step_text"
            ): uninstall_ue4ss,
            translator.translator.translate(
                "downloading_ue4ss_zip_step_text"
            ): download_ue4ss,
            translator.translator.translate(
                "installing_ue4ss_step_text"
            ): install_ue4ss,
            translator.translator.translate(
                "cleaning_up_temp_files_step_text"
            ): clean_up_temp_files,
        },
    )


def push_reinstalling_screen(sender, app_data, user_data):
    last_installed_file = dpg.get_value("ue4ss_file_to_install_combo_box")
    ue4ss_version = dpg.get_value("tags_combo_box")
    update_game_info_field_from_ui(
        user_data, "last_installed_version", last_installed_file
    )
    update_game_info_field_from_ui(user_data, "ue4ss_version", ue4ss_version)
    screen_tag = "reinstalling_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate("reinstalling_ue4ss_task_text"),
        finished_all_steps_function=push_install_successful_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate(
                "uninstalling_old_ue4ss_files_step_text"
            ): uninstall_ue4ss,
            translator.translator.translate(
                "downloading_ue4ss_zip_step_text"
            ): download_ue4ss,
            translator.translator.translate(
                "installing_ue4ss_step_text"
            ): install_ue4ss,
            translator.translator.translate(
                "cleaning_up_temp_files_step_text"
            ): clean_up_temp_files,
        },
    )


def push_uninstalling_screen(sender, app_data, user_data):
    screen_tag = "uninstalling_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate("uninstalling_ue4ss_task_text"),
        finished_all_steps_function=push_uninstall_successful_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate(
                "uninstalling_old_ue4ss_files_step_text"
            ): uninstall_ue4ss
        },
    )


def dismiss_configure_game_modal():
    dpg.delete_item("configure_game_modal")


def add_centered_text(text, parent, wrap=None):
    char_width = 7.25
    available_width = 508

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2
    wrap_width = wrap if wrap is not None else available_width

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=max(center_x, 0))
        dpg.add_text(text, wrap=wrap_width)


# have the differing offline functionality occur here
def push_configure_game_screen(sender, app_data, user_data):
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        str(user_data)
    )
    if game_info:
        if dpg.does_item_exist("configure_game_modal"):
            dpg.delete_item("configure_game_modal")
        dpg.add_window(
            modal=True,
            tag="configure_game_modal",
            no_title_bar=True,
            min_size=[524, 1],
            max_size=[524, 999],
            autosize=True,
            no_open_over_existing_popup=False,
            pos=[30, 160],
        )

        install_dir = str(game_info.install_dir)
        matched = False

        centered_game_name_text = "default centered game name text"

        for game_key in constants.GAME_PATHS_TO_DISPLAY_NAMES.keys():
            if game_key in install_dir:
                centered_game_name_text = (
                    f"Game: {str(constants.GAME_PATHS_TO_DISPLAY_NAMES[game_key])}"
                )
                matched = True
                break

        if not matched:
            centered_game_name_text = f"Game: {game_info.game_title}"

        add_centered_text(centered_game_name_text, parent="configure_game_modal")

        dpg.add_spacer(parent="configure_game_modal")

        add_centered_text(
            f"{translator.translator.translate('game_directory_text_label')} {str(game_info.install_dir)}",
            parent="configure_game_modal",
        )

        dpg.add_spacer(parent="configure_game_modal")

        # with dpg.group(horizontal=True, parent="configure_game_modal", width=-1):
        #     dpg.add_text(translator.translator.translate('game_directory_text_label'))
        #     dpg.add_text(str(game_info.install_dir), wrap=376)

        # dpg.add_spacer(parent="configure_game_modal")
        
        if online_check.is_online:
            add_centered_text(
                translator.translator.translate("ue4ss_version_text_label"),
                parent="configure_game_modal",
            )

            dpg.add_spacer(parent="configure_game_modal")

            if game_info.show_pre_releases:
                combo_items = ue4ss.get_all_tags_with_assets()
            else:
                combo_items = ue4ss.get_normal_release_tags_with_assets()
            if game_info.ue4ss_version in combo_items:
                default_combo_item = game_info.ue4ss_version
            else:
                default_combo_item = combo_items[0]

            dpg.add_input_text(
                width=-1,
                hint="filter ue4ss version here...",
                parent="configure_game_modal",
                tag="filter_ue4ss_tag",
                callback=filter_ue4sS_tag,
                user_data=user_data,
            )

            dpg.add_combo(
                tag="tags_combo_box",
                items=combo_items,
                default_value=default_combo_item,
                callback=on_ue4ss_version_tag_combo_box_selected,
                user_data=user_data,
                width=-1,
                parent="configure_game_modal",
            )

            dpg.add_spacer(parent="configure_game_modal")

            add_centered_text(
                translator.translator.translate("ue4ss_file_to_install_text_label"),
                parent="configure_game_modal",
            )

            dpg.add_spacer(parent="configure_game_modal")

            dpg.add_input_text(
                hint="filter file archive to install here...",
                parent="configure_game_modal",
                width=-1,
                tag="filter_ue4ss_file_to_install",
                callback=filter_ue4ss_file_to_install,
                user_data=user_data,
            )

            dpg.add_combo(
                tag="ue4ss_file_to_install_combo_box",
                items=[],
                default_value="",
                user_data=user_data,
                width=-1,
                parent="configure_game_modal",
            )

            refresh_file_to_install_combo_box(user_data)

            dpg.add_spacer(parent="configure_game_modal", height=4)
            with dpg.group(horizontal=True, parent="configure_game_modal"):
                dpg.add_checkbox(
                    default_value=game_info.show_pre_releases,
                    tag="pre_releases_check_box",
                    callback=on_using_pre_releases_check_box_toggled,
                    user_data=user_data,
                )
                dpg.add_text(
                    translator.translator.translate("enable_pre_releases_text_label")
                )

        # with dpg.group(horizontal=True, parent="configure_game_modal"):
        #     dpg.add_checkbox(
        #         default_value=game_info.using_keep_mods_and_settings,
        #         tag="keep_mods_and_settings_check_box",
        #         callback=on_keep_mods_and_settings_check_box_toggled,
        #         user_data=user_data,
        #     )
        #     dpg.add_text(translator.translator.translate('keep_mods_and_settings_text_label'))

            with dpg.group(horizontal=True, parent="configure_game_modal"):
                dpg.add_checkbox(
                    default_value=game_info.using_developer_version,
                    tag="developer_version_check_box",
                    callback=on_developer_check_box_toggled,
                    user_data=user_data,
                )
                dpg.add_text(
                    translator.translator.translate("install_developer_version_text_label")
                )

            dpg.add_spacer(parent="configure_game_modal")

            with dpg.group(horizontal=True, parent="configure_game_modal"):
                dpg.add_checkbox(
                    default_value=game_info.using_developer_version,
                    tag="portable_version_check_box",
                    callback=on_portable_version_check_box_toggled,
                    user_data=user_data,
                )
                dpg.add_text(
                    translator.translator.translate("install_portable_version_text_label")
                )

            dpg.add_spacer(parent="configure_game_modal")

        with dpg.group(
            horizontal=True, tag="button_row", parent="configure_game_modal"
        ):
            if online_check.is_online:
                should_show_buttons = get_should_show_uninstall_button(user_data)
                dpg.add_button(
                    label=translator.translator.translate("install_button_text"),
                    height=28,
                    callback=push_installing_screen,
                    user_data=pathlib.Path(user_data),
                    show=not should_show_buttons,
                )
                dpg.add_button(
                    label=translator.translator.translate("install_from_zip_button_text"),
                    height=28,
                    callback=push_installing_from_zip_screen_file_selection,
                    user_data=pathlib.Path(user_data),
                    show=not should_show_buttons,
                )
                dpg.add_button(
                    label=translator.translator.translate("reinstall_button_text"),
                    height=28,
                    callback=push_reinstalling_screen,
                    user_data=pathlib.Path(user_data),
                    show=should_show_buttons,
                )
                dpg.add_button(
                    label=translator.translator.translate("uninstall_button_text"),
                    height=28,
                    callback=push_uninstalling_screen,
                    user_data=pathlib.Path(user_data),
                    show=should_show_buttons,
                )
            else:
                should_show_buttons = get_should_show_uninstall_button(user_data)
                dpg.add_button(
                    label=translator.translator.translate("install_from_zip_button_text"),
                    height=28,
                    callback=push_installing_from_zip_screen_file_selection,
                    user_data=pathlib.Path(user_data),
                    show=not should_show_buttons,
                )
                dpg.add_button(
                    label=translator.translator.translate("uninstall_button_text"),
                    height=28,
                    callback=push_uninstalling_screen,
                    user_data=pathlib.Path(user_data),
                    show=should_show_buttons,
                )

        resize_install_related_buttons()

        dpg.add_spacer(parent="configure_game_modal", height=-1)
        dpg.add_button(
            label=translator.translator.translate("open_game_exe_directory"),
            parent="configure_game_modal",
            width=-1,
            height=28,
            callback=open_game_exe_dir,
            user_data=str(game_info.install_dir),
        )

        dpg.add_spacer(parent="configure_game_modal", height=-1)
        dpg.add_button(
            label=translator.translator.translate("close_button_text"),
            parent="configure_game_modal",
            width=-1,
            height=28,
            callback=dismiss_configure_game_modal,
        )


def open_game_exe_dir(sender, app_data, game_directory: pathlib.Path):
    exe_dir = get_exe_dir_from_game_dir(pathlib.Path(game_directory))
    if settings.is_windows():
        os.startfile(exe_dir)
    else:
        subprocess.run(["xdg-open", exe_dir])


def resize_install_related_buttons():
    all_children = dpg.get_item_children("button_row", 1)
    visible_children = [
        child
        for child in all_children  # type: ignore
        if dpg.get_item_configuration(child).get("show", True)
    ]

    button_count = len(visible_children)
    if button_count == 0:
        return

    if button_count == 2:
        button_width = 250
    elif button_count == 1:
        button_width = -1
    else:
        button_width = 164

    for i, child_id in enumerate(visible_children):
        dpg.configure_item(child_id, width=button_width)


def get_should_show_uninstall_button(game_directory: pathlib.Path) -> bool:
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        str(game_directory)
    )
    if game_info:
        if len(game_info.installed_files) > 0:
            return True
        else:
            return False
    no_game_info_error = (
        "No game info, when get should show uninstall button was pressed."
    )
    raise RuntimeError(no_game_info_error)


def refresh_ue4ss_tags_combo_box(user_data):
    filter = dpg.get_value("filter_ue4ss_tag")
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        user_data
    )

    if not game_info:
        return

    if game_info.show_pre_releases:
        all_tags = ue4ss.get_all_tags_with_assets()
    else:
        all_tags = ue4ss.get_normal_release_tags_with_assets()

    filtered_tags = [tag for tag in all_tags if filter.lower() in tag.lower()]

    dpg.configure_item("tags_combo_box", items=filtered_tags)

    if filtered_tags:
        if game_info.ue4ss_version in filtered_tags:
            dpg.set_value("tags_combo_box", game_info.ue4ss_version)
        else:
            dpg.set_value("tags_combo_box", filtered_tags[0])
    else:
        if all_tags:
            dpg.set_value("tags_combo_box", all_tags[0])
        else:
            dpg.set_value("tags_combo_box", "")


def get_exe_dir_from_game_dir(game_directory: pathlib.Path) -> pathlib.Path:
    engine_dir = game_directory / "Engine"

    for subdir in game_directory.rglob("*"):
        if subdir.is_dir():
            if engine_dir in subdir.parents:
                continue

            if subdir.name == "Win64" or subdir.name == "WinGDK":
                return subdir

    return pathlib.Path("")
