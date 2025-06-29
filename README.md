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

An example of the required input directory structure can be found in the [example folder](./example).

### `config.ini`
The config file must contain at least
```ini
title = My Blog
author = Jane Doe
lang = en  # Optional, defaults to 'en'
```

### `template.html`
The template file should include placeholders using Python’s `$` syntax. Most placeholder names correspond directly to keys in the `config.ini` file — for example, `$title` and `$author` will be replaced by the respective config values.

In addition, there are two special placeholders that are not set in the config file but are dynamically provided for each page during generation:

- `$pagetitle`: The title of the individual page (e.g., extracted from the HTML file)
- `$content`: The main HTML content of the page

Example template:
```html
<html>
  <head>
    <title>$pagetitle</title>
    <meta name="author" content="${author}" />
  </head>
  <body>
    <header><h1>$title</h1></header>
    <main>$content</main>
    <footer>Author: $author, Generated on $date</footer>
  </body>
</html>
```

### Blog posts
Any file in `pages/` matching the pattern `YYYY-MM-DD-title.html` is treated as a blog post.
These posts are automatically listed on the homepage (`index.html`) in reverse chronological order (newest first).

To enable this listing, your `pages/index.html` file must include the special placeholder `$index_table`, which will be replaced by a generated HTML table containing all blog post entries.

### Output directory
By default, when the site generator runs, it creates a new directory called `outputs` inside the input directory you specify. All generated HTML files, copied assets (like CSS and images), and other output files will be saved there. This keeps the original input files separate from the generated website.

For example, if your input directory is `my-site`, the generated site will be in `my-site/outputs/`.

You can optionally specify a custom output directory using the `-o` or `--output` option:
```sh
website-generator -o ./custom_output_directory my-site
```

In this case, all generated files will be saved in `./custom_output_folder` instead.

You can then serve or upload the contents of the outputs folder as your static website.

## Acknowledgments
Inspired in part by [saait](https://codemadness.org/saait.html).
