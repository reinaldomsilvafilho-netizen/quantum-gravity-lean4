"""Liga módulos novos: LeanReal.lean, verificar.sh, CI e README.
Uso: python wire_lote.py <L2_report.md> <Titulo da secao README> Mod1 Mod2 ...
"""
import sys, re
rep, title, new = sys.argv[1], sys.argv[2], sys.argv[3:]
# Same forbidden-token check as the CI (it also matches words inside comments).
PAT = re.compile(r"\bsorry\b|\badmit\b|native_decide|decide\s*\+native|^\s*(private\s+|protected\s+)?axiom\b|\bunsafe\b|implemented_by|@\[extern|skipKernelTC|^\s*(elab|macro|macro_rules|syntax)\b")
bad = []
for m in new:
    for i, line in enumerate(open(f"LeanReal/{m}.lean", encoding="utf-8"), 1):
        if PAT.search(line):
            bad.append(f"LeanReal/{m}.lean:{i}: {line.strip()}")
if bad:
    sys.exit("forbidden token (CI will fail; reword comments too):\n" + "\n".join(bad))
p = "LeanReal.lean"; s = open(p, encoding="utf-8").read()
s = s.rstrip("\n") + "\n" + "".join(f"import LeanReal.{m}\n" for m in new if f"import LeanReal.{m}\n" not in s)
open(p, "w", encoding="utf-8", newline="\n").write(s)
p = "verificar.sh"; s = open(p, encoding="utf-8").read()
m = re.search(r"for m in ([^;]*); do", s); mods = m.group(1).split()
mods += [x for x in new if x not in mods]
s = s[:m.start()] + "for m in " + " ".join(mods) + "; do" + s[m.end():]
open(p, "w", encoding="utf-8", newline="\n").write(s)
p = "../../.github/workflows/lean_mathlib.yml"; s = open(p, encoding="utf-8").read()
m = re.search(r"lake env leanchecker LeanReal([^\n]*)", s); cur = m.group(1).split()
cur += ["LeanReal." + x for x in new if "LeanReal." + x not in cur]
s = s[:m.start()] + "lake env leanchecker LeanReal " + " ".join(cur) + s[m.end():]
open(p, "w", encoding="utf-8", newline="\n").write(s)
r = open(rep, encoding="utf-8").read().split("\n")
rows = [l for l in r if l.startswith("| `") and any(f"`{x}`" in l.split("|")[1] for x in new)]
p = "README.md"; s = open(p, encoding="utf-8").read()
s = s.rstrip("\n") + f"\n\n## {title}\n\nFidelity review: `{rep.split('/')[-1]}`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.\n\n| Module | Source and statement | Coverage |\n|---|---|---|\n" + "\n".join(rows) + "\n"
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("rows", len(rows), "mods", new)
