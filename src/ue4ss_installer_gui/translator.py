from babel.plural import PluralRule
import json
from string import Template
import glob
import os
import locale
from datetime import datetime
from babel.dates import format_datetime

from ue4ss_installer_gui import file_io


supported_format = ['json']


translator = None
def init_translator():
    global translator
    translator = Translator(f'{file_io.SCRIPT_DIR}/assets/localization')

    system_locale = locale.getdefaultlocale()[0]
    short_locale = system_locale.split('_')[0] if system_locale else 'en'

    translator.set_locale(short_locale)
    print(f"Using locale: {translator.get_locale()}")
    print(translator.translate('uninstall_button_text'))


class Translator():
    def __init__(self, translations_folder, file_format='json', default_locale='en'):
        # initialization
        self.data = {}
        self.locale = 'en'
        self.plural_rule = PluralRule({'one': 'n is 1'})

        # check if format is supported
        if file_format in supported_format:
            # get list of files with specific extensions
            files = glob.glob(os.path.join(translations_folder, f'*.{file_format}'))
            for fil in files:
                # get the name of the file without extension, will be used as locale name
                loc = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, 'r', encoding='utf8') as f:
                    if file_format == 'json':
                        self.data[loc] = json.load(f)

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print('Invalid locale')

    def get_locale(self):
        return self.locale

    def set_plural_rule(self, rule):
        try:
            self.plural_rule = PluralRule(rule)
        except Exception:
            print('Invalid plural rule')

    def get_plural_rule(self):
        return self.plural_rule

    def translate(self, key, **kwargs):
        # return the key instead of translation text if locale is not supported
        if self.locale not in self.data:
            return key

        text = self.data[self.locale].get(key, key)
        # type dict represents key with plural form
        if type(text) == dict:
            count = kwargs.get('count', 1)
            # parse count to int
            try:
                count = int(count)
            except Exception:
                print('Invalid count')
                return key
            text = text.get(self.plural_rule(count), key)
        return Template(text).safe_substitute(**kwargs)


def parse_datetime(dt, input_format='%Y-%m-%d', output_format='MMMM dd, yyyy', output_locale='en'):
    dt = datetime.strptime(dt, input_format)
    return format_datetime(dt, format=output_format, locale=output_locale)