#!/usr/bin/env python3
"""Week 5 · Task 3 — dense reference and sparse PageRank implementation."""


class DenseMatrix:
    """PageRank as written in the equations. Stores n^2 floats."""
    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta, self.tol, self.max_iter = beta, tol, max_iter

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)
        self._n = n
        if n == 0:
            self.iterations = 0
            return {}
        index = {v: i for i, v in enumerate(nodes)}
        M = [[0.0] * n for _ in range(n)]
        for v, outs in graph.items():
            if outs:
                share = 1.0 / len(outs)
                for w in outs:
                    M[index[w]][index[v]] = share
            else:
                for i in range(n):
                    M[i][index[v]] = 1.0 / n
        r = [1.0 / n] * n
        for self.iterations in range(1, self.max_iter + 1):
            nr = [0.0] * n
            for i in range(n):
                row = M[i]
                s = 0.0
                for j in range(n):
                    if row[j]:
                        s += row[j] * r[j]
                nr[i] = self.beta * s + (1 - self.beta) / n
            delta = sum(abs(a - b) for a, b in zip(nr, r))
            r = nr
            if delta < self.tol:
                break
        return {v: r[index[v]] for v in nodes}

    def memory_floats(self):
        return getattr(self, "_n", 0) ** 2


class YourPageRank:
    """Adjacency-list PageRank; stores rank vectors, not an n-by-n matrix."""
    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta = beta
        self.tol = tol
        self.max_iter = max_iter
        self._n = 0
        self.iterations = 0
        self._memory = 0

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)
        self._n = n
        if n == 0:
            self.iterations = 0
            self._memory = 0
            return {}
        index = {v: i for i, v in enumerate(nodes)}
        # The input is already sparse: retain only the adjacency list and two
        # length-n rank vectors. No transition matrix is constructed.
        r = [1.0 / n] * n
        self._memory = 2 * n
        outdegree = [len(graph[v]) for v in nodes]
        outgoing = [[index[w] for w in graph[v] if w in index] for v in nodes]

        for step in range(1, self.max_iter + 1):
            dangling = sum(r[i] for i, outs in enumerate(outgoing) if not outs)
            base = (1.0 - self.beta) / n + self.beta * dangling / n
            nr = [base] * n
            for i, outs in enumerate(outgoing):
                if not outs:
                    continue
                contribution = self.beta * r[i] / outdegree[i]
                for j in outs:
                    nr[j] += contribution
            delta = sum(abs(a - b) for a, b in zip(nr, r))
            r = nr
            self.iterations = step
            if delta < self.tol:
                break

        # DenseMatrix uses the same iteration equation but sums contributions
        # in a different order, so tiny floating-point differences are normal.
        return {v: r[index[v]] for v in nodes}

    def memory_floats(self):
        # Two persistent length-n vectors: current ranks and next ranks.
        return self._memory
