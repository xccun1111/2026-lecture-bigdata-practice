# Week 03 LSH Observation

## Task 1 — MinHash and LSH

I implemented Jaccard similarity, MinHash signatures, and LSH candidate generation.

The Jaccard similarity and MinHash tests passed successfully. The implementation produced the expected signatures for the provided test sets.

LSH is used to reduce the number of document pairs that need to be checked by grouping documents with similar MinHash signatures into the same bands.

---

## Task 2 — Crossover Experiment

I measured brute-force search and LSH at five input sizes: 250, 500, 1000, 2000, and 4000.

The largest measured size was 16 times the smallest size:

4000 / 250 = 16

The results were:

| n | Brute-force time | Brute-force comparisons | LSH time | LSH comparisons |
|---:|---:|---:|---:|---:|
| 250 | 0.19 s | 31,125 | 3.03 s | 1 |
| 500 | 0.74 s | 124,750 | 5.91 s | 7 |
| 1000 | 3.10 s | 499,500 | 11.79 s | 28 |
| 2000 | 12.65 s | 1,999,000 | 23.21 s | 117 |
| 4000 | 13.72 s | 2,246,140 | 24.40 s | 133 |

No crossover was observed within the available dataset range. Brute force was faster in wall-clock time at every measured size.

This is because LSH has preprocessing overhead for computing MinHash signatures and constructing LSH buckets. For a relatively small dataset, this overhead can be larger than the time saved by reducing exact similarity comparisons.

However, at n = 4000, LSH reduced the number of exact comparisons from 2,246,140 to only 133, avoiding approximately 99.99% of the comparisons.

The experiment was performed on:

- CPU: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz
- RAM: 31.67 GB (approximately 32 GB)
- Python: 3.11.9
- OS: Windows

The provided benchmark contains 2,120 documents, so sizes larger than the available dataset cannot be measured directly.

---

## Task 3 — LSH Scaling

I implemented an LSH-based near-duplicate finder using:

- Number of MinHash functions: n = 120
- Number of bands: b = 30
- Rows per band: r = 4

The relationship is:

120 = 30 × 4

Therefore, each LSH band contains 4 MinHash rows.

The LSH candidate probability is:

P(candidate) = 1 - (1 - s^r)^b

With b = 30 and r = 4, the S-curve transition is approximately:

(1 / 30)^(1 / 4) ≈ 0.427

The similarity threshold used by the benchmark is 0.6. This banding configuration provides a high probability of generating candidates for truly similar document pairs while avoiding unnecessary comparisons.

The final benchmark result was:

- Recall: 100.0%
- Precision: 100.0%
- LSH comparisons: 133
- Baseline comparisons: 2,246,140
- Comparisons avoided: 99.99%
- Result: strong

The LSH implementation therefore achieved full recall while dramatically reducing the number of exact similarity comparisons.