# reconstructs.py
from ReconstructSecret import ReconstructSecret  # your SSS reconstruction
MOD = 2**61 - 1

def client_reconstruct(responses, used_x):
    # Build list of (x,y) tuples expected by ReconstructSecret
    shares = []
    for i in range(0,len(responses)):
        x = used_x[i]
        y = int(responses[i]) % MOD
        shares.append((x, y))

    secret = ReconstructSecret(shares, MOD)
    return int(secret) % MOD
