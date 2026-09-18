from typing import List, Dict, Any, Tuple
import math

class DyadicEncoder:
    @staticmethod
    def encode_binary_path(bits: List[int]) -> int:
        acc = 1
        for b in bits:
            acc = (acc << 1) | (1 if b else 0)
        return acc

    @staticmethod
    def decode_integer(n: int) -> List[int]:
        if n <= 0:
            raise ValueError("Dyadic arithmetization requires n >= 1")
        if n == 1:
            return []
        b_str = bin(n)[3:]
        return [int(c) for c in b_str]

class AdaptiveInvariantSieve:
    def __init__(self):
        self.leaves: Dict[int, Any] = {}

    def build_sieve(self, objects: List[Tuple[str, Any]], extractor_fn) -> Dict[str, int]:
        sorted_objs = sorted(objects, key=lambda x: extractor_fn(x[1]))
        result = {}
        n = len(sorted_objs)
        if n == 0:
            return result
        if n == 1:
            result[sorted_objs[0][0]] = 1
            return result

        depth = max(1, math.ceil(math.log2(n)))
        for idx, (oid, obj) in enumerate(sorted_objs):
            b_format = f"{idx:0{depth}b}"
            bits = [int(c) for c in b_format]
            val = DyadicEncoder.encode_binary_path(bits)
            result[oid] = val
        return result
