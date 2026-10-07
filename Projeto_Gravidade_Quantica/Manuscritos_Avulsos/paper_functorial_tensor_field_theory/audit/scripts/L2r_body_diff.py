"""L2r: word-level diff of the body (bibliography removed) between the pre-reference-audit
backup and the current .tex, for all four works; output used for the claim review
(title/abstract/introduction/conclusion). Writes L2r_body_diff.out.txt."""
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARQ = ROOT.parent / "_arquivo"
PRE = {
    "paper_functorial_tensor_field_theory": "backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory_refs.tex",
    "paper_functional_realizations": "backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations_refs.tex",
    "paper_geometric_measures_functional_tensors": "backup_tex_2026-10-07/Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/paper_geometric_measures_functional_tensors_refs.tex",
    "paper_beyond_the_spectrum_3": "backup_tex_2026-10-07/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3_refs.tex",
}
out = []
for w, p in PRE.items():
    a = (ARQ / p).read_text(encoding="utf-8").split(r"\begin{thebibliography}")[0]
    b = (ROOT / w / f"{w}.tex").read_text(encoding="utf-8").split(r"\begin{thebibliography}")[0]
    sa = re.split(r"(?<=[.!?])\s+|\n\s*\n", a)
    sb = re.split(r"(?<=[.!?])\s+|\n\s*\n", b)
    sa = [" ".join(s.split()) for s in sa if s.strip()]
    sb = [" ".join(s.split()) for s in sb if s.strip()]
    out.append(f"######## {w}")
    for line in difflib.unified_diff(sa, sb, lineterm="", n=0):
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
            out.append(line)
(Path(__file__).with_suffix(".out.txt")).write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out))
