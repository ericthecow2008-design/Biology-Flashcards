# BIOL 130 flashcards

This repository holds my (Eric's) BIOL 130 flashcard series and the tools that build it.

**Before you do anything, read `START_HERE.md` and `STYLE_GUIDE.md` in full and follow them.**
- `START_HERE.md` says what's done and what's left.
- `STYLE_GUIDE.md` says how every card has to be written.

## Notes for cloud sessions (this repository on claude.ai/code)

- **Setup:** run `pip install -r requirements.txt`, then `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install`.
- **Page images:** `python3 render_pages.py` renders the notes to `pages/p-68.png` … `pages/p-94.png`. Use them to read figures and filled-in blanks.
- **Browser checks:** `check_overlaps.js`, `shoot_gallery.js` and `smoke_test.js` use any Chromium already on the machine (`find_chromium.js`).
  - If none is found, try `npx playwright install chromium`.
  - If that download is blocked, skip those three checks and tell me. The study-page template and all 15 diagrams were already tested, so only re-check what you change.
- **Deliverables:** copy `BIOL130_Modules3-6.apkg`, `biol130-flashcards.html` and `biol130_modules3-6.md` into `deliverables/`, commit, and push your branch.
  - If you can also update my study page and my BIOL 130 Project directly (see `START_HERE.md`), do that too.
  - If you can't, say so; the files in `deliverables/` are enough.
- **Commit the reviewed sources as well:** the `cards_*.py` files, `cards_m56.json`, `cards_m56_audit.json` and `diagrams_m56.json`. That way the next session starts from the finished set.
