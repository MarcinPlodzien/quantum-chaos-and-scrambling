#!/usr/bin/env python3
"""Copy the source notebooks (in ./source_notebooks) into ./notebooks/chN/,
giving each a clean Quarto title/description and converting bare '---' rules to
<hr/> (which otherwise collide with YAML front-matter parsing).
Source notebooks are never modified."""
import os, re, glob, shutil, nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source_notebooks")
DST = os.path.join(HERE, "notebooks")

CH_NAMES = {
    "ch1": "Mathematical Foundations", "ch2": "Random Matrix Theory",
    "ch3": "Haar Measure & Weingarten Calculus", "ch4": "Quantum Dynamics & Chaos",
    "ch5": "Designs & Clifford Ensembles", "ch6": "Applications of Scrambling",
    "ch7": "Quantum Machine Learning",
}

def pretty(stem):
    s = re.sub(r"^solution_ch\d+_", "", stem)
    return s.replace("_", " ").strip().title()

def first_h1(nb):
    for c in nb.cells:
        if c.cell_type == "markdown":
            m = re.search(r"^\s*#\s+(.+)$", c.source, re.M)
            if m:
                return m.group(1).strip()
    return None

if os.path.isdir(DST):
    shutil.rmtree(DST)

n = 0
for path in sorted(glob.glob(os.path.join(SRC, "solution_ch*.ipynb"))):
    stem = os.path.splitext(os.path.basename(path))[0]
    ch = re.match(r"solution_(ch\d+)_", stem).group(1)
    outdir = os.path.join(DST, ch)
    os.makedirs(outdir, exist_ok=True)
    nb = nbformat.read(path, as_version=4)
    for c in nb.cells:
        if c.cell_type == "markdown":
            c.source = re.sub(r"(?m)^\s*---\s*$", "<hr/>", c.source)
    title = first_h1(nb) or pretty(stem)
    title = re.sub(r"^(Solution|Exercise)[:\s-]+", "", title).strip() or pretty(stem)

    def yaml_clean(s):
        s = re.sub(r"\$[^$]*\$", "", s)
        s = s.replace("\\", " ").replace("`", "")
        s = re.sub(r"\s+", " ", s).strip(" -:")
        return s.replace("'", "''")
    title = yaml_clean(title) or pretty(stem)
    desc = f"{CH_NAMES[ch]}, numerical solution."
    raw = ("---\n"
           f"title: '{title}'\n"
           f"description: '{desc}'\n"
           "---\n")
    front = nbformat.v4.new_raw_cell(raw)
    if nb.cells and nb.cells[0].cell_type == "raw" and nb.cells[0].source.lstrip().startswith("---"):
        nb.cells = nb.cells[1:]
    nb.cells.insert(0, front)
    nbformat.write(nb, os.path.join(outdir, stem + ".ipynb"))
    n += 1

print(f"Prepared {n} notebooks into {DST}")
