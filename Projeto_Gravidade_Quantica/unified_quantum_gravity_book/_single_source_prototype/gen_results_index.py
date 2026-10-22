#!/usr/bin/env python3
"""Generate ../appendix_results_index.tex: one row per Theorem/Proposition/Lemma/Corollary of
chapters 1-13 (read-only on the chapters), with

  number      \\ref{chapNN:<label>} (labels are prefixed by extract.py in the single-source master)
  result      environment and short title
  proof       'text' / 'sketch' / 'cited' / 'cited + proof' / 'cited + sketch', detected from the
              source (proof environment after the statement; \\cite or 'classical' in the title),
              with the hand-checked overrides in PROOF_OVERRIDE
  numerics    hand-checked map NUM (V = verify_chapNN_numerical.py, F = the chapter's F02 oracle
              script, A = another targeted checking script of the repository)
  Lean        hand-checked map LEAN: module in formal_proofs_mathlib/LeanReal and the reduction
              declared for it in formal_proofs_mathlib/README.md (nothing beyond the README)
  status      chapter audit status from WORKPLAN.md (F-15: layers 1 and 2 for chapters 1-13) plus
              the finding records of the closing round that touch the result (STATUS_EXTRA)

The NUM, LEAN and STATUS_EXTRA maps were written by hand from the script names/docstrings, the
README tables and the WORKPLAN rows, and checked against the chapter text.
Usage (from this folder): python gen_results_index.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
OUT = BOOK / "appendix_results_index.tex"
ENVS = ("theorem", "proposition", "lemma", "corollary")
BEGIN = re.compile(r"\\begin\{(theorem|proposition|lemma|corollary|conjecture|definition|remark|problem|"
                   r"assumption|example|heuristic|algorithm|proof)\*?\}")
ABBR = {"theorem": "Thm.", "proposition": "Prop.", "lemma": "Lem.", "corollary": "Cor."}

# ---------------------------------------------------------------- hand-checked maps
PROOF_OVERRIDE = {
    (1, "thm:graphon_compactness"): "cited",     # proof cites Lovasz-Szegedy only, no argument in the text
    (2, "prop:tangent_proj_mr"): "cited + sketch",  # cites Vandereycken for the manifold facts, then sketches the argument
    (3, "prop:meromorphic_zero_loci"): "sketch", # no proof environment; derivation given in the statement (reflection formula)
    (3, "cor:dixon_higher"): "text",             # one-line argument in the statement
    (4, "thm:dispersion"): "Ch.~3",              # restates the Fourier-symbol theorem of Ch. 3
}

NUM = {
    (1, "prop:spectral_critical"): "V", (1, "thm:dirichlet_blindness"): "V, F", (1, "thm:tv_matrix"): "V, F",
    (1, "thm:coarea_linkage"): "V", (1, "thm:morse_matrix"): "V", (1, "thm:grothendieck_cutnorm"): "V, A",
    (1, "thm:hypergraphon_compactness"): "A", (1, "thm:attention_sobolev"): "A", (1, "thm:kac_rice_tensors"): "A",
    (1, "thm:critical_scaling"): "V",
    (2, "thm:cone_curvature"): "V", (2, "prop:tangent_proj_mr"): "V, A", (2, "thm:tt_manifold"): "F",
    (2, "thm:tt_tangent_proj"): "V", (2, "thm:toda_qr"): "V, F, A", (2, "thm:rank_preservation"): "V",
    (2, "prop:graphon_dirichlet_energy"): "V", (2, "thm:graphon_heat_existence"): "V, F",
    (2, "thm:heat_smoothing"): "V", (2, "thm:ricci_neckpinch"): "V", (2, "thm:cmps_energy_flow"): "A",
    (2, "thm:continuous_path_integral"): "V, F, A",
    (3, "prop:stifel"): "V, F", (3, "prop:digamma_pde"): "V, A", (3, "thm:2d_row_integral"): "V, F",
    (3, "thm:fibonacci"): "V, F", (3, "thm:lp_rows"): "F", (3, "conj:dixon"): "F", (3, "cor:dixon_real"): "A",
    (3, "thm:alternating_row_integrals"): "V, F", (3, "thm:moments"): "V", (3, "cor:row_log_product"): "A",
    (3, "thm:laplacian_symbol"): "A",
    (4, "prop:self_adjoint_positive"): "V", (4, "thm:dispersion"): "V, F", (4, "thm:nlse_conservation"): "V, F",
    (4, "thm:modulational_instability"): "V, A", (4, "thm:frequency_closed_form"): "V", (4, "thm:msd"): "V, F",
    (5, "prop:fourier_rep"): "V", (5, "thm:sobolev_trace"): "V, F", (5, "thm:dual_extension"): "V",
    (5, "prop:coupled_conservation"): "V", (5, "prop:inversion"): "V, F, A", (5, "thm:barycentric_ratio"): "V, F",
    (5, "thm:siegel_wishart_invariance"): "V, F",
    (6, "assump:kigami_decimation"): "V, F", (6, "thm:sierpinski_spectral_dimension"): "V, F",
    (6, "thm:multifractal"): "F", (6, "prop:pascal_mod2"): "F",
    (7, "prop:knot_gap"): "F", (7, "thm:obstacle_exclusion"): "V, A", (7, "thm:lower_bounds"): "V, F",
    (7, "prop:regularity_free"): "V", (7, "prop:ball_bound"): "A",  # audit/verify/scripts/l1_susp_S3.py l.34: kappa*R>=1 checked on the Nash-Kuiper example curve
    (7, "thm:scaling_law"): "V",
    (8, "thm:sectional_extrinsic"): "V, F", (8, "lem:euclidean_uturn"): "A", (8, "prop:space_form_uturn"): "V, F, A",
    (8, "cor:adm_bounds"): "V, F", (8, "prop:rn_horizon"): "V, F", (8, "prop:wormhole_throat"): "V, F",
    (8, "prop:proper_accel"): "V",
    (9, "prop:holonomy"): "V, A", (9, "prop:subloop"): "F", (9, "thm:loop_bounding"): "V",
    (9, "prop:winding_total_curvature"): "F", (9, "thm:unfolding"): "V", (9, "prop:corridor_gap"): "F",
    (9, "prop:teardrop"): "V",
    (10, "prop:degenerate"): "A", (10, "prop:counterexample"): "F, A",
    (11, "prop:relative_entropy_hessian"): "V", (11, "thm:first_law_entanglement"): "V", (11, "prop:mincut"): "F",
    (11, "prop:mcf_area"): "V", (11, "thm:ashtekar_limit"): "V, F",
    (12, "thm:cartan_metric_emergence"): "V", (12, "thm:minimax_hamiltonian_regularization"): "V",
    (12, "thm:neckpinch_condensation"): "V, A",
}

LEAN = {
    (1, "prop:spectral_critical"): r"\texttt{Chap01Rayleigh}: (i), finite-dimensional; \texttt{BeyondSpectrum1\_B3}: (ii), algebraic part in eigen-coordinates",
    (1, "thm:dirichlet_blindness"): r"\texttt{BeyondSpectrum1}: algebraic part, coefficient form (Parseval step not formalized)",
    (1, "thm:tensor_weierstrass"): r"\texttt{Chap01Tensor}: (i) full; (ii) algebraic step, multipliers as hypothesis",
    (1, "thm:hypergraphon_compactness"): r"\texttt{Chap01Hypergraphon}: (i), finite $k$-linear case; (ii) not formalized",
    (1, "thm:attention_sobolev"): r"\texttt{Chap01Attention}: coefficient form (Parseval not formalized)",
    (1, "thm:kac_rice_tensors"): r"\texttt{Chap01KacRice}: (i), (iv), algebraic core; covariance as hypothesis",
    (1, "thm:critical_scaling"): r"\texttt{Chap01Gaussian}: (ii) for fixed unit vectors; (i) not formalized",
    (2, "prop:tangent_proj_mr"): r"\texttt{Chap02Tangent}: matrix algebra of the projector; manifold structure not formalized",
    (2, "thm:tt_tangent_proj"): r"\texttt{Chap02Tangent}: (iii), abstract projected flow",
    (2, "thm:toda_qr"): r"\texttt{Chap02Toda}: algebraic and pointwise-derivative steps; ODE existence, uniqueness and QR not formalized",
    (2, "thm:rank_preservation"): r"\texttt{Chap02Tangent}: (ii) and its example",
    (2, "prop:graphon_dirichlet_energy"): r"\texttt{Chap02Graphon}: finite graph, symmetric $W$",
    (2, "thm:graphon_heat_existence"): r"\texttt{Chap02Heat}: finite grid (step graphons)",
    (2, "thm:heat_smoothing"): r"\texttt{Chap02Heat}: finite grid (step graphons)",
    (2, "thm:ricci_neckpinch"): r"\texttt{Chap02Flows}: scalar ODE at fixed $(x,y)$, curvature a given function",
    (2, "thm:cmps_energy_flow"): r"\texttt{Chap02Flows}: finite-parameter core",
    (2, "thm:continuous_path_integral"): r"\texttt{Chap02PathIntegral}: (iii) and the example in (ii); bound (i)--(ii) not formalized",
    (3, "prop:stifel"): r"\texttt{Chap03Pascal}: full",
    (3, "prop:digamma_pde"): r"\texttt{Chap03Special}: off the poles, one variable at a time",
    (3, "prop:meromorphic_zero_loci"): r"\texttt{Chap03Pascal}, \texttt{Chap03Analysis}: zeros, positivity, reflection identity; meromorphic extension not formalized",
    (3, "thm:star_of_david"): r"\texttt{Chap03Pascal}: full",
    (3, "thm:fibonacci"): r"\texttt{Chap03Special}: algebraic core; asymptotics not formalized",
    (3, "thm:alternating_row_integrals"): r"\texttt{Chap03Analysis}: full",
    (3, "cor:row_log_product"): r"\texttt{Chap03Analysis}: conditional on the Alexeiewsky identity (hypothesis)",
    (3, "prop:fractional_props"): r"\texttt{Chap03Special}: (1); (2) for $m = 2$; (3) for real $\lambda$",
    (3, "thm:laplacian_symbol"): r"\texttt{Chap04Symbol}: abstract probability measure; permutation invariance as hypothesis",
    (4, "prop:self_adjoint_positive"): r"\texttt{Chap04SelfAdjoint}: finite abelian group in place of $\mathbb{R}^{m-1}$",
    (4, "thm:dispersion"): r"\texttt{Chap04Symbol}: abstract probability measure; permutation invariance as hypothesis",
    (4, "thm:nlse_conservation"): r"\texttt{Chap04Conservation}: finite lattice, Hermitian matrix in place of $\Delta^\alpha$",
    (4, "thm:modulational_instability"): r"\texttt{Chap04Modulational}: after linearization",
    (4, "thm:msd"): r"\texttt{Chap04Moments}: conditional ($E_\beta'(0)$ and $\operatorname{Hess}\sigma(0)$ as hypotheses)",
    (5, "prop:coupled_conservation"): r"\texttt{Chap05Coupled}: abstract inner-product spaces; Green and Neumann identities as hypotheses",
    (5, "prop:inversion"): r"\texttt{Chap05Barycentric}: finite-dimensional algebra; Fourier step not formalized; $\widehat{\mathcal{K}}_\alpha \ne 0$ as hypothesis",
    (5, "thm:barycentric_ratio"): r"\texttt{Chap05Barycentric}: full (slightly more general than the text)",
    (6, "assump:kigami_decimation"): r"\texttt{Chap06Kigami}: exact for $m = 2, 3$; reduced equations for general $m$",
    (6, "thm:multifractal"): r"\texttt{Chap06Multifractal}: conditional on the Stirling and Barnes series (hypotheses)",
    (6, "prop:pascal_mod2"): r"\texttt{Chap06PascalMod2}: combinatorial part; dimension not formalized",
    (7, "prop:knot_gap"): r"\texttt{Chap07Bounds}: conditional on Fenchel and F\'ary--Milnor (hypotheses)",
    (7, "prop:dubins_duality"): r"\texttt{Chap08Chronology}: ordinal reduction; Dubins' theorem as hypothesis",
    (7, "lem:wall_structure"): r"\texttt{Chap07Control}: (c)--(d); item (b) as hypothesis",
    (7, "thm:obstacle_exclusion"): r"\texttt{Chap07Control}: (1)--(2) for curves; distance-function facts as hypotheses",
    (7, "thm:lower_bounds"): r"\texttt{Chap08UTurn}: (3), differentiable tangent angle",
    (7, "prop:optimal_regularity"): r"\texttt{Chap07Control}: core step only",
    (7, "prop:ball_bound"): r"\texttt{Chap07BallBound}: closed curves, twice differentiable",
    (7, "thm:monotonicity"): r"\texttt{Chap07Bounds}: curves only",
    (7, "thm:scaling_law"): r"\texttt{Chap07Bounds}: at one point",
    (7, "prop:gauss_bonnet_floor"): r"\texttt{Chap07Bounds}: pointwise algebra; conditional on Gauss--Bonnet",
    (8, "thm:sectional_extrinsic"): r"\texttt{Chap08Pointwise}: pointwise algebra; Gauss equation as hypothesis",
    (8, "lem:euclidean_uturn"): r"\texttt{Chap08UTurn}: differentiable tangent angle",
    (8, "prop:space_form_uturn"): r"\texttt{Chap08SpaceForms}: Fermi-coordinate reduction; Clairaut identity as hypothesis",
    (8, "prop:raychaudhuri"): r"\texttt{Chap08Pointwise}: along one curve; Raychaudhuri equation as hypothesis",
    (8, "prop:rn_horizon"): r"\texttt{Chap08Pointwise}: algebraic core of (2)",
    (8, "prop:wormhole_throat"): r"\texttt{Chap08Pointwise}: (2)--(3), pointwise at the throat",
    (8, "prop:proper_accel"): r"\texttt{Chap08Pointwise}: linear algebra at one point",
    (8, "prop:causal_constraints"): r"\texttt{Chap08Chronology}: (1)--(2), order-theoretic skeleton",
    (9, "prop:holonomy"): r"\texttt{Chap09Covering}: categorical core; faithfulness as hypothesis",
    (9, "prop:subloop"): r"\texttt{Chap09SubloopCorridor}: differentiable tangent angle",
    (9, "thm:loop_bounding"): r"\texttt{Chap09WindingBounds}: (1), one obstacle; homotopy identity as hypothesis",
    (9, "prop:winding_total_curvature"): r"\texttt{Chap09Winding}: $C^2$ curves; regularity of the angle lift as hypothesis",
    (9, "thm:unfolding"): r"\texttt{Chap09Covering}: more general than the text",
    (9, "prop:corridor_gap"): r"\texttt{Chap09SubloopCorridor}: lower bound; attaining arcs only",
    (9, "prop:teardrop"): r"\texttt{Chap09Teardrop}: (i) for $a < 2\rho$; (ii) for one turning pattern",
    (9, "prop:mouth_halfturn"): r"\texttt{Chap09MouthHalfturn}: differentiable tangent angle in $[0,\pi]$",
    (9, "prop:balloon_height"): r"\texttt{Chap08UTurn}: differentiable tangent angle",
    (9, "prop:teardrop_lower"): r"\texttt{Chap09Teardrop}: conditional, final step only",
    (10, "prop:degenerate"): r"\texttt{Chap10Generalization}: abstract; geodesic property as hypothesis",
    (10, "prop:counterexample"): r"\texttt{Chap10Generalization}: rank hypothesis explicit; Gaussian value not formalized",
    (11, "prop:relative_entropy_hessian"): r"\texttt{Chap11Fisher}: commuting case only",
    (11, "thm:first_law_entanglement"): r"\texttt{Chap11Fisher}: commuting case only",
    (11, "prop:mincut"): r"\texttt{Chap11MinCut}: linear-algebra half; factorization as hypothesis",
    (12, "thm:running_spectral_dimension"): r"\texttt{Chap12Spectral}: heat-kernel diagonal defined by its Fourier formula",
    (12, "thm:cartan_metric_emergence"): r"\texttt{Chap12Spectral}: algebraic and calculus core",
    (12, "thm:minimax_hamiltonian_regularization"): r"\texttt{Chap12Constraint}, \texttt{Chap12ConstraintMatrix}: pointwise, orthonormal frame; constraint as hypothesis",
    (12, "thm:jordan_chronology"): r"\texttt{Chap08Chronology}: order-theoretic skeleton",
    (12, "thm:neckpinch_condensation"): r"\texttt{Chap12Spectral}: pointwise ODE, curvature continuous in $t$",
}

BASE_STATUS = "L1--L2"
STATUS_EXTRA = {
    (1, "thm:grothendieck_cutnorm"): "F-60", (1, "thm:hypergraphon_compactness"): "F-60",
    (2, "prop:tangent_proj_mr"): "F-60", (2, "thm:toda_qr"): "F-60",
    (2, "thm:continuous_path_integral"): "F-63",
    (3, "prop:digamma_pde"): "F-60", (3, "conj:dixon"): "F-54", (3, "cor:dixon_higher"): "F-54",
    (3, "cor:dixon_real"): "F-54", (3, "cor:row_log_product"): "F-56",
    (4, "thm:modulational_instability"): "F-60", (5, "prop:inversion"): "F-60",
    (7, "lem:wall_structure"): "F-52", (7, "prop:ball_bound"): "F-52",
    (9, "prop:teardrop"): "F-52", (9, "prop:mouth_halfturn"): "F-52", (9, "prop:balloon_height"): "F-52",
    (9, "prop:teardrop_lower"): "F-52",
    (10, "prop:counterexample"): "F-59", (12, "thm:neckpinch_condensation"): "F-59",
}


def bracket_arg(text, i):
    if i >= len(text) or text[i] != "[":
        return None, i
    depth_b = depth_s = 0
    for j in range(i, len(text)):
        c = text[j]
        if c == "{":
            depth_b += 1
        elif c == "}":
            depth_b -= 1
        elif c == "[" and depth_b == 0:
            depth_s += 1
        elif c == "]" and depth_b == 0:
            depth_s -= 1
            if depth_s == 0:
                return text[i + 1:j], j + 1
    return None, i


def clean_title(title):
    parts = [p.strip() for p in title.split(";")]
    keep = [p for p in parts if "\\cite" not in p and "classical" not in p.lower()]
    if not keep:  # title is only a citation, e.g. FGHMvR \cite{...}
        keep = [re.sub(r"\{?\\cite(\[[^\]]*\])?\{[^}]*\}\}?", "", parts[0]).strip()]
    t = "; ".join(keep)
    t = re.sub(r"\s*\((after|see)?\s*\{?\\cite(\[[^\]]*\])?\{[^}]*\}\}?\)", "", t)  # "(after \cite{..})"
    t = re.sub(r"\{?\\cite(\[[^\]]*\])?\{[^}]*\}\}?", "", t)
    t = re.sub(r"\s*\((after|see)?\s*\)", "", t)  # empty "(after )" left by a removed citation
    return t.strip().rstrip(",")


def results(ch):
    f = sorted(BOOK.glob(f"chap{ch:02d}_*.tex"))[0]
    text = re.sub(r"(?<!\\)%.*", "", f.read_text(encoding="utf-8"))
    events = [(m.start(), m.group(1), m.end()) for m in BEGIN.finditer(text)]
    rows = []
    for pos, env, end in events:
        if env not in ENVS:
            continue
        title, after = bracket_arg(text, end)
        title = title or ""
        endm = re.search(r"\\end\{" + env + r"\*?\}", text[pos:])
        stmt = text[after:pos + endm.start()]
        head = stmt.split("\\begin{", 1)[0]
        lab = re.search(r"\\label\{([^}]*)\}", head).group(1)
        stmt_end = pos + endm.end()
        nxt = [e for e in events if e[0] >= stmt_end and e[1] not in ("remark", "example")]
        proof_txt = ""
        if nxt and nxt[0][1] == "proof":
            pe = re.search(r"\\end\{proof\}", text[nxt[0][0]:])
            proof_txt = text[nxt[0][0]:nxt[0][0] + pe.end()]
        cited = "\\cite" in title or "classical" in title.lower()
        sketch = bool(re.search(r"(?i)sketch", proof_txt[:300]))
        if (ch, lab) in PROOF_OVERRIDE:
            proof = PROOF_OVERRIDE[(ch, lab)]
        elif cited:
            proof = "cited" + ((" + sketch" if sketch else " + proof") if proof_txt else "")
        elif proof_txt:
            proof = "sketch" if sketch else "text"
        else:
            proof = "none"
        rows.append(dict(ch=ch, env=env, label=lab, title=clean_title(title), proof=proof))
    return rows


HEADER = r"""% Generated by _single_source_prototype/gen_results_index.py -- do not edit by hand.
\chapter[Results Index and Verification Status]{Results Index and Verification Status}
\chaptermark{Results Index}

This index lists every theorem, proposition, lemma and corollary of Chapters~1--13 with the support it has. Conjectures, definitions and remarks are not listed. The columns are:
{\raggedright
\begin{itemize}[leftmargin=1.5em,itemsep=1pt]
  \item \textbf{Proof}: \emph{text} (complete proof in the chapter), \emph{sketch} (proof outline), \emph{cited} (classical result with a precise citation, with or without a proof or sketch in the text), \emph{Ch.~3} (restates a theorem proved in Chapter~3).
  \item \textbf{Num.}: numerical checks of the repository that compare the statement, or a formula in it, with an independent computation and a negative control. V: the chapter's script \texttt{verify\_chapNN\_numerical.py}; F: the chapter's independent oracle script \texttt{F02\_chNN.py}; A: another targeted checking script. A check supports a formula; it does not prove the statement.
  \item \textbf{Lean}: the module of the \textsc{Lean}~4/\textsc{Mathlib} formalization (\texttt{formal\_proofs\_mathlib/LeanReal}) and the reduction declared for it in \texttt{formal\_proofs\_mathlib/README.md}. Every listed module compiles without \texttt{sorry} or new axioms. A module formalizes the stated reduction only (for instance a finite-dimensional, pointwise or conditional form), not the full statement unless it says \emph{full}. The \textsc{Lean} files in \texttt{formal\_proofs\_book} are a naming skeleton and are not listed.
  \item \textbf{Status}: L1--L2 means that the chapter's results were checked in a blind referee report (layer~1), revised by a different hand and re-checked (layer~2). An F-number names a later finding about the result; it is closed unless marked otherwise.
\end{itemize}
\par}
A dash means none.

{\scriptsize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{} >{\raggedright\arraybackslash}p{0.9cm} >{\raggedright\arraybackslash}p{3.7cm} >{\raggedright\arraybackslash}p{1.25cm} >{\raggedright\arraybackslash}p{0.85cm} >{\raggedright\arraybackslash}p{5.3cm} >{\raggedright\arraybackslash}p{1.55cm} @{}}
\toprule
\textbf{No.} & \textbf{Result} & \textbf{Proof} & \textbf{Num.} & \textbf{Lean module: reduction} & \textbf{Status} \\
\midrule
\endfirsthead
\toprule
\textbf{No.} & \textbf{Result} & \textbf{Proof} & \textbf{Num.} & \textbf{Lean module: reduction} & \textbf{Status} \\
\midrule
\endhead
\midrule
\multicolumn{6}{r@{}}{\emph{continued on the next page}} \\
\endfoot
\bottomrule
\endlastfoot
"""

FOOTER = r"""\end{longtable}
}

\textbf{Chapter 13} contains no theorem-type statements. Its closed form for $d_s(\tau)$ and its numerical bounds ($H_{\mathrm{inf}}$, $|\alpha_t|$, $\ell_\ast$, the rescaled delays) are formalized as arithmetic in \texttt{Chap13Numbers}, with the closed form of the heat-kernel integral and the limits $d_s \to 2, 4$ not covered. Some remarks also have \textsc{Lean} counterparts: the comparison of the SLD and Kubo--Mori metrics in Chapter~11 (\texttt{Chap11Fisher}), the slingshot bound in Chapter~8 (\texttt{Chap09WindingBounds}), the formulation remark of Chapter~10 (\texttt{Chap10Generalization}) and the classification table of Chapter~7 (\texttt{Chap07Bounds}).
"""

CHAPTER_NAMES = {
    1: "Functional Realizations of Matrices and Hypertensors", 2: "Geometric Flows on Matrix and Tensor Manifolds",
    3: "Analytic Continuation of Pascal's Simplex", 4: "Nonlinear Simplicial Waves and Porous Transport",
    5: "Inter-Dimensional Simplicial Transforms", 6: "Sierpi\\'nski Gasket Laplacians",
    7: "Minimax-Flat Submanifolds", 8: "Minimax Curvature and ADM Slicings", 9: "Global Minimax Curvature",
    10: "Minimax Trajectories on Statistical Manifolds", 11: "Emergent Spacetime and Quantum Geometry",
    12: "Holographic Entanglement and Quantum Geometry",
}


def main():
    lines = [HEADER]
    seen = set()
    n = 0
    for ch in range(1, 13):
        lines.append(r"\multicolumn{6}{@{}l}{\textbf{Chapter %d. %s}} \\[1pt]" % (ch, CHAPTER_NAMES[ch]))
        for r in results(ch):
            key = (ch, r["label"])
            seen.add(key)
            st = BASE_STATUS + ("; " + STATUS_EXTRA[key] if key in STATUS_EXTRA else "")
            lines.append(r"\ref{chap%02d:%s} & %s %s & %s & %s & %s & %s \\" % (
                ch, r["label"], ABBR[r["env"]], r["title"], r["proof"], NUM.get(key, "--"),
                LEAN.get(key, "--"), st))
            n += 1
        lines.append(r"\addlinespace[2pt]")
    unused = [k for k in list(NUM) + list(LEAN) + list(STATUS_EXTRA) + list(PROOF_OVERRIDE) if k not in seen]
    if unused:
        raise SystemExit(f"map keys that match no result: {sorted(set(unused))}")
    lines.append(FOOTER)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{OUT.name}: {n} results")


if __name__ == "__main__":
    main()
