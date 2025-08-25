# Shamir Secret Sharing (SSS)

This folder contains a simple implementation of **Shamir’s Secret Sharing** with threshold reconstruction.

## Features
- Splits a secret into *n* shares with threshold *t*.
- Uses polynomial interpolation (Lagrange) for reconstruction.
- Operates over a prime field (same prime used across all shares).

## How to Use
1. **Run the main script:**
   ```python
   python main.py
