# Applications of the book's mathematical methods to superconductors

Started 2026-09-28. Status: **exploration, nothing verified**. The same protocol as the book applies: literature review, precise formulation, Python with an independent oracle and a negative control, proof, blind review, then publication.

## Starting point
The quantum-gravity model itself has nothing to say about superconductivity. Its scales (~10⁻³⁰ m) are about 20 orders of magnitude from the meV physics of superconductors. What can transfer are the **mathematical methods** of the book.

## Lines of work

| # | Problem | Methods from the book | Status |
|---|---|---|---|
| **A** | Routing and design of REBCO tape (HTS) coils under a curvature and torsion limit | ch. 7–9: L∞ minimax of the second fundamental form, C^{1,1} regularity, Chebyshev equioscillation, homotopy balloons (salvaged from ch. 14) | **active**, see `A_bobinas_REBCO_curvatura/` |
| **B** | Long-range superconducting coherence on fractal and granular networks, controlled by the spectral dimension | ch. 6: Kigami Laplacian, d_s, Γ-convergence; ch. 12: heat kernel | **active**, see `B_coerencia_redes_fractais/` |
| C | Quartic dispersion (Lifshitz points, band touchings in bilayer graphene and moiré systems): density of states ~ ε^{d_s/2−1} and a T_c enhancement | heat kernel and d_s of the k² + ℓ²k⁴ symbol (`Pesquisa_e_Testes/consistencia_operador/`) | idea; the known tools are only reorganized |

## Other applications (backlog, not started)

| Method | Application | Assessment |
|---|---|---|
| Curvature minimax (ch. 7–9) | optical fibres (bending loss), cables, catheters and needles, rails and roads, CNC | high: the minimum bending radius is the real constraint |
| Continuous multinomials and Dixon (ch. 3) | statistics of compositional data, smoothing of multinomials, likelihood asymptotics | medium to high; connects to the author's statistics texts |
| Barnes G (ch. 5) | random matrix theory | established; marginal contribution |
| d_s and transport (ch. 4, 6) | porous media, battery electrodes, anomalous diffusion | medium |
| Fisher–Rao (ch. 10) | natural-gradient optimization | medium; a crowded field |

## Rules for this folder
- One topic per subfolder, one file per subject, updated in place.
- A claim of novelty only after a literature search, recorded in `literatura.md`.
- The older folders under `Aplicacoes_Tecnologicas/` (01–05, Fusao_Nuclear, …) were produced with Gemini and **have not been audited**. Their "AUDIT_CERTIFICATE" files do not count as verification.
