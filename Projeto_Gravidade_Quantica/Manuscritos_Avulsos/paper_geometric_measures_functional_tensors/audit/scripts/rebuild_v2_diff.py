"""Compile a copy of the .tex in the scratchpad and word-diff it against the Zenodo v2 Vol. II PDF.
Ignores running heads, page numbers and the TOC page numbers by filtering pure digits and header strings."""
import os, re, sys, shutil, subprocess, difflib, pymupdf
SCR = os.path.dirname(os.path.abspath(__file__))
FOLD = r"C:/Users/monar/Documents/antigravity/resilient-turing/Projeto_Gravidade_Quantica/Manuscritos_Avulsos/paper_geometric_measures_functional_tensors"
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(FOLD, "audit", "v2_reconstructed.tex")
work = os.path.join(SCR, "build_v2")
os.makedirs(work, exist_ok=True)
shutil.copy(src, os.path.join(work, "v2.tex"))
for _ in range(2):
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "v2.tex"], cwd=work, capture_output=True, timeout=300)
HEAD = {"BEYOND", "THE", "SPECTRUM", "II", "REINALDO", "M.", "SILVA-FILHO"}
def words(path):
    d = pymupdf.open(path)
    t = " ".join(p.get_text() for p in d)
    w = re.sub(r"\s+", " ", t).split(" ")
    return [x for x in w if not x.isdigit() and x not in HEAD]
wa = words(os.path.join(FOLD, "audit", "zenodo_latest_vol2.pdf"))
wb = words(os.path.join(work, "v2.pdf"))
sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
out = ["words zenodo %d rebuilt %d; diff ops %d; similarity %.4f" % (len(wa), len(wb), len(ops), sm.ratio())]
for o in ops:
    out.append("%s | V2: %s | REBUILT: %s" % (o[0], " ".join(wa[max(0, o[1]-4):o[2]+4])[:300], " ".join(wb[max(0, o[3]-4):o[4]+4])[:300]))
txt = "\n".join(out)
open(os.path.join(SCR, "rebuild_v2_diff.out.txt"), "w", encoding="utf8").write(txt)
print(txt.encode("ascii", "replace").decode()[:8000])
