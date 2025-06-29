import configparser
from datetime import date

from website_generator.utils import get_localized_date

def read_config_dict(config_path: str) -> dict:
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(config_path)
    config_dict = dict(config[configparser.UNNAMED_SECTION])

    # Remove 'page_title' and 'content' if present
    config_dict.pop('page_title', None)
    config_dict.pop('content', None)

    required_keys = {'title', 'author'}
    missing_keys = required_keys - config_dict.keys()
    if missing_keys:
        print(f"Error: Missing required config keys: {', '.join(missing_keys)}", file=sys.stderr)
        sys.exit(1)
    # Set default language to 'en' if not provided or empty
    lang = config_dict.get('lang').strip().lower() or 'en'
    config_dict['lang'] = lang
    config_dict['date'] = get_localized_date(date.today(), lang, include_year=True)
    return config_dict
