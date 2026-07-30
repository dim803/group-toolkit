"""
sylow_demo.py
--------------
Finds the Sylow p-subgroups of S4 (order 24 = 2^3 * 3) and checks the results
against Sylow's theorems: n_p == 1 (mod p), n_p divides |G|/p^k, and all
Sylow p-subgroups are conjugate to one another.
"""

from group_toolkit import symmetric_group
from group_toolkit.sylow import sylow_subgroups, sylow_summary


if __name__ == "__main__":
    s4 = symmetric_group(4)
    print(f"S4: order {s4.n} = 2^3 * 3\n")

    for p in [2, 3]:
        summary = sylow_summary(s4, p)
        print(f"Sylow {p}-subgroups:")
        print(f"  order of each: {summary['p_power']}")
        print(f"  count n_{p} = {summary['num_sylow_subgroups']}")
        print(f"  n_{p} == 1 (mod {p}): {summary['congruent_to_1_mod_p']}")
        print(f"  n_{p} divides |G|/{summary['p_power']} = {summary['cofactor']}: "
              f"{summary['divides_cofactor']}")
        print(f"  all conjugate: {summary['all_conjugate']}")

        subgroups = sylow_subgroups(s4, p)
        for sg in subgroups:
            print("   ", sorted(s4.labels[e] for e in sg))
        print()
