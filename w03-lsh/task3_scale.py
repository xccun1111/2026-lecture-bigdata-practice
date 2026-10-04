#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """LSH-based near-duplicate finder."""

    def __init__(self, threshold):
        self.threshold = threshold

        # 120 MinHash functions split into 30 bands.
        # Each band contains 4 rows.
        self.n_hashes = 120
        self.bands = 30
        self.rows_per_band = self.n_hashes // self.bands

        # Prime larger than the shingle vocabulary (0..4999).
        self.prime = 10007

        # Deterministic hash parameters.
        self.a = [
            (i * 7919 + 1237) % self.prime
            for i in range(self.n_hashes)
        ]
        self.b = [
            (i * 104729 + 4321) % self.prime
            for i in range(self.n_hashes)
        ]

    def _signature(self, doc):
        """Compute a 120-value MinHash signature for one document."""
        sig = [self.prime] * self.n_hashes

        for x in doc:
            for h in range(self.n_hashes):
                value = (self.a[h] * x + self.b[h]) % self.prime

                if value < sig[h]:
                    sig[h] = value

        return sig

    def find(self, docs, similarity):
        """Use LSH to generate candidates, then verify only candidates."""
        signatures = [self._signature(doc) for doc in docs]

        candidates = set()

        for band in range(self.bands):
            start = band * self.rows_per_band
            end = start + self.rows_per_band

            buckets = {}

            for i, sig in enumerate(signatures):
                key = tuple(sig[start:end])

                if key not in buckets:
                    buckets[key] = []

                buckets[key].append(i)

            for indices in buckets.values():
                if len(indices) < 2:
                    continue

                for x in range(len(indices)):
                    for y in range(x + 1, len(indices)):
                        i = indices[x]
                        j = indices[y]

                        if i > j:
                            i, j = j, i

                        candidates.add((i, j))

        result = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                result.add((i, j))

        return result