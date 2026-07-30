from group_toolkit import symmetric_group, dihedral_group, cyclic_group
from group_toolkit.sylow import sylow_subgroups, sylow_summary, p_part


def test_p_part():
    assert p_part(24, 2) == 8
    assert p_part(24, 3) == 3
    assert p_part(30, 5) == 5
    assert p_part(7, 2) == 1  # p does not divide n


def test_sylow_subgroups_of_s4_match_known_counts():
    # Classical facts about S4 (order 24 = 2^3 * 3):
    #   Sylow 2-subgroups have order 8, and there are 3 of them (each isomorphic to D4)
    #   Sylow 3-subgroups have order 3, and there are 4 of them
    s4 = symmetric_group(4)

    sylow2 = sylow_subgroups(s4, 2)
    assert len(sylow2) == 3
    assert all(len(sg) == 8 for sg in sylow2)

    sylow3 = sylow_subgroups(s4, 3)
    assert len(sylow3) == 4
    assert all(len(sg) == 3 for sg in sylow3)


def test_sylow_summary_satisfies_sylows_theorems():
    s4 = symmetric_group(4)
    for p in [2, 3]:
        summary = sylow_summary(s4, p)
        assert summary["congruent_to_1_mod_p"]
        assert summary["divides_cofactor"]
        assert summary["all_conjugate"]


def test_sylow_subgroup_of_prime_order_group_is_whole_group():
    z7 = cyclic_group(7)
    sylow7 = sylow_subgroups(z7, 7)
    assert len(sylow7) == 1
    assert next(iter(sylow7)) == frozenset(range(7))


def test_sylow_2_subgroup_of_d6_has_expected_order():
    # D6 has order 12 = 4 * 3, so Sylow 2-subgroups have order 4
    d6 = dihedral_group(6)
    sylow2 = sylow_subgroups(d6, 2)
    assert all(len(sg) == 4 for sg in sylow2)
