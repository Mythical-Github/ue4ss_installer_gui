import os
import pathlib
from typing import List, Union


MAX_DEPTH = 1


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


def collect_dirs_with_depth(root_dir: pathlib.Path, max_depth: int) -> list[pathlib.Path]:
    all_dirs = []

    def walk_dir(current_path, current_depth):
        if current_depth > max_depth:
            return
        try:
            entries = list(os.scandir(current_path))
        except Exception as e:
            print(f"Skipping {current_path}: {e}")
            return

        all_dirs.append(current_path)
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                walk_dir(pathlib.Path(entry.path), current_depth + 1)

    walk_dir(root_dir, 0)
    return all_dirs


def is_unreal_game_dir(
    root_dir: Union[str, pathlib.Path],
    max_depth: int = 1,
    include_uninstalled: bool = True,
) -> bool:
    all_dirs = collect_dirs_with_depth(pathlib.Path(root_dir), max_depth)

    for _, directory in enumerate(all_dirs):
        if does_directory_contain_unreal_game(directory):
            if include_uninstalled:
                return True
            elif any(f.suffix.lower() == ".exe" for f in directory.glob("*.exe")):
                return True
    return False


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
