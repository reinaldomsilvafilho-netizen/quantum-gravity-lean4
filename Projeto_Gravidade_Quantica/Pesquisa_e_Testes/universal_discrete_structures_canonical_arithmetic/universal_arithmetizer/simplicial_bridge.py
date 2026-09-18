from typing import List, Tuple, Dict, Any, Set
from itertools import combinations
from math import comb
from .core_encoder import DyadicEncoder

class SimplicialComplex:
    def __init__(self, facets: List[List[int]], name: str = "SimplicialComplex"):
        self.name = name
        self.faces: List[Set[int]] = []
        for facet in facets:
            f_set = set(facet)
            self._add_all_subsets(f_set)
        unique_faces = []
        for f in self.faces:
            if f not in unique_faces:
                unique_faces.append(f)
        self.faces = unique_faces
        self.dim = max(len(f) - 1 for f in self.faces) if self.faces else -1

    def _add_all_subsets(self, s: Set[int]):
        s_list = sorted(list(s))
        for k in range(1, len(s_list) + 1):
            for c in combinations(s_list, k):
                self.faces.append(set(c))

    def f_vector(self) -> List[int]:
        f_vec = [0] * (self.dim + 1)
        for f in self.faces:
            k = len(f) - 1
            if k >= 0:
                f_vec[k] += 1
        return f_vec

    def euler_characteristic(self) -> int:
        f = self.f_vector()
        chi = 0
        for i, count in enumerate(f):
            chi += ((-1) ** i) * count
        return chi

    def h_vector(self) -> List[int]:
        f = self.f_vector()
        d = len(f)
        h = [0] * (d + 1)
        h[0] = 1
        for j in range(1, d + 1):
            val = 0
            for i in range(j + 1):
                sign = (-1) ** (j - i)
                c = comb(d - i, j - i)
                f_val = 1 if i == 0 else f[i - 1]
                val += sign * c * f_val
            h[j] = val
        return h

    def canonical_invariant_tuple(self) -> Tuple:
        return (
            self.dim,
            tuple(self.f_vector()),
            tuple(self.h_vector()),
            self.euler_characteristic()
        )

def simplicial_to_canonical_graph(S: SimplicialComplex) -> Dict[str, Any]:
    vertices = set()
    for f in S.faces:
        vertices.update(f)
    return {"num_vertices": len(vertices), "f_vector": S.f_vector(), "dim": S.dim}

def arithmetize_simplicial(S: SimplicialComplex) -> int:
    tup = S.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
