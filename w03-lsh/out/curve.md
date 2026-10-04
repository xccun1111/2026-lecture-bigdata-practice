# Task 2 — Crossover Experiment

## A1. Measurement sizes

I measured the running time at five input sizes:

- n = 250
- n = 500
- n = 1000
- n = 2000
- n = 4000

The largest size is 16 times the smallest size (4000 / 250 = 16).

## A2. Measurement results

| n | Brute-force time | Brute-force comparisons | LSH time | LSH comparisons |
|---:|---:|---:|---:|---:|
| 250 | 0.19 s | 31,125 | 3.03 s | 1 |
| 500 | 0.74 s | 124,750 | 5.91 s | 7 |
| 1000 | 3.10 s | 499,500 | 11.79 s | 28 |
| 2000 | 12.65 s | 1,999,000 | 23.21 s | 117 |
| 4000 | 13.72 s | 2,246,140 | 24.40 s | 133 |

## A3. Crossover

No crossover was observed within the measured range of n = 250 to n = 4000.

Brute force was faster at every measured size. At n = 4000, brute force took 13.72 s, while LSH took 24.40 s.

## A4. Why LSH is slower at small n

LSH has a fixed preprocessing cost for computing MinHash signatures and constructing the LSH buckets. For small datasets, this overhead is larger than the cost saved by avoiding pairwise similarity comparisons.

## A5. Why LSH still reduces comparisons

Although LSH was slower in wall-clock time in this experiment, it reduced the number of exact similarity comparisons dramatically.

At n = 4000:

- Brute force: 2,246,140 comparisons
- LSH: 133 comparisons

Therefore, LSH avoided approximately 99.99% of the pairwise comparisons.

## A6. Experimental environment

- CPU: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz
- RAM: 31.67 GB (approximately 32 GB)
- OS: Windows
- Python: Python 3.11.9

## A7. Interpretation

The experiment shows that reducing the number of similarity comparisons does not necessarily mean lower total running time for a small dataset. LSH introduces preprocessing and hashing overhead.

For this dataset, brute force was still faster up to n = 4000. However, LSH reduced the number of exact comparisons by 99.99%, which suggests that its advantage can become more important as the dataset becomes larger.

## A8. Conclusion

The crossover point was not reached within the available dataset size. The measured range was limited to 2,120 documents because the provided benchmark dataset contains 2,120 documents.

Therefore, this experiment demonstrates the trade-off between preprocessing overhead and the reduction of pairwise comparisons, rather than directly observing the crossover point.