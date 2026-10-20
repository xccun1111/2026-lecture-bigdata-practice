# Week 05 — PageRank convergence report

Generated from the local experiments in `convergence.json`. Timings depend on the machine.

## Machine

- Platform: Windows-10-10.0.26200-SP0
- CPU: Intel64 Family 6 Model 141 Stepping 1, GenuineIntel
- Logical CPUs: 16
- RAM: 31.67 GB

## Runs

| Nodes | β | Tolerance | Iterations | Seconds | Top 3 nodes |
|---:|---:|---:|---:|---:|---|
| 1200 | 0.5 | 1e-10 | 14 | 0.030 | p00009, p00001, p00006 |
| 1200 | 0.7 | 1e-10 | 17 | 0.029 | p00009, p00001, p00006 |
| 1200 | 0.85 | 1e-10 | 20 | 0.031 | p00009, p00001, p00006 |
| 1200 | 0.95 | 1e-10 | 23 | 0.026 | p00009, p00001, p00006 |
| 1200 | 0.99 | 1e-10 | 24 | 0.028 | p00009, p00001, p00006 |
| 20000 | 0.85 | 1e-10 | 21 | 0.606 | p00009, p00001, p00006 |
| 20000 | 0.95 | 1e-10 | 24 | 0.843 | p00009, p00001, p00006 |
| 1200 | 0.85 | 1e-06 | 12 | 0.024 | p00009, p00001, p00006 |

## A3 — Shape of the convergence curve

As β approaches 1, convergence generally takes more iterations: the teleportation contribution (1−β)/n becomes smaller, and the iteration operator contracts more slowly. If a run reaches the 500-iteration limit, it has hit the cap rather than necessarily meeting the tolerance.

## A4 — Graph size versus time

The iteration count is mainly governed by β, the graph structure, and the tolerance; it does not normally grow in direct proportion to node count. Wall time does grow with graph size because each iteration processes nodes and edges. Compare runs with the same β and tolerance at different node counts in the table above.

## A5 — Tolerance

Compare runs with the same node count and β=0.85 at different tolerances. A stricter tolerance usually requires more iterations; the actual extra iterations are shown below.
- Nodes=1200, β=0.85: tolerance 1e-10 → 20 iterations; tolerance 1e-06 → 12 iterations; difference = 8 iterations.

## A6 — Top-10 ranking stability

Top-10 order is compared across β values for each fixed graph size and tolerance. The first β whose ordered top-10 list differs from the lowest-β run is reported below.
- Nodes=1200, tol=1e-10: first change relative to β=0.5 occurs at β=0.7.
- Nodes=20000, tol=1e-10: no top-10 order change among the recorded β values.

## A7 — Other running applications

Record what else was running during the timing tests (for example, VS Code, a browser, or other heavy applications). CPU and RAM are detected automatically; running applications are not.
