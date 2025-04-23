import os
from pathlib import Path
from typing import List, Union

from ue4ss_installer_gui import constants

MAX_DEPTH = 2


def is_unreal_game_dir(
    root_dir: str, max_depth: int = MAX_DEPTH, include_uninstalled: bool = True
) -> bool:
    content_found = False
    win_found = False
    exe_found = False

    stack = [(root_dir, 0)]

    while stack:
        path, depth = stack.pop()
        if depth > max_depth:
            continue

        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        name = entry.name
                        if name == "Content":
                            content_found = True
                        elif name in ("Win64", "WinGDK"):
                            win_found = True

                        if (
                            content_found
                            and win_found
                            and (include_uninstalled or exe_found)
                        ):
                            return True

                        stack.append((entry.path, depth + 1))

                    elif entry.is_file(follow_symlinks=False):
                        if (
                            not include_uninstalled
                            and not exe_found
                            and entry.name.lower().endswith(".exe")
                        ):
                            exe_found = True

                            if content_found and win_found:
                                return True

        except PermissionError:
            continue

    return content_found and win_found and (include_uninstalled or exe_found)


def get_all_unreal_game_directories_in_directory_tree(
    root_directory: Union[str, Path],
    include_uninstalled_existing_game_dirs: bool = True,
    max_depth: int = MAX_DEPTH,
) -> List[str]:
    unreal_game_trees: List[str] = []
    root = Path(root_directory)

    for sub in root.iterdir():
        if not sub.is_dir():
            continue

        if is_unreal_game_dir(
            str(sub), max_depth, include_uninstalled_existing_game_dirs
        ):
            unreal_game_trees.append(str(sub))
        for game_name in constants.MULTI_GAME_NAMES:
            if os.path.basename(str(sub)).strip() == game_name:
                unreal_game_trees.extend(
                    get_all_unreal_game_directories_in_directory_tree(sub)
                )
    return unreal_game_trees


def does_directory_contain_unreal_game(directory: Path) -> bool:
    acceptable_dirs = [
        f"{directory}/Engine/Binaries",
        f"{directory}/Engine/Shared",
        f"{directory}/Windows/Engine/Shared",
        f"{directory}/Windows/Engine/Shared",
        f"{directory}/WindowsNoEditor/Engine/Shared",
        f"{directory}/WindowsNoEditor/Engine/Shared",
    ]
    acceptable_files = [f"{directory}/Manifest_NonUFSFiles_Win64.txt"]
    for acceptable_dir in acceptable_dirs:
        if os.path.isdir(os.path.normpath(acceptable_dir)):
            return True
    for acceptable_file in acceptable_files:
        if os.path.isfile(os.path.normpath(acceptable_file)):
            return True
    return False
