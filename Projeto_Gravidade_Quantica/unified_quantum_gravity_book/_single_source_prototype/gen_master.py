#!/usr/bin/env python3
"""F-19 prototype: generate master_prototype.tex / master_prototype_full.tex
from gen/chapNN_body.tex (produced by extract.py), READ-ONLY on every
chapNN_*.tex and on master_book_unified_quantum_gravity.tex.

Short running-head titles are NOT invented here: they are harvested, in
document order, from the 13 \\chapter{...}/\\chaptermark{...} pairs the
author already wrote in master_book_unified_quantum_gravity.tex (the current
stitched-PDF master). Chapter 14 is excluded (not integrated; F-52) and the
trailing Dictionary chapter is excluded (not part of this 13-chapter prototype).

Usage: run inventory.py, then extract.py, then this script, in that order.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK_DIR = HERE.parent
REAL_MASTER = BOOK_DIR / "master_book_unified_quantum_gravity.tex"

CHAP_RE = re.compile(
    r"\\chapter(?:\[(?P<short_in_cmd>.*?)\])?\{(?P<long>.*?)\}\s*\n"
    r"\\chaptermark\{(?P<mark>.*?)\}",
    re.S,
)


def harvest_titles(n=13):
    """Return a list of (long_title, short_title) for the first n
    \\chapter/\\chaptermark pairs in the real master, in document order."""
    text = REAL_MASTER.read_text(encoding="utf-8")
    pairs = []
    for m in CHAP_RE.finditer(text):
        long_t = m.group("long").strip()
        mark = m.group("mark").strip()
        pairs.append((long_t, mark))
        if len(pairs) == n:
            break
    if len(pairs) != n:
        raise RuntimeError(
            f"expected {n} \\chapter/\\chaptermark pairs in {REAL_MASTER.name}, "
            f"found {len(pairs)}"
        )
    return pairs


PREAMBLE_BLOCK = """% F-19 PROTOTYPE ONLY. Does not touch master_book_unified_quantum_gravity.tex
% or any chapNN_*.tex. Chapters below are generated bodies (gen/chNN_body.tex)
% produced read-only from the originals by extract.py; chapter titles/short
% running heads below are harvested read-only, in order, from the
% \\chapter{{...}}/\\chaptermark{{...}} pairs already authored in
% master_book_unified_quantum_gravity.tex (see gen_master.py). Regenerate
% this file with gen_master.py; do not hand-edit the \\chapter{{}} lines.
\\documentclass[11pt,a4paper,openright,twoside]{{book}}

\\input{{common_preamble}}

\\geometry{{top=3cm,bottom=3cm,left=3cm,right=2.8cm,headheight=14pt}}

\\hypersetup{{
  colorlinks=true,
  linkcolor=NavyBlue,
  citecolor=Mahogany,
  urlcolor=TealBlue,
  pdftitle={{F-19 prototype: single-source build}},
  pdfauthor={{Reinaldo M. Silva-Filho}}
}}

\\title{{F-19 Prototype: Single-Source Build}}
\\author{{Reinaldo M. Silva-Filho}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle
\\tableofcontents

{body}
\\end{{document}}
"""

CHAPTER_BLOCK = """\\chapter[{short}]{{{long}}}
\\chaptermark{{{short}}}
\\input{{gen/chap{num:02d}_body}}
"""


def build(n, out_name):
    pairs = harvest_titles(13)[:n]
    blocks = [
        CHAPTER_BLOCK.format(num=i + 1, long=long_t, short=mark)
        for i, (long_t, mark) in enumerate(pairs)
    ]
    out_text = PREAMBLE_BLOCK.format(body="\n".join(blocks))
    out = HERE / out_name
    out.write_text(out_text, encoding="utf-8")
    print(f"{out_name}: {n} chapters")


OFFICIAL_TEMPLATE = HERE / "official_master_structure.tex"
OFFICIAL_OUT = HERE / "master_single_source.tex"


def build_official():
    """F-19 adoption (not the regression prototypes above): the official
    13-chapter master, front matter included. Its STRUCTURE (title page,
    epigraphs, preface, declarations, \\part/\\chapter/\\chaptermark order,
    and the Dictionary's \\includepdf) is static and lives in the committed
    template `official_master_structure.tex` -- NOT in the live official
    master_book_unified_quantum_gravity.tex, precisely so this function can
    be re-run on every build without the self-reference trap of reading a
    file this same pipeline is about to overwrite (re-reading an already
    \\input{common_preamble}-converted master would double-\\input it and
    hard-error on duplicate \\newtheorem). The template was produced once,
    read-only, from the pre-F19 master (see
    _arquivo/backup_tex_2026-10-07/master_pre_F19_includepdf.tex for the
    frozen original) by mechanically swapping each chapter's
    \\includepdf[pages=1-]{chapNN_...pdf} for \\input{gen/chapNN_body} and
    inserting \\input{common_preamble}. Only the 13 gen/chapNN_body.tex
    files (refreshed by extract.py from the LIVE chapters every run) make
    this regenerate; the template itself only needs a hand update if the
    author reorders/renames/adds/removes a chapter or \\part.
    """
    text = OFFICIAL_TEMPLATE.read_text(encoding="utf-8")
    n_inputs = len(re.findall(r"\\input\{gen/chap\d\d_body\}", text))
    if n_inputs != 13:
        raise RuntimeError(
            f"official_master_structure.tex: expected 13 chapter \\input "
            f"lines, found {n_inputs} -- refusing to stage a short master"
        )
    if "\\includepdf[pages=1-]{DICTIONARY_TERMS_AND_SYMBOLS.pdf}" not in text:
        raise RuntimeError(
            "official_master_structure.tex: Dictionary \\includepdf missing"
        )
    OFFICIAL_OUT.write_text(text, encoding="utf-8")
    print(f"{OFFICIAL_OUT.name}: staged from template ({n_inputs} chapters + Dictionary)")


def main():
    build(3, "master_prototype.tex")
    build(13, "master_prototype_full.tex")
    build_official()


if __name__ == "__main__":
    main()
