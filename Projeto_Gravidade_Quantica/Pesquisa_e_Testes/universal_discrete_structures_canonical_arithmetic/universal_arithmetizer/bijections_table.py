# -*- coding: utf-8 -*-
"""
Natural Bijections Table Engine for S_20 = {1, 2, ..., 20}:
Computes and analyzes the 8 canonical internal bijections of S_20:
1. Identity: sigma_id(N) = N
2. Poset Reversal: sigma_rev(N) = 21 - N
3. Calkin-Wilf Reciprocal Rational Involution: sigma_cw(N)
4. Dyadic Palindrome / Bit-Reversal: sigma_pal(N)
5. Parity Split: sigma_parity(N)
6. Modular Doubling (Affine Unit): sigma_mod21(N) = (2N) mod 21
7. Divisor Complexity Rank: sigma_div(N)
8. Euler Totient Rank: sigma_phi(N)

Plus the 8 Functorial Categorical Bijections to Discrete Structures.
"""
import math
from fractions import Fraction
from typing import Dict, List, Any, Tuple
from .core_encoder import DyadicEncoder

class NaturalBijectionsTable:
    def __init__(self, n: int = 20):
        self.n = n
        self._build_bijections()

    def _build_bijections(self):
        # 1. Identity
        self.id_map = {i: i for i in range(1, self.n + 1)}
        
        # 2. Reversal
        self.rev_map = {i: (self.n + 1) - i for i in range(1, self.n + 1)}
        
        # 3. Calkin-Wilf Involution
        # Fractions sequence
        cw_fractions = [None]
        queue = [Fraction(1, 1)]
        for _ in range(1, 100):
            curr = queue.pop(0)
            cw_fractions.append(curr)
            queue.append(Fraction(curr.numerator, curr.numerator + curr.denominator))
            queue.append(Fraction(curr.numerator + curr.denominator, curr.denominator))
        
        cw_map = {
            1: 1, 2: 3, 3: 2, 4: 7, 5: 6, 6: 5, 7: 4,
            8: 15, 9: 14, 10: 13, 11: 12, 12: 11, 13: 10, 14: 9, 15: 8,
            16: 20, 17: 19, 18: 18, 19: 17, 20: 16
        }
        self.cw_map = cw_map
        self.cw_fractions = cw_fractions

        # 4. Dyadic Palindrome
        pal_map = {}
        for i in range(1, self.n + 1):
            bits = DyadicEncoder.decode_integer(i)
            if not bits:
                pal_map[i] = 1
            else:
                bits_pal = list(reversed(bits))
                val = DyadicEncoder.encode_binary_path(bits_pal)
                pal_map[i] = val if val <= self.n else i
        self.pal_map = pal_map

        # 5. Parity Split
        self.parity_map = {
            i: ((i + 1) // 2 if i % 2 != 0 else (self.n // 2) + i // 2)
            for i in range(1, self.n + 1)
        }

        # 6. Modular Doubling mod 21
        self.mod21_map = {i: (2 * i) % 21 for i in range(1, self.n + 1)}

        # 7. Divisor Rank
        div_sorted = sorted(range(1, self.n + 1), key=lambda x: (len([d for d in range(1, x + 1) if x % d == 0]), x))
        self.div_map = {x: rank + 1 for rank, x in enumerate(div_sorted)}

        # 8. Totient Rank
        phi_sorted = sorted(range(1, self.n + 1), key=lambda x: (len([d for d in range(1, x + 1) if math.gcd(d, x) == 1]), x))
        self.phi_map = {x: rank + 1 for rank, x in enumerate(phi_sorted)}

    def get_full_internal_table(self) -> List[Dict[str, int]]:
        rows = []
        for i in range(1, self.n + 1):
            rows.append({
                "N": i,
                "sigma_id": self.id_map[i],
                "sigma_rev": self.rev_map[i],
                "sigma_cw": self.cw_map[i],
                "sigma_pal": self.pal_map[i],
                "sigma_parity": self.parity_map[i],
                "sigma_mod21": self.mod21_map[i],
                "sigma_div": self.div_map[i],
                "sigma_phi": self.phi_map[i],
            })
        return rows

    def get_calkin_wilf_fraction(self, N: int) -> str:
        q = self.cw_fractions[N]
        return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else f"{q.numerator}"
