import numpy as np
from multiprocessing import Pool

from make_query_shares import make_queries
from server import server_compute
from reconstructs import client_reconstruct

def main():
    DB_FILE = "database.npy"
    db = np.load(DB_FILE, allow_pickle=True).tolist()   # load and convert to Python list (no numpy int64)

    N = len(db)
    SERVERS = 4
    k = 1551  # index client wants

    # make query shares
    queries = make_queries(N, SERVERS, k)

    # servers compute responses in parallel
    with Pool(SERVERS) as pool:
        responses = pool.map(server_compute, [(queries[s], db) for s in range(0,SERVERS)])

    # client reconstructs result
    result = client_reconstruct(responses)

    # show output
    print("\nQueried index:", k)
    print("Database value:", db[k])
    print("Reconstructed :", result,"\n")

# run
if __name__ == "__main__":
    main()
