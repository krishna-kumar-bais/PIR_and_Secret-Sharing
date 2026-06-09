# DPF Secret Sharing (DPF_SS)

A implementation of a **Distributed Point Function (DPF)** based secret sharing scheme. A DPF splits a secret point function — one that evaluates to `β` at a single target index `α` and `0` everywhere else — into two compact keys. Any single key reveals nothing about `α` or `β`; only by combining both evaluations can the original value be recovered.


## Files

| File | Description |
|------|-------------|
| `GenerateDPF.py` | DPF key generation: builds correction words using a SHA-256 PRG |
| `EvalDPF.py` | DPF evaluation: traverses the key tree to produce a secret share |
| `main.py` | Demo: generates keys for a fixed `(alpha, beta)` and prints eval results for `x = 0..7` |

---

## Run

```bash
python3 main.py
```

### Expected Output

The demo uses `alpha = 3`, `beta = 1233499956`, `n = 5 bits`, `prime = 2147483647`:

```
x	Eval0	Eval1	Sum
0 -> <share0> + <share1> = 0
1 -> <share0> + <share1> = 0
2 -> <share0> + <share1> = 0
3 -> <share0> + <share1> = 1233499956     ← only x == alpha is non-zero
4 -> <share0> + <share1> = 0
5 -> <share0> + <share1> = 0
6 -> <share0> + <share1> = 0
7 -> <share0> + <share1> = 0
```

> Shares (`Eval0`, `Eval1`) are random-looking individually. The sum is `beta` only at `x = alpha` and `0` everywhere else — this is the point function property.

---

## Parameters (in `main.py`)

| Variable | Value | Description |
|----------|-------|-------------|
| `alpha`  | `3`   | Secret target index |
| `beta`   | `1233499956` | Secret value at `alpha` |
| `nbits`  | `5`   | Tree depth; domain is `{0, …, 2ⁿ−1}` |
| `prime`  | `2147483647` | Prime modulus (`2³¹ − 1`, a Mersenne prime) |

To test a different point, edit these four values directly in `main.py`.

---
