#!/usr/bin/env python3
"""Week 5 · Task 1 — PageRank, and the two ways it breaks."""
import argparse

SIMPLE = {"A": ["B", "C"], "B": ["C"], "C": ["A"]}
DEAD_END = {"A": ["B", "C"], "B": ["C"], "C": []}
SPIDER_TRAP = {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["C"]}


def pagerank(graph, beta=0.85, iterations=100, tol=1e-10):
    """Return normalized PageRank; handle dead ends and teleportation."""
    if not graph:
        pagerank.iterations = 0
        return {}
    if not 0 <= beta < 1:
        raise ValueError("beta must be in [0, 1)")
    nodes = list(graph)
    n = len(nodes)
    ranks = {node: 1.0 / n for node in nodes}
    used = 0

    for step in range(1, iterations + 1):
        dangling = sum(ranks[node] for node in nodes if not graph[node])
        new = {node: (1.0 - beta) / n + beta * dangling / n for node in nodes}
        for source in nodes:
            outs = graph[source]
            if not outs:
                continue
            contribution = beta * ranks[source] / len(outs)
            for target in outs:
                if target in new:
                    new[target] += contribution
        delta = sum(abs(new[node] - ranks[node]) for node in nodes)
        ranks = new
        used = step
        if delta < tol:
            break

    # Remove tiny floating point drift while conserving total probability.
    total = sum(ranks.values())
    if total:
        ranks = {node: value / total for node, value in ranks.items()}
    pagerank.iterations = used
    return ranks


def pagerank_no_teleport(graph, iterations=100):
    """Intentionally broken PageRank: no teleport and no dead-end repair."""
    if not graph:
        return {}
    nodes = list(graph)
    n = len(nodes)
    ranks = {node: 1.0 / n for node in nodes}
    for _ in range(iterations):
        new = {node: 0.0 for node in nodes}
        for source in nodes:
            outs = graph[source]
            if not outs:
                continue  # broken: rank disappears at dead ends
            contribution = ranks[source] / len(outs)
            for target in outs:
                if target in new:
                    new[target] += contribution
        ranks = new
    return ranks


def verify():
    fails = 0
    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<48} {detail}")
        fails += not ok

    r = pagerank(SIMPLE)
    check("ranks sum to 1", abs(sum(r.values()) - 1) < 1e-6, f"{sum(r.values()):.6f}")
    check("every node ranked", set(r) == set(SIMPLE), str(sorted(r)))
    check("C outranks A and B", r["C"] > r["A"] and r["C"] > r["B"], str({k: round(v, 4) for k, v in sorted(r.items())}))
    broken = pagerank_no_teleport(DEAD_END)
    check("without the fix, a dead end drains the graph", sum(broken.values()) < 0.5, f"total rank {sum(broken.values()):.4f}")
    fixed = pagerank(DEAD_END)
    check("with the fix, rank is conserved", abs(sum(fixed.values()) - 1) < 1e-6, f"{sum(fixed.values()):.6f}")
    trapped = pagerank_no_teleport(SPIDER_TRAP)
    check("without the fix, a spider trap takes everything", trapped["C"] + trapped["D"] > 0.95, f"C+D = {trapped['C'] + trapped['D']:.4f}")
    untrapped = pagerank(SPIDER_TRAP)
    check("with the fix, A and B keep some rank", untrapped["A"] > 0.01 and untrapped["B"] > 0.01, str({k: round(v, 4) for k, v in sorted(untrapped.items())}))
    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    raise SystemExit(verify() if args.verify else parser.print_help())
