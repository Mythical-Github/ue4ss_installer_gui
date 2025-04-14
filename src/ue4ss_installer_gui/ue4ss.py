import requests


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


def test():
    repo = "https://github.com/UE4SS-RE/RE-UE4SS"
    print(get_all_pre_release_tags_from_repo_url(repo))
    print(get_all_normal_release_tags_from_repo_url(repo))
    print(get_file_names_to_download_links_from_github_repo_tag(repo, "v2.2.1-Hotfix"))
