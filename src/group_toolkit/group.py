"""
group.py
--------
FiniteGroup: a finite group given by its Cayley table (multiplication table),
with axiom validation, subgroup/coset/normality machinery, conjugacy classes,
quotient groups, and a brute-force isomorphism check.

Elements are represented internally as integers 0, ..., n-1. `labels[i]` gives
a human-readable name for element i (defaults to str(i)).
"""

from __future__ import annotations
from itertools import permutations


class GroupAxiomError(ValueError):
    """Raised when a supplied Cayley table does not define a group."""


class FiniteGroup:
    def __init__(self, table: list[list[int]], labels: list[str] | None = None):
        self.n = len(table)
        self.table = table
        self.labels = labels if labels is not None else [str(i) for i in range(self.n)]
        self._validate_table_shape()
        self.identity = self._find_identity()
        self._validate_inverses()
        self._validate_associativity()

    # ------------------------------------------------------------------ #
    # Construction / validation
    # ------------------------------------------------------------------ #

    def _validate_table_shape(self) -> None:
        if self.n == 0:
            raise GroupAxiomError("a group must have at least one element")
        for row in self.table:
            if len(row) != self.n:
                raise GroupAxiomError("Cayley table must be square")
            for v in row:
                if not (0 <= v < self.n):
                    raise GroupAxiomError("Cayley table entries must be valid element indices")
        if len(self.labels) != self.n:
            raise GroupAxiomError("labels must have one entry per element")

    def _find_identity(self) -> int:
        for e in range(self.n):
            if all(self.table[e][x] == x and self.table[x][e] == x for x in range(self.n)):
                return e
        raise GroupAxiomError("no identity element found")

    def _validate_inverses(self) -> None:
        for x in range(self.n):
            if not any(
                self.table[x][y] == self.identity and self.table[y][x] == self.identity
                for y in range(self.n)
            ):
                raise GroupAxiomError(f"element {self.labels[x]} has no inverse")

    def _validate_associativity(self) -> None:
        n, table = self.n, self.table
        for a in range(n):
            for b in range(n):
                ab = table[a][b]
                for c in range(n):
                    if table[ab][c] != table[a][table[b][c]]:
                        raise GroupAxiomError(
                            f"associativity fails for ({self.labels[a]}, "
                            f"{self.labels[b]}, {self.labels[c]})"
                        )

    # ------------------------------------------------------------------ #
    # Basic operations
    # ------------------------------------------------------------------ #

    def multiply(self, a: int, b: int) -> int:
        return self.table[a][b]

    def inverse(self, a: int) -> int:
        for y in range(self.n):
            if self.table[a][y] == self.identity:
                return y
        raise GroupAxiomError(f"no inverse found for {self.labels[a]}")  # unreachable post-init

    def power(self, a: int, k: int) -> int:
        """a**k, for any integer k (negative k uses the inverse)."""
        if k < 0:
            return self.power(self.inverse(a), -k)
        result = self.identity
        for _ in range(k):
            result = self.multiply(result, a)
        return result

    def order_of_element(self, a: int) -> int:
        x, k = a, 1
        while x != self.identity:
            x = self.multiply(x, a)
            k += 1
        return k

    def is_abelian(self) -> bool:
        return all(
            self.table[a][b] == self.table[b][a]
            for a in range(self.n) for b in range(a + 1, self.n)
        )

    def is_cyclic(self) -> bool:
        return any(self.order_of_element(a) == self.n for a in range(self.n))

    # ------------------------------------------------------------------ #
    # Subgroups
    # ------------------------------------------------------------------ #

    def generate_subgroup(self, generators) -> frozenset:
        """The smallest subgroup containing the given elements (closure)."""
        elements = {self.identity, *generators}
        changed = True
        while changed:
            changed = False
            current = list(elements)  # snapshot: never iterate a set while mutating it
            for a in current:
                for b in current:
                    prod = self.multiply(a, b)
                    if prod not in elements:
                        elements.add(prod)
                        changed = True
        return frozenset(elements)

    def all_subgroups(self) -> set:
        """
        All subgroups of G, found by taking cyclic subgroups of every element
        and then repeatedly closing pairs of known subgroups under generation
        until no new subgroup appears. Practical for |G| up to a few dozen.
        """
        subgroups = {frozenset({self.identity})}
        for a in range(self.n):
            subgroups.add(self.generate_subgroup({a}))

        changed = True
        while changed:
            changed = False
            current = list(subgroups)
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    combined = self.generate_subgroup(current[i] | current[j])
                    if combined not in subgroups:
                        subgroups.add(combined)
                        changed = True
        return subgroups

    def is_subgroup(self, subset) -> bool:
        subset = set(subset)
        if self.identity not in subset:
            return False
        return all(
            self.multiply(a, self.inverse(b)) in subset
            for a in subset for b in subset
        )

    # ------------------------------------------------------------------ #
    # Cosets and normality
    # ------------------------------------------------------------------ #

    def left_coset(self, subgroup, g: int) -> frozenset:
        return frozenset(self.multiply(g, h) for h in subgroup)

    def right_coset(self, subgroup, g: int) -> frozenset:
        return frozenset(self.multiply(h, g) for h in subgroup)

    def left_cosets(self, subgroup) -> list[frozenset]:
        subgroup = frozenset(subgroup)
        seen, cosets = set(), []
        for g in range(self.n):
            if g in seen:
                continue
            coset = self.left_coset(subgroup, g)
            cosets.append(coset)
            seen |= coset
        return cosets

    def is_normal(self, subgroup) -> bool:
        subgroup = frozenset(subgroup)
        return all(
            self.left_coset(subgroup, g) == self.right_coset(subgroup, g)
            for g in range(self.n)
        )

    # ------------------------------------------------------------------ #
    # Conjugacy and the center
    # ------------------------------------------------------------------ #

    def conjugate(self, a: int, g: int) -> int:
        """g a g^{-1}."""
        return self.multiply(self.multiply(g, a), self.inverse(g))

    def conjugacy_class(self, a: int) -> frozenset:
        return frozenset(self.conjugate(a, g) for g in range(self.n))

    def conjugacy_classes(self) -> list[frozenset]:
        seen, classes = set(), []
        for a in range(self.n):
            if a in seen:
                continue
            cls = self.conjugacy_class(a)
            classes.append(cls)
            seen |= cls
        return classes

    def center(self) -> frozenset:
        return frozenset(
            a for a in range(self.n)
            if all(self.table[a][x] == self.table[x][a] for x in range(self.n))
        )

    # ------------------------------------------------------------------ #
    # Quotient groups
    # ------------------------------------------------------------------ #

    def quotient_group(self, normal_subgroup) -> "FiniteGroup":
        if not self.is_normal(normal_subgroup):
            raise GroupAxiomError("quotient requires a normal subgroup")
        cosets = self.left_cosets(normal_subgroup)
        index = {coset: i for i, coset in enumerate(cosets)}

        def coset_of(g: int) -> frozenset:
            return self.left_coset(normal_subgroup, g)

        m = len(cosets)
        table = [[0] * m for _ in range(m)]
        for i, ci in enumerate(cosets):
            rep_i = next(iter(ci))
            for j, cj in enumerate(cosets):
                rep_j = next(iter(cj))
                product_coset = coset_of(self.multiply(rep_i, rep_j))
                table[i][j] = index[product_coset]

        labels = [
            "{" + ", ".join(self.labels[e] for e in sorted(c)) + "}"
            for c in cosets
        ]
        return FiniteGroup(table, labels=labels)

    # ------------------------------------------------------------------ #
    # Display
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return f"FiniteGroup(order={self.n}, abelian={self.is_abelian()})"


def is_isomorphic(g1: FiniteGroup, g2: FiniteGroup) -> bool:
    """
    Brute-force isomorphism test: tries every bijection sending g1's identity
    to g2's identity and checks the homomorphism property. Fine for small
    groups (this project uses it on groups of order <= 8).
    """
    if g1.n != g2.n:
        return False
    n = g1.n
    g1_rest = [x for x in range(n) if x != g1.identity]
    g2_rest = [x for x in range(n) if x != g2.identity]

    for perm in permutations(g2_rest):
        mapping = {g1.identity: g2.identity}
        mapping.update(zip(g1_rest, perm))
        if all(
            mapping[g1.multiply(a, b)] == g2.multiply(mapping[a], mapping[b])
            for a in range(n) for b in range(n)
        ):
            return True
    return False
