
import sys
import numpy as np
import random
import argparse
import time
from multiprocessing import Pool

from make_query_shares_dpf import make_query_shares_dpf
from server_dpf import server_compute_dpf
from reconstructs_dpf import client_reconstruct_dpf

MOD = 2**61 - 1

def generate_database(DB_SIZE, DB_FILE):
    """Generate random database and save to file."""
    db = [random.randint(0, 10_000_000) for j in range(DB_SIZE)]
    np.save(DB_FILE, db)
    print(f"\nDatabase saved to {DB_FILE}")
    return db

def main(argv=None):
    parser = argparse.ArgumentParser(description="PIR-DPF: Pure 2-Server Distributed Point Function")
    parser.add_argument("--DB_SIZE", type=int, default=10000, help="Database size")
    parser.add_argument("--k", type=int, default=0, help="Index to query")
    parser.add_argument("--DB_FILE", type=str, default="database_dpf.npy", help="Database file")
    args = parser.parse_args(argv)
    
    # Generate or load database
    if not np.any(np.load(args.DB_FILE, allow_pickle=True) if __name__ != "__main__" else False):
        db = generate_database(args.DB_SIZE, args.DB_FILE)
    else:
        db = np.load(args.DB_FILE, allow_pickle=True).tolist()
    
    N = len(db)
    if not (0 <= args.k < N):
        raise SystemExit(f"Invalid --k {args.k}. Must be in [0, {N-1}] for DB size {N}.")

    print(f"Database size: {N}")
    print(f"Query index (k): {args.k}")
    print(f"Database value at k: {db[args.k]}")

    # ==================== QUERY PHASE ====================
    start_query = time.time()
    k0, k1 = make_query_shares_dpf(N, args.k)
    end_query = time.time()
    Query_generation_time = round((end_query - start_query) * 1000, 3)

    # ==================== SERVER COMPUTATION ====================
    start_server = time.time()
    with Pool(2) as pool:
        dpf_responses = pool.map(server_compute_dpf, [(k0, db), (k1, db)])
    end_server = time.time()
    Server_computation_time = round((end_server - start_server) * 1000, 3)
    print(f"DPF Response 0: {dpf_responses[0]}")
    print(f"DPF Response 1: {dpf_responses[1]}")

    # ==================== CLIENT RECONSTRUCTION ====================
    used_server_responses = dpf_responses

    start_recon = time.time()
    result = client_reconstruct_dpf(used_server_responses)
    end_recon = time.time()
    Reconstruction_time = round((end_recon - start_recon) * 1000, 3)
    print(f"Reconstructed value:   {result}")

    # ==================== TIMING SUMMARY ====================

    print(f"\nTiming Summary (ms)")
    print(f"DPF Key Generation:    {Query_generation_time} ms")
    print(f"Server Computation:    {Server_computation_time} ms")
    print(f"Reconstruction:        {Reconstruction_time} ms")
    total_time = Query_generation_time + Server_computation_time + Reconstruction_time
    print(f"Total Time:            {total_time} ms")

    return {
        'query_gen_time': Query_generation_time,
        'server_time': Server_computation_time,
        'recon_time': Reconstruction_time,
        'result': result,
        'expected': db[args.k]
    }

if __name__ == "__main__":
    main()
