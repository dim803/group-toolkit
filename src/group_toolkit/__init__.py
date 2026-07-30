"""
group_toolkit
-------------
A small toolkit for working with finite groups given by Cayley tables:
axiom validation, subgroups, cosets, normality, conjugacy classes, quotient
groups, isomorphism testing, and constructors for the standard families.
"""

from .group import FiniteGroup, GroupAxiomError, is_isomorphic
from .constructions import (
    cyclic_group,
    dihedral_group,
    symmetric_group,
    direct_product,
    klein_four_group,
)
from .semidirect import semidirect_product, inversion_action
from .sylow import sylow_subgroups, sylow_summary, p_part
from .visualize import draw_cayley_table

__all__ = [
    "FiniteGroup",
    "GroupAxiomError",
    "is_isomorphic",
    "cyclic_group",
    "dihedral_group",
    "symmetric_group",
    "direct_product",
    "klein_four_group",
    "semidirect_product",
    "inversion_action",
    "sylow_subgroups",
    "sylow_summary",
    "p_part",
    "draw_cayley_table",
]
