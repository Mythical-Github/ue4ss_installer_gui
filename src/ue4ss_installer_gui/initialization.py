import asyncio

from ue4ss_installer_gui import ue4ss


def init():
    asyncio.run(auto_fetch_tags_on_start())
    asyncio.run(auto_scan_dirs())


async def auto_fetch_tags_on_start():
    ue4ss.cache_repo_releases_info("UE4SS-RE", "RE-UE4SS")


async def auto_scan_dirs():
    # do dir scanning here and populate the scroll box once it's ready, have scrollbox loading thing or something
    return
