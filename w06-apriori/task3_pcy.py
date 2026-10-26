
#!/usr/bin/env python3
"""Week 6 Task 3: PCY frequent-pair mining."""

from collections import Counter
from itertools import combinations


class PlainApriori:
    """Baseline implementation for comparison."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()

        for basket in baskets:
            counts.update(basket)

        frequent_items = {
            item for item, count in counts.items()
            if count >= self.support
        }

        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent_items)

            for pair in combinations(items, 2):
                pair_counts[pair] += 1

            self.peak_counters = max(
                self.peak_counters, len(pair_counts)
            )

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= self.support
        }


class YourAlgorithm:
    """PCY algorithm using hash buckets and a bitmap."""

    BUCKETS = 100_003

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    
    @staticmethod
    def hash_pair(a, b):
        """Map an unordered pair to a deterministic bucket."""
        if a > b:
            a, b = b, a

        value = 0
        for char in f"{a}\0{b}":
            value = (value * 31 + ord(char)) % 2_147_483_647

        return value % YourAlgorithm.BUCKETS


    def run(self, baskets):
        bucket_count = self.BUCKETS

        # Pass 1: count items and hash buckets for all pairs.
        item_counts = Counter()
        bucket_counts = [0] * bucket_count

        for basket in baskets:
            item_counts.update(basket)

            for a, b in combinations(sorted(basket), 2):
                bucket = self.hash_pair(a, b)
                bucket_counts[bucket] += 1

        frequent_items = {
            item for item, count in item_counts.items()
            if count >= self.support
        }

        # Convert bucket counts into a compact bitmap.
        bitmap = bytearray((bucket_count + 7) // 8)

        for bucket, count in enumerate(bucket_counts):
            if count >= self.support:
                bitmap[bucket >> 3] |= 1 << (bucket & 7)

        # Release the full bucket-count array before pass 2.
        del bucket_counts

        # Pass 2: count only frequent-item pairs in frequent buckets.
        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent_items)

            for a, b in combinations(items, 2):
                bucket = self.hash_pair(a, b)

                if not (
                    bitmap[bucket >> 3] & (1 << (bucket & 7))
                ):
                    continue

                pair_counts[(a, b)] += 1

            self.peak_counters = max(
                self.peak_counters, len(pair_counts)
            )

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= self.support
        }
