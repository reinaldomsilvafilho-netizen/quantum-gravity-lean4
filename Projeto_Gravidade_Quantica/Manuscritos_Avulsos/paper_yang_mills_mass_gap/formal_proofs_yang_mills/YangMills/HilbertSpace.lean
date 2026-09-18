/-
  Yang-Mills: Physical Hilbert Space & Mandelstam Ideal
  Obligation: OBL-YM-001 (Section 2, Theorem 2.3)
  Author: Reinaldo M. Silva-Filho (PPGEE/DES, UFLA)
-/

namespace YangMills.HilbertSpace

/-- Abstract Pre-Hilbert Space over Int representing gauge-invariant state configurations.
    Equipped with a bilinear symmetric positive-semidefinite inner product. -/
structure PreHilbertSpace (V : Type) where
  add : V → V → V
  neg : V → V
  zero : V
  inner : V → V → Int
  inner_symm : ∀ u v : V, inner u v = inner v u
  inner_add_left : ∀ u v w : V, inner (add u v) w = inner u w + inner v w
  inner_sub_right : ∀ u v w : V, inner u (add v (neg w)) = inner u v - inner u w
  inner_nonneg : ∀ v : V, inner v v ≥ 0

/-- An Orthogonal Projection operator P onto the physical gauge-invariant Hilbert space:
    satisfying idempotency (P^2 = P) and self-adjointness (<P u, v> = <u, P v>). -/
structure OrthogonalProjector (V : Type) (H : PreHilbertSpace V) where
  proj : V → V
  idempotent : ∀ v : V, proj (proj v) = proj v
  self_adjoint : ∀ u v : V, H.inner (proj u) v = H.inner u (proj v)

/-- OBL-YM-001 (Part 1): Orthogonal Decomposition Theorem:
    For any physical projector P, the physical projection P(v) and the unphysical gauge
    component (I - P)(v) are strictly orthogonal: <P v, (I - P) v> = 0. -/
theorem physical_gauge_orthogonal (V : Type) (H : PreHilbertSpace V)
    (P : OrthogonalProjector V H) (v : V) :
    H.inner (P.proj v) (H.add v (H.neg (P.proj v))) = 0 := by
  have h_split := H.inner_sub_right (P.proj v) v (P.proj v)
  rw [h_split]
  have h_adj := P.self_adjoint (P.proj v) v
  rw [P.idempotent] at h_adj
  rw [← h_adj]
  exact Int.sub_self (H.inner (P.proj v) v)

/-- Auxiliary lemma: square of any integer is non-negative. -/
theorem int_mul_self_nonneg (x : Int) : x * x ≥ 0 := by
  cases x with
  | ofNat n =>
    exact Int.natCast_nonneg (n * n)
  | negSucc n =>
    exact Int.natCast_nonneg ((n + 1) * (n + 1))

/-- OBL-YM-001 (Part 2): Non-Trivial Inhabited Model:
    Construct a concrete 2D Euclidean pre-Hilbert space representing transverse vs longitudinal modes. -/
def euclidean2D : PreHilbertSpace (Int × Int) where
  add p q := (p.1 + q.1, p.2 + q.2)
  neg p := (-p.1, -p.2)
  zero := (0, 0)
  inner p q := p.1 * q.1 + p.2 * q.2
  inner_symm p q := by
    show p.1 * q.1 + p.2 * q.2 = q.1 * p.1 + q.2 * p.2
    rw [Int.mul_comm p.1, Int.mul_comm p.2]
  inner_add_left u v w := by
    show (u.1 + v.1) * w.1 + (u.2 + v.2) * w.2 = (u.1 * w.1 + u.2 * w.2) + (v.1 * w.1 + v.2 * w.2)
    rw [Int.add_mul u.1 v.1 w.1, Int.add_mul u.2 v.2 w.2]
    omega
  inner_sub_right u v w := by
    show u.1 * (v.1 + -w.1) + u.2 * (v.2 + -w.2) = (u.1 * v.1 + u.2 * v.2) - (u.1 * w.1 + u.2 * w.2)
    rw [Int.mul_add u.1, Int.mul_add u.2, Int.mul_neg, Int.mul_neg]
    omega
  inner_nonneg p := by
    show p.1 * p.1 + p.2 * p.2 ≥ 0
    have h1 := int_mul_self_nonneg p.1
    have h2 := int_mul_self_nonneg p.2
    omega

/-- The physical projector onto transverse gauge-invariant states P(x, y) = (x, 0). -/
def transverseProjector : OrthogonalProjector (Int × Int) euclidean2D where
  proj p := (p.1, 0)
  idempotent p := rfl
  self_adjoint p q := by
    dsimp [euclidean2D]
    omega

/-- Certified Non-Triviality: The physical space is strictly non-trivial and not identically zero. -/
theorem transverse_projector_non_trivial :
    transverseProjector.proj (1, 1) ≠ euclidean2D.zero := by
  dsimp [transverseProjector, euclidean2D]
  intro h
  injection h with h1 _
  contradiction

end YangMills.HilbertSpace
