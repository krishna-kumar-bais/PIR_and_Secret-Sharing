import random
from GenerateShare import GenerateShare   # SSS Share Generater

MOD = 2**61 - 1
def make_queries(n, servers, k,t):  # k = index client wants
    
    # initialize query vectors for each server with 0
    queries = []
    for i in range(0,servers):
        queries.append([0] * n) 

    for j in range(0,n):
        if j == k:
            secret = 1 
        else :
            secret = 0
        
        shares = GenerateShare(secret, t, servers, MOD)

        # shares is list of (x,y) tuples in order x=1..servers
        for idx in range(0, servers):
            queries[idx][j] = shares[idx][1] % MOD

    return queries