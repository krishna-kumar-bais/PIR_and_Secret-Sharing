# PIR with Additive Secret Sharing(SS)

This project implements a Private Information Retrieval (PIR) protocol using additive secret sharing. The client can retrieve a value from a database distributed across multiple simulated servers without revealing which element was queried.

---

## ✨ Features
- Database generated and stored in **`database.npy`**
- Query shares built using **additive secret sharing**
- Multiple simulated servers process queries in parallel (**multiprocessing**)
- Client reconstructs the requested database value from **all server responses**
- Simple **command-line interface** for customization

---

## ⚙️ Command-line Arguments

| Argument   | Description | Default |
|------------|-------------|---------|
| `--DB_SIZE` | Size of the database (number of entries) | `10000` |
| `--SERVERS` | Number of servers among which shares are distributed | `4` |
| `--k`       | Index of the database element the client wants (`0 ≤ k < DB_SIZE`) | `0` |
| `--DB_FILE` | File name to store/load the database | `database.npy` |

---

## 🚀 How to Run

1. Run with default parameters:
   ```bash
   python main.py
2. Run with custom database size, number of servers, and query index:
   ```bash
   python main.py --DB_SIZE 20 --SERVERS 3 --k 5
