import os
import tomlkit
from ue4ss_installer import file_io, logger

SETTINGS_FILE = os.path.normpath(f'{file_io.SCRIPT_DIR}/settings.toml')

def make_settings_file():
    settings = {
        'games': []
    }
    
    toml_str = tomlkit.dumps(settings)
    
    with open(SETTINGS_FILE, 'w') as f:
        f.write(toml_str)
    logger.log_message(f"Settings file created at {SETTINGS_FILE}")

def init_settings():
    if not os.path.isfile(SETTINGS_FILE):
        make_settings_file()
    logger.log_message(f"Settings initialized from {SETTINGS_FILE}")

def load_settings() -> tomlkit.TOMLDocument:
    if not os.path.isfile(SETTINGS_FILE):
        logger.log_message(f"Settings file {SETTINGS_FILE} does not exist!")
        raise FileNotFoundError('Missing settings file.')
    
    with open(SETTINGS_FILE, 'r') as f:
        settings_data = tomlkit.load(f)
    
    return settings_data

def save_settings(settings_dictionary: dict):
    toml_str = tomlkit.dumps(settings_dictionary)
    
    with open(SETTINGS_FILE, 'w') as f:
        f.write(toml_str)
    logger.log_message(f"Settings saved to {SETTINGS_FILE}")

