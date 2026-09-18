from typing import List, Tuple, Dict, Any, Set
from itertools import combinations
from .core_encoder import DyadicEncoder

class MatroidStructure:
    def __init__(self, ground_set: List[int], bases: List[Set[int]], name: str = "Matroid"):
        self.E = set(ground_set)
        self.bases = [set(b) for b in bases]
        self.name = name
        self.rank = len(self.bases[0]) if self.bases else 0

    def rank_of_subset(self, A: Set[int]) -> int:
        if not self.bases:
            return 0
        return max(len(A.intersection(B)) for B in self.bases)

    def tutte_polynomial_evals(self) -> Dict[str, int]:
        n = len(self.E)
        rE = self.rank
        num_bases = len(self.bases)
        total_subsets = 1 << n
        independent_count = 0
        spanning_count = 0
        e_list = sorted(list(self.E))
        for k in range(n + 1):
            for combo in combinations(e_list, k):
                A = set(combo)
                rA = self.rank_of_subset(A)
                if rA == len(A):
                    independent_count += 1
                if rA == rE:
                    spanning_count += 1
        return {
            "T_1_1_bases": num_bases,
            "T_2_2_subsets": total_subsets,
            "T_1_0_independent": independent_count,
            "T_0_1_spanning": spanning_count
        }

    def canonical_invariant_tuple(self) -> Tuple:
        evals = self.tutte_polynomial_evals()
        return (
            len(self.E),
            self.rank,
            evals["T_1_1_bases"],
            evals["T_1_0_independent"],
            evals["T_0_1_spanning"]
        )

def matroid_to_canonical_graph(M: MatroidStructure) -> Dict[str, Any]:
    return {"elements": len(M.E), "rank": M.rank, "bases_count": len(M.bases)}

def arithmetize_matroid(M: MatroidStructure) -> int:
    tup = M.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
