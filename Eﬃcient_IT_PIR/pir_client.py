import math
import os
import sys
from typing import List, Optional, Tuple


from GenerateDPF import GenerateDPF, DPFKey  


def _is_power_of_two(x: int) -> bool:
    return x >= 1 and (x & (x - 1)) == 0


def _bits_lsb_first(value: int, num_bits: int) -> List[int]:
    return [(value >> i) & 1 for i in range(num_bits)]


class PIRClient:
    def __init__(self, num_records: int, record_size: int, prime: int,
                 num_servers: int):
        if num_records < 2:
            raise ValueError("PIR needs at least 2 records.")
        if not _is_power_of_two(num_servers) or num_servers < 2:
            raise ValueError("num_servers must be a power of two and >= 2.")
        self.N = num_records
        self.L = record_size
        self.p = prime
        self.ell = num_servers
        self.d = int(round(math.log2(num_servers)))   # number of DPF levels
        self.n_bits = max(1, math.ceil(math.log2(num_records)))

        self._last_query_index: int = -1   # only for diagnostics

    # ------------------------------------------------------------------
    #  client builds queries
    # ------------------------------------------------------------------
    def generate_query(self, index: int) -> List[List[DPFKey]]:
        if not (0 <= index < self.N):
            raise IndexError(f"index {index} out of range [0, {self.N})")
        self._last_query_index = index

        # Generate d independent DPF key pairs, all for the SAME j.
        level_pairs: List[Tuple[DPFKey, DPFKey]] = []
        for _ in range(self.d):
            k0, k1 = GenerateDPF(index, 1, self.n_bits, self.p)
            level_pairs.append((k0, k1))

        # Assign keys to each server by its binary label.
        server_keys: List[List[DPFKey]] = []
        for b in range(self.ell):
            b_bits = _bits_lsb_first(b, self.d)
            keys_for_b = [level_pairs[i][b_bits[i]] for i in range(self.d)]
            server_keys.append(keys_for_b)
        return server_keys

    # ------------------------------------------------------------------
    #  client reconstructs from the (partial) responses
    # ------------------------------------------------------------------
    def reconstruct(self,
                    responses: List[Optional[List[List[int]]]],
                    responded: Optional[List[int]] = None) -> List[int]:
        if responded is None:
            responded = [b for b, r in enumerate(responses) if r is not None]
        if len(responded) < 2:
            raise RuntimeError("Need at least 2 responding servers to reconstruct.")

        # Find any pair (b, b') of responders that differ in some bit.
        for idx_a in range(len(responded)):
            for idx_b in range(idx_a + 1, len(responded)):
                b = responded[idx_a]
                b_prime = responded[idx_b]
                xor = b ^ b_prime
                if xor == 0:
                    continue
                # Lowest differing bit i.
                i = (xor & -xor).bit_length() - 1
                ans_b   = responses[b][i]
                ans_bp  = responses[b_prime][i]
                if len(ans_b) != self.L or len(ans_bp) != self.L:
                    raise ValueError("server answer has wrong length")
                return [(a + c) % self.p for a, c in zip(ans_b, ans_bp)]

        raise RuntimeError("No two responding servers have differing labels "
                           "(should be impossible for distinct indices).")
