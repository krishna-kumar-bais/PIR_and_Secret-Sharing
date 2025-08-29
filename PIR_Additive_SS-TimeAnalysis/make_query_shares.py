import random

MOD = 2**61 - 1
def make_queries(n, servers, k):  # k = index client wants
    queries = []
    # random queries for first (servers-1)
    for s in range(0, servers-1):
        q = []
        for j in range(0, n):
            q.append(random.randint(0, MOD-1))
        queries.append(q)
    # compute last query so sums = unit vector
    q_last = []
    for j in range(0, n):
        ssum = 0
        for s in range(0, servers-1):
            ssum = (ssum + queries[s][j]) % MOD
        if j == k:
            q_last.append((1 - ssum) % MOD)
        else:
            q_last.append((-ssum) % MOD)
    queries.append(q_last)
    return queries
