# 📊 Comparison: PIR with Shamir Secret Sharing vs Additive Secret Sharing

This document compares the performance and properties of two PIR implementations:

- **PIR_SSS**: Private Information Retrieval with **Shamir Secret Sharing**
- **PIR_ASS**: Private Information Retrieval with **Additive Secret Sharing**

The experiments were run with database sizes of **20,000** and **100**, using **3 servers** and querying index `k=5`.

---

## ⏱ Performance Results

| Metric | PIR_SSS (DB=20k) | PIR_ASS (DB=20k) | PIR_SSS (DB=100) | PIR_ASS (DB=100) |
|--------|------------------|------------------|------------------|------------------|
| **Avg Query Creation Time** | 57.174 ms | **37.694 ms** | 0.260 ms | **0.171 ms** |
| **Std (Query Creation)**    | 11.185 ms | 7.380 ms | 0.003 ms | 0.001 ms |
| **Avg Reconstruction Time** | 0.019 ms | **0.007 ms** | 0.016 ms | **0.004 ms** |
| **Std (Reconstruction)**    | 0.003 ms | 0.003 ms | 0.001 ms | 0.000 ms |
| **Bandwidth Sent**          | **468.91 KB** | 506.88 KB | **2.51 KB** | 2.70 KB |

---

## 🔎 Observations

1. **Query Creation Time**  
   - PIR_ASS is faster than PIR_SSS.
   - Shamir incurs extra overhead due to polynomial generation.

2. **Reconstruction Time**  
   - PIR_ASS is slightly faster.

3. **Bandwidth Usage**  
   - PIR_SSS is more bandwidth-efficient.
   - PIR_ASS sends larger queries due to additive shares.
