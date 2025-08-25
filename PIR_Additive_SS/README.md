# Simple PIR Protocol

This is a basic implementation of a Private Information Retrieval (PIR) protocol using additive secret sharing and 4 simulated servers via Python multiprocessing.

## Features
- Database stored in database.npy (10,000 entries)
- Query shares generated using additive secret sharing
- Servers compute responses in parallel using Python multiprocessing
- Client reconstructs the desired database value from server responses
  
## How to Run

1. Generate the database:
   ```bash
   python setup_database.py
2. Run the client:
   ```bash
   python main.py

