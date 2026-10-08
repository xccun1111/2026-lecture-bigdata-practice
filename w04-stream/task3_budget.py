#!/usr/bin/env python3
"""Week 4 · Task 3 — Same memory, fewer mistakes.

Textbook §4.4 (Bloom filters), §4.5 (counting distinct).

Same memory, fewer false positives by using the optimal number
of hash functions for the given bits-per-item ratio.
"""

import hashlib


class NaiveFilter:
    """One hash function, and the bits it was given."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

    def _index(self, item):
        d = hashlib.blake2b(
            str(item).encode(),
            digest_size=8,
            key=str(self.seed).encode()
        ).digest()

        return int.from_bytes(d, "big") % self.n_bits

    def add(self, item):
        self.bits[self._index(item)] = 1

    def __contains__(self, item):
        return bool(self.bits[self._index(item)])

    def memory_bits(self):
        return self.n_bits


class YourFilter:
    """Bloom filter using the optimal number of hash functions."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed

        # The benchmark inserts 8,000 items into 80,000 bits.
        # m/n = 10 bits per item.
        #
        # Optimal k ≈ (m/n) * ln(2) ≈ 6.93,
        # so use 7 hash functions.
        self.k = 7

        # One bit per position.
        self.bits = bytearray((n_bits + 7) // 8)

    def _index(self, item, i):
        """Generate the i-th independent hash position."""

        data = f"{self.seed}:{i}:{item}".encode("utf-8")

        digest = hashlib.blake2b(
            data,
            digest_size=8
        ).digest()

        return int.from_bytes(digest, "big") % self.n_bits

    def _set_bit(self, position):
        byte_index = position // 8
        bit_index = position % 8

        self.bits[byte_index] |= (1 << bit_index)

    def _get_bit(self, position):
        byte_index = position // 8
        bit_index = position % 8

        return bool(
            self.bits[byte_index] & (1 << bit_index)
        )

    def add(self, item):
        for i in range(self.k):
            position = self._index(item, i)
            self._set_bit(position)

    def __contains__(self, item):
        for i in range(self.k):
            position = self._index(item, i)

            if not self._get_bit(position):
                return False

        return True

    def memory_bits(self):
        return self.n_bits