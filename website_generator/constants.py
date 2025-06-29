import re

CONFIG_FILENAME = 'config.ini'
TEMPLATE_FILENAME = 'template.html'
PAGES_DIRNAME = 'pages'
INDEX_FILENAME = 'index.html'
OUTPUT_DIRNAME = 'outputs'
ASSETS_DIRNAME = 'assets'
STYLESHEET_FILENAME = 'style.css'

BLOG_POST_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.html$")
