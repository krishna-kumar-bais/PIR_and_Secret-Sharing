MOD = 2**61 - 1
def client_reconstruct(responses):
    total = 0
    for r in range(0, len(responses)):
        total = (total + responses[r]) % MOD
    return total
