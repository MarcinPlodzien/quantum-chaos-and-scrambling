# From Haar Random States to Quantum Machine Learning

**A hands-on numerical tutorial on randomness, scrambling, and learning in quantum systems.**

[![Website](https://img.shields.io/badge/website-live-2ea44f)](https://marcinplodzien.github.io/quantum-chaos-and-scrambling/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Notebooks](https://img.shields.io/badge/notebooks-41-orange)](source_notebooks)
[![Made with Quarto](https://img.shields.io/badge/made%20with-Quarto-75AADB)](https://quarto.org)

A surprising amount of modern quantum theory rests on one question: **what happens
when you average over random quantum evolutions?** This tutorial builds that
toolkit once — the Haar measure and the Weingarten calculus — and follows it
across random matrix theory, scrambling dynamics, unitary designs, classical
shadows, and the trainability of quantum machine-learning models.

Everything is **self-contained and runnable**: 41 short Jupyter notebooks, each
demonstrating one result, plus a complete set of worked exercises. No quantum
hardware, no special libraries — just `numpy`, `scipy`, and `matplotlib`.

> **Read it online:** <https://marcinplodzien.github.io/quantum-chaos-and-scrambling/>

---

## What's inside

| Chapter | Topic | Notebooks |
|---|---|---|
| 1 | Mathematical Foundations — channels, Lie algebras, state geometry, measure theory | 14 |
| 2 | Random Matrix Theory — level repulsion, the semicircle law | 3 |
| 3 | Haar Measure & Weingarten Calculus — twirling, the Page formula, concentration | 7 |
| 4 | Quantum Dynamics & Chaos — OTOCs, the spectral form factor, Krylov complexity | 3 |
| 5 | Designs & Clifford Ensembles — $t$-designs, magic / stabilizer Rényi entropy | 2 |
| 6 | Applications of Scrambling — classical shadows, randomized benchmarking, Hayden–Preskill | 5 |
| 7 | Quantum Machine Learning — barren plateaus, quantum kernels, reservoir computing | 7 |

- **`source_notebooks/`** — the 41 tutorial notebooks (clean, output-free).
- **`verify_exercises/`** — standalone Python scripts that numerically check the key results.
- **`exercises_and_solutions_complete.pdf`** — all exercises with full step-by-step solutions, flashcards, and derivation blueprints, interleaved by chapter.
- **`chapters/`, `index.qmd`, `_quarto.yml`** — the source of the website.
- **`docs/`** — the pre-built website (served by GitHub Pages).

## Quick start

```bash
git clone https://github.com/MarcinPlodzien/quantum-chaos-and-scrambling
cd quantum-chaos-and-scrambling
pip install -r requirements.txt
jupyter lab          # open any notebook in source_notebooks/
```

Want to check the numbers without opening a notebook? The scripts are runnable on their own:

```bash
python verify_exercises/solution_ch3_page_formula.py
python verify_exercises/solution_ch7_barren_plateau.py
```

## How to use it

- **As a course** — read the chapters in order on the website; each concept page is
  followed by its runnable notebooks, and the exercises PDF lets you self-test.
- **As a reference** — jump to any notebook; they stand on their own.
- **In teaching** — the notebooks, exercises, and flashcards are built to drop
  straight into a lecture or problem set.

## Rebuilding the website

The site is built with [Quarto](https://quarto.org) (≥ 1.3). The notebooks are
executed at build time so the published pages include all plots and results;
the source notebooks are kept output-free for clean diffs.

```bash
bash build.sh        # prep → execute notebooks → render into ./docs (15–30 min)
```

See the publishing steps below, or `build.sh` for details.

## Publishing on GitHub Pages

1. Push this repository to GitHub.
2. **Settings → Pages → Source:** either
   - **Deploy from a branch** → `main` / `/docs` (serves the pre-built site), or
   - **GitHub Actions** (uses `.github/workflows/deploy.yml` to rebuild on every push).
3. The site goes live at `https://<user>.github.io/<repo>/`.

## Citing

If this tutorial helps your work, please cite it (see [`CITATION.cff`](CITATION.cff)).
You can also use the "Cite this repository" button on GitHub.

## Relation to the book

This is the open, hands-on companion to the monograph *Quantum Chaos and
Information Scrambling: From Random Matrix Theory to Quantum Machine Learning*.
The tutorial is designed to stand entirely on its own; the book provides the
extended narrative and full derivations.

## Contributing

Found a bug, an unclear explanation, or a result that doesn't reproduce on your
machine? Please [open an issue or a pull request](https://github.com/MarcinPlodzien/quantum-chaos-and-scrambling/issues).
The notebooks are meant to be poked at.

## License

Released under the [MIT License](LICENSE) — free to use, modify, and share,
with attribution.
