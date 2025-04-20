import os
import requests
import pathlib


ALL_TAGS = []
PRE_RELEASE_TAGS = []
NORMAL_RELEASE_TAGS = []


DEFAULT_ALL_TAGS = [
    "v3.0.1",
    "v3.0.0",
    "v2.5.2",
    "v2.5.1",
    "v2.5.0",
    "v2.3.1-Hotfix",
    "v2.3.0",
    "v2.2.1-Hotfix",
    "v2.2.0",
    "v2.1.1-HotFix",
    "v2.1.0",
    "v2.0.0.1Alpha-Hotfix",
    "v2.0Alpha",
    "v1.3.6",
    "v1.3.5-RE",
    "experimental-latest",
    "experimental",
]
DEFAULT_PRE_RELEASE_TAGS = [
    "v2.0.0.1Alpha-Hotfix",
    "v1.3.6",
    "v1.3.5-RE",
    "experimental-latest",
    "experimental",
]
DEFAULT_NORMAL_RELEASE_TAGS = [
    "v3.0.1",
    "v3.0.0",
    "v2.5.2",
    "v2.5.1",
    "v2.5.0",
    "v2.3.1-Hotfix",
    "v2.3.0",
    "v2.2.1-Hotfix",
    "v2.2.0",
    "v2.1.1-HotFix",
    "v2.1.0",
    "v2.0Alpha",
]


def get_all_tags_from_repo_url(repo_url: str) -> list[str]:
    """Returns a list of all Git tags from the GitHub repository."""
    repo = repo_url.rstrip("/").replace("https://github.com/", "")
    url = f"https://api.github.com/repos/{repo}/tags"
    tags = []

    page = 1
    while True:
        response = requests.get(url, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to fetch tags: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        tags.extend(tag["name"] for tag in data)
        page += 1

    return tags


def get_all_pre_release_tags_from_repo_url(repo_url: str) -> list[str]:
    """Returns a list of pre-release tags from the GitHub repository."""
    repo = repo_url.rstrip("/").replace("https://github.com/", "")
    url = f"https://api.github.com/repos/{repo}/releases"
    response = requests.get(url)
    releases = response.json()

    pre_release_tags = [
        release["tag_name"] for release in releases if release.get("prerelease")
    ]
    return pre_release_tags


def get_all_normal_release_tags_from_repo_url(repo_url: str) -> list[str]:
    """Returns a list of normal (non-pre-release) tags from the GitHub repository."""
    repo = repo_url.rstrip("/").replace("https://github.com/", "")
    url = f"https://api.github.com/repos/{repo}/releases"
    response = requests.get(url)
    releases = response.json()

    normal_release_tags = [
        release["tag_name"] for release in releases if not release.get("prerelease")
    ]
    return normal_release_tags


def get_file_names_to_download_links_from_github_repo_tag(
    repo_url: str, tag: str
) -> dict[str, str]:
    """Returns a dictionary mapping file names to download URLs for a specific release tag."""
    repo = repo_url.rstrip("/").replace("https://github.com/", "")
    url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"
    response = requests.get(url)
    release = response.json()

    download_links = {
        asset["name"]: asset["browser_download_url"]
        for asset in release.get("assets", [])
    }
    return download_links


def get_default_ue4ss_version_tag() -> str:
    return "latest"


def is_ue4ss_installed(game_directory: pathlib.Path) -> bool:
    if os.path.isdir(game_directory):
        for dir_one_level_in in game_directory.iterdir():
            if not dir_one_level_in.is_dir():
                continue

            win64_dir = dir_one_level_in / "Binaries" / "Win64"

            if not win64_dir.is_dir():
                continue

            if (win64_dir / "dwmapi.dll").is_file():
                if (win64_dir / "ue4ss" / "ue4ss.dll").is_file():
                    return True
                if (win64_dir / "ue4ss.dll").is_file():
                    return True

            if (win64_dir / "xinput1_3.dll").is_file() and (
                win64_dir / "UE4SS-settings.ini"
            ).is_file():
                return True
    return False
