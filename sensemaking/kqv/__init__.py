"""The KQV attention suboperad of ``sarr`` (see SPEC.md).

Public API:

* ``attention_head``, ``prior_box`` -- the generators (con.head, ex.zeroary).
* ``Head``, ``Sub`` -- the free-operad term algebra; a ``KQVTerm`` *is* a member of
  the suboperad by construction (obs.generate).
* ``realize`` -- the functor ``F : KQV -> sarr`` (uses only dap's operad operations).
* ``leaf``, ``flat`` -- convenience builders.
* ``param_dim``, ``unpack``, ``open_boxes``, ``width`` -- helpers.
"""

from .builders import Builder
from .head import attention_head, param_dim, prior_box, unpack
from .operad import (
    KQVSystem,
    KQVTerm,
    Head,
    Par,
    Sub,
    flat,
    leaf,
    open_boxes,
    realize,
    target_boxes,
    trace,
    width,
)

__all__ = [
    "attention_head",
    "prior_box",
    "param_dim",
    "unpack",
    "KQVTerm",
    "Head",
    "Sub",
    "Par",
    "realize",
    "leaf",
    "flat",
    "open_boxes",
    "width",
    "target_boxes",
    "KQVSystem",
    "trace",
    "Builder",
]
