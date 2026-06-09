# Time Analysis Comparison of PIR Methods

Benchmarked across four database sizes using `run_all_time_analysis.py`.  
Each method was run with its default server count and query index `k=0`.  
`Eﬃcient_IT_PIR` results are averaged over **10 runs**; all others over **1 run**.

---

## DB_SIZE = 100

| Method | Avg Query Creation (ms) | Std Query (ms) | Avg Server Computation (ms) | Std Server (ms) | Avg Reconstruction (ms) | Std Recon (ms) | Bandwidth (KB) |
|--------|------------------------|----------------|----------------------------|-----------------|------------------------|----------------|----------------|
| PIR_Additive_SS | 0.192 | 0.000 | 192.637 | 0.000 | 0.005 | 0.000 | 2.70 |
| PIR_SSS | 0.291 | 0.000 | 181.899 | 0.000 | 0.020 | 0.000 | 2.51 |
| PIR_DPF | 0.084 | 0.000 | 187.825 | 0.000 | 0.002 | 0.000 | 12.50 |
| Eﬃcient_IT_PIR | 0.133 | 0.019 | 22.272 | 0.684 | 0.006 | 0.006 | 1.19 |

---

## DB_SIZE = 1000

| Method | Avg Query Creation (ms) | Std Query (ms) | Avg Server Computation (ms) | Std Server (ms) | Avg Reconstruction (ms) | Std Recon (ms) | Bandwidth (KB) |
|--------|------------------------|----------------|----------------------------|-----------------|------------------------|----------------|----------------|
| PIR_Additive_SS | 1.659 | 0.000 | 151.705 | 0.000 | 0.006 | 0.000 | 25.95 |
| PIR_SSS | 2.654 | 0.000 | 153.169 | 0.000 | 0.025 | 0.000 | 23.60 |
| PIR_DPF | 0.108 | 0.000 | 189.149 | 0.000 | 0.004 | 0.000 | 125.00 |
| Eﬃcient_IT_PIR | 0.170 | 0.008 | 251.039 | 7.343 | 0.005 | 0.001 | 1.61 |

---

## DB_SIZE = 5000

| Method | Avg Query Creation (ms) | Std Query (ms) | Avg Server Computation (ms) | Std Server (ms) | Avg Reconstruction (ms) | Std Recon (ms) | Bandwidth (KB) |
|--------|------------------------|----------------|----------------------------|-----------------|------------------------|----------------|----------------|
| PIR_Additive_SS | 8.565 | 0.000 | 154.121 | 0.000 | 0.029 | 0.000 | 122.70 |
| PIR_SSS | 39.593 | 0.000 | 166.688 | 0.000 | 0.018 | 0.000 | 117.35 |
| PIR_DPF | 0.132 | 0.000 | 360.888 | 0.000 | 0.004 | 0.000 | 625.00 |
| Eﬃcient_IT_PIR | 0.214 | 0.043 | 2556.471 | 47.221 | 0.005 | 0.001 | 2.03 |

---

## DB_SIZE = 10000

| Method | Avg Query Creation (ms) | Std Query (ms) | Avg Server Computation (ms) | Std Server (ms) | Avg Reconstruction (ms) | Std Recon (ms) | Bandwidth (KB) |
|--------|------------------------|----------------|----------------------------|-----------------|------------------------|----------------|----------------|
| PIR_Additive_SS | 16.959 | 0.000 | 154.955 | 0.000 | 0.004 | 0.000 | 249.54 |
| PIR_SSS | 26.490 | 0.000 | 155.381 | 0.000 | 0.018 | 0.000 | 234.54 |
| PIR_DPF | 0.126 | 0.000 | 602.542 | 0.000 | 0.003 | 0.000 | 1250.00 |
| Eﬃcient_IT_PIR | 0.229 | 0.049 | 5658.742 | 235.071 | 0.006 | 0.001 | 2.17 |

---

## Observations

### Query Creation Time
- **PIR_DPF** and **Eﬃcient_IT_PIR** have near-constant sub-millisecond query creation regardless of DB size — DPF key generation does not depend on N.
- **PIR_Additive_SS** and **PIR_SSS** scale linearly with DB size, since they generate one share per database entry.
- **PIR_SSS** is the slowest at query creation due to the overhead of polynomial evaluation (Shamir) on top of the linear scan.

### Server Computation Time
- **Eﬃcient_IT_PIR** server time grows steeply with DB size (22 ms at N=100 → 5659 ms at N=10000), as it requires a full DPF tree evaluation across all records.
- **PIR_DPF** also scales with DB size (188 ms → 603 ms), but grows more slowly than Eﬃcient_IT_PIR at larger sizes.
- **PIR_Additive_SS** and **PIR_SSS** server times stay relatively flat (~150–170 ms) — the parallel multiprocessing pool startup dominates at all tested sizes.

### Reconstruction Time
- All four methods reconstruct in well under **0.03 ms** — reconstruction is negligible across all DB sizes and methods.

### Bandwidth
- **Eﬃcient_IT_PIR** is the most bandwidth-efficient, growing logarithmically (1.19 KB → 2.17 KB), because only DPF keys (not full shares) are sent per server.
- **PIR_SSS** and **PIR_Additive_SS** bandwidth grows linearly with DB size; both are comparable (2.51–234.54 KB and 2.70–249.54 KB respectively).
- **PIR_DPF** has the highest bandwidth at large sizes (12.50 KB → 1250.00 KB), since it sends full-length DPF keys for a 2-server scheme without the tree-based compression of Eﬃcient_IT_PIR.

### Summary

| Criterion | Best Method |
|-----------|-------------|
| Fastest query creation | PIR_DPF |
| Fastest server computation (small DB) | Eﬃcient_IT_PIR |
| Fastest server computation (large DB) | PIR_Additive_SS / PIR_SSS |
| Lowest bandwidth | Eﬃcient_IT_PIR |
| Simplest scheme | PIR_Additive_SS |
