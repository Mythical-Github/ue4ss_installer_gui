import os
import asyncio

from ue4ss_installer_gui import ue4ss, settings, translator, logger, file_io
from ue4ss_installer_gui.checks import online_check


def init():
    online_check.init_is_online()
    print(f"Is online: {online_check.is_online}")
    logger.set_log_base_dir(os.path.normpath(f"{file_io.SCRIPT_DIR}/logs"))
    logger.configure_logging()
    settings.init_settings()
    translator.init_translator()
    if online_check.is_online:
        asyncio.run(auto_fetch_tags_on_start())
    asyncio.run(auto_scan_dirs())


async def auto_fetch_tags_on_start():
    ue4ss.cache_repo_releases_info("UE4SS-RE", "RE-UE4SS")


async def auto_scan_dirs():
    # do dir scanning here and populate the scroll box once it's ready, have scrollbox loading thing or something
    return
