import sys
sys.path.insert(0, '/Users/krishna/Desktop/PIR_DPF')

from PIR_DPF.GenerateDPF import GenerateDPF

MOD = 2**61 - 1

def make_query_shares_dpf(n, k):

    if not (0 <= k < n):
        raise ValueError(f"Invalid k={k}. Must be in [0, {n-1}]")
    
    # Determine number of bits needed to represent positions
    nbits = n.bit_length()
    
    # Generate DPF keys for alpha=k, beta=1
    # This creates keys where DPF(k0, k) + DPF(k1, k) = 1
    # and DPF(k0, j) + DPF(k1, j) = 0 for j != k
    alpha = k
    beta = 1
    
    k0, k1 = GenerateDPF(alpha, beta, nbits, MOD)
    
    return k0, k1
