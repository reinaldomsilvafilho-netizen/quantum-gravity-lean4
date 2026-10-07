"""Copy a paper .tex to audit/L2b_build and run pdflatex 3x; report log diagnostics.
Usage: python L2b_build.py <paper_dir> <name>"""
import sys, shutil, subprocess, re, os

pdir, name = sys.argv[1], sys.argv[2]
bdir = os.path.join(pdir, "audit", "L2b_build")
os.makedirs(bdir, exist_ok=True)
shutil.copy(os.path.join(pdir, name + ".tex"), bdir)
codes = []
for _ in range(3):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"],
                       cwd=bdir, capture_output=True, timeout=300)
    codes.append(r.returncode)
log = open(os.path.join(bdir, name + ".log"), encoding="latin-1").read()
errs = len(re.findall(r"^! ", log, re.M))
warns = len(re.findall(r"Warning", log))
over = len(re.findall(r"Overfull", log))
under = len(re.findall(r"Underfull", log))
undef = len(re.findall(r"undefined", log, re.I))
pages = re.findall(r"Output written on .*?\((\d+) pages?", log)
res = (f"{name}: exit codes {codes}; errors {errs}; warnings {warns}; overfull {over}; "
       f"underfull {under}; undefined {undef}; pages {pages}")
print(res)
for l in log.splitlines():
    if "Warning" in l or "Overfull" in l or "undefined" in l.lower():
        print("  ", l)
open(os.path.join(pdir, "audit", "scripts", "L2b_build.out.txt"), "w").write(res + "\n")
sys.exit(int(any(codes) or errs or warns or over or undef))
