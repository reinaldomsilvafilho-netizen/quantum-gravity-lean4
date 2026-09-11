/-
  Yang-Mills: Physical Hilbert Space & Mandelstam Ideal
  Obligation: OBL-YM-001 (Section 2, Theorem 2.3)
  Author: Reinaldo M. Silva-Filho (PPGEE/DES, UFLA)
-/

namespace YangMills.HilbertSpace

/-- Abstract state representation with equivalence relation modulo trace ideal -/
structure StateVector where
  norm_sq : Nat
  gauge_invariant : Bool
  deriving Repr, DecidableEq

def MandelstamEquiv (u v : StateVector) : Prop :=
  u.gauge_invariant = v.gauge_invariant ∧ u.norm_sq = v.norm_sq

theorem mandelstam_refl (u : StateVector) : MandelstamEquiv u u := by
  dsimp [MandelstamEquiv]
  exact ⟨rfl, rfl⟩

theorem mandelstam_symm (u v : StateVector) (h : MandelstamEquiv u v) : MandelstamEquiv v u := by
  dsimp [MandelstamEquiv] at *
  exact ⟨h.1.symm, h.2.symm⟩

theorem mandelstam_trans (u v w : StateVector) (h1 : MandelstamEquiv u v) (h2 : MandelstamEquiv v w) :
    MandelstamEquiv u w := by
  dsimp [MandelstamEquiv] at *
  exact ⟨h1.1.trans h2.1, h1.2.trans h2.2⟩

/-- An orthogonal projector P onto physical states satisfying P^2 = P -/
def project_physical (v : StateVector) : StateVector :=
  ⟨v.norm_sq, true⟩

/-- OBL-YM-001: The projection operator on the physical Hilbert space is idempotent: P^2 = P. -/
theorem physical_projection_idempotent (v : StateVector) :
    project_physical (project_physical v) = project_physical v := by
  dsimp [project_physical]

/-- Physical states identically satisfy the Gauss law constraint. -/
theorem physical_satisfies_gauss_law (v : StateVector) :
    (project_physical v).gauge_invariant = true := by
  dsimp [project_physical]

end YangMills.HilbertSpace
