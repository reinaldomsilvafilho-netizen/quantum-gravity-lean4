import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

disclaimer = """
## ⚠️ Epistemic Status & Codebase Limitations

Following an independent adversarial audit (September 2026), this repository adopts a stance of strict **epistemic humility**. While the main 13-chapter treatise and accompanying manuscripts rigorously delimit phenomenological analogies from established physics theorems, the **Lean 4 and Python codebase** currently serve as **structural scaffolding and proofs-of-concept**, rather than full mechanical verifications of quantum gravity dynamics.

**Specifically:**
1. **Tautological Proofs:** Several Lean proofs assert physical relations (like the Koide formula or Wheeler-DeWitt boundary conditions) as axiomatic definitions and prove arithmetic equivalences, rather than deriving them from first-principles optimal transport or Lagrangian physics.
2. **Unconstrained Booleans:** Constraints in Lean (such as the ADM Hamiltonian and Diffeomorphism constraints) are currently modeled as unconstrained `Bool` variables (`true`/`false`) rather than actual non-linear partial differential equations.
3. **Construct-then-Check Python Scripts:** Some Python testbeds construct tensors specifically to pass mathematical checks, which validates the shape of the theory but does not constitute an independent physical simulation.

We are fully transparent about these limitations. The current code is mechanically clean (0 `sorry`, 0 axioms), but **does not** yet constitute a rigorous formal foundation for quantum gravity. A deep refactoring roadmap is underway to align the codebase with the strict mathematical rigor of the textual treatise.

---

"""

# Insert right before '## 🛠️ Building and Verifying the Proofs'
content = content.replace("## 🛠️ Building and Verifying the Proofs", disclaimer + "## 🛠️ Building and Verifying the Proofs")

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("README patched successfully.")
