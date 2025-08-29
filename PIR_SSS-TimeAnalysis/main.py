# main.py
import numpy as np
import random
from multiprocessing import Pool
import argparse
import time

from make_query_shares import make_queries
from server import server_compute
from reconstructs import client_reconstruct

def generate_database(DB_SIZE,DB_FILE):
    db = []
    for j in range(0,DB_SIZE):
        db.append(random.randint(0, 10_000_000))
    np.save(DB_FILE, db)
    print("\nDatabase saved to", DB_FILE)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--DB_SIZE", type=int, default=1000)
    parser.add_argument("--SERVERS", type=int, default=4)
    parser.add_argument("--t", type=int, default=2)
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--DB_FILE", type=str, default="database.npy")
    args = parser.parse_args(argv)

    # create db 
    generate_database(args.DB_SIZE, args.DB_FILE)
    db = np.load(args.DB_FILE, allow_pickle=True).tolist()
    N = len(db)
    
    # --- essential input checking ---
    if not (1 <= args.t <= args.SERVERS - 1):
        raise SystemExit(f"Invalid --t {args.t}. Must be in [1, {args.SERVERS-1}] for SERVERS={args.SERVERS}.")
    if args.SERVERS < 2:
        raise SystemExit("Invalid --SERVERS. Must be at least 2.")
    if not (0 <= args.k < N):
        raise SystemExit(f"Invalid --k {args.k}. Must be in [0, {N-1}] for DB size {N}.")

    # build Shamir-based query shares
    start_query = time.time()
    queries = make_queries(N, args.SERVERS, args.k, args.t)
    end_query = time.time()
    Query_creation_time = round((end_query - start_query) * 1000, 3)
    print(f"Query creation time: {Query_creation_time} ms")

    # servers compute responses in parallel
    with Pool(args.SERVERS) as pool:
        responses = pool.map(server_compute, [(queries[s], db) for s in range(0,args.SERVERS)])

    # choose any t+1 server responses for reconstruction (here: first t+1)
    used_x = []
    used_responses = [] 
    for i in range(0, args.t+1):
        used_x.append(i+1)
        used_responses.append(responses[i])

    # client reconstructs result
    start_query = time.time()
    result = client_reconstruct(used_responses, used_x)
    end_query = time.time()
    Reconstruction_time = round((end_query - start_query) * 1000, 3)
    print(f"Reconstruction time: {Reconstruction_time} ms")

    # show output
    print("Queried index:", args.k)
    print("Database value:", db[args.k])
    print("Reconstructed :", result,"\n")
        
    return Query_creation_time, Reconstruction_time, queries

# run
if __name__ == "__main__":
    main()
