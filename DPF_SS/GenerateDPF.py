# DPF/GenerateDPF.py
import secrets, hashlib
from typing import Tuple
from dataclasses import dataclass

def prg(seed: bytes, out_len: int) -> bytes:
    out = b''; counter = 0
    while len(out) < out_len:
        out += hashlib.sha256(seed + counter.to_bytes(4,'big')).digest()
        counter += 1
    return out[:out_len]

def to_bits(x: int, n: int):
    return [(x >> i) & 1 for i in range(n-1, -1, -1)]

@dataclass
class DPFKey:
    party: int
    root_seed: bytes
    root_t: int
    cws: list       # list of (sCW, tLCW, tRCW) for each level
    cw_last: int

def GenerateDPF(alpha: int, beta: int, n: int, prime: int, seed_len: int = 16) -> Tuple[DPFKey, DPFKey]:
    # Random initial seeds and tag bits (root state)
    s0 = secrets.token_bytes(seed_len)
    s1 = secrets.token_bytes(seed_len)
    t0 = secrets.randbits(1)
    t1 = t0 ^ 1
    # Save root state for keys【12†L695-L702】
    s0_root, s1_root = s0, s1
    t0_root, t1_root = t0, t1

    alpha_bits = to_bits(alpha, n)
    cws = []
    for bit in alpha_bits:
        # Expand each seed by PRG
        out0 = prg(s0, 2*(seed_len+1))
        out1 = prg(s1, 2*(seed_len+1))
        # Parse PRG output
        sL0, tL0 = out0[:seed_len],  out0[seed_len] & 1
        sR0, tR0 = out0[seed_len+1:2*seed_len+1], out0[-1] & 1
        sL1, tL1 = out1[:seed_len],  out1[seed_len] & 1
        sR1, tR1 = out1[seed_len+1:2*seed_len+1], out1[-1] & 1

        # Decide which branch is "keep" vs "lose"
        if bit == 0:
            sKeep0, tKeep0, sLose0, _ = sL0, tL0, sR0, tR0
            sKeep1, tKeep1, sLose1, _ = sL1, tL1, sR1, tR1
            # For bit=0 (keep left), tKeepCW = tL^CW
            tKeepCW = (tL0 ^ tL1 ^ 1) & 1
        else:
            sKeep0, tKeep0, sLose0, _ = sR0, tR0, sL0, tL0
            sKeep1, tKeep1, sLose1, _ = sR1, tR1, sL1, tL1
            # For bit=1 (keep right), tKeepCW = tR^CW
            tKeepCW = (tR0 ^ tR1 ^ 1) & 1

        # Compute correction words (as in Figure 1)【12†L650-L658】
        sCW = bytes(a ^ b for a,b in zip(sLose0, sLose1))
        tLCW = (tL0 ^ tL1 ^ bit ^ 1) & 1
        tRCW = (tR0 ^ tR1 ^ bit) & 1
        cws.append((sCW, tLCW, tRCW))

        # Update seeds depending on tag bits
        if t0 == 1:
            s0 = bytes(a ^ b for a,b in zip(sKeep0, sCW))
        else:
            s0 = sKeep0
        if t1 == 1:
            s1 = bytes(a ^ b for a,b in zip(sKeep1, sCW))
        else:
            s1 = sKeep1

        t0 = (tKeep0 ^ (t0 & tKeepCW)) & 1
        t1 = (tKeep1 ^ (t1 & tKeepCW)) & 1

    # Final correction word for β (as in Figure 1)【12†L681-L689】
    def convert(seed: bytes) -> int:
        return int.from_bytes(hashlib.sha256(seed).digest(), 'big') % prime
    output_cw = ((-1)**t1) * ((beta - convert(s0) + convert(s1)) % prime) % prime

    # Build keys with ROOT seeds (not final ones)【12†L695-L702】
    k0 = DPFKey(0, s0_root, t0_root, cws.copy(), output_cw)
    k1 = DPFKey(1, s1_root, t1_root, cws.copy(), output_cw)
    return k0, k1
