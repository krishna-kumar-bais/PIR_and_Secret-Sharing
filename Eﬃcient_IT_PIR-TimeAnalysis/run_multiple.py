import argparse
import statistics
from typing import List, Optional

from main import print_timing_summary, setup_pir, run_query_timed


def run_multiple(db_sizes: List[int], k: int, record_size: int, servers: int,
                 runs: int) -> dict:
    results = {}

    for db_size in db_sizes:
        print(f"\n=== Running for DB_SIZE = {db_size} ===")
        if not (0 <= k < db_size):
            print(f"SKIP: k={k} out of range [0, {db_size})")
            continue

        try:
            db, client, server_list = setup_pir(db_size, record_size, servers)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            continue

        times_query = []
        times_recon = []
        bandwidth_kb = 0.0
        all_correct = True

        for run in range(runs):
            print(f"\nRun {run + 1}/{runs}:")

            timings = run_query_timed(k, client, server_list, db)
            result = timings.to_result_dict()

            print(f"Reconstructed value:   {result['result']}")
            print_timing_summary(timings)

            # Match PIR_DPF: query creation stat = key gen + server compute
            times_query.append(result["query_gen_time"] + result["server_time"])
            times_recon.append(result["recon_time"])
            bandwidth_kb = result["bandwidth_kb"]

            if result["result"] != result["expected"]:
                all_correct = False

        results[db_size] = {
            "query_gen": {
                "avg": statistics.mean(times_query),
                "stdev": statistics.stdev(times_query) if runs > 1 else 0,
                "min": min(times_query),
                "max": max(times_query),
            },
            "recon": {
                "avg": statistics.mean(times_recon),
                "stdev": statistics.stdev(times_recon) if runs > 1 else 0,
                "min": min(times_recon),
                "max": max(times_recon),
            },
            "bandwidth_kb": bandwidth_kb,
            "all_correct": all_correct,
        }

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
        print(f"Bandwidth sent to servers: {bandwidth_kb:.2f} KB")
        print(f"{'=' * 51}")

    return results


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run IT-PIR with multiple database sizes.")
    parser.add_argument(
        "--DB_SIZES", type=int, nargs="+", required=True,
        metavar="N",
        help="database sizes to test, e.g. --DB_SIZES 100 20000")
    parser.add_argument(
        "--k", type=int, default=5,
        help="secret record index to retrieve (default: 5)")
    parser.add_argument(
        "--runs", type=int, default=10,
        help="number of repetitions per DB_SIZE (default: 10)")
    parser.add_argument(
        "--record-size", type=int, default=1,
        help="field elements per record L (default: 1)")
    parser.add_argument(
        "--servers", type=int, default=4,
        help="number of servers ell (default: 4, must be power of 2)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.runs < 1:
        raise SystemExit("--runs must be at least 1")

    results = run_multiple(
        db_sizes=args.DB_SIZES,
        k=args.k,
        record_size=args.record_size,
        servers=args.servers,
        runs=args.runs,
    )

    failures = sum(1 for r in results.values() if not r["all_correct"])
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
