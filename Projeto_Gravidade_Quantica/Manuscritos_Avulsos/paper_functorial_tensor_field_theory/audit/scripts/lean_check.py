"""Concatenate the paper's Lean files (working tree and git HEAD = pushed version) into one file,
append #print axioms for the headline theorems and a vacuity probe, and compile with `lean`.
Negative control: a deliberately false statement must fail to compile."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))
LEAN_DIR = os.path.join(REPO, "Projeto_Gravidade_Quantica", "formal_proofs_lean4")
FILES = ["Category", "CTensMan", "Cobordism", "EmergentFunctor", "MonoidalCoherence", "NullEnergy"]
TAIL = """
namespace QuantumGravity
#print axioms map_id_preservation
#print axioms map_comp_preservation
#print axioms object_monoidal_isomorphism
#print axioms braiding_naturality
#print axioms null_energy_condition
-- vacuity probe: the 'Einstein equations' predicate holds for every metric
example : ∀ g : LorentzianMetric, Einstein_Equations_Satisfied g := by
  intro g; first | trivial | exact True.intro | sorry
end QuantumGravity
"""
NEG = """
namespace QuantumGravity
theorem neg_control : (2 : Nat) + 2 = 5 := by decide
end QuantumGravity
"""

def source(name, rev):
    if rev == "work":
        return open(os.path.join(LEAN_DIR, name + ".lean"), encoding="utf8").read()
    return subprocess.run(["git", "-C", REPO, "show", f"HEAD:Projeto_Gravidade_Quantica/formal_proofs_lean4/{name}.lean"],
                          capture_output=True, text=True, encoding="utf8").stdout

def build(rev, extra, tag=""):
    parts = []
    for n in FILES:
        s = source(n, rev)
        s = re.sub(r"^import .*$", "", s, flags=re.M)
        parts.append(s)
    txt = "\n".join(parts) + extra
    p = os.path.join(HERE, f"_lean_concat_{rev}{tag}.lean")
    open(p, "w", encoding="utf8").write(txt)
    r = subprocess.run(["lean", p], capture_output=True, text=True, timeout=600)
    n_axiom_decl = len(re.findall(r"^axiom ", txt, flags=re.M))
    return r.returncode, r.stdout + r.stderr, n_axiom_decl

out = []
fails = 0
for rev in ["work", "HEAD"]:
    rc, log, nax = build(rev, TAIL)
    out.append(f"=== {rev}: exit={rc} axiom declarations={nax} imports Mathlib={'Mathlib' in log}")
    out.append(chr(10).join(l for l in log.splitlines() if "defProp" not in l and "linter" not in l and l.strip())[:5000])
rc, log, _ = build("work", NEG, "_neg")
out.append(f"=== negative control (2+2=5 must fail): exit={rc}")
out.append(log.strip()[:600])
if rc == 0:
    fails += 1
s = "\n".join(out)
print(s)
open(os.path.join(HERE, "lean_check.out.txt"), "w", encoding="utf8").write(s)
sys.exit(fails)
