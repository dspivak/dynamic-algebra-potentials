#!/bin/bash
# Build the MSCS submission (CDLM--MSCS.tex).
#
# Why this script exists: biber dies *silently* (leaving an empty .bbl, so the
# bibliography vanishes) when it inherits a stale Perl environment -- which is
# what a GUI editor or a polluted login shell passes it. Running biber under a
# clean environment (`env -i`) with an explicit PATH sidesteps every inherited
# perl/PAR variable and makes the run reproducible.
#
# Usage:  cd MSCS && ./build.sh
# Requires nothing in PATH; all tool locations are absolute.

set -euo pipefail

JOB=CDLM--MSCS
TEXBIN=/usr/local/texlive/2024/bin/universal-darwin
PDFLATEX="$TEXBIN/pdflatex"
BIBER="$TEXBIN/biber"

cd "$(dirname "$0")"

run_pdflatex() { "$PDFLATEX" -interaction=nonstopmode -halt-on-error "$JOB.tex"; }

# Clean environment for biber: no inherited perl/PAR vars can redirect its
# bundled perl. This is the single line that makes biber reliable here.
run_biber() { env -i PATH="$TEXBIN:/usr/bin:/bin" HOME="$HOME" "$BIBER" "$JOB"; }

echo "==> pdflatex (pass 1)"; run_pdflatex >/dev/null
echo "==> biber"            ; run_biber
echo "==> pdflatex (pass 2)"; run_pdflatex >/dev/null
echo "==> pdflatex (pass 3)"; run_pdflatex >/dev/null

if [ ! -s "$JOB.bbl" ]; then
  echo "ERROR: $JOB.bbl is empty -- biber failed. Check $JOB.blg." >&2
  exit 1
fi

undef=$(grep -c "Citation.*undefined" "$JOB.log" || true)
echo "==> done: $JOB.pdf  (undefined citations: ${undef:-0})"
