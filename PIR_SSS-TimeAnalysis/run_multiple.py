import argparse
import sys
from main import main   # import main() from main.py

def run_multiple():
    parser = argparse.ArgumentParser()
    parser.add_argument("--DB_SIZES", type=int, nargs="+", required=True)
    parser.add_argument("--SERVERS", type=int, default=3)
    parser.add_argument("--t", type=int, default=2)
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--DB_FILE", type=str, default="database.npy")
    parser.add_argument("--runs", type=int, default=1)
    args = parser.parse_args()

    for size in args.DB_SIZES:
        q_times, r_times, bandwidths = [], [], []
        print(f"\n=== Running for DB_SIZE={size} ===")
        for _ in range(args.runs):
            q_time, r_time, queries = main([
                "--DB_SIZE", str(size),
                "--SERVERS", str(args.SERVERS),
                "--t", str(args.t),
                "--k", str(args.k),
                "--DB_FILE", args.DB_FILE
            ])
            q_times.append(q_time)
            r_times.append(r_time)
        avg_q = sum(q_times) / len(q_times)
        avg_r = sum(r_times) / len(r_times)
        print(f"\nAverage Query creation time: {avg_q:.3f} ms")
        print(f"Average Reconstruction time: {avg_r:.3f} ms")

        # bandwidth (same across runs → just use first queries)
        bandwidth_bytes = sum(sys.getsizeof(q) for q in queries)

        # --- standard deviations ---
        std_q = (sum((x - avg_q) ** 2 for x in q_times) / len(q_times)) ** 0.5
        std_r = (sum((x - avg_r) ** 2 for x in r_times) / len(r_times)) ** 0.5
        print(f"\nStandard Deviation (Query creation): {std_q:.3f} ms")
        print(f"Standard Deviation (Reconstruction): {std_r:.3f} ms")
        print(f"Bandwidth sent to servers: {bandwidth_bytes/1024:.2f} KB\n")

if __name__ == "__main__":
    run_multiple()
