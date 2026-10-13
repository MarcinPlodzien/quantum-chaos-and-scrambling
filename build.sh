#!/usr/bin/env bash
# Build the website: copy notebooks, execute them (so outputs render), and
# render the site into ./docs (which GitHub Pages serves).
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/3] Preparing notebook copies..."
python3 prep_notebooks.py

echo "[2/3] Executing notebooks (this can take 15-30 minutes)..."
EXEC_TIMEOUT="${EXEC_TIMEOUT:-600}"
fail=0
for nb in notebooks/ch*/solution_*.ipynb notebooks/ch*/example_*.ipynb; do
  if jupyter nbconvert --to notebook --execute --inplace \
       --ExecutePreprocessor.timeout="$EXEC_TIMEOUT" "$nb" > /dev/null 2>&1; then
    echo "    ok   $nb"
  else
    echo "    FAIL $nb"; fail=$((fail+1))
  fi
done
[ "$fail" -eq 0 ] && echo "    all notebooks executed" || echo "    WARNING: $fail notebook(s) failed"

echo "[3/3] Rendering site into ./docs ..."
quarto render

if [ "$fail" -ne 0 ]; then
  echo "FAILED: $fail notebook(s) did not execute; their pages have no outputs."
  echo "The site in ./docs is for inspection only. Do not publish it."
  exit 1
fi
# Marks ./notebooks as a complete set of executed copies (update_site.sh --text-only needs it).
touch notebooks/.build_ok
echo "Done. The website is in ./docs (open ./docs/index.html)."
