import sys
sys.path.insert(0, '/Users/krishna/Desktop/PIR_DPF')
sys.path.insert(0, '/Users/krishna/Desktop/PIR_DPF/PIR_DPF')

import argparse
import numpy as np
import random
import statistics
from main import generate_database, main as pir_dpf_main

def run_multiple(DB_SIZES, k=0, DB_FILE="database_dpf.npy", runs=1):
    results = {}
    
    for db_size in DB_SIZES:
        print(f"\n=== Running for DB_SIZE = {db_size} === ")        
        times_query = []
        times_server = []
        times_recon = []
        all_correct = True
        
        for run in range(runs):
            if run == 0:
                # Generate fresh database for each size
                generate_database(db_size, DB_FILE)
            
            print(f"\nRun {run + 1}/{runs}:")
            
            # Run single PIR_DPF test (2-server pure DPF)
            result = pir_dpf_main([
                '--DB_SIZE', str(db_size),
                '--k', str(k),
                '--DB_FILE', DB_FILE
            ])
            
            times_query.append(result['query_gen_time'] + result['server_time'])  # Total query/computation time
            times_server.append(result['server_time'])
            times_recon.append(result['recon_time'])
            
            if result['result'] != result['expected']:
                all_correct = False
        
        # Compute statistics
        results[db_size] = {
            'query_gen': {
                'avg': statistics.mean(times_query),
                'stdev': statistics.stdev(times_query) if runs > 1 else 0,
                'min': min(times_query),
                'max': max(times_query),
            },
            'server': {
                'avg': statistics.mean(times_server),
                'stdev': statistics.stdev(times_server) if runs > 1 else 0,
                'min': min(times_server),
                'max': max(times_server),
            },
            'recon': {
                'avg': statistics.mean(times_recon),
                'stdev': statistics.stdev(times_recon) if runs > 1 else 0,
                'min': min(times_recon),
                'max': max(times_recon),
            },
            # 'all_correct': all_correct,
        }
        
        # Print statistics for this DB_SIZE
        print(f"\nAverage Query creation time: {statistics.mean(times_query):.3f} ms")
        print(f"Average Reconstruction time: {statistics.mean(times_recon):.3f} ms")
        
        if runs > 1:
            std_query = statistics.stdev(times_query)
            std_recon = statistics.stdev(times_recon)
        else:
            std_query = 0
            std_recon = 0
        
        print(f"\nStandard Deviation (Query creation): {std_query:.3f} ms")
        print(f"Standard Deviation (Reconstruction): {std_recon:.3f} ms")
        # Bandwidth: DPF key size (typically 32 bytes per key) * 2 servers, converted to KB
        dpf_key_size_bytes = 64 * 2  # 2 keys, 32 bytes each
        bandwidth_kb = (dpf_key_size_bytes * db_size) / 1024
        print(f"Bandwidth sent to servers: {bandwidth_kb:.2f} KB")
        print(f"{'='*51}")
    

    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PIR_DPF with multiple database sizes (Pure 2-Server)")
    parser.add_argument("--DB_SIZES", nargs='+', type=int, required=True, help="List of database sizes")
    parser.add_argument("--k", type=int, default=0, help="Query index")
    parser.add_argument("--DB_FILE", type=str, default="database_dpf.npy", help="Database file")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs per size")
    
    args = parser.parse_args()
    
    run_multiple(
        DB_SIZES=args.DB_SIZES,
        k=args.k,
        DB_FILE=args.DB_FILE,
        runs=args.runs
    )
