"""
sylow.py
--------
Sylow p-subgroup search.

By Sylow's first theorem, if p^k is the largest power of a prime p dividing
|G|, then G has a subgroup of order p^k (a Sylow p-subgroup), and every
p-subgroup of G is contained in one. This module finds all Sylow p-subgroups
by filtering FiniteGroup.all_subgroups() for the maximal p-power order --
no separate search algorithm is needed since all_subgroups() already
enumerates every subgroup.
"""

from __future__ import annotations

from .group import FiniteGroup


def p_part(n: int, p: int) -> int:
    """The largest power of p dividing n."""
    k = 1
    while n % (k * p) == 0:
        k *= p
    return k


def sylow_subgroups(group: FiniteGroup, p: int) -> set:
    """All Sylow p-subgroups of `group` (subgroups of the maximal p-power order)."""
    target_order = p_part(group.n, p)
    return {sg for sg in group.all_subgroups() if len(sg) == target_order}


def sylow_summary(group: FiniteGroup, p: int) -> dict:
    """
    Diagnostic summary of the Sylow p-subgroups of `group`, including a check
    of Sylow's third theorem: the number n_p of Sylow p-subgroups satisfies
    n_p == 1 (mod p) and n_p divides |G| / p^k.
    """
    order = group.n
    k = 0
    m = order
    while m % p == 0:
        m //= p
        k += 1
    target_order = p ** k

    subgroups = sylow_subgroups(group, p)
    n_p = len(subgroups)

    return {
        "p": p,
        "group_order": order,
        "p_power": target_order,
        "cofactor": m,
        "num_sylow_subgroups": n_p,
        "congruent_to_1_mod_p": (n_p % p == 1) if k > 0 else True,
        "divides_cofactor": (m % n_p == 0) if n_p > 0 else False,
        "all_conjugate": _all_conjugate(group, subgroups),
    }


def _all_conjugate(group: FiniteGroup, subgroups) -> bool:
    """Sylow's second theorem: all Sylow p-subgroups are conjugate to one another."""
    subgroups = list(subgroups)
    if len(subgroups) <= 1:
        return True
    first = subgroups[0]
    for other in subgroups[1:]:
        if not any(
            frozenset(group.conjugate(a, g) for a in first) == other
            for g in range(group.n)
        ):
            return False
    return True
