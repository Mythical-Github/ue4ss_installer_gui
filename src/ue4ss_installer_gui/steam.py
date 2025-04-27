import os
import re
import pathlib

from ue4ss_installer_gui import file_io, settings


def get_windows_steam_registry_paths() -> list[pathlib.Path]:
    """Get Steam library paths from Windows Registry."""
    import winreg
    steam_dirs = []
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, fr"Software\Valve\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            steamapps_common = pathlib.Path(steam_path) / "steamapps" / "common"
            if steamapps_common.is_dir():
                for game_dir in steamapps_common.iterdir():
                    if game_dir.is_dir():
                        steam_dirs.append(game_dir)
    except Exception:
        pass
    return steam_dirs


def get_windows_default_steam_paths() -> list[pathlib.Path]:
    """Get Steam library paths from default drive locations."""
    steam_dirs = []
    for drive_letter in file_io.get_all_drive_letter_paths():
        if drive_letter.startswith("C"):
            steam_directory = os.path.normpath(
                f"{drive_letter}Program Files (x86)/Steam/steamapps/common"
            )
        else:
            steam_directory = os.path.normpath(
                f"{drive_letter}SteamLibrary/steamapps/common"
            )
        if os.path.isdir(steam_directory):
            for game_dir in pathlib.Path(steam_directory).iterdir():
                if game_dir.is_dir():
                    steam_dirs.append(game_dir)
    return steam_dirs


def get_linux_default_steam_paths() -> list[pathlib.Path]:
    """Get Steam library paths from default Linux locations."""
    steam_dirs = []
    steamapps_dirs = [
        os.path.expanduser("~/.steam/steam/steamapps"),
        os.path.expanduser("~/.local/share/Steam/steamapps"),
        os.path.expanduser("~/Steam/steamapps"),
        os.path.expanduser("~/snap/steam/common/.steam/steam/steamapps"),
        os.path.expanduser("~/snap/steam/current/.steam/steam/steamapps"),
    ]
    for steamapps in steamapps_dirs:
        common_path = pathlib.Path(steamapps) / "common"
        if common_path.is_dir():
            for game_dir in common_path.iterdir():
                if game_dir.is_dir():
                    steam_dirs.append(game_dir)
    return steam_dirs


def get_linux_libraryfolders_paths() -> list[pathlib.Path]:
    """Get Steam library paths from Linux libraryfolders.vdf files."""
    steam_dirs = []
    steamapps_dirs = [
        os.path.expanduser("~/.steam/steam/steamapps"),
        os.path.expanduser("~/.local/share/Steam/steamapps"),
        os.path.expanduser("~/Steam/steamapps"),
        os.path.expanduser("~/snap/steam/common/.steam/steam/steamapps"),
        os.path.expanduser("~/snap/steam/current/.steam/steam/steamapps"),
    ]
    for steamapps in steamapps_dirs:
        vdf_path = pathlib.Path(steamapps) / "libraryfolders.vdf"
        if vdf_path.exists():
            try:
                with open(vdf_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                matches = re.findall(r'"\d+"\s*"\s*(.*?)\s*"', content)
                for match in matches:
                    other_common = pathlib.Path(match.strip()) / "steamapps/common"
                    if other_common.is_dir():
                        for game_dir in other_common.iterdir():
                            if game_dir.is_dir():
                                steam_dirs.append(game_dir)
            except Exception:
                pass
    return steam_dirs


def get_all_steam_game_directories() -> list[pathlib.Path]:
    """Combine all possible Steam game directories."""
    steam_dirs = []

    if settings.is_windows():
        steam_dirs.extend(get_windows_steam_registry_paths())
        steam_dirs.extend(get_windows_default_steam_paths())
    else:
        steam_dirs.extend(get_linux_default_steam_paths())
        steam_dirs.extend(get_linux_libraryfolders_paths())

    return steam_dirs
