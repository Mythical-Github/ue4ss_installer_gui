import os
import pathlib

import dearpygui.dearpygui as dpg

from ue4ss_installer_gui import settings, ue4ss, constants, translator
from ue4ss_installer_gui.widgets import setup_screen, centered_text


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
        dpg.set_value('portable_version_check_box', False)
        update_game_info_field_from_ui(user_data, "using_portable_version", False)

    refresh_file_to_install_combo_box(user_data)


def on_portable_version_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "using_portable_version", app_data)
    
    if app_data:
        dpg.set_value('developer_version_check_box', False)
        update_game_info_field_from_ui(user_data, "using_developer_version", False)

    refresh_file_to_install_combo_box(user_data)


def on_keep_mods_and_settings_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "using_keep_mods_and_settings", app_data)


def on_using_pre_releases_check_box_toggled(sender, app_data, user_data):
    update_game_info_field_from_ui(user_data, "show_pre_releases", app_data)
    refresh_ue4ss_tags_combo_box(user_data=user_data)
    refresh_file_to_install_combo_box(user_data=user_data)


def install_ue4ss_through_zip(user_data):
    # have the ue4ss tag be saved into the file when this is called
    # have custom be v_custom_hash_of_zip
    # have this add the files it unzipped into the dir into the installed_files settings array
    return


def uninstall_ue4ss(user_data):
    # have the ue4ss tag set to 'none' when this is called
    # have this remove the files it removed from the dir from the installed_files settings array
    from time import sleep

    sleep(2)


def install_ue4ss(user_data):
    # have the ue4ss tag be saved into the file when this is called
    # have this add the files it unzipped into the dir into the installed_files settings array

    # filter default things to install ticked releases download files by
    #     "Dev" and "UE4SS"
    #     not "Dev" and "UE4SS"
    #     if not "Dev" in any "XInput"
    from time import sleep

    sleep(2)


def download_ue4ss(user_data):
    from time import sleep

    sleep(2)


def clean_up_temp_files(user_data):
    from time import sleep

    sleep(2)


def push_installing_from_zip_screen(sender, app_data, user_data):
    screen_tag = "installing_ue4ss_from_zip_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate('installing_from_zip_ue4ss_task_text'),
        finished_all_steps_function=push_configure_game_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate('uninstalling_old_ue4ss_files_step_text'): uninstall_ue4ss,
            translator.translator.translate('installing_ue4ss_step_text'): install_ue4ss_through_zip,
            translator.translator.translate('cleaning_up_temp_files_step_text'): clean_up_temp_files,
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
    )
    dpg.add_file_extension(parent="zip_picker", extension=".zip")
    dpg.add_file_extension(parent="zip_picker", extension=".rar")
    dpg.add_file_extension(parent="zip_picker", extension=".7z")


def push_installing_screen(sender, app_data, user_data):
    screen_tag = "installing_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate('installing_ue4ss_task_text'),
        finished_all_steps_function=push_configure_game_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate('uninstalling_old_ue4ss_files_step_text'): uninstall_ue4ss,
            translator.translator.translate('downloading_ue4ss_zip_step_text'): download_ue4ss,
            translator.translator.translate('installing_ue4ss_step_text'): install_ue4ss,
            translator.translator.translate('cleaning_up_temp_files_step_text'): clean_up_temp_files,
        },
    )


def push_reinstalling_screen(sender, app_data, user_data):
    screen_tag = "reinstalling_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate('reinstalling_ue4ss_task_text'),
        finished_all_steps_function=push_configure_game_screen,
        user_data=user_data,
        step_text_to_step_functions={
            translator.translator.translate('uninstalling_old_ue4ss_files_step_text'): uninstall_ue4ss,
            translator.translator.translate('downloading_ue4ss_zip_step_text'): download_ue4ss,
            translator.translator.translate('installing_ue4ss_step_text'): install_ue4ss,
            translator.translator.translate('cleaning_up_temp_files_step_text'): clean_up_temp_files,
        },
    )


def push_uninstalling_screen(sender, app_data, user_data):
    screen_tag = "uninstalling_ue4ss_modal"
    if dpg.does_item_exist(screen_tag):
        dpg.delete_item(screen_tag)
    setup_screen.push_setup_screen(
        tag=screen_tag,
        task_text=translator.translator.translate('uninstalling_ue4ss_task_text'),
        finished_all_steps_function=push_configure_game_screen,
        user_data=user_data,
        step_text_to_step_functions={translator.translator.translate('uninstalling_old_ue4ss_files_step_text'): uninstall_ue4ss},
    )


def dismiss_configure_game_modal():
    dpg.delete_item("configure_game_modal")


def push_configure_game_screen(user_data):
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
        )
        install_dir = str(game_info.install_dir)
        matched = False

        centered_game_name_text = "default centered game name text"

        for game_key in constants.GAME_PATHS_TO_DISPLAY_NAMES.keys():
            if game_key in install_dir:
                centered_game_name_text = str(
                    constants.GAME_PATHS_TO_DISPLAY_NAMES[game_key]
                )
                matched = True
                break

        if not matched:
            centered_game_name_text = game_info.game_title

        with dpg.group(horizontal=True, parent="configure_game_modal", tag='game_label_container'):
            centered_text.add_centered_text(f'{translator.translator.translate('game_label')}: {centered_game_name_text}', parent='game_label_container')

        dpg.add_spacer(parent="configure_game_modal")

        with dpg.group(horizontal=True, parent="configure_game_modal", tag='game_dir_label_container'):
            centered_text.add_centered_text(f'{translator.translator.translate('game_directory_text_label')}: {str(game_info.install_dir)}', parent='game_dir_label_container')

        dpg.add_spacer(parent="configure_game_modal")

        centered_text.add_centered_text(translator.translator.translate('ue4ss_version_text_label'), parent="configure_game_modal")
        
        if game_info.show_pre_releases:
            combo_items = ue4ss.get_all_tags_with_assets()
        else:
            combo_items = ue4ss.get_normal_release_tags_with_assets()
        if game_info.ue4ss_version in combo_items:
            default_combo_item = game_info.ue4ss_version
        else:
            default_combo_item = combo_items[0]

        dpg.add_input_text(
            tag='filter_ue4ss_tag', 
            parent="configure_game_modal", 
            callback=ue4ss_tags_filter_changed, 
            user_data=user_data, 
            width=-1,
            hint=f'{translator.translator.translate('filter_ue4ss_versions_filter_label')}...'
        )

        dpg.add_combo(
            tag="tags_combo_box",
            items=combo_items,
            default_value=default_combo_item,
            callback=on_ue4ss_version_tag_combo_box_selected,
            user_data=user_data, 
            parent="configure_game_modal",
            width=-1
        )

        dpg.add_spacer(parent="configure_game_modal")

        centered_text.add_centered_text(translator.translator.translate('ue4ss_file_to_install_text_label'), parent="configure_game_modal")

        dpg.add_input_text(
            tag='filter_ue4ss_file_to_install', 
            parent="configure_game_modal", 
            callback=ue4ss_archive_to_install_filter_changed, 
            user_data=user_data, 
            width=-1,
            hint=f'{translator.translator.translate('filter_file_to_install_filter_label')}...'
        )

        # add the missing for items and default here later
        dpg.add_combo(
            tag="ue4ss_file_to_install_combo_box",
            items=[],
            default_value='default_combo_item',
            callback=on_ue4ss_file_to_select_combo_box_selected,
            user_data=user_data, 
            parent="configure_game_modal",
            width=-1
        )

        refresh_file_to_install_combo_box(str(game_info.install_dir))

        dpg.add_spacer(parent="configure_game_modal")

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_checkbox(
                default_value=game_info.show_pre_releases,
                tag="pre_releases_check_box",
                callback=on_using_pre_releases_check_box_toggled,
                user_data=user_data,
            )
            dpg.add_text(translator.translator.translate('enable_pre_releases_text_label'))

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
            dpg.add_text(translator.translator.translate('install_developer_version_text_label'))

        with dpg.group(horizontal=True, parent="configure_game_modal"):
            dpg.add_checkbox(
                default_value=game_info.using_portable_version,
                tag="portable_version_check_box",
                callback=on_portable_version_check_box_toggled,
                user_data=user_data,
            )
            dpg.add_text(translator.translator.translate('portable_version_text_label'))

        dpg.add_spacer(parent="configure_game_modal")

        with dpg.group(
            horizontal=True, tag="button_row", parent="configure_game_modal"
        ):
            should_show_buttons = get_should_show_uninstall_button(user_data)
            dpg.add_button(
                label=translator.translator.translate('install_button_text'),
                height=28,
                callback=push_installing_screen,
                user_data=pathlib.Path(user_data),
                show=not should_show_buttons,
            )
            dpg.add_button(
                label=translator.translator.translate('install_from_zip_button_text'),
                height=28,
                callback=push_installing_from_zip_screen_file_selection,
                user_data=pathlib.Path(user_data),
                show=not should_show_buttons,
            )
            dpg.add_button(
                label=translator.translator.translate('reinstall_button_text'),
                height=28,
                callback=push_reinstalling_screen,
                user_data=pathlib.Path(user_data),
                show=should_show_buttons,
            ) 
            dpg.add_button(
                label=translator.translator.translate('uninstall_button_text'),
                height=28,
                callback=push_uninstalling_screen,
                user_data=pathlib.Path(user_data),
                show=should_show_buttons,
            )
        resize_install_related_buttons()

        dpg.add_spacer(parent="configure_game_modal", height=-1)
        dpg.add_button(
            label=translator.translator.translate('open_game_exe_directory_label'),
            parent="configure_game_modal",
            width=-1,
            height=28,
            callback=open_directory_in_file_browser,
            user_data=pathlib.Path(user_data)
        )

        dpg.add_spacer(parent="configure_game_modal", height=-1)
        dpg.add_button(
            label=translator.translator.translate('close_button_text'),
            parent="configure_game_modal",
            width=-1,
            height=28,
            callback=dismiss_configure_game_modal,
        )



def get_exe_dir_from_game_dir(game_directory: str) -> str:
    game_dir_path = pathlib.Path(game_directory)
    exclude_dirs = [
        game_dir_path / "Engine",
        game_dir_path / "WindowsNoEditor" / "Engine",
        game_dir_path / "Windows" / "Engine"
    ]
    
    for root in game_dir_path.rglob('*'):
        if any(root.is_relative_to(exclude_dir) for exclude_dir in exclude_dirs):
            continue
        
        if root.name == 'Win64' and root.is_dir():
            return str(root)
        elif root.name == 'WinGDK' and root.is_dir():
            return str(root)
    
    return ''


def open_directory_in_file_browser(sender, app_data, game_directory: pathlib.Path):
    exe_dir = get_exe_dir_from_game_dir(str(game_directory))
    if settings.is_windows():
        os.startfile(exe_dir)
    else:
        os.system(f'xdg-open "{exe_dir}"')


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


def update_ue4ss_tags_combo_box(user_data):
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(
        user_data
    )

    if not game_info:
        return

    if game_info.show_pre_releases:
        all_tags = ue4ss.get_all_tags_with_assets()
    else:
        all_tags = ue4ss.get_normal_release_tags_with_assets()

    dpg.configure_item("tags_combo_box", items=all_tags)

    if game_info.ue4ss_version in all_tags:
        dpg.set_value("tags_combo_box", game_info.ue4ss_version)
    else:
        dpg.set_value("tags_combo_box", all_tags[0] if all_tags else "")


def refresh_file_to_install_combo_box(user_data):
    filter = dpg.get_value('filter_ue4ss_tag')
    game_info = settings.get_game_info_instance_in_settings_from_game_directory(user_data)
    selected_tag = dpg.get_value('tags_combo_box')

    if not game_info or ue4ss.cached_repo_releases_info is None:
        return

    tag_info = next((tag for tag in ue4ss.cached_repo_releases_info.tags if tag.tag == selected_tag), None)
    if not tag_info:
        return
    
    default_items = []

    for asset in tag_info.assets:
        filename = asset.file_name
        lower = filename.lower()
        is_dev = 'dev' in lower

        if (game_info.using_developer_version and is_dev) or (not game_info.using_developer_version and not is_dev):
            if lower not in ['zcustomgameconfigs.zip', 'zmapgenbp.zip']:
                default_items.append((filename, asset.created_at))

    default_items.sort(key=lambda x: x[1], reverse=True)

    sorted_filenames = [filename for filename, _ in default_items]

    filtered_filenames = [filename for filename in sorted_filenames if filter.lower() in filename.lower()]

    if not game_info.using_developer_version:
        portable_enabled = dpg.get_value('portable_version_check_box')

        if portable_enabled:
            filtered_filenames = [filename for filename in filtered_filenames if "Standard" in filename]
        else:
            filtered_filenames = [filename for filename in filtered_filenames if "Standard" not in filename]

    if filtered_filenames:
        default_value = game_info.last_installed_version if game_info.last_installed_version in filtered_filenames else filtered_filenames[0]
        dpg.configure_item("ue4ss_file_to_install_combo_box", items=filtered_filenames, default_value=default_value)
    else:
        default_value = game_info.last_installed_version if game_info.last_installed_version in sorted_filenames else sorted_filenames[0]
        dpg.configure_item("ue4ss_file_to_install_combo_box", items=sorted_filenames, default_value=default_value)


def refresh_ue4ss_tags_combo_box(user_data):
    filter = dpg.get_value('filter_ue4ss_file_to_install')
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

    if game_info.ue4ss_version in filtered_tags:
        dpg.set_value("tags_combo_box", game_info.ue4ss_version)
    else:
        dpg.set_value("tags_combo_box", filtered_tags[0] if filtered_tags else (all_tags[0] if all_tags else ""))


def ue4ss_tags_filter_changed(sender, app_Data, user_data):
    return


def ue4ss_archive_to_install_filter_changed(sender, app_Data, user_data):
    return


def on_ue4ss_file_to_select_combo_box_selected(sender, app_data, user_data):
    refresh_ue4ss_tags_combo_box(user_data)
