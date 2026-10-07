"""L2r build gate. Copies <paper>.tex (the paper folder is ../..) into audit/L2_final_build/,
runs pdflatex 3 times, and counts in the final log: errors, LaTeX/Package/Class warnings,
overfull and underfull boxes, undefined references/citations, "Rerun" requests and pdfTeX
notices (notices are reported, not counted as failures). Also compares the text of the
shipped PDF with the fresh build (pdftotext), so a stale shipped PDF is detected.
Negative control: the parser must flag a synthetic bad log.
Exit code = gate failures.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent.parent
name = PAPER.name
bdir = PAPER / "audit" / "L2_final_build"
bdir.mkdir(parents=True, exist_ok=True)
for f in bdir.glob(f"{name}.*"):
    f.unlink()
shutil.copy2(PAPER / f"{name}.tex", bdir / f"{name}.tex")
codes = []
for _ in range(3):
    p = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"],
                       cwd=bdir, capture_output=True, timeout=600)
    codes.append(p.returncode)


def parse(log):
    return {
        "errors": len(re.findall(r"^! ", log, re.M)),
        "latex_warnings": len(re.findall(r"^(?:LaTeX|Package \S+|Class \S+) Warning", log, re.M)),
        "overfull": len(re.findall(r"^Overfull", log, re.M)),
        "underfull": len(re.findall(r"^Underfull", log, re.M)),
        "undefined": len(re.findall(r"undefined (?:references|citations)|Reference `[^']*' on page \d+ undefined|Citation `[^']*' on page \d+ undefined", log)),
        "rerun": len(re.findall(r"Rerun to get", log)),
    }


log = (bdir / f"{name}.log").read_text(encoding="latin-1")
res = parse(log)
notices = re.findall(r"^.*pdfTeX warning.*$", log, re.M)
pages = re.search(r"Output written on .*?\((\d+) pages", log)
out = [f"paper: {name}", f"pdflatex exit codes: {codes}", f"counts: {res}",
       f"pages: {pages.group(1) if pages else '?'}", f"pdfTeX notices ({len(notices)}):"]
out += [f"  {n.strip()}" for n in notices]


def text(pdf):
    p = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, timeout=120)
    t = p.stdout.decode("utf-8", "replace")
    return [ln.rstrip() for ln in t.splitlines() if ln.strip()]


shipped = PAPER / f"{name}.pdf"
same = None
if shipped.exists():
    a, b = text(shipped), text(bdir / f"{name}.pdf")
    same = a == b
    out.append(f"shipped PDF text identical to fresh build: {same}"
               + ("" if same else f" (lines {len(a)} vs {len(b)})"))
ctrl = parse("! Undefined control sequence.\nOverfull \\hbox (3.0pt too wide)\n"
             "LaTeX Warning: Reference `x' on page 1 undefined on input line 3.\n")
ok_ctrl = ctrl["errors"] == 1 and ctrl["overfull"] == 1 and ctrl["undefined"] == 1 and ctrl["latex_warnings"] == 1
out.append(f"negative control (synthetic bad log) flagged: {ok_ctrl} {ctrl}")
fails = int(any(codes)) + sum(res.values()) + (0 if ok_ctrl else 1) + (1 if same is False else 0)
out.append(f"gate failures: {fails}")
for ext in ("aux", "out", "toc"):
    pass  # aux kept for label-number checks; build dir is an audit artefact
print("\n".join(out))
(HERE / "L2r_build.out.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
sys.exit(min(fails, 255))
