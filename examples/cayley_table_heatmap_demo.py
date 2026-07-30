"""
cayley_table_heatmap_demo.py
------------------------------
Renders Cayley tables as heatmaps colored by conjugacy class, making the
group's internal symmetry visible directly in the multiplication table.
Saves PNG files next to this script.
"""

import os

from group_toolkit import dihedral_group, symmetric_group, draw_cayley_table

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    d4 = dihedral_group(4)
    out = os.path.join(OUTPUT_DIR, "cayley_table_d4.png")
    draw_cayley_table(d4, out, title="Cayley table of D4 (colored by conjugacy class)")
    print(f"saved {out}")

    s3 = symmetric_group(3)
    out = os.path.join(OUTPUT_DIR, "cayley_table_s3.png")
    draw_cayley_table(s3, out, title="Cayley table of S3 (colored by conjugacy class)")
    print(f"saved {out}")
