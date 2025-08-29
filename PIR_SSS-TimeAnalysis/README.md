# PIR with Shamir Secret Sharing — Time Analysis

This project extends the **Private Information Retrieval (PIR)** implementation with **Shamir Secret Sharing (SSS)** to measure the **query creation** and **reconstruction times** for different database sizes and multiple runs.  
It allows evaluating the performance of PIR operations in terms of **average time** and **standard deviation**.

---

## ✨ Features
- Automatically generates a database (`database.npy`) of configurable size
- Measures **Query Creation Time** and **Reconstruction Time** for PIR operations
- Supports multiple runs to calculate **average times** and **standard deviations**
- Computes and reports **Bandwidth sent to servers**
- Handles multiple database sizes in a single run
- Simple **command-line interface** for customization

---

## ⚙️ Command-line Arguments

| Argument     | Description | Default |
|--------------|-------------|---------|
| `--DB_SIZES` | List of database sizes to test (e.g., 100 1000 10000) | **Required** |
| `--SERVERS`  | Number of servers among which shares are distributed | `3` |
| `--t`        | Threshold value: minimum number of servers needed for reconstruction (`1 ≤ t ≤ SERVERS-1`) | `2` |
| `--k`        | Index of the database element the client wants (`0 ≤ k < DB_SIZE`) | `0` |
| `--DB_FILE`  | File name to store/load the database | `database.npy` |
| `--runs`     | Number of runs for each database size (for averaging & standard deviation) | `1` |

---

## 🚀 How to Run

1. Run for a single database size with default parameters:
   ```bash
   python run_multiple.py --DB_SIZES 20000
2. Run for multiple database sizes with custom parameters and repeated runs:
   ```bash
   python run_multiple.py --DB_SIZES 20000 100 3234 --SERVERS 3 --t 2 --k 5 --runs 2
