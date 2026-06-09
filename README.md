# PIR and Secret Sharing

A collection of **Private Information Retrieval (PIR)** protocols and **Secret Sharing** schemes implemented in Python. The repository covers four distinct PIR constructions, their time-analysis variants, a standalone DPF secret sharing module, a runner that benchmarks all four in one command, and a comparison document with real measured results.

---

## Repository Structure

```
PIR_and_Secret-Sharing/
│
├── SSS/                          # Shamir Secret Sharing (standalone)
├── DPF_SS/                       # DPF-based Secret Sharing (standalone)
│
├── PIR_Additive_SS/              # PIR using Additive Secret Sharing
├── PIR_with_SSS/                 # PIR using Shamir Secret Sharing
├── Eﬃcient_IT_PIR/               # (2, ℓ)-IT-PIR using DPF (multi-server)
│
├── PIR_Additive_SS-TimeAnalysis/ # Time analysis for PIR_Additive_SS
├── PIR_SSS-TimeAnalysis/         # Time analysis for PIR_with_SSS
├── PIR_DPF-TimeAnalysis/         # Time analysis for PIR-DPF (2-server)
├── Eﬃcient_IT_PIR-TimeAnalysis/  # Time analysis for Eﬃcient_IT_PIR
│
├── run_all_time_analysis.py      # Runs all 4 TimeAnalysis scripts + prints combined table
├── Time-Comparison.md            # Measured performance comparison across all 4 methods
└── README.md
```

---

## Run All Four — Combined Benchmark

`run_all_time_analysis.py` at the repo root executes all four `TimeAnalysis/run_multiple.py` scripts in sequence, then prints and saves a combined results table (one table per DB size).

### Usage

```bash
python3 run_all_time_analysis.py --DB_SIZES 100 1000 5000 10000
python3 run_all_time_analysis.py --DB_SIZES 100 1000 --runs 5 --k 0
python3 run_all_time_analysis.py --DB_SIZES 100 1000 --csv my_results.csv
```


| Argument     | Default                     | Description                            |
| ------------ | --------------------------- | -------------------------------------- |
| `--DB_SIZES` | **required**                | Space-separated list of database sizes |
| `--runs`     | each script's default       | Repetitions per DB size                |
| `--k`        | each script's default       | Query index                            |
| `--csv`      | `time_analysis_results.csv` | Output CSV path                        |


### Output

- Output from each script is streamed to the console.
- After all scripts complete, a per-DB_SIZE table is printed:

```
======================================================================
DB_SIZE = 1000
======================================================================
Method          | Avg Query Creation Time (ms) | Std (Query Creation) (ms) | Avg Server Computation Time (ms) | ...
PIR_Additive_SS | 1.659                        | 0.000                     | 151.705                          | ...
PIR_SSS         | 2.654                        | 0.000                     | 153.169                          | ...
PIR_DPF         | 0.108                        | 0.000                     | 189.149                          | ...
Eﬃcient_IT_PIR  | 0.170                        | 0.008                     | 251.039                          | ...
```

- Results are also written to `time_analysis_results.csv`.

---

## Performance Summary

Full measured results are in `[Time-Comparison.md](Time-Comparison.md)`. Key takeaways from DB sizes 100–10000:


| Criterion                             | Best Method                                    |
| ------------------------------------- | ---------------------------------------------- |
| Fastest query creation                | PIR_DPF (sub-0.2 ms, constant)                 |
| Lowest server computation at small DB | Eﬃcient_IT_PIR (~22 ms at N=100)               |
| Lowest server computation at large DB | PIR_Additive_SS / PIR_SSS (~155 ms at N=10000) |
| Lowest bandwidth (all sizes)          | Eﬃcient_IT_PIR (1.19–2.17 KB, logarithmic)     |
| Fastest reconstruction                | PIR_DPF (< 0.005 ms)                           |


---

## Requirements

- Python 3.7+
- `numpy` — `pip install numpy`

---

## Quick Start

```bash
# Clone and enter repo
git clone https://github.com/krishna-kumar-bais/PIR_and_Secret-Sharing
cd PIR_and_Secret-Sharing

# Install dependency
pip install numpy

# Run all benchmarks for 4 DB sizes and get a combined table
python3 run_all_time_analysis.py --DB_SIZES 100 1000 5000 10000
```

