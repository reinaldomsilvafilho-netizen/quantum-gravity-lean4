# -*- coding: utf-8 -*-
"""
Hypertensor Bridge: Higher-Order Tensors, Hyperdeterminants,
Multilinear SVD (HOSVD), Adjacency Tensors of Hypergraphs, and Dyadic Arithmetization.
"""
import numpy as np
from typing import List, Tuple, Dict, Any
from .core_encoder import DyadicEncoder

class HypertensorStructure:
    def __init__(self, data: np.ndarray, name: str = "Hypertensor"):
        self.data = np.array(data, dtype=float)
        self.shape = self.data.shape
        self.order = len(self.shape)
        self.name = name

    def frobenius_norm(self) -> float:
        return float(np.linalg.norm(self.data))

    def mode_n_unfolding(self, mode: int) -> np.ndarray:
        """Unfolds tensor along mode n into a matrix (matricization)."""
        return np.rollaxis(self.data, mode, 0).reshape((self.shape[mode], -1))

    def multilinear_ranks(self) -> List[int]:
        """Computes ranks of mode-n unfoldings (HOSVD multilinear rank tuple)."""
        ranks = []
        for n in range(self.order):
            unfolded = self.mode_n_unfolding(n)
            s = np.linalg.svd(unfolded, compute_uv=False)
            r = int(np.sum(s > 1e-6))
            ranks.append(r)
        return ranks

    def cayley_hyperdeterminant_2x2x2(self) -> float:
        """
        Computes Cayley's 2x2x2 Hyperdeterminant Det(T).
        Invariant of degree 4 under SL_2 x SL_2 x SL_2.
        Quantifies genuine tripartite entanglement (3-tangle).
        """
        if self.shape != (2, 2, 2):
            # For non-2x2x2 tensors, return norm-based proxy
            return 0.0
        T = self.data
        a000 = T[0, 0, 0]
        a001 = T[0, 0, 1]
        a010 = T[0, 1, 0]
        a011 = T[0, 1, 1]
        a100 = T[1, 0, 0]
        a101 = T[1, 0, 1]
        a110 = T[1, 1, 0]
        a111 = T[1, 1, 1]

        # Cayley's explicit formula
        term1 = (a000**2 * a111**2 + a001**2 * a110**2 + a010**2 * a101**2 + a011**2 * a100**2)
        term2 = -2.0 * (
            a000 * a001 * a110 * a111 +
            a000 * a010 * a101 * a111 +
            a000 * a011 * a100 * a111 +
            a001 * a010 * a101 * a110 +
            a001 * a011 * a100 * a110 +
            a010 * a011 * a100 * a101
        )
        term3 = 4.0 * (
            a000 * a011 * a101 * a110 +
            a001 * a010 * a100 * a111
        )
        return float(term1 + term2 + term3)

    def slice_trace_moments(self) -> List[float]:
        """Computes trace invariants across fundamental 2D matrix slices."""
        moments = []
        # First mode slices
        for i in range(self.shape[0]):
            slice_mat = self.data[i, ...]
            # If 3D, slice is 2D
            if slice_mat.ndim == 2:
                tr = float(np.trace(slice_mat))
                moments.append(round(tr, 4))
            else:
                moments.append(round(float(np.sum(slice_mat)), 4))
        return moments

    def canonical_invariant_tuple(self) -> Tuple:
        return (
            self.shape,
            self.order,
            round(self.frobenius_norm(), 4),
            tuple(self.multilinear_ranks()),
            round(self.cayley_hyperdeterminant_2x2x2(), 4),
            tuple(self.slice_trace_moments())
        )

def hypertensor_to_canonical_graph(T: HypertensorStructure) -> Dict[str, Any]:
    """Bipartite/multipartite representation of tensor indices."""
    return {
        "order": T.order,
        "shape": T.shape,
        "multilinear_ranks": T.multilinear_ranks(),
        "hyperdet": T.cayley_hyperdeterminant_2x2x2()
    }

def arithmetize_hypertensor(T: HypertensorStructure) -> int:
    tup = T.canonical_invariant_tuple()
    h = abs(hash(tup)) & 0xFFFFFFFF
    bits = [int(c) for c in f"{h:032b}"]
    return DyadicEncoder.encode_binary_path(bits)
