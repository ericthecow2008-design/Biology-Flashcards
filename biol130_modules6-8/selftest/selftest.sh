#!/usr/bin/env bash
# Run the whole pipeline on throwaway cards (every format, every module, a bridge card) in a scratch copy
# of the kit, to prove the tools and this machine's setup work before any real work starts. Nothing is
# published, and your work/ and outputs/ folders are not touched.
# Usage (from the kit folder):  bash selftest/selftest.sh
set -u
KIT="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
cp -r "$KIT/tools" "$KIT/ref" "$T/" && mkdir -p "$T/work" "$T/outputs"
cp "$KIT"/selftest/cards_*.py "$KIT"/selftest/diagrams_*.py "$KIT/selftest/concept_ledger_m68.json" "$T/work/"
[ -d "$KIT/node_modules" ] && ln -s "$KIT/node_modules" "$T/node_modules"
cd "$T"
pass=0; fail=0
step() { local name="$1"; shift; if "$@" > "$T/log_$pass$fail.txt" 2>&1; then echo "PASS  $name"; pass=$((pass+1)); else echo "FAIL  $name   (log below)"; tail -15 "$T/log_$pass$fail.txt"; fail=$((fail+1)); fi; }
step "build_diagrams"               python3 tools/build_diagrams.py
step "check_overlaps (default font)" node tools/check_overlaps.js
step "check_overlaps (DejaVu Sans)"  env FONT='"DejaVu Sans"' node tools/check_overlaps.js
step "shoot_gallery"                 node tools/shoot_gallery.js
step "build_cards"                   python3 tools/build_cards.py
step "build_apkg"                    python3 tools/build_apkg.py
step "verify_apkg (Anki engine)"     python3 tools/verify_apkg.py
step "update_page"                   python3 tools/update_page.py ref/live_page.html
step "page_test"                     node tools/page_test.js
step "update_page --replace"         python3 tools/update_page.py outputs/biol130-flashcards.html --replace
step "build_md"                      python3 tools/build_md.py
step "make_review"                   python3 tools/make_review.py
echo "selftest: $pass passed, $fail failed   (scratch copy: $T)"
[ "$fail" -eq 0 ]
