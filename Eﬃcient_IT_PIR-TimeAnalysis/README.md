# Efficient IT-PIR: (2, ℓ)-Server

Private Information Retrieval using Distributed Point Functions — **(2, ℓ)-IT-PIR** with ℓ = 8 servers (d = 3 DPF levels).

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--DB_SIZE` | `16` | Number of database records N |
| `--k` | `11` | Secret query index (`DB[k]`), must satisfy `0 ≤ k < DB_SIZE` |
| `--record-size` | `4` | Field elements per record L |
| `--servers` | `8` | Number of servers ℓ (power of 2, ≥ 2) |

When `DB_SIZE ≤ 32`, `main.py` also prints the full database table.

---

## `main.py` — Single Query

**Command:**

```bash
python3 main.py --DB_SIZE 100 --k 5 --record-size 1 --servers 4
```

**Output:**

```
Database size: 100
Query index (k): 5
Database value at k: [ 696628629]
(2, 4)-IT-PIR, d = 2, n_bits = 7
Reconstructed value:   [ 696628629]

Timing Summary (ms)
DPF Key Generation:    0.306 ms
Server Computation:    37.311 ms
Reconstruction:        0.007 ms
Total Time:            37.624 ms
Bandwidth sent:        1.19 KB
Match: True
```

---

## `run_multiple.py` — Multi-Size Benchmark

**Command:**

```bash
python3 run_multiple.py --DB_SIZES 100 20000 --k 5 --runs 3 --servers 4
```

**Output:**

```
=== Running for DB_SIZE = 100 ===

Run 1/3:
Reconstructed value:   [696628629]

Timing Summary (ms)
DPF Key Generation:    0.235 ms
Server Computation:    36.14 ms
Reconstruction:        0.008 ms
Total Time:            36.383 ms
Bandwidth sent:        1.19 KB

Run 2/3:
Reconstructed value:   [696628629]

Timing Summary (ms)
DPF Key Generation:    0.202 ms
Server Computation:    36.543 ms
Reconstruction:        0.006 ms
Total Time:            36.751 ms
Bandwidth sent:        1.19 KB

Run 3/3:
Reconstructed value:   [696628629]

Timing Summary (ms)
DPF Key Generation:    0.196 ms
Server Computation:    36.65 ms
Reconstruction:        0.007 ms
Total Time:            36.853 ms
Bandwidth sent:        1.19 KB

Average Query creation time: 36.655 ms
Average Reconstruction time: 0.007 ms

Standard Deviation (Query creation): 0.248 ms
Standard Deviation (Reconstruction): 0.001 ms
Bandwidth sent to servers: 1.19 KB
===================================================

=== Running for DB_SIZE = 20000 ===

Run 1/3:
Reconstructed value:   [696628629]

Timing Summary (ms)
DPF Key Generation:    0.394 ms
Server Computation:    20216.733 ms
Reconstruction:        0.014 ms
Total Time:            20217.141 ms
Bandwidth sent:        2.31 KB

(... runs 2/3 and 3/3 ...)

Average Query creation time: 19370.885 ms
Average Reconstruction time: 0.013 ms

Standard Deviation (Query creation): 740.112 ms
Standard Deviation (Reconstruction): 0.001 ms
Bandwidth sent to servers: 2.31 KB
===================================================
```

> **Note:** `Average Query creation time` = DPF key generation + server computation (same convention as PIR_DPF).

---

## Verification

| Command | Exit code | Result |
|---------|-----------|--------|
| `python3 main.py --DB_SIZE 100 --k 5 --record-size 1 --servers 4` | `0` | **Pass** — `Match: True` |
| `python3 run_multiple.py --DB_SIZES 100 20000 --k 5 --runs 3 --servers 4` | `0` | **Pass** |

## Files

| File | Purpose |
|------|---------|
| `main.py` | Single query execution with timing summary |
| `run_multiple.py` | Multi-size benchmark with mean/std timings |
| `pir_client.py` | DPF key generation + client reconstruction |
| `pir_server.py` | EvalFull + database inner product per server |
| `database.py` | In-memory database over Z_p |
| `GenerateDPF.py` | DPF key generation |
| `EvalDPF.py` | DPF point evaluation |
