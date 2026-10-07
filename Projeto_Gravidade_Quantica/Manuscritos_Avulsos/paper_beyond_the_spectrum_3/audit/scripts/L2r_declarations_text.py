"""L2r: declarations, house style and bibliography-identifier claims for the four works.

Checks per work (same script copied to each folder; it inspects all four, so the
blocks can be compared with each other):
  - affiliation line, CAPES/Finance Code 001 line, competing-interests line;
  - Lean sentence exactly as required, and no version history ("earlier version",
    "accompanied earlier", "withdrawn", "previous version", "audit/") anywhere in the .tex;
  - the AI-use block is the same standard text in all four (up to the reference
    sentence and "paper"/"volume");
  - every bibitem has a DOI or arXiv id, except those the "Every reference" sentence names;
  - every bibitem is cited and every cited key has a bibitem.
Negative controls: an injected "earlier versions" string and a bibitem stripped of its
DOI must be detected.
Exit code = number of failures.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKS = ["paper_functorial_tensor_field_theory", "paper_functional_realizations",
         "paper_geometric_measures_functional_tensors", "paper_beyond_the_spectrum_3"]
AFFIL = ("Master's student, Postgraduate Program in Statistics and Agricultural Experimentation "
         "(PPGEE/DES), Department of Statistics (DES), Federal University of Lavras (UFLA), Lavras, MG, Brazil")
LEAN = ("The \\textsc{Lean 4} files in the author's repository associated with this work are a "
        "placeholder skeleton without Mathlib and verify none of the statements.")
CAPES = ("This research was financed in part by the Coordena\\c{c}\\~ao de Aperfei\\c{c}oamento de "
         "Pessoal de N\\'ivel Superior -- Brasil (CAPES) -- Finance Code 001.")
FORBIDDEN = ["earlier version", "accompanied earlier", "withdrawn", "previous version",
             "audit/", "was corrected", "has been corrected", "in a prior version"]
out, fail = [], 0


def log(s):
    out.append(s)
    print(s)


def norm(s):
    return " ".join(s.split())


def bib(tex):
    body = tex.split("\\begin{thebibliography}")[1].split("\\end{thebibliography}")[0]
    parts = re.split(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", body)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def has_id(raw):
    return bool(re.search(r"10\.\d{4,9}/", raw) or re.search(r"arXiv[:\s~]*[0-9a-z\-./]+\d", raw, re.I))


def ai_block(tex):
    t = norm(tex)
    a = t.find("\\textbf{Use of generative AI tools.}")
    b = t.find("\\textbf{Verification status.}")
    return t[a:b]


def check(name, tex, quiet=False):
    f = 0
    t = norm(tex)
    msgs = []
    for label, needle in (("affiliation", AFFIL), ("CAPES", CAPES), ("Lean sentence", LEAN),
                          ("competing interests", "The author declares no competing interests.")):
        ok = needle in t
        f += not ok
        msgs.append(f"  {label}: {'ok' if ok else 'MISSING'}")
    low = t.lower()
    hits = [w for w in FORBIDDEN if w in low]
    f += bool(hits)
    msgs.append(f"  forbidden history words: {hits or 'none'}")
    items = bib(tex)
    noid = sorted(k for k, v in items.items() if not has_id(v))
    msgs.append(f"  bibitems: {len(items)}; without DOI/arXiv: {noid}")
    body = tex.split("\\begin{thebibliography}")[0]
    cited = set()
    for m in re.finditer(r"\\cite[pt]?(?:\[[^\]]*\])?\{([^}]*)\}", body):
        cited |= {k.strip() for k in m.group(1).split(",")}
    unc, undef = sorted(set(items) - cited), sorted(cited - set(items))
    f += bool(unc) + bool(undef)
    msgs.append(f"  uncited bibitems: {unc or 'none'}; cited without bibitem: {undef or 'none'}")
    if not quiet:
        for m_ in msgs:
            log(m_)
    return f, noid


blocks = {}
for w in WORKS:
    tex = (ROOT / w / f"{w}.tex").read_text(encoding="utf-8")
    log(f"== {w}")
    f, noid = check(w, tex)
    fail += f
    blocks[w] = ai_block(tex)
    sent = re.search(r"Every reference was resolved[^.]*\.", blocks[w])
    log(f"  reference sentence: {sent.group(0) if sent else 'MISSING'}")

# AI blocks: identical after removing the reference sentence and paper/volume
canon = {w: re.sub(r"Every reference was resolved[^.]*\.", "", b).replace("this volume", "this paper")
         for w, b in blocks.items()}
same = len(set(canon.values())) == 1
fail += not same
log(f"AI-use block identical across the four works (modulo reference sentence, paper/volume): {same}")

# negative controls
tex0 = (ROOT / WORKS[0] / f"{WORKS[0]}.tex").read_text(encoding="utf-8")
f1, _ = check("neg1", tex0.replace("Code availability", "files that accompanied earlier versions. Code availability"), quiet=True)
k0 = next(iter(bib(tex0)))
raw0 = bib(tex0)[k0]
stripped = tex0.replace(raw0, re.sub(r"10\.\d{4,9}/\S+|arXiv[:\s~]*\S+", "", raw0), 1)
_, noid2 = check("neg2", stripped, quiet=True)
okn = f1 > 0 and k0 in noid2
fail += not okn
log(f"negative controls (injected history words; stripped DOI of {k0}) detected: {okn}")
log(f"failures={fail}")
(Path(__file__).with_suffix(".out.txt")).write_text("\n".join(out) + "\n", encoding="utf-8")
sys.exit(fail)
