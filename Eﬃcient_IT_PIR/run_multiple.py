import argparse
import time
from typing import List, Optional

from main import run_pir


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark (2, ell)-IT-PIR over multiple DB sizes.")
    parser.add_argument(
        "--DB_SIZES", type=int, nargs="+", required=True,
        metavar="N",
        help="database sizes to test, e.g. --DB_SIZES 100 500 1000")
    parser.add_argument(
        "--k", type=int, required=True,
        help="secret record index to retrieve (must be < each DB_SIZE)")
    parser.add_argument(
        "--runs", type=int, default=1,
        help="number of repetitions per DB_SIZE (default: 1)")
    parser.add_argument(
        "--record-size", type=int, default=4,
        help="field elements per record L (default: 4)")
    parser.add_argument(
        "--servers", type=int, default=8,
        help="number of servers ell (default: 8, must be power of 2)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.runs < 1:
        raise SystemExit("--runs must be at least 1")

    print(f"Input: DB_SIZES = {args.DB_SIZES}, k = {args.k}, runs = {args.runs}")
    print("-" * 60)

    failures = 0
    total = 0

    for db_size in args.DB_SIZES:
        if args.k >= db_size:
            print(f"DB_SIZE={db_size}: SKIP (k={args.k} out of range [0, {db_size}))")
            continue

        for run in range(1, args.runs + 1):
            total += 1
            t0 = time.perf_counter()
            try:
                ok = run_pir(
                    db_size=db_size,
                    k=args.k,
                    record_size=args.record_size,
                    num_servers=args.servers,
                    verbose=False,
                )
            except ValueError as exc:
                print(f"DB_SIZE={db_size} run {run}/{args.runs}: ERROR  {exc}")
                failures += 1
                continue

            elapsed = time.perf_counter() - t0
            status = "PASS" if ok else "FAIL"
            if not ok:
                failures += 1
            print(f"DB_SIZE={db_size:>5}  run {run}/{args.runs}  "
                  f"{status}  time={elapsed:.3f}s")

    print("-" * 60)
    passed = total - failures
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
