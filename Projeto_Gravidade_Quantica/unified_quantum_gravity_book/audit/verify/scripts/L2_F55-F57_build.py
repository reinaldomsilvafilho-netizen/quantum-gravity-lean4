"""Compile edited files 3x with pdflatex in a scratch copy (audit/verify/L2_F55-F57_build/)."""
import os, re, shutil, subprocess, sys

BOOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(BOOK, "audit", "verify", "L2_F55-F57_build")
os.makedirs(OUT, exist_ok=True)
FILES = ["chap02_geometric_flows_tensor_varieties", "chap03_pascal_simplex_continuous_multinomials",
         "DICTIONARY_TERMS_AND_SYMBOLS"]
for f in FILES + ["declarations_chapter"]:
    shutil.copy(os.path.join(BOOK, f + ".tex"), OUT)
fail = 0
for f in FILES:
    for _ in range(3):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f + ".tex"],
                           cwd=OUT, capture_output=True, timeout=300)
    log = open(os.path.join(OUT, f + ".log"), encoding="latin-1").read()
    err = len(re.findall(r"^! ", log, re.M))
    warn = len(re.findall(r"(LaTeX|Package \w+|Class \w+) Warning", log))
    over = len(re.findall(r"Overfull \\[hv]box", log))
    undef = len(re.findall(r"undefined", log, re.I))
    under = len(re.findall(r"Underfull \\[hv]box", log))
    pages = re.findall(r"Output written on .*?\((\d+) pages", log)
    print(f"{f}: exit {r.returncode}, errors {err}, warnings {warn}, overfull {over}, "
          f"undefined {undef}, underfull {under}, pages {pages}")
    if r.returncode or err or warn or over or undef:
        fail += 1
sys.exit(fail)
