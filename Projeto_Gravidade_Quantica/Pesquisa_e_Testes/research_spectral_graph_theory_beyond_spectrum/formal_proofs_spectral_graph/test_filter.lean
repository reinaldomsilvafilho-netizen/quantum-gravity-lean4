
namespace SpectralGraph

-- An r-uniform hyperedge is a list of vertices.
-- Intersection predicate: does edge `e` contain all singletons in `target`?
def hits_all (target : List Nat) (e : List Nat) : Bool :=
  target.all (fun u => e.contains u)

-- Partition cut capacity: sum of weights of edges that hit all singletons in `target`
def cap_r (target : List Nat) (edges : List (List Nat)) (w : List Nat -> Int) : Int :=
  ((edges.filter (fun e => hits_all target e)).map w).foldl (· + ·) 0

-- Concrete hypergraph on vertices {0, 1, 2, 3, 4} with 3-uniform hyperedges:
def sample_edges : List (List Nat) :=
  [[0, 1, 2], [0, 1, 3], [0, 2, 4], [1, 2, 3], [2, 3, 4]]

def sample_w : List Nat -> Int
  | [0, 1, 2] => 17
  | [0, 1, 3] => 23
  | [0, 2, 4] => 31
  | [1, 2, 3] => 47
  | [2, 3, 4] => 59
  | _ => 0

-- Evaluation: the filter isolates ONLY [0, 1, 2]
theorem filter_isolates_target :
    sample_edges.filter (fun e => hits_all [0, 1, 2] e) = [[0, 1, 2]] := by
  rfl

-- Therefore, the partition cut evaluates to the exact weight w([0, 1, 2]) = 17:
theorem cap_r_evaluates_exactly_to_target :
    cap_r [0, 1, 2] sample_edges sample_w = 17 := by
  rfl

-- For any target e in sample_edges, no other edge in sample_edges contains all 3 vertices:
theorem sample_edge_1_unique (e : List Nat) (he : e ∈ sample_edges) (hh : hits_all [0, 1, 3] e = true) :
    e = [0, 1, 3] := by
  revert he hh
  intro he hh
  cases he with
  | head => revert hh; decide
  | tail _ h1 =>
    cases h1 with
    | head => rfl
    | tail _ h2 =>
      cases h2 with
      | head => revert hh; decide
      | tail _ h3 =>
        cases h3 with
        | head => revert hh; decide
        | tail _ h4 =>
          cases h4 with
          | head => revert hh; decide
          | tail _ h5 => contradiction

-- The partition cut for [0, 1, 3] evaluates to 23:
theorem cap_r_evaluates_target_1 :
    cap_r [0, 1, 3] sample_edges sample_w = 23 := by
  rfl

-- Inductive isolation theorem:
-- Given an edge list where head is the target, hits_all target head = true,
-- and NO element in tail satisfies hits_all target, the filter collapses to [target]:
theorem filter_collapse (target : List Nat) (tail : List (List Nat))
    (h_head : hits_all target target = true)
    (h_tail_none : ∀ e ∈ tail, hits_all target e = false) :
    (target :: tail).filter (fun e => hits_all target e) = [target] := by
  simp only [List.filter]
  rw [h_head]
  have h_nil : tail.filter (fun e => hits_all target e) = [] := by
    induction tail with
    | nil => rfl
    | cons x xs ih =>
      simp only [List.filter]
      have hx : hits_all target x = false := h_tail_none x (List.Mem.head xs)
      rw [hx]
      apply ih
      intro e he
      exact h_tail_none e (List.Mem.tail x he)
  rw [h_nil]

-- Corollary: the cut capacity of (target :: tail) is exactly w(target):
theorem cap_r_collapse (target : List Nat) (tail : List (List Nat)) (w : List Nat -> Int)
    (h_head : hits_all target target = true)
    (h_tail_none : ∀ e ∈ tail, hits_all target e = false) :
    cap_r target (target :: tail) w = w target := by
  dsimp [cap_r]
  have h_filt := filter_collapse target tail h_head h_tail_none
  rw [h_filt]
  dsimp [List.map, List.foldl]
  omega

end SpectralGraph
