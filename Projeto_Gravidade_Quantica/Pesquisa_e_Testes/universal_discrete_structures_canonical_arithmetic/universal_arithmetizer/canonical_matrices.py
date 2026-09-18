# -*- coding: utf-8 -*-
"""
Canonical Matrices Module:
Generates the two fundamental canonical representation matrices for the first N natural numbers:
1. Canonical Symbolic Avatar Matrix M_symb:
   - Arithmetic prime factors, dyadic word, graph avatar, characteristic polynomial,
     local Dirichlet generating seed, hypertensor entanglement class.
2. Canonical Numerical Results Matrix M_num:
   - Euler totient, divisor count, divisor sum, spectral radius, Fiedler gap,
     spectral energy, Chen holonomy norm, Cayley hyperdeterminant, Frobenius norm, Betti_1.
3. 20x20 Inter-Number Smith GCD Matrix S_20 and Coprimality Adjacency C_20.
"""
import math
import numpy as np
from typing import List, Dict, Any, Tuple
from .natural_fingerprint import NaturalFingerprint
from .core_encoder import DyadicEncoder

class CanonicalMatricesEngine:
    def __init__(self, max_n: int = 20):
        self.max_n = max_n
        self._compute_matrices()

    def _compute_matrices(self):
        self.symbolic_matrix = []
        self.numeric_matrix = []

        for N in range(1, self.max_n + 1):
            fp = NaturalFingerprint(N)
            fp_master = fp.master_digital_fingerprint()
            bits = DyadicEncoder.decode_integer(N)
            bit_str = "".join(str(b) for b in bits) if bits else "ε"
            
            # 1. Arithmetic symbol
            factors = fp.prime_factorization()
            if N == 1:
                arith_sym = "1"
            else:
                parts = [f"{p}^{a}" if a > 1 else f"{p}" for p, a in factors]
                arith_sym = " * ".join(parts)
                
            divs = [d for d in range(1, N + 1) if N % d == 0]
            dirichlet_terms = [f"{d}^(-s)" if d > 1 else "1" for d in divs]
            dirichlet_sym = " + ".join(dirichlet_terms)
            
            # 2. Graph & Characteristic polynomial
            adj = fp.adj_matrix
            n_dim = fp.matrix_dim
            n_edges = int(np.sum(adj)) // 2
            
            poly_coeffs = [int(round(c)) for c in np.poly(adj)]
            deg = len(poly_coeffs) - 1
            terms = []
            for i, c in enumerate(poly_coeffs):
                p = deg - i
                if c == 0:
                    continue
                sign = "+" if c > 0 and len(terms) > 0 else ("-" if c < 0 and len(terms) > 0 else ("-" if c < 0 else ""))
                val = abs(c)
                val_str = "" if val == 1 and p > 0 else str(val)
                if p == 0:
                    term = f"{val}"
                elif p == 1:
                    term = f"{val_str}t"
                else:
                    term = f"{val_str}t^{p}"
                terms.append(f"{sign} {term}" if len(terms) > 0 else f"{sign}{term}")
            char_poly_str = " ".join(terms) if terms else "t^3"

            # 3. Hypertensor entanglement state
            cayley_val = fp_master["hypertensor"]["cayley_hyperdeterminant"]
            if abs(cayley_val) > 1e-5:
                ent_state = "GHZ-like (τ > 0)"
            elif any(b == 1 for b in bits):
                ent_state = "W-like (τ = 0)"
            else:
                ent_state = "Separable"

            self.symbolic_matrix.append({
                "N": N,
                "arithmetic": arith_sym,
                "dyadic_address": bit_str,
                "graph_avatar": f"G_{N}(V={n_dim}, E={n_edges})",
                "char_polynomial": char_poly_str,
                "dirichlet_seed": dirichlet_sym,
                "tensor_state": ent_state
            })

            arith = fp_master["arithmetic"]
            spec = fp_master["spectrum"]
            pspec = fp_master["post_spectrum"]
            ht = fp_master["hypertensor"]

            self.numeric_matrix.append({
                "N": N,
                "euler_totient": arith["euler_totient"],
                "num_divisors": arith["num_divisors"],
                "sum_divisors": arith["sum_divisors"],
                "spectral_radius": round(max(spec["adj_spectrum"]), 4),
                "fiedler_gap": round(spec["fiedler_gap"], 4),
                "spectral_energy": round(spec["spectral_energy"], 4),
                "chen_holonomy_norm": round(pspec["chen_holonomy_norm"], 4),
                "cayley_hyperdeterminant": round(ht["cayley_hyperdeterminant"], 4),
                "frobenius_norm": round(ht["frobenius_norm"], 4),
                "betti_1_cycles": pspec["betti_1_cycles"]
            })

    def get_symbolic_matrix(self) -> List[Dict[str, Any]]:
        return self.symbolic_matrix

    def get_numeric_matrix(self) -> List[Dict[str, Any]]:
        return self.numeric_matrix

    def get_smith_gcd_matrix_20(self) -> np.ndarray:
        S = np.zeros((self.max_n, self.max_n), dtype=int)
        for i in range(1, self.max_n + 1):
            for j in range(1, self.max_n + 1):
                S[i-1, j-1] = math.gcd(i, j)
        return S

    def get_coprimality_matrix_20(self) -> np.ndarray:
        C = np.zeros((self.max_n, self.max_n), dtype=int)
        for i in range(1, self.max_n + 1):
            for j in range(1, self.max_n + 1):
                C[i-1, j-1] = 1 if math.gcd(i, j) == 1 else 0
        return C

    def cesare_determinant(self) -> int:
        det = 1
        for row in self.numeric_matrix:
            det *= row["euler_totient"]
        return det
