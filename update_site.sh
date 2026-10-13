#!/usr/bin/env bash
# =============================================================================
#  UPDATE THE LIVE SITE
#
#  Run this after you edit anything (a notebook, a chapter page, the README).
#  It rebuilds the website, shows you what would be published, asks for
#  confirmation, and only then commits and pushes. GitHub Pages refreshes on
#  its own.
#
#  USAGE:
#    bash update_site.sh "short note about what you changed"
#    bash update_site.sh                      (uses a default message)
#
#    bash update_site.sh --text-only "msg"    FAST: skip re-running notebooks.
#                                             Use when you changed only pages,
#                                             style or config (*.qmd, _quarto.yml,
#                                             assets/). Edits in source_notebooks/
#                                             are NOT published and NOT committed
#                                             in this mode.
#
#    bash update_site.sh --dry-run ...        build and show what would be
#                                             published; commit and push nothing
#    bash update_site.sh --yes ...            do not ask for confirmation
#
#  SAFETY (the script stops instead of publishing when):
#    - you are not on main, or main is behind GitHub (pull first);
#    - something is already staged in git;
#    - any notebook fails to execute, or the render fails;
#    - --text-only is used without a complete earlier full build.
#  Only site files are committed (never `git add -A`); anything else that is
#  modified or untracked is listed and left alone. The push is never forced.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

SITE_URL="https://marcinplodzien.github.io/quantum-chaos-and-scrambling/"
die() { echo "ERROR: $*" >&2; exit 1; }

MODE=full; DRY=0; YES=0; MSG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --text-only) MODE=text ;;
    --dry-run)   DRY=1 ;;
    --yes|-y)    YES=1 ;;
    -h|--help)   sed -n '2,33p' "$0"; exit 0 ;;
    --*)         die "unknown option: $1 (see --help)" ;;
    *)           [ -z "$MSG" ] || die "more than one commit message given"; MSG="$1" ;;
  esac
  shift
done
MSG="${MSG:-Update site}"

# ---------------------------------------------------------------- pre-flight
echo "==> [0/4] Checking the repository..."
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[ "$BRANCH" = "main" ] || die "you are on branch '$BRANCH'; the site is published from main."
git diff --cached --quiet || die "there are already staged changes; commit or unstage them first (git reset)."
git fetch --quiet origin || die "cannot reach GitHub (git fetch failed)."
BEHIND="$(git rev-list --count HEAD..origin/main)"
[ "$BEHIND" -eq 0 ] || die "main is $BEHIND commit(s) behind GitHub; run 'git pull --rebase' first."

SRC_CHANGED="$(git status --porcelain -- source_notebooks)"
if [ -n "$SRC_CHANGED" ]; then
  if [ "$MODE" = text ]; then
    echo "    NOTE: these notebook edits are NOT published and NOT committed in --text-only mode:"
  else
    echo "    These notebook edits will be executed, published and committed:"
  fi
  echo "$SRC_CHANGED" | sed 's/^/      /'
  if [ "$MODE" = full ]; then
    for f in $(git ls-files --others --exclude-standard -- source_notebooks); do
      stem="$(basename "$f" .ipynb)"
      grep -q "$stem" _quarto.yml || echo "    WARNING: new notebook $stem is not listed in _quarto.yml (it will have a page but no sidebar entry)."
    done
  fi
fi

# ---------------------------------------------------------------- build
if [ "$MODE" = full ]; then
  echo "==> [1/4] Rebuilding site (re-running notebooks + rendering)..."
  echo "    This can take 15-30 min because every notebook is executed."
  EXEC_TIMEOUT="${EXEC_TIMEOUT:-600}" bash build.sh \
    || die "the build failed (see above). Nothing was committed or pushed."
else
  echo "==> [1/4] Text-only render (notebooks NOT re-run)..."
  # Reuse the executed copies in ./notebooks from the last full build. They are
  # NOT regenerated here: prep_notebooks.py would replace them with the
  # output-free sources and the published pages would lose their figures.
  [ -f notebooks/.build_ok ] \
    || die "no complete full build found (notebooks/.build_ok is missing); run without --text-only once."
  quarto render || die "quarto render failed. Nothing was committed or pushed."
fi

[ -s docs/index.html ] || die "docs/index.html is missing or empty after the build."
# GitHub Pages needs .nojekyll so underscore-prefixed asset folders are served.
touch docs/.nojekyll

# ---------------------------------------------------------------- stage
echo "==> [2/4] Selecting files to publish..."
if [ "$MODE" = full ]; then
  git add -u -- .
  git add -- docs assets chapters ./*.qmd source_notebooks verify_exercises
else
  git add -u -- . ':(exclude)source_notebooks'
  git add -- docs assets chapters ./*.qmd verify_exercises
fi

if git diff --cached --quiet; then
  echo "    Nothing changed — nothing to commit. (Site is already up to date.)"
  exit 0
fi

echo "    Source files:"
git diff --cached --name-status -- . ':(exclude)docs' | sed 's/^/      /'
echo "    Rendered site (docs/): $(git diff --cached --shortstat -- docs)"
PAGES="$(git diff --cached --name-status --diff-filter=AD -- 'docs/*.html' || true)"
[ -z "$PAGES" ] || { echo "    Pages added (A) or removed (D):"; echo "$PAGES" | sed 's/^/      /'; }
LEFT="$(git status --porcelain | grep -v '^[MADRC]  ' || true)"
[ -z "$LEFT" ] || { echo "    Left out (not committed):"; echo "$LEFT" | sed 's/^/      /'; }

if [ "$DRY" = 1 ]; then
  git reset --quiet
  echo "==> Dry run: nothing committed or pushed. The built site is in ./docs (open ./docs/index.html)."
  exit 0
fi

if [ "$YES" != 1 ]; then
  [ -t 0 ] || { git reset --quiet; die "not an interactive terminal; re-run with --yes to publish."; }
  read -r -p "==> Publish this to the live site? [y/N] " ANSWER
  case "$ANSWER" in
    y|Y|yes|YES) ;;
    *) git reset --quiet; echo "    Cancelled. Nothing committed or pushed; the built site is in ./docs."; exit 1 ;;
  esac
fi

# ---------------------------------------------------------------- commit + push
echo "==> [3/4] Committing changes..."
git commit --quiet -m "$MSG"

echo "==> [4/4] Pushing to GitHub..."
if ! git push origin main; then
  echo "ERROR: push failed. The commit exists locally only." >&2
  echo "       Run 'git pull --rebase' and then 'git push origin main'. Do not force-push." >&2
  exit 1
fi

echo ""
echo "============================================================"
echo " Pushed. GitHub Pages will refresh in ~1-2 minutes:"
echo "   $SITE_URL"
echo "============================================================"
