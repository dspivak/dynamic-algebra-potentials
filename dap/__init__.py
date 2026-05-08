"""dap: dynamic-algebra-potentials, Stage-2 Python core.

Package implementing the principal constructions of the paper
``dynamic-algebra-potentials.tex``: paired vector spaces, polynomial
maps, potentialized lenses, and the functor chain
``cint -> leg -> dyn`` whose composite is Phi (thm.functor).
"""

from .pvect import PairedVectorSpace
from .polynomial import Yon, Cot, DirichletProduct, PolyMap
from .lens import PotLensMap
from .org import OrgMorphism
from . import functors
from . import wiring

__all__ = [
    "PairedVectorSpace",
    "Yon",
    "Cot",
    "DirichletProduct",
    "PolyMap",
    "PotLensMap",
    "OrgMorphism",
    "functors",
    "wiring",
]
