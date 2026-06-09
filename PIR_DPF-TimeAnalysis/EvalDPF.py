# DPF/EvalDPF.py
from GenerateDPF import DPFKey, prg
import hashlib

def convert(seed: bytes, prime: int) -> int:
    return int.from_bytes(hashlib.sha256(seed).digest(), 'big') % prime

def EvaluateDPF(key: DPFKey, x: int, n: int, prime: int) -> int:
    seed = key.root_seed
    t = key.root_t
    bits = [(x >> i) & 1 for i in range(n-1, -1, -1)]

    for i, xi in enumerate(bits, start=1):
        out = prg(seed, 2*(len(seed)+1))
        sL = out[:len(seed)]; tL = out[len(seed)] & 1
        sR = out[len(seed)+1:2*len(seed)+1]; tR = out[-1] & 1

        # Apply correction if t==1
        if t == 1:
            sCW, tLCW, tRCW = key.cws[i-1]
            cw_bytes = sCW + bytes([tLCW]) + sCW + bytes([tRCW])
            out = bytes(a ^ b for a,b in zip(out, cw_bytes))
            sL = out[:len(seed)]; tL = out[len(seed)] & 1
            sR = out[len(seed)+1:2*len(seed)+1]; tR = out[-1] & 1

        # Move down the tree
        if xi == 0:
            seed, t = sL, tL
        else:
            seed, t = sR, tR

    # Final share reconstruction
    val = (convert(seed, prime) + t * key.cw_last) % prime
    return (-val if key.party == 1 else val) % prime
