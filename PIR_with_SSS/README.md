# PIR with Shamir Secret Sharing

This project implements a **Private Information Retrieval (PIR)** protocol using **Shamir Secret Sharing (SSS)**.  
It allows a client to retrieve an element from a distributed database across multiple servers **without revealing which element was queried**.

---

## ✨ Features
- Database generated and stored in **`database.npy`**
- Query shares built using **Shamir’s Secret Sharing** with configurable threshold `t`
- Multiple simulated servers process queries in parallel (**multiprocessing**)
- Client reconstructs the requested database value from any **t+1 responses**
- Simple **command-line interface** for customization

---

## ⚙️ Command-line Arguments

| Argument   | Description | Default |
|------------|-------------|---------|
| `--DB_SIZE` | Size of the database (number of entries) | `10000` |
| `--SERVERS` | Number of servers among which shares are distributed | `4` |
| `--t`       | Threshold value: minimum number of servers needed for reconstruction (`1 ≤ t ≤ SERVERS-1`) | `2` |
| `--k`       | Index of the database element the client wants (`0 ≤ k < DB_SIZE`) | `0` |
| `--DB_FILE` | File name to store/load the database | `database.npy` |

---

## 🚀 How to Run

1. Run with default parameters:
   ```bash
   python main.py
2. Run with custom database size, number of servers, threshold, and query index:
   ```bash
   python main.py --DB_SIZE 20 --SERVERS 3 --t 2 --k 5

