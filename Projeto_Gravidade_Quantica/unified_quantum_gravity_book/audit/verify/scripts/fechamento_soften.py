from pathlib import Path
B = Path(r"C:\Users\monar\Documents\antigravity\resilient-turing\Projeto_Gravidade_Quantica\unified_quantum_gravity_book")
EDITS = {
    "chap11_emergent_spacetime_tensor_networks_holonomies.tex": [
        ("gravitational geometry that this treatise uses.", "gravitational geometry that this book uses."),
        ("collects the parts of that line which the treatise uses,", "collects the parts of that line which the book uses,"),
        ("lists the correspondences used in the treatise, each with its status.", "lists the correspondences used in the book, each with its status."),
    ],
    "chap12_grand_unification_quantum_gravity_treatise.tex": [
        ("it contains no theorems. A unified framework often seeks to relate the standard model of particle physics to low-energy geometric condensations. In this section,",
         "it contains no theorems. Several approaches to quantum gravity try to relate the standard model of particle physics to low-energy geometric structures. In this section,"),
        ("Table~\\ref{tab:grand_unification} establishes the theoretical dictionary uniting all four domains of the theory.",
         "Table~\\ref{tab:grand_unification} lists correspondences between the four areas of the book; they are analogies unless a row cites a result proved here."),
        ("establish about quantum gravity from what they suggest.", None),
        ("the three programs of this treatise establish", "the three programs of this book establish"),
    ],
    "_single_source_prototype/official_master_structure.tex": [
        ("This comprehensive monograph consolidates the multidisciplinary investigations developed across three fundamental programs of contemporary theoretical research: functional tensor algebra and geometric flows, fractional calculus on continuous Pascal simplices, and the variational theory of minimax extrinsic curvature with causal Jordan embeddings.",
         "This monograph collects work on three programs: functional tensor algebra and geometric flows, fractional calculus on continuous Pascal simplices, and the variational theory of minimax extrinsic curvature with causal Jordan embeddings."),
    ],
}
for name, reps in EDITS.items():
    p = B / name
    t = p.read_text(encoding="utf-8")
    for old, new in reps:
        n = t.count(old)
        if n != 1:
            raise SystemExit(f"{name}: {old[:60]!r} occurs {n} times")
        if new is not None:
            t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
    print(name, "ok")
