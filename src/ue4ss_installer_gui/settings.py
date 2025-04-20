import os
import tomlkit
import pathlib

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


def make_settings_file():
    settings = {"games": []}

    toml_str = tomlkit.dumps(settings)

    with open(SETTINGS_FILE, "w") as f:
        f.write(toml_str)
    logger.log_message(f"Settings file created at {SETTINGS_FILE}")


def save_settings(settings_dictionary: dict):
    print(settings_dictionary)
    toml_str = tomlkit.dumps(settings_dictionary)

    with open(SETTINGS_FILE, "w") as f:
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
    str_game_settings_list = []
    for game_dir in settings.get_game_dirs_in_settings():
        str_game_settings_list.append(game_dir)
    all_game_dirs.extend(str_game_settings_list)
    for game_dir in all_game_dirs:
        if unreal_engine.does_directory_contain_unreal_game(
            pathlib.Path(game_dir)
        ) or ue4ss.is_ue4ss_installed(pathlib.Path(game_dir)):
            if not get_is_game_in_settings(pathlib.Path(game_dir)):
                add_game.add_manual_game_to_settings_file(pathlib.Path(game_dir))
    loaded_settings = get_settings()
    all_games = loaded_settings.get("games", [])
    all_game_dirs = []
    for game in all_games:
        install_dir = game.get("install_dir")
        if not os.path.isdir(install_dir):
            remove_game_entry_by_game_dir(pathlib.Path(install_dir))
        if not ue4ss.is_ue4ss_installed(
            pathlib.Path(install_dir)
        ) and not unreal_engine.does_directory_contain_unreal_game(
            pathlib.Path(install_dir)
        ):
            remove_game_entry_by_game_dir(pathlib.Path(install_dir))

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
    loaded_settings = get_settings()
    games = loaded_settings.get("games", [])
    for game in games:
        if os.path.normpath(game.get("install_dir")) == os.path.normpath(
            game_directory
        ):
            pathlib_installed_files_list = []
            for file in game.get("installed_files", []):
                pathlib_installed_files_list.append(pathlib.Path(file))
            game_info = data_structures.GameInfo(
                install_dir=pathlib.Path(game.get("install_dir")),
                game_title=game.get("game_title"),
                ue4ss_version=game.get("ue4ss_version"),
                installed_files=pathlib_installed_files_list,
                platform=data_structures.GamePlatforms(
                    data_structures.get_enum_from_val(
                        data_structures.GamePlatforms, game.get("platform")
                    )
                ),
            )
            return game_info
    return None
