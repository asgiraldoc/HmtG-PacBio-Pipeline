# Configuration file for the Sphinx documentation builder.
#
# This project is intended to be hosted on GitHub Pages (built via GitHub Actions)
# and styled similarly to Read the Docs projects using the RTD theme.

from __future__ import annotations

import datetime

project = "Haemo Mito Pipeline"
author = "Escalante–Pacheco Lab (Temple University)"
copyright = f"{datetime.datetime.now().year}, {author}"

extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
]

# Make section labels unique across files
autosectionlabel_prefix_document = True

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# --- HTML output ---
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Lab branding
# Sphinx supports setting a logo via html_logo. (The RTD theme will render it in the sidebar.)
# Put the image under docs/source/_static/.
# Ref: https://www.sphinx-doc.org/en/master/usage/configuration.html
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_title = "Haemo Mito Pipeline — Escalante–Pacheco Lab"

# Include a small CSS override file for colors/buttons/spacing.
# Ref: https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_css_files = [
    "custom.css",
]

# RTD theme options (safe defaults)
html_theme_options = {
    "logo_only": True,
    "display_version": False,
    "collapse_navigation": False,
    # NOTE: navigation_depth behavior can vary across theme/Sphinx versions.
    # Keep it modest to avoid surprising sidebars.
    "navigation_depth": 4,
}

# Useful link shortcuts
extlinks = {
    "doi": ("https://doi.org/%s", "doi:%s"),
}

# Optional: link to external docs
# Sphinx >= 8 expects the inventory location to be a string or None (not {}).
# Ref: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Optional GitHub integration (uncomment + fill in once you know your repo)
# html_context = {
#     "display_github": True,
#     "github_user": "<GITHUB_ORG_OR_USER>",
#     "github_repo": "<REPO_NAME>",
#     "github_version": "main",
#     "conf_py_path": "/docs/source/",
# }
