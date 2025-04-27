import os
import pathlib
from typing import List, Union


MAX_DEPTH = 2


def get_all_win_gdk_dirs_in_dir_tree(directory: pathlib.Path) -> List[pathlib.Path]:
    return [p for p in directory.rglob("*") if p.is_dir() and p.name == "WinGDK"]


def get_all_win_64_dirs_in_dir_tree(directory: pathlib.Path) -> List[pathlib.Path]:
    return [p for p in directory.rglob("*") if p.is_dir() and p.name == "Win64"]


def get_all_main_exe_dirs_in_dir_tree(directory: pathlib.Path) -> List[pathlib.Path]:
    return get_all_win_gdk_dirs_in_dir_tree(
        directory
    ) + get_all_win_64_dirs_in_dir_tree(directory)


def does_dir_tree_contain_multiple_main_exe_dirs(directory: pathlib.Path) -> bool:
    dirs = get_all_main_exe_dirs_in_dir_tree(directory)
    return len(dirs) > 1


def does_root_dir_contain_windows_dir(directory: pathlib.Path) -> bool:
    return (directory / "Windows").is_dir()


def does_root_dir_contain_windows_no_editor_dir(directory: pathlib.Path) -> bool:
    return (directory / "WindowsNoEditor").is_dir()


def does_root_dir_contain_exe(directory: pathlib.Path) -> bool:
    return any(file.suffix.lower() == ".exe" for file in directory.glob("*"))


def is_unreal_game_dir(
    root_dir: Union[str, pathlib.Path],
    max_depth: int = MAX_DEPTH,
    include_uninstalled: bool = True,
) -> bool:
    content_found = False
    win_found = False
    exe_found = False
    binaries_win64_found = False

    stack = [(pathlib.Path(root_dir), 0)]

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
                        elif name == "Binaries":
                            binaries_win64 = pathlib.Path(entry.path) / "Win64"
                            if binaries_win64.is_dir():
                                if any(
                                    f.suffix.lower() == ".exe"
                                    for f in binaries_win64.glob("*.exe")
                                ):
                                    binaries_win64_found = True
                        stack.append((pathlib.Path(entry.path), depth + 1))

                    elif entry.is_file(follow_symlinks=False):
                        if entry.name.lower().endswith(".exe"):
                            exe_found = True

                    if (
                        content_found
                        and win_found
                        and (include_uninstalled or exe_found)
                    ):
                        return True

        except PermissionError:
            continue

    if binaries_win64_found:
        return True

    return content_found and win_found and (include_uninstalled or exe_found)


def get_all_unreal_game_directories_in_directory_tree(
    root_directory: Union[str, pathlib.Path],
    include_uninstalled_existing_game_dirs: bool = True,
    max_depth: int = MAX_DEPTH,
) -> List[str]:
    unreal_game_dirs: List[str] = []
    root = pathlib.Path(root_directory)

    def recursive_scan(current_dir: pathlib.Path, depth: int):
        if depth > max_depth:
            return

        if is_unreal_game_dir(
            current_dir,
            max_depth=1,
            include_uninstalled=include_uninstalled_existing_game_dirs,
        ):
            unreal_game_dirs.append(str(current_dir))

        try:
            for sub in current_dir.iterdir():
                if sub.is_dir():
                    recursive_scan(sub, depth + 1)
        except PermissionError:
            pass

    recursive_scan(root, 0)
    return unreal_game_dirs


def does_dir_contain_engine_binaries_folder(directory: pathlib.Path) -> bool:
    return (directory / "Engine" / "Binaries").is_dir()


def does_dir_contain_engine_shared_folder(directory: pathlib.Path) -> bool:
    return (directory / "Engine" / "Shared").is_dir()


def does_dir_contain_unreal_manifest_file(directory: pathlib.Path) -> bool:
    return (directory / "Manifest_NonUFSFiles_Win64.txt").is_file()


def does_directory_contain_unreal_game(directory: pathlib.Path) -> bool:
    checks = [
        does_dir_contain_engine_binaries_folder(directory),
        does_dir_contain_engine_shared_folder(directory),
        does_dir_contain_unreal_manifest_file(directory),
    ]
    if not any(checks):
        for subdir in ("Windows", "WindowsNoEditor"):
            sub_path = directory / subdir
            checks.extend(
                [
                    does_dir_contain_engine_binaries_folder(sub_path),
                    does_dir_contain_engine_shared_folder(sub_path),
                ]
            )
    return any(checks)
