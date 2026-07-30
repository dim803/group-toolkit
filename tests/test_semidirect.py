import pytest

from group_toolkit import (
    cyclic_group,
    dihedral_group,
    is_isomorphic,
    semidirect_product,
    inversion_action,
)
from group_toolkit.group import GroupAxiomError


def test_semidirect_reconstructs_dihedral_group_small_cases():
    # is_isomorphic is O(n!); keep this check within its documented safe
    # range (order <= 8) rather than hitting the same combinatorial wall
    # described in the README's "known limitations" section.
    for n in [3, 4]:
        zn = cyclic_group(n)
        z2 = cyclic_group(2)
        semi = semidirect_product(zn, z2, inversion_action(n))
        dn = dihedral_group(n)
        assert semi.n == dn.n == 2 * n
        assert is_isomorphic(semi, dn)


def test_semidirect_reconstructs_dihedral_group_structurally_for_larger_n():
    # For larger n, skip the expensive brute-force isomorphism check and
    # instead verify the structural properties that pin down D_n: correct
    # order, non-abelian, and matching multiset of element orders (a cheap
    # isomorphism invariant).
    for n in [5, 6, 8]:
        zn = cyclic_group(n)
        z2 = cyclic_group(2)
        semi = semidirect_product(zn, z2, inversion_action(n))
        dn = dihedral_group(n)
        assert semi.n == dn.n == 2 * n
        assert semi.is_abelian() == dn.is_abelian() == False
        semi_orders = sorted(semi.order_of_element(x) for x in range(semi.n))
        dn_orders = sorted(dn.order_of_element(x) for x in range(dn.n))
        assert semi_orders == dn_orders


def test_semidirect_with_trivial_action_is_direct_product():
    # if the action is trivial (every h acts as the identity automorphism),
    # the semidirect product is just the direct product
    from group_toolkit import direct_product

    z3 = cyclic_group(3)
    z2 = cyclic_group(2)
    trivial_action = [list(range(z3.n))] * z2.n
    semi = semidirect_product(z3, z2, trivial_action)
    direct = direct_product(z3, z2)
    assert is_isomorphic(semi, direct)


def test_semidirect_rejects_non_bijective_action():
    z4 = cyclic_group(4)
    z2 = cyclic_group(2)
    bad_action = [[0, 1, 2, 3], [0, 0, 0, 0]]
    with pytest.raises(GroupAxiomError):
        semidirect_product(z4, z2, bad_action)


def test_semidirect_rejects_non_automorphism_action():
    z4 = cyclic_group(4)
    z2 = cyclic_group(2)
    # a bijection of Z4's elements that is not a group automorphism
    bad_action = [[0, 1, 2, 3], [1, 0, 3, 2]]
    with pytest.raises(GroupAxiomError):
        semidirect_product(z4, z2, bad_action)


def test_semidirect_rejects_action_not_a_homomorphism():
    # action[H.identity] must be the identity automorphism
    z3 = cyclic_group(3)
    z2 = cyclic_group(2)
    bad_action = [[1, 2, 0], [0, 1, 2]]  # action[0] is not the identity map
    with pytest.raises(GroupAxiomError):
        semidirect_product(z3, z2, bad_action)
