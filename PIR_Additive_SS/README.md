# Simple PIR Protocol

This is a basic implementation of a Private Information Retrieval (PIR) protocol using additive secret sharing and 4 simulated servers via Python multiprocessing.

## Features
- Additive secret sharing over `uint64`
- Communication between client and servers
- Dot product computation and reconstruction
- Database of 10,000 64-bit entries

## How to Run

1. Generate the database:
   ```bash
   python setup_database.py
2. Run the client:
   ```bash
   python client.py

