# python3 main.py --DB_SIZE 2000 --SERVERS 11 --k 4
import numpy as np
import random
import argparse
from multiprocessing import Pool

from make_query_shares import make_queries
from server import server_compute
from reconstructs import client_reconstruct

def generate_database(DB_SIZE,DB_FILE):
    db = []
    for j in range(0,DB_SIZE):
        db.append(random.randint(0, 10_000_000))
    np.save(DB_FILE, db)
    print("\nDatabase saved to", DB_FILE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--DB_SIZE", type=int, default=10_000)
    parser.add_argument("--SERVERS", type=int, default=4) # No. of servers
    parser.add_argument("--k", type=int, default=0) # Index that data user wants
    parser.add_argument("--DB_FILE", type=str, default="database.npy")
    args = parser.parse_args() 

    # create db 
    generate_database(args.DB_SIZE, args.DB_FILE)
    db = np.load(args.DB_FILE, allow_pickle=True).tolist()
    N = len(db) # length of Database

    # --- essential input checking ---
    if args.SERVERS < 1:
        raise SystemExit("Invalid --SERVERS. Must be at least 1.")
    if not (0 <= args.k < N):
        raise SystemExit(f"Invalid --k {args.k}. Must be in [0, {N-1}] for DB size {N}.")

    # make query shares
    queries = make_queries(args.DB_SIZE, args.SERVERS, args.k)

    # servers compute responses in parallel
    with Pool(args.SERVERS) as pool:
        responses = pool.map(server_compute, [(queries[s], db) for s in range(0,args.SERVERS)])

    # client reconstructs result
    result = client_reconstruct(responses)

    # show output
    print("Queried index:", args.k)
    print("Database value:", db[args.k])
    print("Reconstructed :", result,"\n")

# run
if __name__ == "__main__":
    main()
