import sys
import os
import argparse

from website_generator.utils import (
    validate_input_directory,
    copy_stylesheet,
    copy_assets_directory
)
from website_generator.constants import (
    CONFIG_FILENAME,
    TEMPLATE_FILENAME,
    PAGES_DIRNAME,
    INDEX_FILENAME
)
from website_generator.config import read_config_dict
from website_generator.html import generate_base_template
from website_generator.pages import process_content_pages, process_index_page

def parse_args():
    parser = argparse.ArgumentParser(description="Website-Generator: Static site generator for blogs.")
    parser.add_argument("input_dir", help="Path to input directory containing site source files")
    parser.add_argument(
        "-o", "--output",
        help="Path to output directory (default: <input_dir>/outputs)",
        default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_dir = args.input_dir
    validate_input_directory(input_dir)
    
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(input_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    config_path = os.path.join(input_dir, CONFIG_FILENAME)
    config_dict = read_config_dict(config_path)

    template_path = os.path.join(input_dir, TEMPLATE_FILENAME)
    base_template = generate_base_template(template_path, config_dict)

    blog_index_entries = process_content_pages(input_dir, output_dir, base_template)

    index_path = os.path.join(input_dir, PAGES_DIRNAME, INDEX_FILENAME)
    lang_code = config_dict.get('lang', 'en')
    fallback_title = config_dict['title']
    process_index_page(index_path, output_dir, base_template, blog_index_entries, lang_code, fallback_title)

    # Copy stylesheet and assets directory to output directory:
    copy_stylesheet(input_dir, output_dir)
    copy_assets_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
