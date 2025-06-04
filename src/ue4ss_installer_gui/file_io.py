import os
import sys
import pathlib
import requests
import zipfile


SCRIPT_DIR = (
    pathlib.Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else pathlib.Path(__file__).resolve().parent
)


PACKED_DIR = sys._MEIPASS if getattr(sys, "frozen", False) else SCRIPT_DIR  # type: ignore


def get_all_drive_letter_paths() -> list[str]:
    drive_letters = []
    for drive in range(0, 26):
        drive_letter = f"{chr(drive + ord('A'))}:\\"
        if os.path.exists(drive_letter):
            drive_letters.append(drive_letter)
    return drive_letters


def get_temp_dir() -> pathlib.Path:
    return pathlib.Path(os.path.normpath(f"{SCRIPT_DIR}/temp"))


def download_file(url, destination_path):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {destination_path}")
    except Exception as e:
        print(f"Failed to download {url} -> {e}")


def unzip_zip(zip_file: pathlib.Path, output_directory: pathlib.Path):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(output_directory)


def get_paths_of_files_in_zip(zip_file: pathlib.Path) -> list[str]:
    paths_of_files_in_zip = []
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        paths_of_files_in_zip = zip_ref.namelist()
    return paths_of_files_in_zip


def get_contents_of_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return file.read()


def save_content_to_file(content: str, file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
