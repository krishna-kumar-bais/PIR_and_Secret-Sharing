MOD = 2**61 - 1
def server_compute(args):
    query, db = args
    total = 0
    for j in range(0, len(db)):
        total = (total + query[j] * db[j]) % MOD
    return total
