from ue4ss_installer_gui import settings
from ue4ss_installer_gui.themes import (
    dracula,
    halloween,
    tokyo_night,
    tokyo_night_dark,
    retro,
    default,
    jaguar,
)


def get_preferred_theme():
    settings_data = settings.get_settings() or {}
    return get_theme_from_theme_name(
        settings_data.get("GUI", {}).get("preferred_theme", "default")
    )


def get_preferred_theme_name():
    settings_data = settings.get_settings() or {}
    return settings_data.get("GUI", {}).get("preferred_theme", "default")


def get_theme_from_theme_name(theme_name):
    theme_func = theme_labels_to_themes.get(theme_name)
    if theme_func:
        return theme_func()
    else:
        return theme_labels_to_themes.get("default")


def get_default_theme():
    return get_theme_from_theme_name("default")


theme_labels_to_themes = {
    "default": default.create_theme,
    "retro": retro.create_theme,
    "dracula": dracula.create_theme,
    "tokyo_night": tokyo_night.create_theme,
    "tokyo_night_dark": tokyo_night_dark.create_theme,
    "halloween": halloween.create_theme,
    "jaguar": jaguar.create_theme,
}
