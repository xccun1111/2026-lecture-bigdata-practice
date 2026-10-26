
# Week 06 Lab Observations

## Task 1 — A-Priori and Association Rules

A-Priori first filters infrequent items and then counts pairs
containing only frequent items, reducing unnecessary pair counting.
The verification confirmed the expected frequent pairs and the
confidence of diaper -> beer was 0.8.

## Task 2 — Threshold Explosion

When support decreased to [actual support], peak counters increased
from [actual value] to [actual value], while frequent-pair counts
changed from [actual value] to [actual value].
I stopped at [actual support] because [actual observation].

## Task 3 — PCY

PCY found the same 6,397 frequent pairs as the baseline, with no missing or extra pairs, while reducing peak pair counters from 820,259 to 148,468 (an 81.9% reduction). However, runtime increased from about 1.4 seconds to 6.7 seconds in this run.

The hash bucket array requires memory during pass one, but it is released before pass two and replaced by a bitmap. Therefore, fewer pair counters do not necessarily mean faster execution or lower total peak memory.
