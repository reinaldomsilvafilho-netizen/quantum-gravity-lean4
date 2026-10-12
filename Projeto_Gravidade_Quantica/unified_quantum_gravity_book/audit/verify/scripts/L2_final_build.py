import glob, os, re, shutil, subprocess
SRC = r"C:/Users/monar/Documents/antigravity/resilient-turing/Projeto_Gravidade_Quantica/unified_quantum_gravity_book"
OUT = SRC + "/audit/verify/L2_final_integration_build"
os.makedirs(OUT, exist_ok=True)
targets = sorted(f for f in glob.glob(SRC + "/chap[01][0-9]_*.tex") if int(os.path.basename(f)[4:6]) <= 13)
targets.append(SRC + "/DICTIONARY_TERMS_AND_SYMBOLS.tex")
for f in targets + [SRC + "/declarations_chapter.tex", SRC + "/master_book_unified_quantum_gravity.tex"]:
    shutil.copy(f, OUT)
for f in glob.glob(SRC + "/*.bib") + glob.glob(SRC + "/*.png") + glob.glob(SRC + "/*.pdf"):
    b = os.path.basename(f)
    if b.endswith(".pdf"):
        continue  # PDFs are rebuilt here
    shutil.copy(f, OUT)

def run(name):
    for _ in range(3):
        p = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name], cwd=OUT,
                           capture_output=True, timeout=600)
    log = open(os.path.join(OUT, name[:-4] + ".log"), encoding="latin-1").read()
    err = len(re.findall(r"^! ", log, re.M))
    warn = len(re.findall(r"(LaTeX|Package|Class) (\w+ )?Warning", log))
    over = len(re.findall(r"Overfull \\[hv]box", log))
    undef = len(re.findall(r"undefined", log, re.I))
    ok = os.path.exists(os.path.join(OUT, name[:-4] + ".pdf"))
    print(f"{name[:40]:40s} err={err} warn={warn} overfull={over} undef={undef} pdf={ok}")
    if warn:
        for l in re.findall(r"^.*(?:LaTeX|Package|Class) (?:\w+ )?Warning.*$", log, re.M)[:5]:
            print("    ", l)

for f in targets:
    run(os.path.basename(f))
run("master_book_unified_quantum_gravity.tex")
