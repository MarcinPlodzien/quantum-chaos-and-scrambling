#!/usr/bin/env bash
# =============================================================================
#  UPDATE THE LIVE SITE
#
#  Run this after you edit anything (a notebook, a chapter page, the README).
#  It rebuilds the website and pushes it; GitHub Pages refreshes on its own.
#
#  USAGE:
#    bash update_site.sh "short note about what you changed"
#    bash update_site.sh                      (uses a default message)
#
#    bash update_site.sh --text-only "msg"    FAST: skip re-running notebooks
#                                             (use ONLY if you changed text/
#                                              chapter pages, not notebook code)
# =============================================================================
set -e
cd "$(dirname "$0")"

# parse optional --text-only flag
REBUILD=1
if [ "$1" = "--text-only" ]; then REBUILD=0; shift; fi
MSG="${1:-Update site}"

if [ "$REBUILD" = "1" ]; then
  echo "==> [1/3] Rebuilding site (re-running notebooks + rendering)..."
  echo "    This can take 15-30 min because every notebook is executed."
  EXEC_TIMEOUT="${EXEC_TIMEOUT:-600}" bash build.sh
else
  echo "==> [1/3] Text-only render (notebooks NOT re-run)..."
  python3 prep_notebooks.py
  # reuse the already-rendered notebook outputs so plots survive
  if [ -d docs/notebooks ]; then
    for d in notebooks/ch*/; do :; done
  fi
  quarto render
fi

echo "==> [2/3] Committing changes..."
git add -A
if git diff --cached --quiet; then
  echo "    Nothing changed — nothing to commit. (Site is already up to date.)"
  exit 0
fi
git commit -m "$MSG"

echo "==> [3/3] Pushing to GitHub..."
git push

echo ""
echo "============================================================"
echo " Pushed. GitHub Pages will refresh in ~1-2 minutes:"
echo "   https://marcinplodzien.github.io/quantum-chaos-and-scrambling/"
echo "============================================================"
