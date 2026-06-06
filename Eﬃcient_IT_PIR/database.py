import random
from typing import List, Tuple

Record = Tuple[int, ...]
Database = List[Record]


def make_database(num_records: int, record_size: int, prime: int,
                  seed: int = 0xC5670) -> Database:
    
    rng = random.Random(seed)
    db: Database = []
    for _ in range(num_records):
        rec = tuple(rng.randrange(prime) for _ in range(record_size))
        db.append(rec)
    return db


def pretty(record: Record, width: int = 10) -> str:
    return "[" + ", ".join(f"{x:>{width}}" for x in record) + "]"
