import os
import tomlkit
import pathlib
import platform

from platformdirs import user_config_dir

from ue4ss_installer_gui import (
    logger,
    steam,
    epic,
    unreal_engine,
    ue4ss,
    constants,
    data_structures,
)


config_dir = user_config_dir(appname=constants.APP_TITLE, appauthor="mythical_programs")

os.makedirs(config_dir, exist_ok=True)

SETTINGS_FILE = os.path.join(config_dir, "settings.toml")


# def get_valid_language_options() -> list[str]:
#     specified_dir = os.path.normpath(f'{file_io.SCRIPT_DIR}/assets/localization')

#     if not os.path.isdir(specified_dir):
#         return []

#     language_options = [
#         os.path.splitext(file)[0]
#         for file in os.listdir(specified_dir)
#         if os.path.isfile(os.path.join(specified_dir, file))
#     ]

#     return language_options


def get_default_locale() -> str:
    return "en"


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def make_settings_file():
    settings = {
        "games": [],
        "GUI": {
            "use_custom_font": False,
            "custom_font_path": get_system_font_path(),
            "language": "en",
        },
    }

    toml_str = tomlkit.dumps(settings)

    with open(SETTINGS_FILE, "w") as f:
        f.write(toml_str)
    logger.log_message(f"Settings file created at {SETTINGS_FILE}")


def to_toml_value(value):
    if isinstance(value, dict):
        table = tomlkit.table()
        for k, v in value.items():
            table[k] = to_toml_value(v)
        return table
    elif isinstance(value, list):
        if all(isinstance(i, dict) for i in value):
            aot = tomlkit.aot()
            for item in value:
                aot.append(to_toml_value(item))
            return aot
        else:
            return value
    else:
        return value


def to_pretty_toml(data: dict):
    table = tomlkit.table()
    for key, value in data.items():
        table[key] = to_toml_value(value)
    return table


def save_settings(settings_dictionary: dict):
    pretty_data = to_pretty_toml(settings_dictionary)
    toml_str = tomlkit.dumps(pretty_data)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(toml_str)

    logger.log_message(f"Settings saved to {SETTINGS_FILE}")


def get_is_game_in_settings(game_directory: pathlib.Path) -> bool:
    is_game_already_in_list = False
    for game_entry in get_game_entries_in_settings():
        if os.path.normpath(game_entry["install_dir"]) == os.path.normpath(
            str(game_directory)
        ):
            is_game_already_in_list = True
            break
    return is_game_already_in_list


def remove_game_entry_by_game_dir(game_directory: pathlib.Path):
    loaded_settings = get_settings()
    games = loaded_settings.get("games", [])

    target_path = game_directory.resolve(strict=False)
    updated_games = []

    for game in games:
        install_dir = game.get("install_dir")
        if install_dir is None:
            updated_games.append(game)
            continue

        install_path = pathlib.Path(install_dir).resolve(strict=False)
        if install_path != target_path:
            updated_games.append(game)

    loaded_settings["games"] = updated_games
    save_settings(loaded_settings)


has_inited_settings = False


def collect_all_scan_dirs():
    all_game_dirs = []

    # Steam and Epic Games
    for dir_source in (
        steam.get_all_steam_game_directories(),
        epic.get_all_epic_games_game_directories(),
    ):
        for base_dir in dir_source:
            all_game_dirs.extend(
                unreal_engine.get_all_unreal_game_directories_in_directory_tree(
                    str(base_dir)
                )
            )

    # Custom game directories
    for base_dir in get_settings().get("custom_game_directories", []):
        all_game_dirs.extend(
            unreal_engine.get_all_unreal_game_directories_in_directory_tree(
                str(base_dir)
            )
        )

    # Game directories already in settings
    all_game_dirs.extend(get_game_dirs_in_settings())

    return all_game_dirs


def collect_games_to_add():
    all_game_dirs = collect_all_scan_dirs()
    games_to_add = []

    for game_dir in all_game_dirs:
        game_path = pathlib.Path(game_dir)
        if unreal_engine.does_directory_contain_unreal_game(
            game_path
        ) or ue4ss.is_ue4ss_installed(game_path):
            if not get_is_game_in_settings(game_path):
                games_to_add.append(game_path)

    return games_to_add


def collect_games_to_remove():
    games_to_remove = []
    loaded_settings = get_settings()
    all_games = loaded_settings.get("games", [])

    for game in all_games:
        install_dir = game.get("install_dir")
        path = pathlib.Path(install_dir)
        if not os.path.isdir(install_dir):
            games_to_remove.append(path)
        elif not ue4ss.is_ue4ss_installed(
            path
        ) and not unreal_engine.does_directory_contain_unreal_game(path):
            games_to_remove.append(path)

    return games_to_remove


def init_settings():
    global has_inited_settings
    if not os.path.isfile(SETTINGS_FILE):
        make_settings_file()

    has_inited_settings = True
    logger.log_message(f"Settings initialized from {SETTINGS_FILE}")


def get_settings() -> tomlkit.TOMLDocument:
    if not os.path.isfile(SETTINGS_FILE):
        logger.log_message(f"Settings file {SETTINGS_FILE} does not exist!")
        raise FileNotFoundError("Missing settings file.")

    with open(SETTINGS_FILE, "r") as f:
        settings_data = tomlkit.load(f)

    return settings_data


def get_game_dirs_in_settings() -> list[pathlib.Path]:
    settings_game_dirs = []
    for entry in get_game_entries_in_settings():
        settings_game_dirs.append(os.path.normpath(entry.get("install_dir")))
    return settings_game_dirs


def get_install_dirs_to_game_titles() -> dict[str, str]:
    install_dir_dict = {}
    for game in get_game_entries_in_settings():
        game_title = game.get("game_title")
        install_dir = game.get("install_dir")

        if game_title in constants.INVALID_GAMES:
            continue

        matched = False
        for game_key in constants.GAME_PATHS_TO_DISPLAY_NAMES.keys():
            if game_key in install_dir:
                display_name = constants.GAME_PATHS_TO_DISPLAY_NAMES[game_key]
                install_dir_dict[install_dir] = display_name
                matched = True
                break

        if not matched:
            install_dir_dict[install_dir] = game_title

    return install_dir_dict


def get_game_titles_to_install_dirs() -> dict[str, str]:
    game_dict = {}
    for game in get_game_entries_in_settings():
        game_title = game.get("game_title")
        install_dir = game.get("install_dir")

        if game_title in constants.INVALID_GAMES:
            continue

        matched = False
        for game_key in constants.GAME_PATHS_TO_DISPLAY_NAMES.keys():
            if game_key in install_dir:
                display_name = constants.GAME_PATHS_TO_DISPLAY_NAMES[game_key]
                game_dict[display_name] = install_dir
                matched = True
                break

        if not matched:
            game_dict[game_title] = install_dir

    return game_dict


def get_game_info_instance_in_settings_from_game_directory(
    game_directory: str,
) -> data_structures.GameInfo | None:
    for game in get_game_entries_in_settings():
        if os.path.normpath(game.get("install_dir")) == os.path.normpath(
            game_directory
        ):
            return game_info_dict_to_game_info_data_class(game)
    return None


def game_info_data_class_to_game_info_dict(game_info: data_structures.GameInfo) -> dict:
    return {
        "install_dir": os.path.normpath(str(game_info.install_dir)),
        "game_title": game_info.game_title,
        "ue4ss_version": game_info.ue4ss_version,
        "last_installed_version": game_info.last_installed_version,
        "platform": game_info.platform.value
        if hasattr(game_info.platform, "value")
        else game_info.platform,
        "using_developer_version": game_info.using_developer_version,
        "show_pre_releases": game_info.show_pre_releases,
        "using_portable_version": game_info.using_portable_version,
        "using_keep_mods_and_settings": game_info.using_keep_mods_and_settings,
        "installed_files": [str(path) for path in game_info.installed_files],
    }


def game_info_dict_to_game_info_data_class(game_dict: dict) -> data_structures.GameInfo:
    return data_structures.GameInfo(
        install_dir=pathlib.Path(game_dict["install_dir"]),
        game_title=game_dict["game_title"],
        ue4ss_version=game_dict["ue4ss_version"],
        last_installed_version=game_dict.get("last_installed_version", ""),
        platform=data_structures.GamePlatforms(
            data_structures.get_enum_from_val(
                data_structures.GamePlatforms, game_dict["platform"]
            )
        ),
        using_developer_version=game_dict["using_developer_version"],
        show_pre_releases=game_dict["show_pre_releases"],
        using_portable_version=game_dict.get("using_portable_version", False),
        using_keep_mods_and_settings=game_dict["using_keep_mods_and_settings"],
        installed_files=[
            pathlib.Path(installed_file_path)
            for installed_file_path in game_dict.get("installed_files", [])
        ],
    )


def save_game_info_to_settings_file(game_info: data_structures.GameInfo):
    loaded_settings = get_settings()
    games_list = loaded_settings.get("games", [])

    install_dir_str = os.path.normpath(str(game_info.install_dir))
    updated_game_dict = game_info_data_class_to_game_info_dict(game_info)

    for game in games_list:
        if os.path.normpath(game["install_dir"]) == install_dir_str:
            game.update(updated_game_dict)
            break
    else:
        games_list.append(updated_game_dict)

    loaded_settings["games"] = games_list
    save_settings(loaded_settings)


def remove_game_entries_by_game_dirs(
    game_directories: list[pathlib.Path], loaded_settings: dict
) -> dict:
    for game_directory in game_directories:
        games = loaded_settings.get("games", [])

        target_path = game_directory.resolve(strict=False)
        updated_games = []

        for game in games:
            install_dir = os.path.normpath(game.get("install_dir"))
            if install_dir is None:
                updated_games.append(game)
                continue

            install_path = pathlib.Path(install_dir).resolve(strict=False)
            if install_path != target_path:
                updated_games.append(game)

        loaded_settings["games"] = updated_games
    return loaded_settings


def get_settings_gui_section_from_settings():
    return get_settings().get("GUI", {})


def get_default_theme_name() -> str:
    return "grey"


def get_preferred_theme_name_from_settings():
    return get_settings_gui_section_from_settings().get(
        "preferred_theme", get_default_theme_name()
    )


def get_game_entries_in_settings():
    return get_settings().get("games", [])


def get_custom_game_directories():
    return get_settings().get("custom_game_directories", [])


def save_global_font_scale(font_scale: float):
    loaded_settings = get_settings()
    gui_settings = loaded_settings.get("GUI", {})
    gui_settings["global_font_scale"] = font_scale
    loaded_settings["GUI"] = gui_settings
    save_settings(loaded_settings)


def get_gui_setting(key, default=None):
    return get_settings_gui_section_from_settings().get(key, default)


def get_use_force_online_mode_in_settings():
    return get_gui_setting("use_force_offline_mode", False)


def get_use_automatic_game_scanning_in_settings():
    return get_gui_setting("use_automatic_game_scanning", True)


def get_language_from_settings():
    return get_gui_setting("language", get_default_locale())


def get_use_language_override_from_settings():
    return get_gui_setting("use_language_override", False)


def get_custom_font_path_from_settings():
    return get_gui_setting("custom_font_path", get_system_font_path())


def get_use_custom_font_from_settings():
    return get_gui_setting("use_custom_font", False)


def get_global_font_scale_from_settings():
    return get_gui_setting("global_font_scale", 1.0)


def get_system_font_path() -> str | None:
    system = platform.system()
    if system == "Windows":
        return os.path.normpath("C:/Windows/Fonts/arial.ttf")
    elif system == "Linux":
        possible_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
        for path in possible_paths:
            if os.path.isfile(path):
                return os.path.normpath(path)
    return None


def set_app_window_properties_in_settings(width, height, x_position, y_position):
    loaded_settings = get_settings()
    gui_settings = loaded_settings.get("GUI", {})

    gui_settings["x"] = x_position
    gui_settings["y"] = y_position
    gui_settings["width"] = width
    gui_settings["height"] = height

    loaded_settings["GUI"] = gui_settings
    save_settings(loaded_settings)


def update_gui_setting(key, value):
    loaded_settings = get_settings()
    gui_settings = loaded_settings.get("GUI", {})
    gui_settings[key] = value
    loaded_settings["GUI"] = gui_settings
    save_settings(loaded_settings)


def save_custom_font_path_to_settings(app_data):
    update_gui_setting("custom_font_path", app_data["file_path_name"])


def toggle_force_offline_mode_in_settings_file(sender, app_data, user_data):
    update_gui_setting("use_force_offline_mode", app_data)


def toggle_use_custom_font_in_settings_file(app_data):
    update_gui_setting("use_custom_font", app_data)


def toggle_use_automatic_game_scanning_in_settings_file(sender, app_data, user_data):
    update_gui_setting("use_automatic_game_scanning", app_data)


def language_combo_box_selection_changed(sender, app_data, user_data):
    update_gui_setting("language", app_data)


def toggle_use_language_override_in_settings_file(app_data):
    update_gui_setting("use_language_override", app_data)


def change_preferred_theme_in_settings(app_data):
    update_gui_setting("preferred_theme", app_data or "default")
