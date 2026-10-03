"""Render the Modules 5-6 notes to PNGs, so reviewers can see figures and filled-in blanks.

Output: pages/p-68.png ... pages/p-94.png, numbered by notes page.
Usage:  python3 render_pages.py            (every page)
        python3 render_pages.py 78 80      (notes pages 78-80 only)
Uses PyMuPDF (pip install pymupdf). Falls back to pdftoppm (poppler-utils) if
PyMuPDF isn't installed.
"""
import os, shutil, subprocess, sys

PDF = "notes/BIOL130_notes_pp68-94.pdf"
FIRST = 68  # page 1 of this PDF is notes page 68
DPI = 110

os.makedirs("pages", exist_ok=True)
try:
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
    except ImportError:
        import fitz  # older PyMuPDF
    doc = fitz.open(PDF)
    count = doc.page_count
except ImportError:
    doc = None
    if not shutil.which("pdftoppm"):
        sys.exit("Install PyMuPDF (pip install pymupdf) or poppler-utils (apt-get install -y poppler-utils).")
    info = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout
    count = int(next(l.split()[-1] for l in info.splitlines() if l.startswith("Pages:")))

lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (FIRST, FIRST + count - 1)
for page in range(max(lo, FIRST), min(hi, FIRST + count - 1) + 1):
    i = page - FIRST  # 0-based index in this PDF
    out = f"pages/p-{page}"
    if doc is not None:
        doc[i].get_pixmap(dpi=DPI).save(out + ".png")
    else:
        subprocess.run(["pdftoppm", "-f", str(i + 1), "-l", str(i + 1), "-r", str(DPI), "-png", "-singlefile", PDF, out], check=True)
    print("wrote", out + ".png")
