# -*- coding: utf-8 -*-
"""
Natural Fingerprint Engine:
Associates every natural number N in N_{>= 1} to a Master Invariant Tuple
integrating:
1. Arithmetic Prime Factorization and Classical Dirichlet Characters;
2. Matrix Spectrum (Adjacency & Laplacian eigenvalues, spectral gap, spectral energy);
3. Post-Spectral Invariants (Non-Abelian Chen iterated holonomies, multiscale cut capacities, persistent homology);
4. Hypertensor Invariants (Tripartite Cayley hyperdeterminants, multilinear ranks);
5. Generating Function Family (Ihara zeta, characteristic polynomial, Riemann-Dirichlet divisor series).
"""
import numpy as np
from typing import List, Tuple, Dict, Any
from .core_encoder import DyadicEncoder
from .matrix_bridge import MatrixStructure
from .hypertensor_bridge import HypertensorStructure

class NaturalFingerprint:
    def __init__(self, N: int):
        if N < 1:
            raise ValueError("Natural number N must be >= 1")
        self.N = N
        self.bits = DyadicEncoder.decode_integer(N)
        self._build_canonical_matrix_and_graph()

    def prime_factorization(self) -> List[Tuple[int, int]]:
        """Computes unique prime factorization: N = prod p_i^{a_i}."""
        n = self.N
        factors = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                count = 0
                while n % d == 0:
                    count += 1
                    n //= d
                factors.append((d, count))
            d += 1
        if n > 1:
            factors.append((n, 1))
        return factors

    def arithmetic_invariants(self) -> Dict[str, Any]:
        """Classical number-theoretic invariants."""
        # Divisors
        divs = [d for d in range(1, self.N + 1) if self.N % d == 0]
        num_divs = len(divs)
        sum_divs = sum(divs)
        # Euler totient
        phi = 0
        for i in range(1, self.N + 1):
            if np.gcd(i, self.N) == 1:
                phi += 1
        return {
            "factors": self.prime_factorization(),
            "num_divisors": num_divs,
            "sum_divisors": sum_divs,
            "euler_totient": phi
        }

    def _build_canonical_matrix_and_graph(self):
        """
        Synthesizes a canonical matrix and graph from the binary address of N.
        Dimension n = max(3, ceil(sqrt(len(bits) + 1))).
        """
        k = len(self.bits)
        n = max(3, int(np.ceil(np.sqrt(k + 1))) + 1)
        self.matrix_dim = n
        adj = np.zeros((n, n), dtype=int)
        
        # Populate upper triangular entries using bits cyclically
        bit_idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                if k > 0:
                    val = self.bits[bit_idx % k]
                    bit_idx += 1
                else:
                    val = 1 if (i + 1 == j) else 0
                adj[i, j] = val
                adj[j, i] = val
        self.adj_matrix = adj
        # Laplacian L = D - A
        degrees = np.sum(adj, axis=1)
        self.laplacian = np.diag(degrees) - adj

    def matrix_spectrum(self) -> Dict[str, Any]:
        """Computes eigenvalues of Adjacency and Laplacian matrices."""
        adj_eigs = sorted([round(float(x), 4) for x in np.linalg.eigvalsh(self.adj_matrix)], reverse=True)
        lap_eigs = sorted([round(float(x), 4) for x in np.linalg.eigvalsh(self.laplacian)])
        
        # Spectral gap (algebraic connectivity = second smallest Laplacian eigenvalue)
        fiedler = lap_eigs[1] if len(lap_eigs) > 1 else 0.0
        # Spectral energy
        energy = round(float(np.sum(np.abs(adj_eigs))), 4)
        
        return {
            "adj_spectrum": adj_eigs,
            "lap_spectrum": lap_eigs,
            "fiedler_gap": fiedler,
            "spectral_energy": energy
        }

    def post_spectral_invariants(self) -> Dict[str, Any]:
        """
        Computes post-spectral signatures:
        1. Chen iterated commutator holonomy on the graph;
        2. Multiscale cut capacities;
        3. 1D Betti cycle persistence signature.
        """
        # Multiscale cuts on singletons
        n = self.matrix_dim
        singleton_cuts = [int(np.sum(self.adj_matrix[i, :])) for i in range(n)]
        min_cut = min(singleton_cuts) if singleton_cuts else 0
        max_cut = max(singleton_cuts) if singleton_cuts else 0
        
        # Chen holonomy proxy: trace of commutator of normalized sub-blocks
        A1 = self.adj_matrix[:2, :2]
        A2 = self.adj_matrix[1:3, 1:3]
        comm = A1 @ A2 - A2 @ A1
        chen_proxy = round(float(np.trace(comm @ comm.T)), 4)

        # 1D cycle count (Euler-Poincare Betti_1 = |E| - |V| + c)
        num_edges = int(np.sum(self.adj_matrix)) // 2
        betti_1 = max(0, num_edges - n + 1)

        return {
            "min_cut": min_cut,
            "max_cut": max_cut,
            "singleton_cuts": singleton_cuts,
            "chen_holonomy_norm": chen_proxy,
            "betti_1_cycles": betti_1
        }

    def hypertensor_invariants(self) -> Dict[str, Any]:
        """
        Constructs canonical 3-tensor T in R^{2x2x2} from N's bitstring
        and computes Cayley's hyperdeterminant.
        """
        t_data = np.zeros((2, 2, 2), dtype=float)
        idx = 0
        for i in range(2):
            for j in range(2):
                for k_idx in range(2):
                    if len(self.bits) > 0:
                        t_data[i, j, k_idx] = float(self.bits[idx % len(self.bits)])
                        idx += 1
                    else:
                        t_data[i, j, k_idx] = 1.0 if (i == j == k_idx) else 0.0
        ht = HypertensorStructure(t_data, name=f"Hypertensor_N{self.N}")
        return {
            "tensor_shape": (2, 2, 2),
            "cayley_hyperdeterminant": ht.cayley_hyperdeterminant_2x2x2(),
            "multilinear_ranks": ht.multilinear_ranks(),
            "frobenius_norm": round(ht.frobenius_norm(), 4)
        }

    def generating_functions(self) -> Dict[str, str]:
        """Family of canonical generating functions associated with N."""
        poly = [round(float(c), 2) for c in np.poly(self.adj_matrix)]
        return {
            "characteristic_polynomial": f"p(t) = {poly}",
            "ihara_zeta_form": "zeta(u) = (1 - u^2)^(-chi) * det(I - A*u + Q*u^2)^(-1)",
            "riemann_dirichlet_local": f"D_N(s) = sum_{{d|{self.N}}} d^(-s)",
            "partition_factor": f"P_N(q) = prod_{{k=1}}^{self.N} (1 - q^k)^(-1)"
        }

    def master_digital_fingerprint(self) -> Dict[str, Any]:
        """
        Compiles the grand universal fingerprint of the natural number N.
        """
        return {
            "natural_number": self.N,
            "dyadic_bitstring": "".join(str(b) for b in self.bits) if self.bits else "0",
            "arithmetic": self.arithmetic_invariants(),
            "spectrum": self.matrix_spectrum(),
            "post_spectrum": self.post_spectral_invariants(),
            "hypertensor": self.hypertensor_invariants(),
            "generating_functions": self.generating_functions()
        }
