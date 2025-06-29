import os
import sys
from datetime import datetime
from string import Template
from bs4 import BeautifulSoup

from website_generator.constants import BLOG_POST_PATTERN, PAGES_DIRNAME
from website_generator.html import extract_title_and_clean_html, generate_html_table

def process_content_pages(input_dir: str, output_dir: str, base_template: str):
    pages_dir = os.path.join(input_dir, PAGES_DIRNAME)
    blog_index_entries = []
    for filename in os.listdir(pages_dir):
        filepath = os.path.join(pages_dir, filename)
        if not os.path.isfile(filepath):
            continue
        elif not filename.endswith(".html"):
            continue
        elif filename == "index.html":
            continue
        try:
            index_entry = process_content_page(filepath, output_dir, base_template)
        except RuntimeError:
            print(f"Could not process file {filepath}. Skipping.", file=sys.stderr)
            continue
        if index_entry:
            blog_index_entries.append(index_entry)
    return blog_index_entries


def process_content_page(filepath: str, output_dir: str, base_template: str):
    """
    Processes a single HTML page by extracting the title, applying the template,
    and writing the result to the output directory.

    Args:
        filepath (str): Path to the HTML file.
        output_dir (str): Where to save the output file.
        base_template (Template): A string.Template instance with pre-filled values.
        blog_post_pattern (Pattern): Regex pattern to identify blog post filenames.

    Returns:
        tuple[datetime, str, str] or None: Blog index entry (date, title, filename) or None.

    Raises:
        RuntimeError: If the file can't be read or processed.
    """
    print(f"Processing {filepath}")
    filename = os.path.basename(filepath)
    match = BLOG_POST_PATTERN.match(filename)
    is_blogpost = False
    if match:
        is_blogpost = True
        year, month, day, fallback_title = match.groups()
        date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    else:
        fallback_title = os.path.splitext(filename)[0]
    title = process_page(filepath, output_dir, base_template, fallback_title)
    
    if is_blogpost:
        return (date_obj, title, filename)
    return None


def process_index_page(
    index_path: str,
    output_dir: str,
    base_template: str,
    blog_index_entries: list,
    lang_code: str,
    fallback_title: str
):
    blog_index_html = generate_html_table(blog_index_entries, lang_code)
    process_page(
        index_path,
        output_dir,
        base_template,
        fallback_title,
        extra_placeholders = {'index_table': blog_index_html}
    )


def process_page(
    filepath: str,
    output_dir: str,
    base_template: str,
    fallback_title: str,
    extra_placeholders=None
):
    filename = os.path.basename(filepath)

    title, cleaned_html = extract_title_and_clean_html(filepath, fallback_title)
    placeholders = {
        "pagetitle": title,
        "content": cleaned_html,
    }

    tpl = Template(base_template)
    page_html = tpl.safe_substitute(placeholders)

    if extra_placeholders:
        page_html = Template(page_html).safe_substitute(extra_placeholders)

    soup = BeautifulSoup(page_html, "html.parser")
    pretty_html = soup.prettify()

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_html)
    return title
