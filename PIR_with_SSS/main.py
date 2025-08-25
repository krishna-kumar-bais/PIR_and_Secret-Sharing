import numpy as np
import random
from multiprocessing import Pool
import argparse

from make_query_shares import make_queries
from server import server_compute
from reconstructs import client_reconstruct

def generate_database(DB_SIZE,DB_FILE):
    db = []
    for j in range(0,DB_SIZE):
        db.append(random.randint(0, 10_000_000))
    np.save(DB_FILE, db)
    print("Database saved to", DB_FILE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--DB_SIZE", type=int, default=10_000, help="Database size")
    parser.add_argument("--SERVERS", type=int, default=4, help="Number of servers")
    parser.add_argument("--t", type=int, default=2, help="Threshold value")
    parser.add_argument("--k", type=int, default=0, help="Index client wants")
    parser.add_argument("--DB_FILE", type=str, default="database.npy", help="Database file name")
    args = parser.parse_args()

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
    queries = make_queries(N, args.SERVERS, args.k, args.t)

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
    result = client_reconstruct(used_responses, used_x)

    # show output
    print("\nQueried index:", args.k)
    print("Database value:", db[args.k])
    print("Reconstructed :", result,"\n")

# run
if __name__ == "__main__":
    main()
