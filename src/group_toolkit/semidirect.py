"""
semidirect.py
-------------
Semidirect products G semidirect H, built from an action of H on G by
automorphisms.

Given a homomorphism phi: H -> Aut(G), the semidirect product G semidirect_phi H
has underlying set G x H and multiplication

    (g1, h1) * (g2, h2) = (g1 * phi(h1)(g2), h1 * h2).

phi is supplied as `action`: a list of length H.n, where action[h] is itself a
list of length G.n giving the permutation phi(h) applied to G's elements
(i.e. action[h][g] = phi(h)(g)).

For this to define a genuine group, `action` must satisfy:
  1. action[h] is a bijection of {0, ..., G.n - 1} for every h,
  2. action[h] is an automorphism of G: action[h][G.multiply(a,b)]
     == G.multiply(action[h][a], action[h][b]) for all a, b,
  3. h -> action[h] is a homomorphism H -> Aut(G): action[H.identity] is the
     identity permutation, and action[H.multiply(h1,h2)] == the composite
     action[h1] . action[h2].

All three are validated before building the table.
"""

from __future__ import annotations

from .group import FiniteGroup, GroupAxiomError


def _validate_action(G: FiniteGroup, H: FiniteGroup, action) -> None:
    if len(action) != H.n:
        raise GroupAxiomError("action must supply one automorphism per element of H")

    for h, phi_h in enumerate(action):
        if len(phi_h) != G.n or set(phi_h) != set(range(G.n)):
            raise GroupAxiomError(f"action[{h}] is not a permutation of G's elements")
        for a in range(G.n):
            for b in range(G.n):
                if phi_h[G.multiply(a, b)] != G.multiply(phi_h[a], phi_h[b]):
                    raise GroupAxiomError(
                        f"action[{h}] is not an automorphism of G "
                        f"(fails at G-elements {a}, {b})"
                    )

    identity_perm = list(range(G.n))
    if action[H.identity] != identity_perm:
        raise GroupAxiomError("action[H.identity] must be the identity automorphism")

    for h1 in range(H.n):
        for h2 in range(H.n):
            composite = [action[h1][action[h2][g]] for g in range(G.n)]
            if action[H.multiply(h1, h2)] != composite:
                raise GroupAxiomError(
                    "action is not a homomorphism H -> Aut(G) "
                    f"(fails at H-elements {h1}, {h2})"
                )


def semidirect_product(G: FiniteGroup, H: FiniteGroup, action) -> FiniteGroup:
    """G semidirect H, with H acting on G via `action` (see module docstring)."""
    _validate_action(G, H, action)

    def idx(g: int, h: int) -> int:
        return g * H.n + h

    order = G.n * H.n
    table = [[0] * order for _ in range(order)]
    for g1 in range(G.n):
        for h1 in range(H.n):
            row = idx(g1, h1)
            phi_h1 = action[h1]
            for g2 in range(G.n):
                for h2 in range(H.n):
                    col = idx(g2, h2)
                    new_g = G.multiply(g1, phi_h1[g2])
                    new_h = H.multiply(h1, h2)
                    table[row][col] = idx(new_g, new_h)

    labels = [f"({G.labels[g]}, {H.labels[h]})" for g in range(G.n) for h in range(H.n)]
    return FiniteGroup(table, labels=labels)


def inversion_action(n: int):
    """
    The action of Z/2Z on Z/nZ by inversion (g -> -g mod n): action[0] is the
    identity, action[1] sends g to (n - g) mod n. Feeding this into
    semidirect_product(cyclic_group(n), cyclic_group(2), inversion_action(n))
    reconstructs the dihedral group D_n.
    """
    identity_perm = list(range(n))
    inversion_perm = [(-g) % n for g in range(n)]
    return [identity_perm, inversion_perm]
