
import sys
sys.path.insert(0, '/Users/krishna/Desktop/PIR_DPF')

from PIR_DPF.EvalDPF import EvaluateDPF

MOD = 2**61 - 1

def server_compute_dpf(args):
    dpf_key, db = args
    
    n = len(db)
    nbits = n.bit_length()
    
    total = 0
    for j in range(n):
        # Evaluate DPF at position j
        eval_val = EvaluateDPF(dpf_key, j, nbits, MOD)
        # Multiply by database value and accumulate
        total = (total + eval_val * db[j]) % MOD
    
    return total
