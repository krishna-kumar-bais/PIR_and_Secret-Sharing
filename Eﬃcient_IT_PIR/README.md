# Efficient IT-PIR: (2, ℓ)-Server

Private Information Retrieval using Distributed Point Functions — **(2, ℓ)-IT-PIR** with ℓ = 8 servers (d = 3 DPF levels).

## Run Single Query

```bash
python3 main.py --DB_SIZE 1000 --k 42
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--DB_SIZE` | `16` | Number of database records N |
| `--k` | `11` | Secret query index (`DB[k]`), must satisfy `0 ≤ k < DB_SIZE` |
| `--record-size` | `4` | Field elements per record L |
| `--servers` | `8` | Number of servers ℓ (power of 2, ≥ 2) |

**Example:**

```bash
python3 main.py --DB_SIZE 1000 --k 42
python3 main.py --DB_SIZE 500 --k 100 --record-size 4 --servers 8
```

## Output

```
Input: DB_SIZE = 1000, k = 42
Database: 1000 records of 4 field elements over Z_2147483647
(2, 8)-IT-PIR, d = 3, n_bits = 10

Query: all 8 servers respond, k = 42
  Reconstructed : [  22621858,  829624907, 2100515581,  698576150]
  Expected      : [  22621858,  829624907, 2100515581,  698576150]
  Match         : True
  Setup time    : 0.003s
  Query time    : 0.769s
```

When `DB_SIZE ≤ 32`, the full database table is also printed.

## Verification

| Command | Exit code | Result |
|---------|-----------|--------|
| `python3 main.py --DB_SIZE 1000 --k 42` | `0` | **Pass** — `Match: True` |

## Files

| File | Purpose |
|------|---------|
| `main.py` | Single query execution |
| `pir_client.py` | DPF key generation + client reconstruction |
| `pir_server.py` | EvalFull + database inner product per server |
| `database.py` | In-memory database over Z_p |
| `GenerateDPF.py` | DPF key generation |
| `EvalDPF.py` | DPF point evaluation |
