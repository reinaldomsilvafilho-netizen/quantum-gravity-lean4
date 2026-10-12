"""Independent check of cross-chapter references against fresh .aux files (L2 build).
For each reference 'Type X.Y' in chapter N, list aux labels numbered X.Y and their env type.
Negative control: a deliberately wrong reference (Theorem 9.9 of Ch. 3; Proposition 2.2 of Ch. 5) must fail."""
import re, glob, os, sys
B = r"C:/Users/monar/Documents/antigravity/resilient-turing/Projeto_Gravidade_Quantica/unified_quantum_gravity_book"
AUX = B + "/audit/verify/L2_final_integration_build"
TYPES = {"Theorem": "thm|theorem", "Thm": "thm|theorem", "Proposition": "prop|proposition", "Prop": "prop|proposition",
         "Remark": "rem|remark", "Rem": "rem|remark", "Conjecture": "conj|conjecture", "Lemma": "lem|lemma",
         "Definition": "def|definition", "Problem": "prob|problem"}

def labels(n):
    f = glob.glob(AUX + f"/chap{n:02d}_*.aux")[0]
    out = []
    for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", open(f, encoding="latin-1").read()):
        out.append((m.group(1), m.group(2), m.group(5)))
    return out

def check(typ, num, ch):
    hits = [(l, a) for (l, nn, a) in labels(ch) if nn == num]
    ok = [h for h in hits if re.match(r"(" + TYPES[typ] + r")[.\-]", h[1], re.I) or re.match(r"(" + TYPES[typ] + r"):", h[0], re.I)]
    return ok, hits

cites = {"silvafilho2026simplex": 3}
refs = []
for f in sorted(glob.glob(B + "/chap[01][0-9]_*.tex")) + [B + "/DICTIONARY_TERMS_AND_SYMBOLS.tex"]:
    base = os.path.basename(f)
    if base.startswith("chap14"): continue
    t = open(f, encoding="utf8").read()
    for m in re.finditer(r"(Theorem|Proposition|Remark|Conjecture|Lemma|Thm\.|Prop\.|Rem\.)~(\d+\.\d+) of Chapter~(\d+)", t):
        refs.append((base, m.group(1).rstrip("."), m.group(2), int(m.group(3))))
    for m in re.finditer(r"(?:Chapter|Ch\.)~(\d+),? (Theorem|Proposition|Remark|Thm\.|Prop\.|Rem\.)~(\d+\.\d+)", t):
        refs.append((base, m.group(2).rstrip("."), m.group(3), int(m.group(1))))
    for m in re.finditer(r"\\cite\[(Thm|Rem|Prop)\.~(\d+\.\d+)\]\{(silvafilho2026\w+)\}", t):
        refs.append((base, m.group(1), m.group(2), cites.get(m.group(3), -1)))
print(len(refs), "references")
bad = 0
for base, typ, num, ch in refs:
    if ch < 0:
        print("UNRESOLVED cite", base, typ, num); bad += 1; continue
    ok, hits = check(typ, num, ch)
    status = "OK" if ok else ("UNLABELED?" if not hits else "TYPE-MISMATCH")
    if not ok: bad += 1
    print(f"{status:12s} {base[:6]} -> Ch.{ch} {typ} {num}: {[h[0] for h in (ok or hits)][:3]}")
print("problems:", bad)
# negative controls
for typ, num, ch in [("Theorem", "9.9", 3), ("Proposition", "9.9", 5), ("Theorem", "2.2", 6)]:
    ok, hits = check(typ, num, ch)
    print("NEG-CONTROL", typ, num, "ch", ch, "->", "FAILS (good)" if not ok else "PASSES (bad control)")
