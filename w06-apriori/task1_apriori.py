
#!/usr/bin/env python3
"""Week 6 Task 1: A-Priori and association rules."""

import argparse
from collections import Counter
from itertools import combinations

BASKETS = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "egg"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
    {"bread", "milk", "beer"},
    {"diaper", "beer"},
]


def frequent_singletons(baskets, support):
    """Return frequent items and their occurrence counts."""
    counts = Counter()
    for basket in baskets:
        counts.update(basket)

    return {
        item: count
        for item, count in counts.items()
        if count >= support
    }


def frequent_pairs(baskets, support):
    """Find frequent pairs using the A-Priori two-pass strategy."""
    single_counts = frequent_singletons(baskets, support)
    frequent_items = set(single_counts)

    pair_counts = Counter()

    for basket in baskets:
        items = sorted(basket & frequent_items)

        for pair in combinations(items, 2):
            pair_counts[frozenset(pair)] += 1

    return {
        pair: count
        for pair, count in pair_counts.items()
        if count >= support
    }


def association_rules(baskets, support, min_confidence):
    """Return (antecedent, consequent, confidence, lift) rules."""
    n = len(baskets)
    if n == 0:
        return []

    single_counts = frequent_singletons(baskets, support)
    pairs = frequent_pairs(baskets, support)
    rules = []

    for pair, pair_count in pairs.items():
        i, j = sorted(pair)

        # Rule i -> j
        confidence = pair_count / single_counts[i]
        lift = confidence / (single_counts[j] / n)

        if confidence >= min_confidence:
            rules.append((i, j, confidence, lift))

        # Rule j -> i
        confidence = pair_count / single_counts[j]
        lift = confidence / (single_counts[i] / n)

        if confidence >= min_confidence:
            rules.append((j, i, confidence, lift))

    rules.sort(key=lambda rule: (-rule[2], rule[0], rule[1]))
    return rules


def verify():
    fails = 0

    def check(label, got, want):
        nonlocal fails
        ok = got == want
        print(
            f"  {'ok  ' if ok else 'FAIL'}  {label:<44} {got}"
            + ("" if ok else f"\n{'':>54}want {want}")
        )
        if not ok:
            fails += 1

    singles = frequent_singletons(BASKETS, 3)
    check(
        "frequent singletons at support 3",
        dict(sorted(singles.items())),
        {"beer": 5, "bread": 5, "diaper": 5, "milk": 5},
    )

    pairs = frequent_pairs(BASKETS, 3)
    got = {tuple(sorted(pair)): count for pair, count in pairs.items()}

    check(
        "frequent pairs at support 3",
        dict(sorted(got.items())),
        {
            ("beer", "bread"): 3,
            ("beer", "diaper"): 4,
            ("beer", "milk"): 3,
            ("bread", "diaper"): 3,
            ("bread", "milk"): 4,
            ("diaper", "milk"): 3,
        },
    )

    check(
        "infrequent items excluded from pairs",
        any("cola" in pair or "egg" in pair for pair in pairs),
        False,
    )

    rules = association_rules(BASKETS, 3, 0.75)
    hit = [
        rule for rule in rules
        if rule[0] == "diaper" and rule[1] == "beer"
    ]

    check(
        "diaper -> beer confidence",
        round(hit[0][2], 3) if hit else None,
        0.8,
    )

    check(
        "rules are sorted by confidence",
        all(
            rules[i][2] >= rules[i + 1][2]
            for i in range(len(rules) - 1)
        ),
        True,
    )

    print(f"\n  {'all ok' if fails == 0 else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    raise SystemExit(verify() if args.verify else parser.print_help())
