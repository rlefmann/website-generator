# website-generator
A simple static website generator.

## Installation
```sh
git clone https://github.com/rlefmann/website-generator
cd website-generator
pip install .
```

Once installed, you can run the generator using:
```sh
website-generator <input-directory>
```

## Input Directory Structure

The input directory must have the following structure:
```
your-site/
├── config.ini          # Site configuration (title, author, optional lang)
├── template.html       # Base HTML template with placeholders
├── style.css           # (Optional) Stylesheet to apply to all pages
├── assets/             # (Optional) Additional files like images, scripts, etc.
└── pages/
    ├── index.html      # Main index page (required)
    ├── 2023-11-12-title.html  # Blog post HTML files
    └── other.html      # Other content pages
```

### `config.ini`
The config file must contain at least
```ini
title = My Blog
author = Jane Doe
lang = en  # Optional, defaults to 'en'
```

### `template.html`
The template file should include placeholders using Python's $ syntax, e.g.:
```html
<html>
  <head><title>$pagetitle</title></head>
  <body>
    <header><h1>$title</h1></header>
    <main>$content</main>
    <footer>Author: $author, Generated on $date</footer>
  </body>
</html>
```

### Blog posts
Any file in `pages/` matching the pattern `YYYY-MM-DD-title.html` is treated as a blog post.
These will be listed on the homepage in reverse chronological order.

## Acknowledgments
Inspired in part by [saait](https://codemadness.org/saait.html).
