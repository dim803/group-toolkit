"""
constructions.py
-----------------
Standard finite groups, built as Cayley tables for use with FiniteGroup.
"""

from __future__ import annotations
from itertools import permutations as _permutations

from .group import FiniteGroup


def cyclic_group(n: int) -> FiniteGroup:
    """Z/nZ under addition mod n."""
    table = [[(i + j) % n for j in range(n)] for i in range(n)]
    labels = [str(i) for i in range(n)]
    return FiniteGroup(table, labels=labels)


def dihedral_group(n: int) -> FiniteGroup:
    """
    D_n, the symmetries of a regular n-gon: n rotations and n reflections,
    order 2n. Elements are indexed 0..n-1 for rotations r^0..r^(n-1), and
    n..2n-1 for reflections s*r^0..s*r^(n-1).

    Multiplication uses the standard relation s*r^k = r^(-k)*s, giving, for
    elements (a, e1) and (b, e2) with e in {0, 1} marking a reflection:

        e1 = 0:  (a, 0)*(b, e2) = (a+b mod n, e2)
        e1 = 1:  (a, 1)*(b, e2) = (a-b mod n, 1 - e2)
    """
    if n < 3:
        raise ValueError("dihedral group is usually defined for n >= 3")
    order = 2 * n

    def to_idx(e: int, a: int) -> int:
        return e * n + (a % n)

    def from_idx(idx: int):
        e, a = divmod(idx, n)
        return e, a

    table = [[0] * order for _ in range(order)]
    for i in range(order):
        e1, a1 = from_idx(i)
        for j in range(order):
            e2, a2 = from_idx(j)
            if e1 == 0:
                e, a = e2, (a1 + a2) % n
            else:
                e, a = 1 - e2, (a1 - a2) % n
            table[i][j] = to_idx(e, a)

    def label(idx: int) -> str:
        e, a = from_idx(idx)
        if e == 0:
            return "e" if a == 0 else f"r^{a}"
        return "s" if a == 0 else f"s*r^{a}"

    labels = [label(i) for i in range(order)]
    return FiniteGroup(table, labels=labels)


def symmetric_group(n: int) -> FiniteGroup:
    """S_n, all permutations of {0, ..., n-1} under composition (f*g)(x) = f(g(x))."""
    perms = list(_permutations(range(n)))
    index = {p: i for i, p in enumerate(perms)}

    def compose(f, g):
        return tuple(f[g[x]] for x in range(n))

    table = [
        [index[compose(perms[i], perms[j])] for j in range(len(perms))]
        for i in range(len(perms))
    ]
    labels = [str(p) for p in perms]
    return FiniteGroup(table, labels=labels)


def direct_product(g1: FiniteGroup, g2: FiniteGroup) -> FiniteGroup:
    """G1 x G2, with (a1,b1)*(a2,b2) = (a1*a2, b1*b2)."""
    n1, n2 = g1.n, g2.n

    def idx(i, j):
        return i * n2 + j

    table = [[0] * (n1 * n2) for _ in range(n1 * n2)]
    for i1 in range(n1):
        for j1 in range(n2):
            row = idx(i1, j1)
            for i2 in range(n1):
                for j2 in range(n2):
                    col = idx(i2, j2)
                    table[row][col] = idx(g1.table[i1][i2], g2.table[j1][j2])

    labels = [f"({g1.labels[i]}, {g2.labels[j]})" for i in range(n1) for j in range(n2)]
    return FiniteGroup(table, labels=labels)


def klein_four_group() -> FiniteGroup:
    """V4 = Z/2 x Z/2, the smallest non-cyclic group."""
    return direct_product(cyclic_group(2), cyclic_group(2))
