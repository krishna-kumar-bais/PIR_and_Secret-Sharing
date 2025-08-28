# setup_database.py – Create the database
import numpy as np
import random

DB_SIZE = 10_000
DB_FILE = "database.npy"

def generate_database():
    db = []
    for j in range(0,DB_SIZE):
        db.append(random.randint(0, 10_000_000))
    np.save(DB_FILE, db)
    print("Database saved to", DB_FILE)

if __name__ == "__main__":
    generate_database()

