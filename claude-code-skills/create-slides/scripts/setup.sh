#!/usr/bin/env bash
# setup.sh: build the Python environment the create-slides scripts need.
#
#   bash setup.sh [--venv PATH] [--browsers PATH]
#
# Creates a virtual environment (default: ${XDG_DATA_HOME:-~/.local/share}/create-slides/venv) with
# playwright, pymupdf, matplotlib, pillow and python-pptx, then installs Playwright's headless
# Chromium unless a Chrome or Chromium is already found the way deck.py finds one ($CHROME_PATH,
# PATH, a Playwright browser cache). --browsers sets where Playwright keeps browsers
# (PLAYWRIGHT_BROWSERS_PATH); without it Playwright's default cache is used.
# Idempotent: a second run installs nothing that is already there. pip honours PIP_CACHE_DIR and
# TMPDIR from the environment; point both at a disk with room when the home disk is small.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${XDG_DATA_HOME:-$HOME/.local/share}/create-slides/venv"
BROWSERS=""
PACKAGES=(playwright pymupdf matplotlib pillow python-pptx)
MODULES="playwright, pymupdf, matplotlib, PIL, pptx"

while [ $# -gt 0 ]; do
  case "$1" in
    --venv) VENV="$2"; shift 2 ;;
    --browsers) BROWSERS="$2"; shift 2 ;;
    -h|--help) awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"; exit 0 ;;
    *) echo "unknown argument: $1 (see --help)" >&2; exit 2 ;;
  esac
done

PY="$VENV/bin/python"
if [ ! -x "$PY" ]; then
  echo "creating venv: $VENV"
  mkdir -p "$(dirname "$VENV")"
  python3 -m venv "$VENV" || { echo "python3 -m venv failed: install python3-venv (or python3 >= 3.9 with venv)" >&2; exit 1; }
fi

if "$PY" -c "import $MODULES" 2>/dev/null; then
  echo "packages: already installed"
else
  echo "installing: ${PACKAGES[*]}"
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet "${PACKAGES[@]}"
fi

if [ -n "$BROWSERS" ]; then
  mkdir -p "$BROWSERS"
  export PLAYWRIGHT_BROWSERS_PATH="$(cd "$BROWSERS" && pwd)"
fi
find_chrome() { "$PY" -c "import sys; sys.path.insert(0, '$HERE'); import deck; print(deck.find_chrome())" 2>/dev/null; }
if CHROME="$(find_chrome)"; then
  echo "chrome: $CHROME"
else
  echo "installing Playwright's headless Chromium${BROWSERS:+ into $PLAYWRIGHT_BROWSERS_PATH}"
  if "$PY" -m playwright install --help 2>/dev/null | grep -q -- "--only-shell"; then
    "$PY" -m playwright install --only-shell chromium
  else
    "$PY" -m playwright install chromium
  fi
  CHROME="$(find_chrome)" || { echo "no Chrome found after the install; if Chromium fails to start, run: $PY -m playwright install-deps chromium (needs root)" >&2; exit 1; }
  echo "chrome: $CHROME"
fi

"$PY" - <<'EOF'
from importlib.metadata import version
print("versions: " + ", ".join(f"{p} {version(p)}" for p in ("playwright", "pymupdf", "matplotlib", "pillow", "python-pptx")))
EOF
echo
echo "ready. Use the venv's python for the scripts:"
echo "  source \"$VENV/bin/activate\""
if [ -n "$BROWSERS" ]; then echo "  export PLAYWRIGHT_BROWSERS_PATH=\"$PLAYWRIGHT_BROWSERS_PATH\""; fi
echo "  python \"$HERE/deck.py\" selftest <empty dir>   # confirms the checks catch what they should"
