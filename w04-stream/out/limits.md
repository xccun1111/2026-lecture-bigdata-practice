powershell -Command "@'
# Task 2 — Memory and Accuracy Limits

| n | Exact memory | Exact time | FM memory | FM time | FM ratio |
|---:|---:|---:|---:|---:|---:|
| 100,000 | 4.2 MB | 0.49 s | 0.00 MB | 58.97 s | 1.90x |
| 200,000 | 6.3 MB | 0.76 s | 0.00 MB | 109.71 s | 2.23x |
| 400,000 | 12.8 MB | 1.73 s | 0.00 MB | 403.54 s | 3.01x |
| 1,600,000 | 51.3 MB | 6.45 s | 0.00 MB | 76055.08 s | 2.73x |

## A2 — Where it became unpleasant

At 1.6 million stream items, the exact set still completed in 6.45 seconds and used 51.3 MB, so the exact method had not yet exhausted the machine. However, the Flajolet-Martin implementation became computationally impractical at this scale, taking 76,055 seconds (about 21 hours).

## A4 — Memory growth

The exact set's memory increased from 4.2 MB at 100,000 items to 51.3 MB at 1,600,000 items. The FM sketch used essentially constant measured memory.

## A5 — Accuracy

The FM ratios were 1.90x, 2.23x, 3.01x, and 2.73x across the four measurements. The estimates were therefore rough and did not consistently remain within a factor of two.

## A6 — Machine

Platform: Windows, Python 3.11.9. CPU: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz. RAM: 31.67 GB.
'@ | Set-Content -Encoding UTF8 w04-stream\out\limits.md"