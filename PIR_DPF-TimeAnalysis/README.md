# PIR-DPF: Pure 2-Server Mode

Private Information Retrieval using Distributed Point Functions (2 server implementation).

## Run Single Query
```bash
python3 main.py --DB_SIZE 1000 --k 42
```

## Run Multiple Tests with Statistics
```bash
python3 run_multiple.py --DB_SIZES 100 500 1000 --runs 3
```

## Parameters

### main.py
- `--DB_SIZE`: Database size (default: 1000)
- `--k`: Query index (default: 0)
- `--DB_FILE`: Database file path (default: database_dpf.npy)

**Example:**
```bash
python3 main.py --DB_SIZE 5000 --k 100 --DB_FILE my_database.npy
```

### run_multiple.py
- `--DB_SIZES` (required): Space-separated list of database sizes
- `--k`: Query index (default: 0)
- `--DB_FILE`: Database filename (default: database_dpf.npy)
- `--runs`: Number of runs per size (default: 1)

**Examples:**
```bash
# Test 3 sizes, 5 runs each
python3 run_multiple.py --DB_SIZES 100 500 1000 --runs 5

# Test with custom query index
python3 run_multiple.py --DB_SIZES 1000 5000 --k 50 --runs 3
```

## Output

### Single Query Output
```
Database size: 1000
Query index (k): 5
Database value at k: 4010102
DPF Response 0: 261334782518924484
DPF Response 1: 2044508226698779569
Reconstructed value: 4010102

Timing Summary (ms)
DPF Key Generation:    0.117 ms
Server Computation:    344.172 ms
Reconstruction:        0.007 ms
Total Time:            344.296 ms
```

### Multiple Tests Output
Shows per-run details for each DB_SIZE, followed by average timing and statistics:
```
Average Query creation time: 321.066 ms
Average Reconstruction time: 0.007 ms
Standard Deviation (Query creation): 24.391 ms
Standard Deviation (Reconstruction): 0.001 ms
Bandwidth sent to servers: 62.50 KB
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Single query execution |
| `run_multiple.py` | Batch testing with statistics |
| `make_query_shares_dpf.py` | DPF key generation |
| `server_dpf.py` | Server computation |
| `reconstructs_dpf.py` | Client reconstruction |



