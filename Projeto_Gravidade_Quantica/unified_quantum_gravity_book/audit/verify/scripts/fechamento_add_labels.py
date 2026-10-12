"""Insert a \\label after the \\begin{env}[Title] line of the 19 unlabeled results, so that the
Results Index can \\ref them. Exact-substring matching; each begin-line must occur exactly once.
Run with --dry to only check."""
import sys
from pathlib import Path

BOOK = Path(r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book")
ITEMS = [
    (1, r"\begin{proposition}[Spectral and Critical Correspondence]", "prop:spectral_critical"),
    (2, r"\begin{proposition}[Dirichlet Energy of the Graphon Laplacian]", "prop:graphon_dirichlet_energy"),
    (3, r"\begin{proposition}[Global Stifel Recurrence]", "prop:stifel"),
    (3, r"\begin{proposition}[Digamma Partial Differential Equation System]", "prop:digamma_pde"),
    (3, r"\begin{proposition}[Global Meromorphic Extension and Zero Loci]", "prop:meromorphic_zero_loci"),
    (3, r"\begin{theorem}[Alternating Row Integrals]", "thm:alternating_row_integrals"),
    (4, r"\begin{proposition}[Self-Adjointness and Positivity]", "prop:self_adjoint_positive"),
    (4, r"\begin{theorem}[Global Conservation of Mass and Energy]", "thm:nlse_conservation"),
    (4, r"\begin{theorem}[Simplicial Modulational Instability]", "thm:modulational_instability"),
    (4, r"\begin{theorem}[Closed-Form Solution in Frequency Domain]", "thm:frequency_closed_form"),
    (5, r"\begin{theorem}[Dual Simplicial Extension Operator]", "thm:dual_extension"),
    (5, r"\begin{proposition}[Conservation of Total Mass and Energy Dissipation; formal computation]", "prop:coupled_conservation"),
    (5, r"\begin{proposition}[Inversion]", "prop:inversion"),
    (5, r"\begin{theorem}[Invariance and Spherical Harmonic Eigenfunctions;", "thm:siegel_wishart_invariance"),
    (6, r"\begin{theorem}[Spectral Dimension of the Sierpi\'nski Simplex;", "thm:sierpinski_spectral_dimension"),
    (8, r"\begin{theorem}[Equations of Gauss, Codazzi-Mainardi, and Ricci;", "thm:gauss_codazzi_ricci"),
    (8, r"\begin{theorem}[Sectional-Extrinsic Coupling]", "thm:sectional_extrinsic"),
    (8, r"\begin{theorem}[ADM Constraint Equations;", "thm:adm_constraints"),
    (8, r"\begin{theorem}[Israel Junction Theorem;", "thm:israel_junction"),
]

dry = "--dry" in sys.argv
by_file = {}
for ch, begin, lab in ITEMS:
    f = sorted(BOOK.glob(f"chap{ch:02d}_*.tex"))[0]
    by_file.setdefault(f, []).append((begin, lab))
for f, items in by_file.items():
    text = f.read_text(encoding="utf-8")
    for begin, lab in items:
        if f"\\label{{{lab}}}" in text:
            raise SystemExit(f"{f.name}: label {lab} already present")
        n = text.count(begin)
        if n != 1:
            raise SystemExit(f"{f.name}: '{begin}' occurs {n} times")
        i = text.index(begin)
        eol = text.index("\n", i)
        line = text[i:eol]
        if "\\label" in line:
            raise SystemExit(f"{f.name}: begin line already has a label: {line}")
        text = text[:eol + 1] + f"\\label{{{lab}}}\n" + text[eol + 1:]
        print(f"{f.name}: + \\label{{{lab}}} after: {line[:90]}")
    if not dry:
        f.write_text(text, encoding="utf-8")
print("dry run" if dry else "written")
