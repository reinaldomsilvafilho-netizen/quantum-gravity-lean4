"""Compare text of a fresh compile of the local .tex (scratch build, path given as argv[1])
with the Zenodo latest Volume II (audit/zenodo_latest_vol2.pdf). Word-level diff, ignoring the date line."""
import os, re, sys, difflib, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
def words(path):
    d = pymupdf.open(path)
    t = " ".join(p.get_text() for p in d)
    return re.sub(r"\s+", " ", t).split(" "), len(d)
wa, na = words(os.path.join(AUD, "zenodo_latest_vol2.pdf"))
wb, nb = words(sys.argv[1])
out = ["zenodo vol2 pages %d words %d; local tex build pages %d words %d" % (na, len(wa), nb, len(wb))]
sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
out.append("diff ops: %d ; similarity %.4f" % (len(ops), sm.ratio()))
for o in ops:
    out.append("%s | ZENODO: %s | LOCAL-TEX: %s" % (o[0], " ".join(wa[max(0,o[1]-3):o[2]+3])[:400], " ".join(wb[max(0,o[3]-3):o[4]+3])[:400]))
txt = "\n".join(out)
open(os.path.join(HERE, "compare_tex_vs_zenodo.out.txt"), "w", encoding="utf8").write(txt)
print(txt.encode("ascii", "replace").decode()[:12000])
