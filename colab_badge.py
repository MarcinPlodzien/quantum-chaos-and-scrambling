#!/usr/bin/env python3
"""Put an "Open in Colab" badge at the top of every notebook page.

Edits the website copies in ./notebooks/chN/ in place (text only: no cell is
executed and no output is touched). The badge links to the tracked source
notebook on GitHub, source_notebooks/<name>.ipynb, because ./notebooks is not
committed. Safe to re-run: an existing badge cell is replaced, never duplicated.
Called by build.sh (after prep_notebooks.py) and by update_site.sh --text-only.

    python3 colab_badge.py              # all notebooks in ./notebooks
    python3 colab_badge.py a.ipynb ...  # only the given files
"""
import os, sys, glob, nbformat

REPO = "MarcinPlodzien/quantum-chaos-and-scrambling"
BRANCH = "main"
TAG = "colab-badge"
HERE = os.path.dirname(os.path.abspath(__file__))
BADGE_IMG = "https://colab.research.google.com/assets/colab-badge.svg"


def colab_url(stem):
    return (f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}"
            f"/source_notebooks/{stem}.ipynb")


def add_badge(nb, stem):
    """Insert (or refresh) the badge cell right after the YAML front matter."""
    nb.cells = [c for c in nb.cells
                if TAG not in c.get("metadata", {}).get("tags", [])]
    # Raw HTML, not ![](...): Quarto turns a lone Markdown image into a captioned figure.
    md = (f'<a href="{colab_url(stem)}" target="_blank" rel="noopener">'
          f'<img src="{BADGE_IMG}" alt="Open In Colab"/></a>')
    cell = nbformat.v4.new_markdown_cell(md, metadata={"tags": [TAG]})
    pos = 1 if (nb.cells and nb.cells[0].cell_type == "raw"
                and nb.cells[0].source.lstrip().startswith("---")) else 0
    nb.cells.insert(pos, cell)
    return nb


def main(paths):
    if not paths:
        paths = sorted(glob.glob(os.path.join(HERE, "notebooks", "ch*", "*.ipynb")))
    done = 0
    for p in paths:
        stem = os.path.splitext(os.path.basename(p))[0]
        if not os.path.exists(os.path.join(HERE, "source_notebooks", stem + ".ipynb")):
            print(f"    skip (no source notebook): {p}")
            continue
        nb = nbformat.read(p, as_version=4)
        nbformat.write(add_badge(nb, stem), p)
        done += 1
    print(f"Colab badge on {done} notebook(s)")


if __name__ == "__main__":
    main(sys.argv[1:])
