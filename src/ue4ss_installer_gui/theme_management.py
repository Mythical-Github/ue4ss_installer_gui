from ue4ss_installer_gui import settings
from ue4ss_installer_gui.themes import (
    dracula,
    grey,
    halloween,
    tokyo_night,
    tokyo_night_dark,
    retro,
    jaguar
)


def get_preferred_theme():
    return get_theme_from_theme_name(settings.get_preferred_theme_name_from_settings())


def get_preferred_theme_name():
    return settings.get_preferred_theme_name_from_settings()


def get_theme_from_theme_name(theme_name: str):
    theme_func = theme_labels_to_themes.get(theme_name)
    if theme_func:
        return theme_func()
    else:
        return theme_labels_to_themes.get(settings.get_default_theme_name())


def get_default_theme():
    return get_theme_from_theme_name(settings.get_default_theme_name())


theme_labels_to_themes = {
    "grey": grey.create_theme,
    "retro": retro.create_theme,
    "dracula": dracula.create_theme,
    "tokyo_night": tokyo_night.create_theme,
    "tokyo_night_dark": tokyo_night_dark.create_theme,
    "halloween": halloween.create_theme,
    "jaguar": jaguar.create_theme
}
