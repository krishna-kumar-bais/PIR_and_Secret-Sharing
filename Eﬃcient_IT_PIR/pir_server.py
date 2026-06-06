import os
import sys
from typing import List, Sequence

from database import Database
from GenerateDPF import DPFKey  
from EvalDPF import EvaluateDPF  


def eval_full(key: DPFKey, n_bits: int, prime: int) -> List[int]:
    return [EvaluateDPF(key, x, n_bits, prime) for x in range(1 << n_bits)]


class PIRServer:
    def __init__(self, server_id: int, db: Database, prime: int, n_bits: int):
        if not db:
            raise ValueError("database is empty")
        self.server_id = server_id
        self.db = db
        self.p = prime
        self.n_bits = n_bits
        self.N = len(db)
        self.L = len(db[0])
        if any(len(r) != self.L for r in db):
            raise ValueError("all records must have the same length")

    def _inner_product(self, share_vec: List[int]) -> List[int]:
        p = self.p
        L = self.L
        out = [0] * L
        for i in range(self.N):
            si = share_vec[i]
            if si == 0:
                continue
            row: Sequence[int] = self.db[i]
            for l in range(L):
                out[l] = (out[l] + si * row[l]) % p
        return out

    def answer(self, keys: List[DPFKey]) -> List[List[int]]:
        out: List[List[int]] = []
        for k in keys:
            shares = eval_full(k, self.n_bits, self.p)
            out.append(self._inner_product(shares))
        return out
