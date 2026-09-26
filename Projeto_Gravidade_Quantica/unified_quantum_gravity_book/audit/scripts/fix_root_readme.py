"""Neutralize unsupported verification claims in the repository root README (WORKPLAN F-21/F-23)."""
p = '../../README.md'
s = open(p, encoding='utf-8').read()
notice = """
> **Verification status (updated 2026-09-24).** An audit found that the Lean 4 modules listed below
> (`formal_proofs_book/Book`, and the other `*_formal_proofs` packages built the same way) encode each
> result as a structure of Boolean/floating-point placeholders whose "theorems" restate their hypotheses.
> They do **not** import Mathlib and do **not** verify the mathematics of the monographs. Earlier badges and
> phrases such as "Mathlib certified", "100% verified" and "N/N certified obligations" were therefore
> incorrect and have been removed. A genuine Mathlib formalization is in progress
> (`formal_proofs_book/BookReal`). The current status of every result, with known errors and corrections,
> is tracked in `Projeto_Gravidade_Quantica/unified_quantum_gravity_book/WORKPLAN.md` and `CHANGELOG.md`.
"""
reps = [
    ('## Machine-Checked Formal Verification & Type-Theoretic Specification Suite in Lean 4',
     '## Sources, Numerical Checks, and Lean 4 Material (formalization in progress)'),
    ('[![Verified with Mathlib 4](https://img.shields.io/badge/Mathlib_4-Certified-success.svg)](https://github.com/leanprover-community/mathlib4)\n', ''),
    ('[![Zero Sorry](https://img.shields.io/badge/Proofs-100%25%20Verified%20(0%20sorry)-brightgreen.svg)]()\n', ''),
    ('**Permanent GitHub Repository:** [quantum-gravity-lean4](https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4)\n',
     '**Permanent GitHub Repository:** [quantum-gravity-lean4](https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4)\n' + notice),
    (' (Lean 4 Certified Edition)', ''),
    (' (Lean 4 Edition)', ''),
    ('This repository hosts the **complete open-science machine-checked interactive formalization suite in Lean 4** and companion **numerical testbed batteries in Python**',
     'This repository hosts the sources, **Lean 4 material (a naming skeleton; real formalization in progress)** and companion **numerical check scripts in Python**'),
    ('Every theoretical claim across the treatise is systematically verified across three independent, synchronized epistemic pillars:',
     'The project aims at three complementary layers of verification. As stated in the notice above, the formal (Lean) layer is not yet in place:'),
    ('**144 / 144**', '**skeleton only**'),
    ('(**144 certified obligations**', '(Lean naming skeleton, not a formalization;'),
    ('(21 certified obligations)', '(Lean naming skeleton; not yet audited)'),
    ('*Expected output: All 167 proof obligations across Chapters 01-13, Master Lagrangian, Fermion Hierarchy, and Linear Algebra are certified with 0 `sorry` and 0 errors.*',
     '*Note: the executable only prints the names of the skeleton structures; it does not certify any mathematical statement (see the notice at the top).*'),
]
missing = [a for a, _ in reps if a not in s]
for a, b in reps:
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('missing patterns:', missing)
