import os
import asyncio

from ue4ss_installer_gui import ue4ss, settings, translator, logger, file_io
from ue4ss_installer_gui.checks import online_check


def init():
    settings.init_settings()
    loaded_settings = settings.get_settings()
    use_force_offline_mode = loaded_settings.get('GUI', {}).get('use_force_offline_mode', False)
    if not use_force_offline_mode:
        online_check.init_is_online()
    print(f"Is online: {online_check.is_online}")
    logger.set_log_base_dir(os.path.normpath(f"{file_io.SCRIPT_DIR}/logs"))
    logger.configure_logging()
    translator.init_translator()
    if online_check.is_online:
        asyncio.run(auto_fetch_tags_on_start())


async def auto_fetch_tags_on_start():
    ue4ss.cache_repo_releases_info("UE4SS-RE", "RE-UE4SS")
