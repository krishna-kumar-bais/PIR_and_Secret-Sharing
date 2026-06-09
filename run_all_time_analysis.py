"""Run all four TimeAnalysis run_multiple.py scripts and summarize results."""

import argparse
import csv
import os
import re
import subprocess
import sys

# Directories (relative to this file) that contain a run_multiple.py to execute.
TIME_ANALYSIS_DIRS = [
    "PIR_Additive_SS-TimeAnalysis",
    "PIR_SSS-TimeAnalysis",
    "PIR_DPF-TimeAnalysis",
    "Eﬃcient_IT_PIR-TimeAnalysis",
]

CSV_FILENAME = "time_analysis_results.csv"

# --- Regexes for parsing each script's printed output -----------------------
RE_DB_SIZE = re.compile(r"Running for DB_SIZE\s*=\s*(\d+)")
RE_AVG_QUERY = re.compile(r"Average Query creation time:\s*([\d.]+)\s*ms")
RE_AVG_SERVER = re.compile(r"Average Server computation time:\s*([\d.]+)\s*ms")
RE_AVG_RECON = re.compile(r"Average Reconstruction time:\s*([\d.]+)\s*ms")
RE_STD_QUERY = re.compile(r"Standard Deviation \(Query creation\):\s*([\d.]+)\s*ms")
RE_STD_SERVER = re.compile(r"Standard Deviation \(Server computation\):\s*([\d.]+)\s*ms")
RE_STD_RECON = re.compile(r"Standard Deviation \(Reconstruction\):\s*([\d.]+)\s*ms")
RE_BANDWIDTH = re.compile(r"Bandwidth sent to servers:\s*([\d.]+)\s*KB")

# Columns shown in each per-DB_SIZE table (DB_SIZE is the table title, so it is
# not repeated as a column).
TABLE_COLUMNS = [
    ("method", "Method"),
    ("avg_query", "Avg Query Creation Time (ms)"),
    ("std_query", "Std (Query Creation) (ms)"),
    ("avg_server", "Avg Server Computation Time (ms)"),
    ("std_server", "Std (Server Computation) (ms)"),
    ("avg_recon", "Avg Reconstruction Time (ms)"),
    ("std_recon", "Std (Reconstruction) (ms)"),
    ("bandwidth", "Bandwidth Sent (KB)"),
]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Run all 4 TimeAnalysis run_multiple.py scripts and tabulate results.")
    parser.add_argument(
        "--DB_SIZES", type=int, nargs="+", required=True, metavar="N",
        help="database sizes to test, forwarded to every script (e.g. --DB_SIZES 100 1000)")
    parser.add_argument(
        "--runs", type=int, default=None,
        help="repetitions per DB_SIZE; if omitted, each script's own default is used")
    parser.add_argument(
        "--k", type=int, default=None,
        help="record index to retrieve; if omitted, each script's own default is used")
    parser.add_argument(
        "--csv", type=str, default=CSV_FILENAME,
        help=f"path to write the results CSV (default: {CSV_FILENAME})")
    return parser.parse_args(argv)


def build_forwarded_args(args):
    forwarded = ["--DB_SIZES", *[str(s) for s in args.DB_SIZES]]
    if args.runs is not None:
        forwarded += ["--runs", str(args.runs)]
    if args.k is not None:
        forwarded += ["--k", str(args.k)]
    return forwarded


def run_script(work_dir, forwarded):
    """Run one run_multiple.py, streaming its output live and capturing it.

    Returns (return_code, captured_text).
    """
    proc = subprocess.Popen(
        [sys.executable, "run_multiple.py", *forwarded],
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    captured = []
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        captured.append(line)
    proc.wait()
    return proc.returncode, "".join(captured)


def parse_output(method, text):
    """Parse one script's captured output into a list of per-DB_SIZE row dicts."""
    rows = []
    current = None

    def flush():
        if current is not None:
            rows.append(current)

    for line in text.splitlines():
        m = RE_DB_SIZE.search(line)
        if m:
            flush()
            current = {
                "method": method,
                "db_size": m.group(1),
                "avg_query": "",
                "std_query": "",
                "avg_server": "N/A",
                "std_server": "N/A",
                "avg_recon": "",
                "std_recon": "",
                "bandwidth": "",
            }
            continue
        if current is None:
            continue
        for regex, key in (
            (RE_AVG_QUERY, "avg_query"),
            (RE_STD_QUERY, "std_query"),
            (RE_AVG_SERVER, "avg_server"),
            (RE_STD_SERVER, "std_server"),
            (RE_AVG_RECON, "avg_recon"),
            (RE_STD_RECON, "std_recon"),
            (RE_BANDWIDTH, "bandwidth"),
        ):
            mm = regex.search(line)
            if mm:
                current[key] = mm.group(1)
                break
    flush()
    return rows


def group_by_db_size(rows):
    """Group rows by DB_SIZE, preserving first-seen order."""
    grouped = {}
    for row in rows:
        grouped.setdefault(row["db_size"], []).append(row)
    return grouped


def print_table(db_size, rows):
    headers = [label for _, label in TABLE_COLUMNS]
    keys = [key for key, _ in TABLE_COLUMNS]

    table = [headers]
    for row in rows:
        table.append([str(row.get(k, "")) for k in keys])

    widths = [max(len(r[i]) for r in table) for i in range(len(headers))]

    def fmt(cells):
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    sep = "-+-".join("-" * w for w in widths)

    title = f"DB_SIZE = {db_size}"
    print("\n" + "=" * len(sep))
    print(title)
    print("=" * len(sep))
    print(fmt(table[0]))
    print(sep)
    for line in table[1:]:
        print(fmt(line))


def write_csv(grouped, csv_path):
    headers = [label for _, label in TABLE_COLUMNS]
    keys = [key for key, _ in TABLE_COLUMNS]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        for i, (db_size, rows) in enumerate(grouped.items()):
            if i > 0:
                writer.writerow([])  # blank line between tables
            writer.writerow([f"DB_SIZE = {db_size}"])
            writer.writerow(headers)
            for row in rows:
                writer.writerow([row.get(k, "") for k in keys])


def main(argv=None):
    args = parse_args(argv)
    forwarded = build_forwarded_args(args)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    run_status = []
    all_rows = []

    for directory in TIME_ANALYSIS_DIRS:
        work_dir = os.path.join(base_dir, directory)
        script_path = os.path.join(work_dir, "run_multiple.py")

        print("\n" + "#" * 70)
        print(f"# Running: {directory}/run_multiple.py")
        print("#" * 70)

        if not os.path.isfile(script_path):
            print(f"ERROR: not found -> {script_path}")
            run_status.append((directory, None))
            continue

        code, output = run_script(work_dir, forwarded)
        run_status.append((directory, code))
        method_label = directory.replace("-TimeAnalysis", "")
        all_rows.extend(parse_output(method_label, output))

    print("\n" + "=" * 70)
    print("Run Summary")
    print("=" * 70)
    for directory, code in run_status:
        if code is None:
            status = "SKIPPED (script not found)"
        elif code == 0:
            status = "OK"
        else:
            status = f"FAILED (exit code {code})"
        print(f"  {directory}: {status}")

    if all_rows:
        grouped = group_by_db_size(all_rows)
        for db_size, rows in grouped.items():
            print_table(db_size, rows)
        csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(base_dir, args.csv)
        write_csv(grouped, csv_path)
        print(f"\nResults tables written to: {csv_path}")
    else:
        print("\nNo results parsed; tables/CSV not produced.")

    failures = sum(1 for _, code in run_status if code not in (0, None))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
