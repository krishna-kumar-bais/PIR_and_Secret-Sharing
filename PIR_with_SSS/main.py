import numpy as np
from multiprocessing import Pool

from make_query_shares import make_queries
from server import server_compute
from reconstructs import client_reconstruct

def main():
    DB_FILE = "database.npy"
    db = np.load(DB_FILE, allow_pickle=True).tolist()   # load and convert to Python list (no numpy int64)

    MOD = 2**61 - 1
    N = len(db)
    t = 2 # threshold (1,2...,SERVERS-1)
    SERVERS = 4
    k = 1134  # index client wants

    # build Shamir-based query shares
    queries = make_queries(N, SERVERS, k, t)

    # servers compute responses in parallel
    with Pool(SERVERS) as pool:
        responses = pool.map(server_compute, [(queries[s], db) for s in range(0,SERVERS)])

    # choose any t+1 server responses for reconstruction (here: first t+1)
    used_x = []
    used_responses = [] 
    for i in range(0, t+1):
        used_x.append(i+1)
        used_responses.append(responses[i])

    # client reconstructs result
    result = client_reconstruct(used_responses, used_x)

    # show output
    print("\nQueried index:", k)
    print("Database value:", db[k])
    print("Reconstructed :", result,"\n")

# run
if __name__ == "__main__":
    main()
