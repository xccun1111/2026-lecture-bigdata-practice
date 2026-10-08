# Week 4 — Stream Mining Observations

## Task 1

The Bloom filter produced no false negatives, and its measured false-positive rate (0.855%) was very close to the theoretical prediction (0.861%). The Flajolet-Martin sketch estimates the number of distinct items using trailing-zero statistics, while reservoir sampling keeps a uniform sample using only bounded memory.

## Task 2

The exact set remained fast at 1.6 million stream items and used 51.3 MB of memory, while its memory usage increased substantially with the stream size. The Flajolet-Martin implementation used essentially constant memory, but its runtime became impractical at larger sizes (76,055.08 seconds at 1.6 million items), showing the trade-off between memory and computation.

## Task 3

With the same 80,000-bit memory budget, using 7 hash functions reduced the false-positive rate from 9.511% to 0.856%, a 91.0% reduction, while keeping false negatives at zero. The optimal number of hash functions depends on the bits-per-item ratio; when the stream size is unknown, the filter could be resized or configured conservatively as the number of inserted items grows.
