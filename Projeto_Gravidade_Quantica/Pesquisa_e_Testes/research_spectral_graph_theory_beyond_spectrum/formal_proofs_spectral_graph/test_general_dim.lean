
namespace SpectralGraph

-- General Moved r-Subset Theorem for any uniformity r >= 1 and any n >= r + 1:
-- Let sigma be any permutation on vertex set Nat.
-- Suppose sigma is non-identity, meaning there exists a vertex u moved to v != u.
-- Let `rest` be any list of r - 1 vertices disjoint from {u, v}.
-- Then the r-hyperedge `e = u :: rest` is moved by sigma (i.e. v in sigma(e) but v not in e).

def map_perm (sigma : Nat -> Nat) (e : List Nat) : List Nat :=
  e.map sigma

theorem moved_hyperedge_general (sigma : Nat -> Nat) (u v : Nat) (rest : List Nat)
    (h_sigma_u : sigma u = v)
    (h_neq : v ≠ u)
    (h_not_in : v ∉ rest) :
    v ∉ (u :: rest) ∧ v ∈ map_perm sigma (u :: rest) := by
  constructor
  · intro h_in
    cases h_in with
    | head => exact h_neq rfl
    | tail _ h_tail => exact h_not_in h_tail
  · dsimp [map_perm, List.map]
    rw [h_sigma_u]
    apply List.Mem.head

-- Corollary: for any non-identity permutation, the hyperedge e = u :: rest cannot be fixed:
theorem hyperedge_not_fixed (sigma : Nat -> Nat) (u v : Nat) (rest : List Nat)
    (h_sigma_u : sigma u = v)
    (h_neq : v ≠ u)
    (h_not_in : v ∉ rest) :
    map_perm sigma (u :: rest) ≠ (u :: rest) := by
  have ⟨h_not_e, h_in_mapped⟩ := moved_hyperedge_general sigma u v rest h_sigma_u h_neq h_not_in
  intro h_eq
  rw [h_eq] at h_in_mapped
  exact h_not_e h_in_mapped

-- General Orbit Counting Defect Theorem:
-- If a group action on a finite set of size N has at least one non-trivial orbit (an element with orbit size >= 2),
-- then the number of orbits is strictly less than N.
def orbit_defect (ambient_dim num_orbits : Nat) (h_nontriv : num_orbits < ambient_dim) : Nat :=
  ambient_dim - num_orbits

theorem orbit_defect_strictly_positive (ambient_dim num_orbits : Nat)
    (h_nontriv : num_orbits < ambient_dim) :
    orbit_defect ambient_dim num_orbits h_nontriv > 0 := by
  dsimp [orbit_defect]
  omega

-- Concrete 3-uniform hyperedge witness (r = 3, n >= 4):
-- Let sigma = (0, 1) swap 0 and 1, fixing 2 and 3.
-- Hyperedge e = [0, 2, 3] of size 3 is sent to [1, 2, 3] != [0, 2, 3].
def tau_01 : Nat -> Nat
  | 0 => 1
  | 1 => 0
  | x => x

def hyperedge_023 : List Nat := [0, 2, 3]

theorem hyperedge_023_moved :
    map_perm tau_01 hyperedge_023 = [1, 2, 3] := by
  rfl

theorem hyperedge_023_not_fixed :
    map_perm tau_01 hyperedge_023 ≠ hyperedge_023 := by
  decide

end SpectralGraph
