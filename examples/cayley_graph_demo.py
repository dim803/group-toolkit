"""
cayley_graph_demo.py
----------------------
Draws the Cayley graph of a group with respect to a chosen generating set:
one vertex per element, a directed edge g -> g*s for each generator s, with
edges colored by generator. Saves PNG files next to this script.
"""

import os
import networkx as nx
import matplotlib.pyplot as plt

from group_toolkit import dihedral_group, symmetric_group

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def draw_cayley_graph(group, generators, title, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(range(group.n))

    colors = plt.cm.tab10.colors
    edge_colors = []
    for i, s in enumerate(generators):
        color = colors[i % len(colors)]
        for g in range(group.n):
            graph.add_edge(g, group.multiply(g, s), color=color, generator=i)

    pos = nx.circular_layout(graph)
    edge_color_list = [graph[u][v][k]["color"] for u, v, k in graph.edges(keys=True)]

    plt.figure(figsize=(6, 6))
    nx.draw_networkx_nodes(graph, pos, node_color="lightsteelblue", node_size=500)
    nx.draw_networkx_labels(
        graph, pos, labels={i: group.labels[i] for i in range(group.n)}, font_size=8
    )
    nx.draw_networkx_edges(
        graph, pos, edge_color=edge_color_list, connectionstyle="arc3,rad=0.15",
        arrowsize=12,
    )
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"saved {out_path}")


if __name__ == "__main__":
    d4 = dihedral_group(4)
    # generators: rotation r (index 1) and reflection s (index 4, i.e. n=4 -> s = index n)
    draw_cayley_graph(
        d4, generators=[1, 4], title="Cayley graph of D4 (generators r, s)",
        filename="cayley_graph_d4.png",
    )

    s3 = symmetric_group(3)
    # generators: a transposition and a 3-cycle
    transposition = s3.labels.index("(1, 0, 2)")
    three_cycle = s3.labels.index("(1, 2, 0)")
    draw_cayley_graph(
        s3, generators=[transposition, three_cycle],
        title="Cayley graph of S3 (a transposition and a 3-cycle)",
        filename="cayley_graph_s3.png",
    )
