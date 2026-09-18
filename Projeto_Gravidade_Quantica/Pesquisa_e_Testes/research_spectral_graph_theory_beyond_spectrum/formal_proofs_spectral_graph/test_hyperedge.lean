
namespace SpectralGraph

-- An r-uniform hyperedge over vertex set Nat represented by its vertices
def hits_all (singletons : List Nat) (e : List Nat) : Bool :=
  singletons.all (fun x => e.contains x)

-- Direct calculation on concrete hypergraph:
-- Suppose we have a 3-uniform hypergraph on 5 vertices with hyperedges:
def sample_hyperedges : List (List Nat) :=
  [[0, 1, 2], [0, 1, 3], [0, 2, 4], [1, 2, 3], [2, 3, 4]]

def sample_weights : List Nat -> Int
  | [0, 1, 2] => 10
  | [0, 1, 3] => 20
  | [0, 2, 4] => 30
  | [1, 2, 3] => 40
  | [2, 3, 4] => 50
  | _ => 0

def cap_r (target : List Nat) (edges : List (List Nat)) (w : List Nat -> Int) : Int :=
  ((edges.filter (fun e => hits_all target e)).map w).foldl (· + ·) 0

-- Evaluation on target [0, 1, 2]:
theorem cap_r_evaluates_to_target_weight :
    cap_r [0, 1, 2] sample_hyperedges sample_weights = 10 := by
  rfl

-- Filter isolates exactly [0, 1, 2]:
theorem filter_isolates_unique_hyperedge :
    sample_hyperedges.filter (fun e => hits_all [0, 1, 2] e) = [[0, 1, 2]] := by
  rfl

-- General uniqueness lemma:
-- If e has length 3 and contains 0, 1, 2, then if e is chosen from sample_hyperedges, e = [0, 1, 2]
theorem unique_matching_edge (e : List Nat) (he : e ∈ sample_hyperedges) (hh : hits_all [0, 1, 2] e = true) :
    e = [0, 1, 2] := by
  revert he hh
  intro he hh
  -- We can check exhaustively
  cases he with
  | head => rfl
  | tail _ h1 =>
    cases h1 with
    | head => revert hh; decide
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

end SpectralGraph
