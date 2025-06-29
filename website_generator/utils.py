import os
import sys
import shutil
from babel.dates import format_date
from datetime import date

from website_generator.constants import (
    TEMPLATE_FILENAME,
    CONFIG_FILENAME,
    PAGES_DIRNAME,
    INDEX_FILENAME,
    ASSETS_DIRNAME,
    STYLESHEET_FILENAME
)


def validate_input_directory(input_dir: str) -> bool:
    """
    Validates that the given input directory exists and contains:
    - base template file: 'template.html'
    - configuration file: 'config.ini'
    - subdirectory: 'pages/' containing at least 'index.html'
    """
    required_files = [TEMPLATE_FILENAME, CONFIG_FILENAME]
    required_subdir = PAGES_DIRNAME
    required_page_file = INDEX_FILENAME

    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    for filename in required_files:
        path = os.path.join(input_dir, filename)
        if not os.path.isfile(path):
            print(f"Error: Required file '{filename}' not found in '{input_dir}'.", file=sys.stderr)
            sys.exit(1)

    pages_dir = os.path.join(input_dir, required_subdir)
    if not os.path.isdir(pages_dir):
        print(
            f"Error: Required subdirectory '{required_subdir}' not found in '{input_dir}'.",
            file=sys.stderr
        )
        sys.exit(1)

    index_path = os.path.join(pages_dir, required_page_file)
    if not os.path.isfile(index_path):
        print(
            f"Error: '{required_page_file}' not found in '{required_subdir}' directory.",
            file=sys.stderr
        )
        sys.exit(1)
    return True


def get_localized_date(d: date, lang_code: str, include_year: bool = False) -> str:
    try:
        if include_year:
            return format_date(d, format='long', locale=lang_code)
        elif lang_code == 'de':
            return format_date(d, format='dd. MMM', locale=lang_code)
        elif lang_code == 'en':
            return format_date(d, format='MMM dd', locale=lang_code)
        else:
            return format_date(d, format='dd MMM', locale=lang_code)
    except Exception:
        return format_date(d, format='long' if include_year else 'MMM dd', locale='en')


def copy_stylesheet(input_dir: str, output_dir: str):
    src = os.path.join(input_dir, STYLESHEET_FILENAME)
    dst = os.path.join(output_dir, STYLESHEET_FILENAME)
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except OSError as e:
            print(f"Error copying stylesheet: {e}", file=sys.stderr)


def copy_assets_directory(input_dir: str, output_dir: str):
    assets_input_dir = os.path.join(input_dir, ASSETS_DIRNAME)
    assets_output_dir = os.path.join(output_dir, ASSETS_DIRNAME)
    shutil.copytree(assets_input_dir, assets_output_dir, dirs_exist_ok=True)
    
