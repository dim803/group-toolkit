"""
explore_subgroup_structure.py
------------------------------
Walks through the subgroup lattice, cosets, normality, conjugacy classes,
and quotient construction for S3 and D4 -- printing out results that match
standard textbook facts, as a sanity-check-by-inspection of the toolkit.
"""

from group_toolkit import (
    symmetric_group,
    dihedral_group,
    klein_four_group,
    is_isomorphic,
)


def explore_s3():
    print("=== S3 (symmetric group on 3 letters) ===")
    s3 = symmetric_group(3)
    print(f"order = {s3.n}, abelian = {s3.is_abelian()}")

    subgroups = sorted(s3.all_subgroups(), key=len)
    print(f"\n{len(subgroups)} subgroups:")
    for sg in subgroups:
        elems = [s3.labels[e] for e in sorted(sg)]
        print(f"  order {len(sg)}: {elems}  normal={s3.is_normal(sg)}")

    print(f"\ncenter: {[s3.labels[e] for e in s3.center()]}")
    print("conjugacy class sizes:", sorted(len(c) for c in s3.conjugacy_classes()))

    order3 = next(sg for sg in subgroups if len(sg) == 3)
    print(f"\ncosets of the order-3 subgroup (normal, index 2):")
    for coset in s3.left_cosets(order3):
        print(" ", [s3.labels[e] for e in coset])
    print()


def explore_d4():
    print("=== D4 (symmetries of a square) ===")
    d4 = dihedral_group(4)
    print(f"order = {d4.n}, abelian = {d4.is_abelian()}, cyclic = {d4.is_cyclic()}")

    z = d4.center()
    print(f"\ncenter Z(D4) = {[d4.labels[e] for e in z]}")

    q = d4.quotient_group(z)
    v4 = klein_four_group()
    print(f"D4 / Z(D4) has order {q.n}, abelian = {q.is_abelian()}, "
          f"cyclic = {q.is_cyclic()}")
    print(f"D4 / Z(D4) isomorphic to the Klein four-group: {is_isomorphic(q, v4)}")


if __name__ == "__main__":
    explore_s3()
    explore_d4()
