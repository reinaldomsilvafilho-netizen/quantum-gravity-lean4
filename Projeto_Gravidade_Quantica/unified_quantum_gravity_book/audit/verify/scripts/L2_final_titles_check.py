import re, glob, os
os.chdir(r"C:/Users/monar/Documents/antigravity/resilient-turing/Projeto_Gravidade_Quantica/unified_quantum_gravity_book")

def norm(s):
    s = re.sub(r"\\texorpdfstring\{([^{}]*)\}\{[^{}]*\}", r"\1", s)
    s = s.replace("\\\\", " ").replace("\\-", "").replace("\\textbf", "")
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def grab(text, start):
    # balanced-brace arg starting at text[start]=='{'
    d = 0
    for i in range(start, len(text)):
        if text[i] == "{": d += 1
        elif text[i] == "}":
            d -= 1
            if d == 0: return text[start + 1:i]
    return None

titles = {}
for f in sorted(glob.glob("chap[01][0-9]_*.tex")):
    n = int(f[4:6])
    if n > 13: continue
    t = open(f, encoding="utf8").read()
    m = re.search(r"^\s*\\title(\[[^\]]*\])?\{", t, re.M)
    if m:
        titles[n] = norm(grab(t, m.end() - 1))
    else:
        m = re.search(r"pdftitle=\{", t)
        titles[n] = "(no \\title; pdftitle) " + norm(grab(t, m.end() - 1))
    pm = re.search(r"pdftitle=\{", t)
    if pm:
        pt = norm(grab(t, pm.end() - 1)).replace("---", " ")
        if norm(pt) != titles[n].replace("(no \\title; pdftitle) ", ""):
            print(f"[pdftitle differs] ch{n}: {pt}")

M = open("master_book_unified_quantum_gravity.tex", encoding="utf8").read()
chs = []
for m in re.finditer(r"\\chapter(\[[^\]]*\])?\{", M):
    chs.append(norm(grab(M, m.end() - 1)))
print("master chapters:", len(chs))
bad = 0
for i, c in enumerate(chs[:13], 1):
    ok = c == titles[i].replace("(no \\title; pdftitle) ", "")
    bad += not ok
    print(f"ch{i:02d} {'OK ' if ok else 'MISMATCH'} file='{titles[i]}'" + ("" if ok else f"\n        master='{c}'"))
print("master mismatches:", bad)

# bibliography cross-chapter entries
nb = 0; badb = 0
for f in sorted(glob.glob("chap[01][0-9]_*.tex")) + ["DICTIONARY_TERMS_AND_SYMBOLS.tex"]:
    t = open(f, encoding="utf8").read()
    for m in re.finditer(r"\\bibitem\{(silvafilho2026\w*)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", t, re.S):
        body = m.group(2)
        cm = re.search(r"Chapter~(\d+) of", body)
        em = re.search(r"\\emph\{", body)
        if not cm:
            print(f"  {f[:6]} {m.group(1)}: not a chapter ref: {norm(body)[:90]}")
            continue
        nb += 1
        k = int(cm.group(1))
        tt = norm(grab(body, em.end() - 1))
        ok = tt == titles[k]
        badb += not ok
        if not ok:
            print(f"  BIB MISMATCH {f[:6]} {m.group(1)} ch{k}: '{tt}' vs '{titles[k]}'")
print("bib chapter entries:", nb, "mismatches:", badb)
