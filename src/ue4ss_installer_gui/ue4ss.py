import os
import pathlib
import requests
from typing import Dict, List
from dataclasses import dataclass, field


cached_repo_releases_info = None


@dataclass
class ReleaseAssetInfo:
    tag: str
    is_prerelease: bool
    is_latest: bool
    has_assets: bool
    created_at: str
    assets: Dict[str, str] = field(default_factory=dict)


@dataclass
class RepositoryReleasesInfo:
    owner: str
    repo: str
    tags: List[ReleaseAssetInfo]


def cache_repo_releases_info(owner: str, repo: str):
    """
    Caches the repo releases information to avoid redundant API calls.
    """
    global cached_repo_releases_info
    if cached_repo_releases_info is None:
        cached_repo_releases_info = get_all_release_assets(owner, repo)


def get_file_name_to_download_links_from_tag(tag: str) -> dict[str, str]:
    """
    Given a tag, return a dictionary mapping filenames to their download links.
    """
    global cached_repo_releases_info
    if cached_repo_releases_info is None:
        raise Exception(
            "Repo release info is not cached. Please call cache_repo_releases_info first."
        )

    for tag_info in cached_repo_releases_info.tags:
        if tag_info.tag == tag:
            return tag_info.assets

    return {}


def get_all_release_assets(owner: str, repo: str) -> RepositoryReleasesInfo:
    """
    Fetches all release tags with metadata for a GitHub repo, sorted from newest to oldest.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Accept": "application/vnd.github.v3+json"}

    all_releases = []
    page = 1

    while True:
        response = requests.get(
            url, headers=headers, params={"page": page, "per_page": 100}
        )
        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} - {response.text}"
            )
        releases = response.json()
        if not releases:
            break
        all_releases.extend(releases)
        page += 1

    sorted_releases = sorted(
        all_releases, key=lambda r: r.get("created_at", ""), reverse=True
    )

    tag_infos = []

    latest_tag = None
    for release in sorted_releases:
        if not release.get("prerelease", False):
            latest_tag = release.get("tag_name")
            break

    for release in sorted_releases:
        tag = release.get("tag_name")
        is_prerelease = release.get("prerelease", False)
        created_at = release.get("created_at", "")
        assets_list = release.get("assets", [])
        assets = {asset["name"]: asset["browser_download_url"] for asset in assets_list}

        tag_infos.append(
            ReleaseAssetInfo(
                tag=tag,
                is_prerelease=is_prerelease,
                is_latest=(tag == latest_tag),
                has_assets=bool(assets),
                created_at=created_at,
                assets=assets,
            )
        )

    return RepositoryReleasesInfo(owner=owner, repo=repo, tags=tag_infos)


def get_default_ue4ss_version_tag() -> str:
    return get_normal_release_tags_with_assets()[0]


def is_ue4ss_installed(game_directory: pathlib.Path) -> bool:
    """
    Checks if UE4SS is installed in the provided game directory.
    """
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


def get_all_tags_with_assets() -> List[str]:
    """
    Returns all tag names that have associated assets (regardless of release type).
    """
    global cached_repo_releases_info
    if cached_repo_releases_info is None:
        raise Exception(
            "Repo release info is not cached. Please call cache_repo_releases_info first."
        )

    return [
        tag_info.tag
        for tag_info in cached_repo_releases_info.tags
        if tag_info.has_assets
    ]


def get_pre_release_tags_with_assets() -> List[str]:
    """
    Returns all prerelease tag names that have associated assets.
    """
    global cached_repo_releases_info
    if cached_repo_releases_info is None:
        raise Exception(
            "Repo release info is not cached. Please call cache_repo_releases_info first."
        )

    return [
        tag_info.tag
        for tag_info in cached_repo_releases_info.tags
        if tag_info.has_assets and tag_info.is_prerelease
    ]


def get_normal_release_tags_with_assets() -> List[str]:
    """
    Returns all normal (non-prerelease) tag names that have associated assets.
    """
    global cached_repo_releases_info
    if cached_repo_releases_info is None:
        raise Exception(
            "Repo release info is not cached. Please call cache_repo_releases_info first."
        )

    return [
        tag_info.tag
        for tag_info in cached_repo_releases_info.tags
        if tag_info.has_assets and not tag_info.is_prerelease
    ]
