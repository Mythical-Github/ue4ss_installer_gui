import os
from typing import List
from pathlib import Path
from typing import Union


def get_all_directory_paths_in_tree(root_directory: Union[str, Path]) -> List[Path]:
    root = Path(root_directory)
    return [p for p in root.rglob("*") if p.is_dir()]


def get_all_unreal_game_directories_in_directory_tree(
    root_directory: str, include_uninstalled_existing_game_dirs: bool = True
) -> List[str]:
    unreal_game_trees = []

    for sub_dir_name in os.listdir(root_directory):
        sub_dir_path = os.path.join(root_directory, sub_dir_name)
        if not os.path.isdir(sub_dir_path):
            continue

        # Collect all folder names (base names only) recursively under sub_dir_path
        directories = get_all_directory_paths_in_tree(sub_dir_path)
        dir_names = []
        for directory in directories:
            dir_names.append(os.path.basename(directory))

        if ("Win64" in dir_names or "WinGDK" in dir_names) and "Content" in dir_names:
            if include_uninstalled_existing_game_dirs:
                unreal_game_trees.append(sub_dir_path)
            else:
                has_exe = False
                for dirpath, _, filenames in os.walk(sub_dir_path):
                    if any(fname.lower().endswith(".exe") for fname in filenames):
                        has_exe = True
                        break
                if has_exe:
                    unreal_game_trees.append(sub_dir_path)
    return unreal_game_trees
