from typing import List, Tuple, Dict, Any, Set
import numpy as np
from .core_encoder import DyadicEncoder

class FiniteTopology:
    def __init__(self, elements: List[int], open_sets: List[Set[int]], name: str = "Topology"):
        self.elements = elements
        self.n = len(elements)
        self.open_sets = [set(s) for s in open_sets]
        self.name = name

    def specialization_poset(self) -> List[Tuple[int, int]]:
        min_open = {}
        for x in self.elements:
            u_x = set(self.elements)
            for u in self.open_sets:
                if x in u:
                    u_x = u_x.intersection(u)
            min_open[x] = u_x
        order_pairs = []
        for x in self.elements:
            for y in self.elements:
                if min_open[x].issubset(min_open[y]):
                    order_pairs.append((x, y))
        return order_pairs

    def zeta_and_mobius_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        zeta = np.zeros((self.n, self.n), dtype=int)
        poset = set(self.specialization_poset())
        for i, x in enumerate(self.elements):
            for j, y in enumerate(self.elements):
                if (x, y) in poset:
                    zeta[i, j] = 1
        try:
            mu = np.linalg.inv(zeta)
            mu = np.round(mu).astype(int)
        except Exception:
            mu = np.eye(self.n, dtype=int)
        return zeta, mu

    def canonical_invariant_tuple(self) -> Tuple:
        _, mu = self.zeta_and_mobius_matrices()
        mu_trace = int(np.trace(mu))
        mu_sum = int(np.sum(mu))
        return (self.n, len(self.open_sets), mu_trace, mu_sum)

def topology_to_canonical_graph(T: FiniteTopology) -> Dict[str, Any]:
    poset = T.specialization_poset()
    return {"num_nodes": T.n, "dag_edges": poset, "name": T.name}

def arithmetize_topology(T: FiniteTopology) -> int:
    tup = T.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
