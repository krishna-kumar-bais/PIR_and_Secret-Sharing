import argparse
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from database import make_database, pretty
from GenerateDPF import DPFKey
from pir_client import PIRClient
from pir_server import PIRServer

PRIME = 2147483647   # 2^31 - 1
DEFAULT_RECORD_SIZE = 4
DEFAULT_NUM_SERVERS = 8


def _dpf_key_byte_size(key: DPFKey) -> int:
    """Serialized size of one DPF key (bytes on the wire)."""
    size = 1 + len(key.root_seed) + 1 + 8  # party, seed, root_t, cw_last
    for s_cw, _t_l, _t_r in key.cws:
        size += len(s_cw) + 1 + 1
    return size


def _query_bandwidth_bytes(server_keys: List[List[DPFKey]]) -> int:
    """Total upload bandwidth: all DPF keys sent from client to all servers."""
    return sum(_dpf_key_byte_size(key) for keys in server_keys for key in keys)


@dataclass
class QueryTimings:
    query_creation_s: float
    server_compute_s: float
    reconstruction_s: float
    bandwidth_bytes: int
    reconstructed: List[int]
    expected: List[int]

    @property
    def match(self) -> bool:
        return self.reconstructed == self.expected

    def query_gen_ms(self) -> float:
        return round(self.query_creation_s * 1000.0, 3)

    def server_ms(self) -> float:
        return round(self.server_compute_s * 1000.0, 3)

    def recon_ms(self) -> float:
        return round(self.reconstruction_s * 1000.0, 3)

    def total_ms(self) -> float:
        return round(self.query_gen_ms() + self.server_ms() + self.recon_ms(), 3)

    def bandwidth_kb(self) -> float:
        return round(self.bandwidth_bytes / 1024.0, 2)

    def to_result_dict(self) -> Dict[str, Any]:
        return {
            "query_gen_time": self.query_gen_ms(),
            "server_time": self.server_ms(),
            "recon_time": self.recon_ms(),
            "total_time": self.total_ms(),
            "bandwidth_kb": self.bandwidth_kb(),
            "result": self.reconstructed,
            "expected": self.expected,
            "match": self.match,
        }


def print_timing_summary(timings: QueryTimings) -> None:
    print(f"\nTiming Summary (ms)")
    print(f"DPF Key Generation:    {timings.query_gen_ms()} ms")
    print(f"Server Computation:    {timings.server_ms()} ms")
    print(f"Reconstruction:        {timings.recon_ms()} ms")
    print(f"Total Time:            {timings.total_ms()} ms")
    print(f"Bandwidth sent:        {timings.bandwidth_kb():.2f} KB")


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
    timings = run_query_timed(k, client, servers, db, drop_servers)
    return timings.reconstructed, timings.expected


def run_query_timed(k: int, client: PIRClient, servers: List[PIRServer],
                    db, drop_servers: Optional[set] = None) -> QueryTimings:
    """Run one PIR query with per-phase timings (for benchmarking)."""
    drop_servers = drop_servers or set()

    t0 = time.perf_counter()
    server_keys = client.generate_query(k)
    query_creation_s = time.perf_counter() - t0
    bandwidth_bytes = _query_bandwidth_bytes(server_keys)

    t1 = time.perf_counter()
    responses = []
    for b, (server, keys) in enumerate(zip(servers, server_keys)):
        if b in drop_servers:
            responses.append(None)
        else:
            responses.append(server.answer(keys))
    server_compute_s = time.perf_counter() - t1

    t2 = time.perf_counter()
    got = client.reconstruct(responses)
    reconstruction_s = time.perf_counter() - t2

    return QueryTimings(
        query_creation_s=query_creation_s,
        server_compute_s=server_compute_s,
        reconstruction_s=reconstruction_s,
        bandwidth_bytes=bandwidth_bytes,
        reconstructed=got,
        expected=list(db[k]),
    )


def run_pir(db_size: int, k: int,
            record_size: int = DEFAULT_RECORD_SIZE,
            num_servers: int = DEFAULT_NUM_SERVERS,
            verbose: bool = True,
            print_db: Optional[bool] = None) -> Dict[str, Any]:
    """Run a single PIR query. Returns timing result dict."""
    if db_size < 2:
        raise ValueError("DB_SIZE must be at least 2.")
    if not (0 <= k < db_size):
        raise ValueError(f"k must be in [0, {db_size}), got {k}")

    if print_db is None:
        print_db = verbose and db_size <= 32

    db, client, servers = setup_pir(db_size, record_size, num_servers)
    timings = run_query_timed(k, client, servers, db)
    result = timings.to_result_dict()

    if verbose:
        print(f"Database size: {db_size}")
        print(f"Query index (k): {k}")
        print(f"Database value at k: {pretty(tuple(timings.expected))}")
        print(f"(2, {num_servers})-IT-PIR, d = {client.d}, n_bits = {client.n_bits}")
        if print_db:
            print("-" * 78)
            for i, rec in enumerate(db):
                print(f"  DB[{i:>2}] = {pretty(rec)}")
            print("-" * 78)
        print(f"Reconstructed value:   {pretty(tuple(timings.reconstructed))}")
        print_timing_summary(timings)
        print(f"Match: {result['match']}")

    return result


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="(2, ell)-IT-PIR demo from CS670 Module 4 slides 21-22.")
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


def main(argv: Optional[List[str]] = None) -> Dict[str, Any]:
    args = parse_args(argv)
    try:
        return run_pir(
            db_size=args.DB_SIZE,
            k=args.k,
            record_size=args.record_size,
            num_servers=args.servers,
            verbose=True,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    result = main()
    raise SystemExit(0 if result["match"] else 1)
