import os
import glob
import json
import locale
from string import Template
from ue4ss_installer_gui import file_io, settings

supported_format = ["json"]

translator = None


def init_translator():
    global translator
    translator = Translator(
        os.path.normpath(f"{file_io.SCRIPT_DIR}/assets/localization")
    )

    language = settings.get_settings().get("GUI", {}).get("language", "en")

    if not language:
        system_locale = locale.getdefaultlocale()[0]
        language = system_locale.split("_")[0] if system_locale else "en"

    translator.set_locale(language)
    print(f"Using locale: {translator.get_locale()}")


class Translator:
    def __init__(self, translations_folder, file_format="json", default_locale="en"):
        self.data = {}
        self.locale = default_locale

        if file_format in supported_format:
            files = glob.glob(os.path.join(translations_folder, f"*.{file_format}"))
            for fil in files:
                loc = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, "r", encoding="utf8") as f:
                    self.data[loc] = json.load(f)

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print(f"Invalid locale: {loc}")

    def get_locale(self):
        return self.locale

    def translate(self, key, **kwargs):
        translations = self.data.get(self.locale, {})
        value = translations.get(key, key)

        if isinstance(value, dict):
            count = kwargs.get("count", 1)
            try:
                count = int(count)
            except ValueError:
                print("Invalid count value for pluralization")
                return key
            plural_form = "one" if count == 1 else "other"
            value = value.get(plural_form, key)

        return Template(value).safe_substitute(**kwargs)
