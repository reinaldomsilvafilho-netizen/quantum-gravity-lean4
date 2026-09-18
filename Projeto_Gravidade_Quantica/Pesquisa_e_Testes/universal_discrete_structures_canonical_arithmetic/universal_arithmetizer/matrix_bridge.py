import numpy as np
from typing import List, Tuple, Dict, Any
from .core_encoder import DyadicEncoder

class MatrixStructure:
    def __init__(self, data: List[List[int]], name: str = "Matrix"):
        self.data = np.array(data, dtype=int)
        self.m, self.n = self.data.shape
        self.name = name

    def smith_normal_form(self) -> List[int]:
        min_dim = min(self.m, self.n)
        factors = []
        if min_dim == 0:
            return factors
        entries = np.abs(self.data.flatten())
        entries = entries[entries > 0]
        if len(entries) == 0:
            return [0] * min_dim
        g1 = int(np.gcd.reduce(entries))
        factors.append(g1)
        if min_dim >= 2:
            minors2 = []
            for r1 in range(self.m):
                for r2 in range(r1 + 1, self.m):
                    for c1 in range(self.n):
                        for c2 in range(c1 + 1, self.n):
                            det2 = abs(self.data[r1, c1] * self.data[r2, c2] - self.data[r1, c2] * self.data[r2, c1])
                            if det2 > 0:
                                minors2.append(det2)
            if len(minors2) > 0:
                g2 = int(np.gcd.reduce(minors2))
                s2 = g2 // g1 if g1 > 0 else 0
                factors.append(s2)
            else:
                factors.append(0)
        while len(factors) < min_dim:
            factors.append(0)
        return factors

    def characteristic_polynomial(self) -> List[float]:
        if self.m != self.n:
            return []
        poly = np.poly(self.data)
        return [round(float(c), 6) for c in poly]

    def trace_sequence(self, k_max: int = 4) -> List[int]:
        if self.m != self.n:
            return []
        traces = []
        curr = np.eye(self.m, dtype=int)
        for _ in range(k_max):
            curr = curr @ self.data
            traces.append(int(np.trace(curr)))
        return traces

    def to_bipartite_graph(self) -> Dict[str, Any]:
        nodes = self.m + self.n
        edges = []
        for i in range(self.m):
            for j in range(self.n):
                w = self.data[i, j]
                if w != 0:
                    edges.append((i, self.m + j, int(w)))
        return {"num_nodes": nodes, "edges": edges, "rows": self.m, "cols": self.n}

    def canonical_invariant_tuple(self) -> Tuple:
        snf = tuple(self.smith_normal_form())
        char_poly = tuple(self.characteristic_polynomial())
        traces = tuple(self.trace_sequence(4))
        return (self.m, self.n, snf, char_poly, traces)

def matrix_to_canonical_graph(M: MatrixStructure) -> Dict[str, Any]:
    return M.to_bipartite_graph()

def arithmetize_matrix(M: MatrixStructure) -> int:
    tup = M.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
