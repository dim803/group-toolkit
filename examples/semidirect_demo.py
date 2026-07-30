"""
semidirect_demo.py
--------------------
D_n is (isomorphic to) the semidirect product Z/nZ semidirect Z/2Z, where the
nontrivial element of Z/2Z acts on Z/nZ by inversion (g -> -g). This script
builds that semidirect product directly from the action and confirms it
matches dihedral_group(n).
"""

from group_toolkit import (
    cyclic_group,
    dihedral_group,
    is_isomorphic,
    semidirect_product,
    inversion_action,
)


if __name__ == "__main__":
    for n in [3, 4, 5]:
        zn = cyclic_group(n)
        z2 = cyclic_group(2)
        semi = semidirect_product(zn, z2, inversion_action(n))
        dn = dihedral_group(n)

        print(f"Z{n} \u22ca Z2 (inversion action):")
        print(f"  order = {semi.n}, abelian = {semi.is_abelian()}")
        print(f"  isomorphic to D{n}: {is_isomorphic(semi, dn)}")
        print()
