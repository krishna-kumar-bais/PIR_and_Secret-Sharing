import argparse
import time
from typing import List, Optional, Tuple

from database import make_database, pretty
from pir_client import PIRClient
from pir_server import PIRServer

PRIME = 2147483647   # 2^31 - 1
DEFAULT_RECORD_SIZE = 4
DEFAULT_NUM_SERVERS = 8


def setup_pir(db_size: int,
              record_size: int = DEFAULT_RECORD_SIZE,
              num_servers: int = DEFAULT_NUM_SERVERS):
    """Build database, client, and servers."""
    db = make_database(num_records=db_size, record_size=record_size, prime=PRIME)
    client = PIRClient(num_records=db_size, record_size=record_size, prime=PRIME,
                       num_servers=num_servers)
    servers = [PIRServer(b, db, PRIME, client.n_bits) for b in range(num_servers)]
    return db, client, servers


def run_query(k: int, client: PIRClient, servers: List[PIRServer],
              db, drop_servers: Optional[set] = None) -> Tuple[List[int], List[int]]:
    """Run one PIR query and return (reconstructed, expected)."""
    drop_servers = drop_servers or set()
    server_keys = client.generate_query(k)
    responses = []
    for b, (server, keys) in enumerate(zip(servers, server_keys)):
        if b in drop_servers:
            responses.append(None)
        else:
            responses.append(server.answer(keys))
    got = client.reconstruct(responses)
    expected = list(db[k])
    return got, expected


def run_pir(db_size: int, k: int,
            record_size: int = DEFAULT_RECORD_SIZE,
            num_servers: int = DEFAULT_NUM_SERVERS,
            verbose: bool = True,
            print_db: Optional[bool] = None) -> bool:
    """Run a single PIR query. Returns True if reconstruction matches DB[k]."""
    if db_size < 2:
        raise ValueError("DB_SIZE must be at least 2.")
    if not (0 <= k < db_size):
        raise ValueError(f"k must be in [0, {db_size}), got {k}")

    if print_db is None:
        print_db = verbose and db_size <= 32

    t0 = time.perf_counter()
    db, client, servers = setup_pir(db_size, record_size, num_servers)
    setup_s = time.perf_counter() - t0

    t1 = time.perf_counter()
    got, expected = run_query(k, client, servers, db)
    query_s = time.perf_counter() - t1

    match = got == expected

    if verbose:
        print(f"Input: DB_SIZE = {db_size}, k = {k}")
        print(f"Database: {db_size} records of {record_size} field elements "
              f"over Z_{PRIME}")
        print(f"(2, {num_servers})-IT-PIR, d = {client.d}, "
              f"n_bits = {client.n_bits}")
        if print_db:
            print("-" * 78)
            for i, rec in enumerate(db):
                print(f"  DB[{i:>2}] = {pretty(rec)}")
            print("-" * 78)
        print(f"\nQuery: all {num_servers} servers respond, k = {k}")
        print(f"  Reconstructed : {pretty(tuple(got))}")
        print(f"  Expected      : {pretty(tuple(expected))}")
        print(f"  Match         : {match}")
        print(f"  Setup time    : {setup_s:.3f}s")
        print(f"  Query time    : {query_s:.3f}s")

    return match


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="(2, ell)-IT-PIR")
    parser.add_argument(
        "--DB_SIZE", type=int, default=16,
        help="number of database records N (default: 16)")
    parser.add_argument(
        "--k", type=int, default=11,
        help="secret record index to retrieve (default: 11)")
    parser.add_argument(
        "--record-size", type=int, default=DEFAULT_RECORD_SIZE,
        help=f"field elements per record L (default: {DEFAULT_RECORD_SIZE})")
    parser.add_argument(
        "--servers", type=int, default=DEFAULT_NUM_SERVERS,
        help=f"number of servers ell (default: {DEFAULT_NUM_SERVERS}, must be power of 2)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        ok = run_pir(
            db_size=args.DB_SIZE,
            k=args.k,
            record_size=args.record_size,
            num_servers=args.servers,
            verbose=True,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
