MOD = 2**61 - 1
def client_reconstruct_dpf(responses):
    # Pure DPF: sum the two responses
    result = (responses[0] + responses[1]) % MOD
    return result
