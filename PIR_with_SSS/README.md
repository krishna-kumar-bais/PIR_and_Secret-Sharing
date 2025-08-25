# PIR with Shamir Secret Sharing
This project implements a basic Private Information Retrieval (PIR) protocol using Shamir Secret Sharing (SSS) across 4 simulated servers with Python multiprocessing.

## Features
- Database stored in `database.npy` (10,000 entries)
- Query shares generated using SSS (threshold `t`)
- Servers compute dot products on their shares
- Client reconstructs the result from any `t+1` server responses

## How to Run

1. Generate the database:
   ```bash
   python setup_database.py
2. Run the client:
   ```bash
   python main.py

