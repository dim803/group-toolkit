import pytest

from group_toolkit import (
    FiniteGroup,
    GroupAxiomError,
    is_isomorphic,
    cyclic_group,
    dihedral_group,
    symmetric_group,
    direct_product,
    klein_four_group,
)


# ---------------------------------------------------------------------- #
# Axiom validation
# ---------------------------------------------------------------------- #

def test_valid_table_accepted():
    table = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]  # Z3
    g = FiniteGroup(table)
    assert g.n == 3
    assert g.identity == 0


def test_table_with_no_identity_rejected():
    table = [[1, 2, 0], [0, 1, 2], [2, 0, 1]]  # a Latin square, no identity
    with pytest.raises(GroupAxiomError):
        FiniteGroup(table)


def test_non_associative_table_rejected():
    table = [[0, 1, 2], [1, 0, 2], [2, 2, 2]]
    with pytest.raises(GroupAxiomError):
        FiniteGroup(table)


def test_non_square_table_rejected():
    with pytest.raises(GroupAxiomError):
        FiniteGroup([[0, 1], [1, 0], [0, 1]])


# ---------------------------------------------------------------------- #
# Cyclic groups
# ---------------------------------------------------------------------- #

def test_cyclic_group_properties():
    for n in [1, 2, 3, 6, 10]:
        g = cyclic_group(n)
        assert g.n == n
        assert g.is_abelian()
        assert g.is_cyclic()


def test_cyclic_group_element_orders():
    g = cyclic_group(6)
    # element 1 generates the whole group: order 6
    assert g.order_of_element(1) == 6
    # element 2 has order 3 (2,4,0)
    assert g.order_of_element(2) == 3
    # element 3 has order 2 (3,0)
    assert g.order_of_element(3) == 2


# ---------------------------------------------------------------------- #
# Dihedral groups
# ---------------------------------------------------------------------- #

def test_dihedral_group_order_and_abelian():
    for n in [3, 4, 5, 6]:
        d = dihedral_group(n)
        assert d.n == 2 * n
        assert not d.is_abelian()  # D_n is non-abelian for n >= 3
        assert not d.is_cyclic()


def test_dihedral_rotation_subgroup_is_normal_index_2():
    n = 5
    d = dihedral_group(n)
    rotations = frozenset(range(n))  # indices 0..n-1 are the rotations
    assert d.is_subgroup(rotations)
    assert d.is_normal(rotations)
    assert len(d.left_cosets(rotations)) == 2  # index 2


def test_dihedral_center_parity():
    # D_n has trivial center for odd n, center of order 2 for even n
    d5 = dihedral_group(5)
    assert len(d5.center()) == 1

    d4 = dihedral_group(4)
    assert len(d4.center()) == 2


# ---------------------------------------------------------------------- #
# Symmetric group S3 -- checked against the known subgroup lattice
# ---------------------------------------------------------------------- #

def test_s3_order_and_abelian():
    s3 = symmetric_group(3)
    assert s3.n == 6
    assert not s3.is_abelian()


def test_s3_has_exactly_six_subgroups():
    s3 = symmetric_group(3)
    subgroups = s3.all_subgroups()
    sizes = sorted(len(sg) for sg in subgroups)
    assert sizes == [1, 2, 2, 2, 3, 6]


def test_s3_center_is_trivial():
    s3 = symmetric_group(3)
    assert len(s3.center()) == 1


def test_s3_conjugacy_class_sizes():
    # identity (1), transpositions (3), 3-cycles (2)
    s3 = symmetric_group(3)
    sizes = sorted(len(c) for c in s3.conjugacy_classes())
    assert sizes == [1, 2, 3]


def test_s3_order_three_subgroup_is_normal_order_two_is_not():
    s3 = symmetric_group(3)
    subgroups = s3.all_subgroups()
    order3 = next(sg for sg in subgroups if len(sg) == 3)
    order2 = next(sg for sg in subgroups if len(sg) == 2)
    assert s3.is_normal(order3)
    assert not s3.is_normal(order2)


# ---------------------------------------------------------------------- #
# Quotient groups
# ---------------------------------------------------------------------- #

def test_quotient_of_z6_by_order_two_subgroup_is_z3():
    z6 = cyclic_group(6)
    subgroup = z6.generate_subgroup({3})  # {0, 3}, order 2
    assert z6.is_normal(subgroup)  # abelian, so every subgroup is normal
    q = z6.quotient_group(subgroup)
    assert q.n == 3
    assert q.is_cyclic()


def test_quotient_requires_normal_subgroup():
    s3 = symmetric_group(3)
    subgroups = s3.all_subgroups()
    order2 = next(sg for sg in subgroups if len(sg) == 2)
    with pytest.raises(GroupAxiomError):
        s3.quotient_group(order2)


def test_d4_mod_center_is_klein_four():
    # Classical fact: D4 / Z(D4) is isomorphic to the Klein four-group.
    d4 = dihedral_group(4)
    z = d4.center()
    q = d4.quotient_group(z)
    v4 = klein_four_group()
    assert q.n == 4
    assert q.is_abelian()
    assert not q.is_cyclic()
    assert is_isomorphic(q, v4)


# ---------------------------------------------------------------------- #
# Direct products and isomorphism
# ---------------------------------------------------------------------- #

def test_klein_four_is_not_cyclic():
    v4 = klein_four_group()
    assert v4.n == 4
    assert v4.is_abelian()
    assert not v4.is_cyclic()


def test_v4_not_isomorphic_to_z4():
    # the two (non-isomorphic) groups of order 4
    v4 = klein_four_group()
    z4 = cyclic_group(4)
    assert not is_isomorphic(v4, z4)


def test_direct_product_order_and_isomorphism_reflexive():
    g = direct_product(cyclic_group(2), cyclic_group(3))
    assert g.n == 6
    assert g.is_abelian()
    assert is_isomorphic(g, g)
    # Z2 x Z3 is cyclic (gcd(2,3)=1), isomorphic to Z6
    assert g.is_cyclic()
    assert is_isomorphic(g, cyclic_group(6))


def test_isomorphism_is_symmetric_for_distinct_groups():
    s3 = symmetric_group(3)
    d3 = dihedral_group(3)
    # S3 and D3 are isomorphic (both are "the" non-abelian group of order 6)
    assert is_isomorphic(s3, d3)
    assert is_isomorphic(d3, s3)
