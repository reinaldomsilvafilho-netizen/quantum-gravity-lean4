from typing import List, Tuple, Dict, Any
import numpy as np
from .core_encoder import DyadicEncoder

class KnotStructure:
    def __init__(self, name: str, crossings: int, seifert_matrix: List[List[int]], alexander_coeffs: List[int], jones_coeffs: List[int] = None):
        self.name = name
        self.crossings = crossings
        self.seifert = np.array(seifert_matrix, dtype=int)
        self.alexander = alexander_coeffs
        self.jones = jones_coeffs if jones_coeffs else []

    def determinant(self) -> int:
        m = self.seifert + self.seifert.T
        return int(round(abs(float(np.linalg.det(m)))))

    def signature(self) -> int:
        m = self.seifert + self.seifert.T
        eigs = np.linalg.eigvalsh(m)
        pos = int(np.sum(eigs > 1e-6))
        neg = int(np.sum(eigs < -1e-6))
        return pos - neg

    def to_tait_graph(self) -> Dict[str, Any]:
        dim = self.seifert.shape[0]
        nodes = dim + 1
        edges = []
        for i in range(dim):
            edges.append((i, (i + 1) % nodes, +1))
        return {"nodes": nodes, "signed_edges": edges, "knot": self.name}

    def canonical_invariant_tuple(self) -> Tuple:
        return (
            self.crossings,
            tuple(self.alexander),
            self.determinant(),
            self.signature(),
            tuple(self.jones)
        )

def knot_to_canonical_graph(K: KnotStructure) -> Dict[str, Any]:
    return K.to_tait_graph()

def arithmetize_knot(K: KnotStructure) -> int:
    tup = K.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)

STANDARD_KNOTS = {
    "Unknot": KnotStructure("Unknot", 0, [[1]], [1], [1]),
    "Trefoil_3_1": KnotStructure("Trefoil_3_1", 3, [[-1, 1], [0, -1]], [1, -1, 1], [1, 0, 1, -1]),
    "FigureEight_4_1": KnotStructure("FigureEight_4_1", 4, [[1, 0], [-1, -1]], [-1, 3, -1], [1, -1, 1, -1, 1]),
    "Cinquefoil_5_1": KnotStructure("Cinquefoil_5_1", 5, [[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1], [0, 0, 0, -1]], [1, -1, 1, -1, 1], [1, 0, 1, 0, 1, -1]),
    "ThreeTwist_5_2": KnotStructure("ThreeTwist_5_2", 5, [[2, -1], [0, 1]], [2, -3, 2], [1, -1, 2, -1, 1])
}
