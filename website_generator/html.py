import sys
from string import Template
from bs4 import BeautifulSoup

from website_generator.utils import get_localized_date

def generate_base_template(template_path: str, config_dict: dict) -> str:
    try:
        with open(template_path, 'r') as f:
            template_html = f.read()
    except Exception as e:
        print(f"Error: Could not read '{template_path}': {e}", file=sys.stderr)
        sys.exit(1)
    tpl = Template(template_html)
    base_html = tpl.safe_substitute(config_dict)
    return base_html


def extract_title_and_clean_html(filepath: str, fallback_title: str):
    """
    Parses HTML file to extract the title (from <title> or first <h1>),
    removes <title> tag, and returns (clean_html_str, title).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except OSError as e:
        raise RuntimeError(f"Could not read file '{filepath}': {e}")
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        title = title_tag.get_text(strip=True)
        title_tag.decompose()
    else:
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.get_text(strip=True)
        else:
            title = fallback_title
    return title, str(soup)


def generate_html_table(blog_index_entries, lang_code: str):
    blog_index_entries.sort(reverse=True)
    html = ['<table id="blogposts-table">']
    current_year = None
    for date_obj, title, filename in blog_index_entries:
        year = date_obj.year
        if year != current_year:
            tr_class = "year-row" if current_year is not None else "year-row first-year-row"
            html.append(f'<tr class="{tr_class}"><td colspan="2">{year}</td></tr>')
            current_year = year
        formatted_date = get_localized_date(date_obj, lang_code)
        html.append(f'<tr><td class="date-cell">{formatted_date} </td><td><a href="{filename}">{title}</a></td></tr>')
    html.append('</table>')
    html_string = '\n'.join(html)
    return html_string
