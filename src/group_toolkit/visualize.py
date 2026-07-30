"""
visualize.py
------------
draw_cayley_table: renders a group's Cayley table as a heatmap, with cells
colored by which conjugacy class the product a*b falls into. This makes the
group's internal symmetry visible directly -- conjugacy classes show up as
colored regions/patterns rather than as a list of numbers.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from .group import FiniteGroup


def draw_cayley_table(group: FiniteGroup, filename: str, title: str = None) -> None:
    classes = group.conjugacy_classes()
    class_of = {}
    for class_id, cls in enumerate(classes):
        for element in cls:
            class_of[element] = class_id

    n = group.n
    grid = [[class_of[group.multiply(i, j)] for j in range(n)] for i in range(n)]

    cmap = plt.get_cmap("tab20", len(classes))

    fig_size = max(4, n * 0.55)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    ax.imshow(grid, cmap=cmap, vmin=-0.5, vmax=len(classes) - 0.5)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(group.labels, rotation=90, fontsize=7)
    ax.set_yticklabels(group.labels, fontsize=7)
    ax.set_xticks([x - 0.5 for x in range(1, n)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, n)], minor=True)
    ax.grid(which="minor", color="white", linewidth=0.5)
    ax.tick_params(which="minor", length=0)

    ax.set_title(title or f"Cayley table of {group!r}\n(color = conjugacy class of the product)")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
