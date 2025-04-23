import os
import tomlkit
import pathlib
import platform

from ue4ss_installer_gui import (
    file_io,
    logger,
    steam,
    epic,
    unreal_engine,
    settings,
    ue4ss,
    constants,
    data_structures,
)
from ue4ss_installer_gui.screens import add_game

SETTINGS_FILE = os.path.normpath(f"{file_io.SCRIPT_DIR}/settings.toml")


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def make_settings_file():
    settings = {"games": []}

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
    game_entries = settings.get_settings().get("games", {})
    is_game_already_in_list = False
    for game_entry in game_entries:
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
    print(dict(loaded_settings))
    save_settings(loaded_settings)


has_inited_settings = False


def init_settings():
    global has_inited_settings
    if not os.path.isfile(SETTINGS_FILE):
        make_settings_file()

    games_to_remove = []
    games_to_add = []

    all_game_dirs = [
        game
        for dir_source in (
            steam.get_all_steam_game_directories(),
            epic.get_all_epic_games_game_directories(),
        )
        for base_dir in dir_source
        for game in unreal_engine.get_all_unreal_game_directories_in_directory_tree(
            str(base_dir)
        )
    ]
    for base_dir in settings.get_settings().get('custom_game_directories', []):
        for game in unreal_engine.get_all_unreal_game_directories_in_directory_tree(
            str(base_dir)
        ):
            all_game_dirs.append(game)
    str_game_settings_list = []
    for game_dir in settings.get_game_dirs_in_settings():
        str_game_settings_list.append(game_dir)
    all_game_dirs.extend(str_game_settings_list)
    for game_dir in all_game_dirs:
        if unreal_engine.does_directory_contain_unreal_game(
            pathlib.Path(game_dir)
        ) or ue4ss.is_ue4ss_installed(pathlib.Path(game_dir)):
            if not get_is_game_in_settings(pathlib.Path(game_dir)):
                games_to_add.append(pathlib.Path(game_dir))
    loaded_settings = get_settings()
    all_games = loaded_settings.get("games", [])
    all_game_dirs = []
    for game in all_games:
        install_dir = game.get("install_dir")
        if not os.path.isdir(install_dir):
            games_to_remove.append(pathlib.Path(install_dir))
        if not ue4ss.is_ue4ss_installed(
            pathlib.Path(install_dir)
        ) and not unreal_engine.does_directory_contain_unreal_game(
            pathlib.Path(install_dir)
        ):
            games_to_remove.append(pathlib.Path(install_dir))

    save_settings(
        remove_game_entries_by_game_dirs(
            games_to_remove, add_game.add_manual_games_to_settings_file(games_to_add)
        )
    )

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
    loaded_settings = settings.get_settings()
    games_list = loaded_settings.get("games", {})
    for entry in games_list:
        settings_game_dirs.append(entry.get("install_dir"))
    return settings_game_dirs


def get_game_titles_to_install_dirs() -> dict[str, str]:
    game_dict = {}
    for game in get_settings().get("games", []):
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
    for game in get_settings().get("games", []):
        if os.path.normpath(game.get("install_dir")) == os.path.normpath(
            game_directory
        ):
            return game_info_dict_to_game_info_data_class(game)
    return None


def game_info_data_class_to_game_info_dict(game_info: data_structures.GameInfo) -> dict:
    return {
        "install_dir": str(game_info.install_dir),
        "game_title": game_info.game_title,
        "ue4ss_version": game_info.ue4ss_version,
        "platform": game_info.platform.value
        if hasattr(game_info.platform, "value")
        else game_info.platform,
        "using_developer_version": game_info.using_developer_version,
        "show_pre_releases": game_info.show_pre_releases,
        "using_keep_mods_and_settings": game_info.using_keep_mods_and_settings,
        "installed_files": [str(path) for path in game_info.installed_files],
    }


def game_info_dict_to_game_info_data_class(game_dict: dict) -> data_structures.GameInfo:
    return data_structures.GameInfo(
        install_dir=pathlib.Path(game_dict["install_dir"]),
        game_title=game_dict["game_title"],
        ue4ss_version=game_dict["ue4ss_version"],
        platform=data_structures.GamePlatforms(
            data_structures.get_enum_from_val(
                data_structures.GamePlatforms, game_dict["platform"]
            )
        ),
        using_developer_version=game_dict["using_developer_version"],
        show_pre_releases=game_dict["show_pre_releases"],
        using_keep_mods_and_settings=game_dict["using_keep_mods_and_settings"],
        installed_files=[
            pathlib.Path(installed_file_path)
            for installed_file_path in game_dict.get("installed_files", [])
        ],
    )


def save_game_info_to_settings_file(game_info: data_structures.GameInfo):
    loaded_settings = get_settings()
    games_list = loaded_settings.get("games", [])

    install_dir_str = str(game_info.install_dir)
    updated_game_dict = game_info_data_class_to_game_info_dict(game_info)

    for game in games_list:
        if game["install_dir"] == install_dir_str:
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
            install_dir = game.get("install_dir")
            if install_dir is None:
                updated_games.append(game)
                continue

            install_path = pathlib.Path(install_dir).resolve(strict=False)
            if install_path != target_path:
                updated_games.append(game)

        loaded_settings["games"] = updated_games
    return loaded_settings
