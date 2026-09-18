from typing import List, Tuple, Dict, Any
import numpy as np
from .core_encoder import DyadicEncoder

class FiniteGroupStructure:
    def __init__(self, cayley_table: List[List[int]], name: str = "Group"):
        self.table = np.array(cayley_table, dtype=int)
        self.order = self.table.shape[0]
        self.name = name

    def is_abelian(self) -> bool:
        return bool(np.all(self.table == self.table.T))

    def conjugacy_classes(self) -> List[List[int]]:
        e = 0
        inverses = [0] * self.order
        for i in range(self.order):
            for j in range(self.order):
                if self.table[i, j] == e:
                    inverses[i] = j
                    break
        classes = []
        visited = set()
        for x in range(self.order):
            if x not in visited:
                c_set = set()
                for g in range(self.order):
                    g_inv = inverses[g]
                    gx = self.table[g, x]
                    gxg_inv = self.table[gx, g_inv]
                    c_set.add(gxg_inv)
                classes.append(sorted(list(c_set)))
                visited.update(c_set)
        return classes

    def element_orders(self) -> List[int]:
        orders = []
        e = 0
        for x in range(self.order):
            curr = x
            ord_val = 1
            while curr != e:
                curr = self.table[curr, x]
                ord_val += 1
                if ord_val > self.order:
                    break
            orders.append(ord_val)
        return sorted(orders)

    def canonical_invariant_tuple(self) -> Tuple:
        classes = self.conjugacy_classes()
        class_sizes = sorted([len(c) for c in classes])
        return (
            self.order,
            self.is_abelian(),
            len(classes),
            tuple(class_sizes),
            tuple(self.element_orders())
        )

def group_to_canonical_graph(G: FiniteGroupStructure) -> Dict[str, Any]:
    return {"order": G.order, "is_abelian": G.is_abelian(), "classes": len(G.conjugacy_classes())}

def arithmetize_group(G: FiniteGroupStructure) -> int:
    tup = G.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
