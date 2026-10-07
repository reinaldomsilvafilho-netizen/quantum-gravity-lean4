"""Layer-2 build gate: copy the paper .tex to audit/<builddir>/, run pdflatex 3 times,
and count errors, LaTeX/Package/Class warnings, overfull/underfull boxes, undefined
references/citations and pdfTeX notices in the final log.
usage: python L2_build.py <paper.tex> <builddir-name>
Negative control: the log parser must flag a synthetic log containing an Overfull box,
an undefined reference and an error line.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

tex = Path(sys.argv[1]).resolve()
bdir = tex.parent / "audit" / sys.argv[2]
bdir.mkdir(parents=True, exist_ok=True)
dst = bdir / tex.name
shutil.copy2(tex, dst)
out = []
codes = []
for i in range(3):
    p = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", dst.name],
                       cwd=bdir, capture_output=True, timeout=600)
    codes.append(p.returncode)


def parse(log):
    return {
        "errors": len(re.findall(r"^! ", log, re.M)),
        "latex_warnings": len(re.findall(r"^(LaTeX|Package \S+|Class \S+) Warning", log, re.M)),
        "overfull": len(re.findall(r"^Overfull", log, re.M)),
        "underfull": len(re.findall(r"^Underfull", log, re.M)),
        "undefined": len(re.findall(r"undefined", log, re.I)),
        "pdftex_notices": len(re.findall(r"pdfTeX warning", log)),
    }


log = (bdir / (dst.stem + ".log")).read_text(encoding="latin-1")
res = parse(log)
pages = re.search(r"Output written on .*?\((\d+) pages", log)
out.append(f"exit codes: {codes}")
out.append(f"counts: {res}")
out.append(f"pages: {pages.group(1) if pages else '?'}")
for m in re.finditer(r"^.*pdfTeX warning.*$", log, re.M):
    out.append(f"notice: {m.group(0)}")
ctrl = parse("! Undefined control sequence.\nOverfull \\hbox (3.0pt too wide)\nLaTeX Warning: Reference `x' on page 1 undefined\n")
ok_ctrl = ctrl["errors"] == 1 and ctrl["overfull"] == 1 and ctrl["undefined"] >= 1 and ctrl["latex_warnings"] == 1
out.append(f"negative control parser: {ctrl} -> {'flagged' if ok_ctrl else 'NOT FLAGGED'}")
fails = int(any(codes)) + sum(res[k] for k in ("errors", "latex_warnings", "overfull", "underfull", "undefined")) \
    + (0 if ok_ctrl else 1)
out.append(f"gate failures (pdfTeX notices not counted): {fails}")
print("\n".join(out))
(Path(__file__).parent / f"L2_build_{tex.stem}.out.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
sys.exit(min(fails, 255))
