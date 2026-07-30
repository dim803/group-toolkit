import os

from group_toolkit import cyclic_group, dihedral_group, symmetric_group, draw_cayley_table


def test_draw_cayley_table_produces_a_file(tmp_path):
    g = cyclic_group(5)
    out = tmp_path / "cayley_table_z5.png"
    draw_cayley_table(g, str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_draw_cayley_table_works_for_several_groups(tmp_path):
    groups = {
        "d4": dihedral_group(4),
        "s3": symmetric_group(3),
        "z6": cyclic_group(6),
    }
    for name, g in groups.items():
        out = tmp_path / f"{name}.png"
        draw_cayley_table(g, str(out))
        assert out.exists()
        assert out.stat().st_size > 0
