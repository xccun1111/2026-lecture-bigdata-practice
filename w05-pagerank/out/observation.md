# Week 05 Observations

## Task 1 — PageRank and its failures

In the broken version, rank reaching a dead end disappears because that page has no outgoing links; the repaired version redistributes that dangling rank uniformly across all nodes. Uniform teleportation also lets a surfer leave a spider trap, so the same fix both conserves total rank and prevents a closed group from absorbing everything.

The parameter β is the probability that the random surfer follows a link; with probability 1−β, the surfer teleports to a uniformly selected page.

## Task 2 — Convergence

As β approaches 1, convergence generally requires more iterations because teleportation becomes weaker and the update contracts more slowly. Graph size mainly increases the work per iteration and wall-clock time, while iteration count is more strongly affected by β and the tolerance; the exact measured counts and top-10 change point are recorded in `convergence.md`.

For the timing experiment, record any other applications running on the computer in `convergence.md` under A7; CPU and RAM are detected automatically.

## Task 3 — Sparse PageRank

The sparse implementation stores the adjacency list and two length-n rank vectors instead of an n×n transition matrix, so its rank-vector storage is about 2n floats rather than n² matrix floats. Teleportation adds the same scalar (1−β)/n to every node, and dead-end redistribution adds another uniform scalar; these can be combined into a per-node base value without constructing a dense matrix.

The worst per-node difference from the dense baseline is printed by `python w05-pagerank\bench.py --yours` and saved in `bench.txt`; small nonzero differences can arise from floating-point addition order.
