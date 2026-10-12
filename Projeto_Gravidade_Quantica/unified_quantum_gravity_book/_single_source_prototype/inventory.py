#!/usr/bin/env python3
"""F-19 prototype: read-only inventory of chapter preambles.
Does NOT modify any chapter. Writes INVENTARIO.md in this folder.
"""
import re
from pathlib import Path
from collections import defaultdict

BOOK_DIR = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "INVENTARIO.md"

chap_files = sorted(BOOK_DIR.glob("chap[01][0-9]_*.tex"))

macro_defs = defaultdict(dict)  # name -> {chapfile: body}
report = []
report.append("# Inventario das 14 fontes de capitulo (F-19, somente leitura)\n")
report.append(f"Gerado por `inventory.py`. Nao altera nenhum capitulo original.\n")

for f in chap_files:
    txt = f.read_text(encoding="utf-8")
    m_doc = re.search(r"\\documentclass(\[[^\]]*\])?\{([^}]*)\}", txt)
    docclass = m_doc.group(0) if m_doc else "?"
    pkgs = re.findall(r"\\usepackage(\[[^\]]*\])?\{([^}]*)\}", txt)
    pkg_list = [p[1] for p in pkgs]
    newthm = re.findall(r"\\newtheorem\{([a-zA-Z]+)\}(\[[a-zA-Z]+\])?\{([^}]*)\}(\[[a-zA-Z]+\])?", txt)
    n_bibitem = len(re.findall(r"\\bibitem", txt))
    has_bib_env = "\\begin{thebibliography}" in txt
    has_decl = "\\input{declarations_chapter}" in txt
    n_label = len(re.findall(r"\\label\{", txt))
    defs = re.findall(r"\\(?:providecommand|newcommand|renewcommand)\{(\\[A-Za-z]+)\}(\[[0-9]\])?\{(.*?)\}\s*(?=\n|\\)", txt)
    for name, arity, body in defs:
        macro_defs[name][f.name] = body.strip()

    report.append(f"## {f.name}\n")
    report.append(f"- documentclass: `{docclass}`")
    report.append(f"- pacotes: {', '.join(sorted(set(pkg_list)))}")
    report.append(f"- newtheorem: {', '.join(sorted(set(t[0] for t in newthm))) if newthm else '(nenhum)'}")
    report.append(f"- bibitem: {n_bibitem} (thebibliography presente: {has_bib_env})")
    report.append(f"- \\label: {n_label} ocorrencias")
    report.append(f"- \\input" + "{declarations_chapter}: " + str(has_decl))
    report.append("")

report.append("## Macros definidas em mais de um capitulo\n")
report.append("Cada linha lista o nome, e se o corpo da definicao e identico (OK) ou diverge (CONFLITO) entre capitulos.\n")
conflicts = []
for name, by_chap in sorted(macro_defs.items()):
    if len(by_chap) < 2:
        continue
    bodies = set(by_chap.values())
    status = "OK (identica)" if len(bodies) == 1 else "CONFLITO (corpos diferentes)"
    if len(bodies) > 1:
        conflicts.append((name, by_chap))
    report.append(f"- `{name}` em {len(by_chap)} capitulos: {status}")

report.append("\n## Detalhe dos conflitos\n")
if conflicts:
    for name, by_chap in conflicts:
        report.append(f"### `{name}`")
        for chap, body in by_chap.items():
            report.append(f"- {chap}: `{body}`")
else:
    report.append("Nenhum conflito de definicao encontrado: todas as macros repetidas usam o mesmo corpo em todos os capitulos que as definem.")

OUT.write_text("\n".join(report), encoding="utf-8")
print(f"Escrito: {OUT}")
print(f"Capitulos processados: {len(chap_files)}")
print(f"Conflitos de macro: {len(conflicts)}")
