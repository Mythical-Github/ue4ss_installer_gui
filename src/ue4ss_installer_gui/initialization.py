import asyncio
from ue4ss_installer_gui import ue4ss, constants

def init():
    asyncio.run(auto_fetch_tags_on_start(constants.UE4SS_REPO_URL))
    asyncio.run(auto_scan_dirs())

async def auto_fetch_tags_on_start(repo_url: str):
    ue4ss.ALL_TAGS = ue4ss.get_all_tags_from_repo_url(repo_url)


async def auto_scan_dirs():
    # do dir scanning here and populate the scroll box once it's ready, have scrollbox loading thing or something
    return