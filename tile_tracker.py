#!/usr/bin/env python3
"""Tile-replay tracker for the top composition diagram in dynamic-algebra-potentials.tex.

Boundary = two paths (topright, leftbottom) sharing start and end cells.
A path is a list of cells with labelled edges between consecutive cells.

Tile operations:
  swap(side, idx_a, b_new, e1, e2, fact)
      replaces a -[old_e1]-> b -[old_e2]-> c
      with     a -[e1]-> b_new -[e2]-> c
      and tabooes b_new. Untabooes a and c (their adjacent boundary edges changed).

  collapse(side, idx_a, e_ac, fact)
      replaces a -[old_e1]-> b -[old_e2]-> c with a -[e_ac]-> c.
      Drops b. No taboo (degenerate tile). Untabooes a and c.

Taboo rule: cannot introduce a cell whose name is currently tabooed.
A tabooed cell is freed automatically when an incident boundary edge changes.

Run as a script for a quick demo (prints the initial boundary).
"""

import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Boundary:
    topright: list                 # cells along upper composite (in order)
    leftbottom: list               # cells along lower composite (in order)
    tr_edges: list                 # tr_edges[i] = label of edge topright[i] -> topright[i+1]
    lb_edges: list
    tr_pos: list = field(default_factory=list)   # (row, col) of each TR cell on the page
    lb_pos: list = field(default_factory=list)   # (row, col) of each LB cell on the page
    taboo: set = field(default_factory=set)
    log: list = field(default_factory=list)

    @classmethod
    def init(cls, tr_cells, tr_edges, lb_cells, lb_edges, tr_pos=None, lb_pos=None):
        assert len(tr_edges) == len(tr_cells) - 1
        assert len(lb_edges) == len(lb_cells) - 1
        assert tr_cells[0] == lb_cells[0], "paths must share the start cell"
        assert tr_cells[-1] == lb_cells[-1], "paths must share the end cell"
        if tr_pos is not None:
            assert len(tr_pos) == len(tr_cells), "tr_pos length mismatch"
        if lb_pos is not None:
            assert len(lb_pos) == len(lb_cells), "lb_pos length mismatch"
        return cls(list(tr_cells), list(lb_cells), list(tr_edges), list(lb_edges),
                   tr_pos=list(tr_pos) if tr_pos else [],
                   lb_pos=list(lb_pos) if lb_pos else [])

    def _path(self, side):
        if side == 'tr':
            return self.topright, self.tr_edges
        if side == 'lb':
            return self.leftbottom, self.lb_edges
        raise ValueError(f"side must be 'tr' or 'lb', got {side!r}")

    def _pos(self, side):
        return self.tr_pos if side == 'tr' else self.lb_pos

    @staticmethod
    def _arrow_dir(p_from, p_to):
        """Return tikzcd direction string (e.g. 'd', 'dr', 'ddl', 'r') from p_from to p_to.
        Both are (row, col). Returns None if not a single-step or short diagonal."""
        dr, dc = p_to[0] - p_from[0], p_to[1] - p_from[1]
        s = ''
        if dr > 0:
            s += 'd' * dr
        elif dr < 0:
            s += 'u' * (-dr)
        if dc > 0:
            s += 'r' * dc
        elif dc < 0:
            s += 'l' * (-dc)
        return s or 'self'

    def swap(self, side, idx_a, b_new, e1, e2, fact, b_new_pos=None):
        cells, edges = self._path(side)
        if not 0 <= idx_a <= len(cells) - 3:
            raise IndexError(f"idx_a={idx_a} out of range for path of length {len(cells)}")
        a, b, c = cells[idx_a], cells[idx_a + 1], cells[idx_a + 2]
        if b_new in self.taboo:
            raise ValueError(f"taboo violation: {b_new!r} is currently tabooed")
        old_e1, old_e2 = edges[idx_a], edges[idx_a + 1]

        # position bookkeeping & arrow-direction sanity check
        pos = self._pos(side)
        arrow_a_to_new = arrow_new_to_c = None
        if pos:
            if b_new_pos is None:
                raise ValueError(f"swap on positioned boundary requires b_new_pos for {b_new!r}")
            a_pos, b_pos, c_pos = pos[idx_a], pos[idx_a + 1], pos[idx_a + 2]
            arrow_a_to_new = self._arrow_dir(a_pos, b_new_pos)
            arrow_new_to_c = self._arrow_dir(b_new_pos, c_pos)
            # both arrows must move *somewhere* (not self-loop) and not be vacuous
            if arrow_a_to_new == 'self' or arrow_new_to_c == 'self':
                raise ValueError(f"b_new_pos {b_new_pos} coincides with a {a_pos} or c {c_pos}")
            # discourage backtracking (arrows shouldn't point in opposite directions)

        cells[idx_a + 1] = b_new
        edges[idx_a] = e1
        edges[idx_a + 1] = e2
        if pos and b_new_pos is not None:
            pos[idx_a + 1] = b_new_pos
        self.taboo.add(b_new)
        self.taboo.discard(a)
        self.taboo.discard(c)
        log_entry = {
            'step': len(self.log) + 1, 'op': 'swap', 'side': side, 'fact': fact,
            'before': [a, old_e1, b, old_e2, c],
            'after':  [a, e1, b_new, e2, c],
            'taboo_added': b_new,
        }
        if arrow_a_to_new is not None:
            log_entry['arrows'] = {'a_to_new': arrow_a_to_new, 'new_to_c': arrow_new_to_c}
            log_entry['b_new_pos'] = b_new_pos
        self.log.append(log_entry)

    def collapse(self, side, idx_a, e_ac, fact):
        cells, edges = self._path(side)
        if not 0 <= idx_a <= len(cells) - 3:
            raise IndexError(f"idx_a={idx_a} out of range for path of length {len(cells)}")
        a, b, c = cells[idx_a], cells[idx_a + 1], cells[idx_a + 2]
        old_e1, old_e2 = edges[idx_a], edges[idx_a + 1]
        del cells[idx_a + 1]
        edges[idx_a] = e_ac
        del edges[idx_a + 1]
        self.taboo.discard(a)
        self.taboo.discard(c)
        self.log.append({
            'step': len(self.log) + 1, 'op': 'collapse', 'side': side, 'fact': fact,
            'before': [a, old_e1, b, old_e2, c],
            'after':  [a, e_ac, c],
        })

    def relabel_edge(self, side, idx, new_label, fact):
        """Relabel a single edge without changing cells. Used for keystones that change
        only the edge interpretation (e.g., T-algebra associativity treating T(α) ≡ μ_z
        within an α-postcomposed context)."""
        cells, edges = self._path(side)
        if not 0 <= idx < len(edges):
            raise IndexError(f"idx={idx} out of range for {len(edges)} edges")
        old_label = edges[idx]
        edges[idx] = new_label
        self.log.append({
            'step': len(self.log) + 1, 'op': 'relabel_edge', 'side': side, 'fact': fact,
            'idx': idx, 'old_label': old_label, 'new_label': new_label,
            'cell_before': cells[idx], 'cell_after': cells[idx + 1],
        })

    def collapse_range(self, side, start_idx, end_idx, residual_edges, residual_cells, fact):
        """Hypothesis-test op: replace edges[start_idx:end_idx] with residual_edges
        and cells[start_idx+1:end_idx] with residual_cells. start_idx is the index of
        the first cell whose outgoing edge is being absorbed; end_idx is the index of
        the cell that survives (its incoming edge becomes the last residual_edge).
        residual_cells must have length = len(residual_edges) - 1, residual_edges length >= 1.
        Drops position info for affected interior cells (not validated geometrically)."""
        cells, edges = self._path(side)
        if not 0 <= start_idx < end_idx <= len(cells) - 1:
            raise IndexError(f"range [{start_idx},{end_idx}] out of bounds")
        if len(residual_edges) != len(residual_cells) + 1:
            raise ValueError("residual_edges length must be residual_cells length + 1")
        old_edges = edges[start_idx:end_idx]
        old_cells = cells[start_idx+1:end_idx]
        edges[start_idx:end_idx] = residual_edges
        cells[start_idx+1:end_idx] = residual_cells
        pos = self._pos(side)
        if pos:
            pos[start_idx+1:end_idx] = [None] * len(residual_cells)
        for c in old_cells:
            self.taboo.discard(c)
        self.log.append({
            'step': len(self.log) + 1, 'op': 'collapse_range', 'side': side, 'fact': fact,
            'old_edges': old_edges, 'new_edges': residual_edges,
            'old_cells': old_cells, 'new_cells': residual_cells,
        })

    def chain_diff(self):
        """Compare TR and LB edge sequences. Returns (matched_prefix, tr_residual, lb_residual)."""
        i = 0
        while i < len(self.tr_edges) and i < len(self.lb_edges) and self.tr_edges[i] == self.lb_edges[i]:
            i += 1
        return i, self.tr_edges[i:], self.lb_edges[i:]

    def show(self) -> str:
        def render(cells, edges, label):
            yield f"{label}:"
            for i, cell in enumerate(cells):
                mark = "*" if cell in self.taboo else " "
                yield f"  {mark} {cell}"
                if i < len(edges):
                    yield f"      --[{edges[i]}]-->"
        return "\n".join([
            *render(self.topright, self.tr_edges, "topright"),
            *render(self.leftbottom, self.lb_edges, "leftbottom"),
            f"taboo: {sorted(self.taboo)}",
        ])

    def write_log(self, path):
        with open(path, 'w') as f:
            for entry in self.log:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---- initial state: outer perimeter of the top diagram (pre-tile atomization) ----
# Both paths run start -> end through outermost row/col cells.
# End cell is "outp e[e, T(z)]" (= (13,5) and (13,4) in top diagram); the final
# (14,5)=outp e H_e is past the merge and not part of the boundary.

TR_CELLS = [
    "outp c H_c",                    # (1,1)
    "outp c outp c H_c",             # (1,2)
    "outp d outp c H_c",             # (1,3)
    "outp d[d, d outp c H_c]",       # (1,4)
    "outp d[d, T(c) H_c]",           # (1,5)
    "outp d[d, T(c) T(H_c)]",        # (2,5)
    "outp d[d, T(c H_c)]",           # (4,5)
    "outp d[d, T(z)]",               # (5,5)
    "outp d H_d",                    # (6,5)
    "outp d outp d H_d",             # (7,5)
    "outp e outp d H_d",             # (8,5)
    "outp e[e, e outp d H_d]",       # (9,5)
    "outp e[e, T(d) H_d]",           # (10,5)
    "outp e[e, T(d) T(H_d)]",        # (11,5)
    "outp e[e, T(d H_d)]",           # (12,5)
    "outp e[e, T(z)]",               # (13,5)
]
TR_EDGES = [
    "δ", "outp f", "coev_d", "inpt f", "η", "τ", "T(ev)", "α",
    "δ", "outp g", "coev_e", "inpt g", "η", "τ", "T(ev)",
]

LB_CELLS = [
    "outp c H_c",                    # (1,1)
    "outp c outp c H_c",             # (2,1)
    "outp d outp c H_c",             # (4,1)
    "outp e outp c H_c",             # (5,1)
    "outp e[e, e outp c H_c]",       # (6,1)
    "outp e[e, e outp c outp c H_c]",# (7,1)
    "outp e[e, e outp d outp c H_c]",# (8,1)
    "outp e[e, T(d) outp c H_c]",    # (9,1)
    "outp e[e, T(d) T(outp c) H_c]", # (10,1)
    "outp e[e, T(d outp c) H_c]",    # (11,1)
    "outp e[e, T(T(c)) H_c]",        # (12,1)
    "outp e[e, T(c) H_c]",           # (13,1)
    "outp e[e, T(c) T(H_c)]",        # (13,2)
    "outp e[e, T(c H_c)]",           # (13,3)
    "outp e[e, T(z)]",               # (13,4)
]
LB_EDGES = [
    "δ", "outp f", "outp g", "coev_e", "δ", "outp f", "inpt g",
    "η", "τ", "T(inpt f)", "μ", "η", "τ", "T(ev)",
]


TR_POS = [
    (1,1), (1,2), (1,3), (1,4), (1,5),
    (2,5), (3,5), (4,5), (5,5), (6,5),
    (7,5), (8,5), (9,5), (10,5), (11,5), (12,5),
]
LB_POS = [
    (1,1), (2,1), (3,1), (4,1), (5,1),
    (6,1), (7,1), (8,1), (9,1), (10,1),
    (11,1), (12,1), (13,2), (13,3), (13,4),
]


def init_state() -> Boundary:
    return Boundary.init(TR_CELLS, TR_EDGES, LB_CELLS, LB_EDGES, TR_POS, LB_POS)


# ---- prop.Theta (T=id, z=I) — simpler 7×5 rectangle ----
# TR right then down: 4 [r] across row 1, then 6 [d] down col 5. 10 atoms.
# LB down with one [dd] on coev_e (skipping (5,1)), then right across row 7. 9 atoms.
# Both meet at (7,5) = outp e H_e.

THETA_TR_CELLS = [
    "outp c H_c",                     # (1,1)
    "outp c outp c H_c",              # (1,2)
    "outp d outp c H_c",              # (1,3)
    "outp d[d, d outp c H_c]",        # (1,4)
    "outp d[d, c H_c]",               # (1,5)
    "outp d H_d",                     # (2,5) — outp d[d, I]
    "outp d outp d H_d",              # (3,5)
    "outp e outp d H_d",              # (4,5)
    "outp e[e, e outp d H_d]",        # (5,5)
    "outp e[e, d H_d]",               # (6,5)
    "outp e H_e",                     # (7,5) — outp e[e, I]
]
THETA_TR_EDGES = [
    "δ", "outp f", "coev_d", "inpt f", "ev",
    "δ", "outp g", "coev_e", "inpt g", "ev",
]
THETA_TR_POS = [
    (1,1), (1,2), (1,3), (1,4), (1,5),
    (2,5), (3,5), (4,5), (5,5), (6,5), (7,5),
]

THETA_LB_CELLS = [
    "outp c H_c",                       # (1,1)
    "outp c outp c H_c",                # (2,1)
    "outp d outp c H_c",                # (3,1)
    "outp e outp c H_c",                # (4,1)
    "outp e[e, e outp c H_c]",          # (6,1) — reached via [dd coev_e] from (4,1)
    "outp e[e, e outp c outp c H_c]",   # (7,1)
    "outp e[e, e outp d outp c H_c]",   # (7,2)
    "outp e[e, d outp c H_c]",          # (7,3)
    "outp e[e, c H_c]",                 # (7,4)
    "outp e H_e",                       # (7,5)
]
THETA_LB_EDGES = [
    "δ", "outp f", "outp g", "coev_e",
    "δ", "outp f", "inpt g", "inpt f", "ev",
]
THETA_LB_POS = [
    (1,1), (2,1), (3,1), (4,1), (6,1),
    (7,1), (7,2), (7,3), (7,4), (7,5),
]


# ---- inner-boundary diagram (after 14 tiles of replay_simple) — 7×5 layout ----
# TR: (1,1) → (1,5) right via 4 atoms, then (1,5) → (7,5) down via 6 atoms.
# LB: (1,1) → (6,1) down via 5 atoms, then (6,1) → (7,2) diagonal via 1 atom (outp g),
# then (7,2) → (7,5) right via 3 atoms. Total LB = 9 atoms.

INNER1_TR_CELLS = [
    "outp c H_c",                          # (1,1)
    "outp c outp c H_c",                   # (1,2)
    "outp c[d, d outp c H_c]",             # (1,3)
    "outp c[d, c H_c]",                    # (1,4)
    "outp d[d, c H_c]",                    # (1,5)
    "outp d outp d[d, c H_c]",             # (2,5)
    "outp d[e, e outp d[d, c H_c]]",       # (3,5)
    "outp d[e, d [d, c H_c]]",             # (4,5)
    "outp d[e, d H_d]",                    # (5,5)
    "outp d H_e",                          # (6,5)
    "outp e H_e",                          # (7,5)
]
INNER1_TR_EDGES = [
    "δ", "coev_d", "inpt f", "outp f",
    "δ", "coev_e", "inpt g", "ev_c", "ev_d", "outp g",
]
INNER1_TR_POS = [
    (1,1), (1,2), (1,3), (1,4), (1,5),
    (2,5), (3,5), (4,5), (5,5), (6,5), (7,5),
]

INNER1_LB_CELLS = [
    "outp c H_c",                              # (1,1)
    "outp c outp c H_c",                       # (2,1)
    "outp c outp c outp c H_c",                # (3,1)
    "outp c[e, e outp c outp c H_c]",          # (4,1)
    "outp d[e, e outp c outp c H_c]",          # (5,1)
    "outp d[e, e outp d outp c H_c]",          # (6,1)
    "outp e[e, e outp d outp c H_c]",          # (7,2) — diagonal from (6,1)
    "outp e[e, d outp c H_c]",                 # (7,3)
    "outp e[e, c H_c]",                        # (7,4)
    "outp e H_e",                              # (7,5)
]
INNER1_LB_EDGES = [
    "δ", "δ", "coev_e", "outp f", "outp f",
    "outp g", "inpt g", "inpt f", "ev_c",
]
INNER1_LB_POS = [
    (1,1), (2,1), (4,1), (5,1), (6,1), (7,1),
    (7,2), (7,3), (7,4), (7,5),
]


def init_state_inner1() -> Boundary:
    """Inner-boundary diagram after 14 tiles of replay_simple.
    Atoms remaining:
      TR (10): δ, coev_d, inpt f, outp f, δ, coev_e, inpt g, ev_c, ev_d, outp g
      LB (9):  δ, δ, coev_e, outp f, outp f, outp g, inpt g, inpt f, ev_c
    Note: TR's two evs are now distinguished — ev_c is [d,ev_c] (lifted by [e,-]),
    ev_d is [e,ev_d]; LB's single ev is [e,ev_c]. The 'snake' of the proof closes
    via comonoid-hom for outp f + coassoc(δ) at the start; closure-adjunction
    transpose at the end."""
    return Boundary.init(INNER1_TR_CELLS, INNER1_TR_EDGES,
                         INNER1_LB_CELLS, INNER1_LB_EDGES,
                         INNER1_TR_POS, INNER1_LB_POS)


def init_state_simple() -> Boundary:
    """Boundary for prop.Theta (T=id, z=I) — 7×5 rectangle.
    LB has one [dd] arrow on coev_e (4,1)→(6,1); the script's _arrow_dir validates
    'dd' as a legitimate direction string."""
    return Boundary.init(THETA_TR_CELLS, THETA_TR_EDGES, THETA_LB_CELLS, THETA_LB_EDGES,
                         THETA_TR_POS, THETA_LB_POS)


def replay_simple():
    """Tiles for prop.Theta (T=id) — the 7×5 rectangle. Currently empty (reset)."""
    b = init_state_simple()
    return b


def replay_OLD_archived():
    """Apply tiles from the top diagram to transform OUTER perimeter -> rectangle's chain.
    Tiles drawn from the top diagram's interior cells."""
    b = init_state()

    # ---- TR side: 12 swaps to permute (outp f, coev_d, inpt f, η, ...) into rectangle order ----
    b.swap('tr', 1, "outp c[d, d outp c H_c]", "coev_d", "outp f",
           "bifun outp f / coev_d on (1,2)-(1,3)-(1,4)")
    b.swap('tr', 3, "outp d[d, d outp c T(H_c)]", "η", "inpt f",
           "bifun η / inpt f on (1,4)-(1,5)-(2,5)")
    b.swap('tr', 2, "outp c[d, d outp c T(H_c)]", "η", "outp f",
           "bifun η / outp f on (1,3)-(1,4)-(2,4)")
    b.swap('tr', 1, "outp c outp c T(H_c)", "η", "coev_d",
           "bifun η / coev_d on (1,2)-(1,3)-(2,3)")
    # second half: move η forward from pos 13 to pos 9, outp g back from pos 10 to pos 15
    b.swap('tr', 11, "outp e[e, e outp d T(H_d)]", "η", "inpt g",
           "bifun η / inpt g on (9,5)-(10,5)-(11,5)")
    b.swap('tr', 10, "outp e outp d T(H_d)", "η", "coev_e",
           "bifun η / coev_e on (8,5)-(9,5)-(10,5)")
    b.swap('tr', 9, "outp d outp d T(H_d)", "η", "outp g",
           "bifun η / outp g on (7,5)-(8,5)-(9,5)")
    b.swap('tr', 8, "outp d T(H_d)", "η", "δ",
           "bifun η / δ on (6,5)-(7,5)-(8,5)")
    b.swap('tr', 10, "outp d[e, e outp d T(H_d)]", "coev_e", "outp g",
           "bifun coev_e / outp g on (8,5)-(9,5)-(10,5)")
    b.swap('tr', 11, "outp d[e, T(d) T(H_d)]", "inpt g", "outp g",
           "bifun inpt g / outp g on (9,5)-(10,5)-(11,5)")
    b.swap('tr', 12, "outp d[e, T(d H_d)]", "τ", "outp g",
           "bifun τ / outp g on (10,5)-(11,5)-(12,5)")
    b.swap('tr', 13, "outp d[e, T(z)]", "T(ev)", "outp g",
           "bifun T(ev) / outp g on (11,5)-(12,5)-(13,5)")

    # ---- LB side: bring outer chain into rectangle order ----
    # Swap (outp g, coev_e) -> (coev_e, outp g) at start of e-block
    b.swap('lb', 2, "outp d[e, e outp c H_c]", "coev_e", "outp g",
           "bifun coev_e / outp g on (4,1)-(5,1)-(6,1)")
    b.swap('lb', 3, "outp d[e, e outp c outp c H_c]", "δ", "outp g",
           "bifun δ / outp g on (5,1)-(6,1)-(7,1)")
    b.swap('lb', 1, "outp c[e, e outp c H_c]", "coev_e", "outp f",
           "bifun coev_e / outp f on (2,1)-(4,1)-(5,1)")
    b.swap('lb', 2, "outp c[e, e outp c outp c H_c]", "δ", "outp f",
           "bifun δ / outp f on (4,1)-(5,1)-(6,1)")
    b.swap('lb', 1, "outp c outp c outp c H_c", "δ", "coev_e",
           "bifun δ / coev_e on (2,1)-(4,1)-(5,1)")
    # outp f / outp g bifun on inner-vs-outer slot
    b.swap('lb', 4, "outp d[e, e outp d outp c H_c]", "outp f", "outp g",
           "bifun outp f / outp g on (4,1)-(5,1)-(6,1)/(7,3)")
    # move the second η backward through μ, T(inpt f), τ
    b.swap('lb', 10, "outp e[e, T(T(c)) T(H_c)]", "η", "μ",
           "bifun η / μ on (12,1)-(13,1)-(13,2)")
    b.swap('lb', 9, "outp e[e, T(d outp c) T(H_c)]", "η", "T(inpt f)",
           "bifun η / T(inpt f) on (11,1)-(12,1)-(12,2)")
    b.swap('lb', 8, "outp e[e, T(d) T(outp c) T(H_c)]", "η", "τ",
           "bifun η / τ on (10,1)-(11,1)-(11,2)")
    # move the first η backward through inpt g, outp g
    b.swap('lb', 6, "outp e[e, e outp d T(outp c) H_c]", "η", "inpt g",
           "bifun η / inpt g on (8,1)-(9,1)-(10,1)")
    b.swap('lb', 5, "outp d[e, e outp d T(outp c) H_c]", "η", "outp g",
           "bifun η / outp g on (7,3)-(8,1)-(9,1)")
    # final: swap the two outp f's so the inner-first acts on cell 4
    b.swap('lb', 3, "outp c[e, e outp d outp c H_c]", "outp f", "outp f",
           "bifun outp f (inner) / outp f (outer) on (5,4)-(6,4)-(7,3)")

    # ===== rectangle (second diagram) tiles =====
    # TR-1: δ/η bifun, NEW = outp c T(H_c)
    b.swap('tr', 0, "outp c T(H_c)", "η", "δ", "rect TR-1: bifun η / δ")
    # TR-3: outp f / inpt f bifun (outer / inner-d)
    b.swap('tr', 3, "outp c[d, T(c) T(H_c)]", "inpt f", "outp f", "rect TR-3: bifun inpt f / outp f")
    # TR-A: outp f / τ bifun (outer / inner)
    b.swap('tr', 4, "outp c[d, T(c H_c)]", "τ", "outp f", "rect TR-A: bifun τ / outp f")
    # TR-E: outp f / T(ev) bifun (outer / inner)
    b.swap('tr', 5, "outp c[d, T(z)]", "T(ev)", "outp f", "rect TR-E: bifun T(ev) / outp f")
    # BL-B: outp f / η bifun (outer / inner)
    b.swap('lb', 4, "outp c[e, e outp d T(outp c) H_c]", "η", "outp f", "rect BL-B: bifun η / outp f")
    # BL-D: outp g / inpt g bifun (outer / inner-d)
    b.swap('lb', 6, "outp d[e, T(d) T(outp c) H_c]", "inpt g", "outp g", "rect BL-D: bifun inpt g / outp g")
    # TR-F: outp f / α bifun (outer / inner T(z)→z)
    b.swap('tr', 6, "outp c H_d", "α", "outp f", "rect TR-F: bifun α / outp f")
    # BL-F: outp f / inpt g bifun (outer / inner-d)
    b.swap('lb', 5, "outp c[e, T(d) T(outp c) H_c]", "inpt g", "outp f", "rect BL-F: bifun inpt g / outp f")
    # BL-G: outp g / η bifun (outer / inner H_c)
    b.swap('lb', 7, "outp d[e, T(d) T(outp c) T(H_c)]", "η", "outp g", "rect BL-G: bifun η / outp g")
    # TR-H: outp f / η bifun (outer outp c→outp d / inner H_d wrap)
    b.swap('tr', 7, "outp c T(H_d)", "η", "outp f", "rect TR-H: bifun η / outp f")
    # BL-H: outp f / η bifun (outer outp c→outp d / inner H_c wrap)
    b.swap('lb', 6, "outp c[e, T(d) T(outp c) T(H_c)]", "η", "outp f", "rect BL-H: bifun η / outp f")
    # BL-M: outp g / τ bifun (outer outp d→outp e / inner T-laxator)
    b.swap('lb', 8, "outp d[e, T(d outp c) T(H_c)]", "τ", "outp g", "rect BL-M: bifun τ / outp g")
    # BL-N: outp g / T(inpt f) bifun (outer / inner T-applied-inpt-f)
    b.swap('lb', 9, "outp d[e, T(T(c)) T(H_c)]", "T(inpt f)", "outp g", "rect BL-N: bifun T(inpt f) / outp g")
    # BL-O: outp g / μ bifun (outer / inner monad mult)
    b.swap('lb', 10, "outp d[e, T(c) T(H_c)]", "μ", "outp g", "rect BL-O: bifun μ / outp g")
    # BL-Q: outp f / τ bifun (outer / inner T-laxator)
    b.swap('lb', 7, "outp c[e, T(d outp c) T(H_c)]", "τ", "outp f", "rect BL-Q: bifun τ / outp f")
    # BL-R: η / τ bifun (inner H_c wrap / inner T-laxator)
    b.swap('lb', 6, "outp c[e, T(d outp c) H_c]", "τ", "η", "rect BL-R: bifun τ / η")
    # BL-S: η / outp f bifun (inner H_c / outer outp c→outp d)
    b.swap('lb', 7, "outp d[e, T(d outp c) H_c]", "outp f", "η", "rect BL-S: bifun outp f / η")
    # BL-K: coev_e / outp f bifun (inner-wrap / outer outp c→outp d)
    b.swap('lb', 2, "outp c outp d outp c H_c", "outp f", "coev_e", "rect BL-K: bifun outp f / coev_e")
    # rect3 BL-β: η / inpt g bifun (inner outp c / inner e·outp d→T(d))
    b.swap('lb', 4, "outp c[e, T(d) outp c H_c]", "inpt g", "η", "rect3 BL-β: bifun inpt g / η")
    # rect3 BL-γ: τ / outp f bifun (inner T-laxator / outer outp c→outp d)
    b.swap('lb', 6, "outp d[e, T(d) T(outp c) H_c]", "outp f", "τ", "rect3 BL-γ: bifun outp f / τ")
    # rect3 BL-δ: η / outp f bifun (inner outp c→T(outp c) / outer outp c→outp d)
    b.swap('lb', 5, "outp d[e, T(d) outp c H_c]", "outp f", "η", "rect3 BL-δ: bifun outp f / η")
    # rect3 BL-η: τ / η bifun (inner T-laxator / inner H_c wrap)
    b.swap('lb', 7, "outp d[e, T(d) T(outp c) T(H_c)]", "η", "τ", "rect3 BL-η: bifun η / τ")
    # rect3 TR-NAT: naturality of η at α  (η_z ∘ α = T(α) ∘ η_{T(z)})
    # swaps (α, η) for (η, T(α)); not bifunctoriality, introduces T(α) as new atom
    b.swap('tr', 6, "outp c T([d, T(z)])", "η", "T(α)", "rect3 TR-NAT: η-α naturality")
    # rect3 TR-NAT2: T(α) / outp f bifun (inner T-bound / outer outp c→outp d)
    b.swap('tr', 7, "outp d T([d, T(z)])", "outp f", "T(α)", "rect3 TR-NAT2: bifun outp f / T(α)")
    # rect3 TR-NAT3: T(α) / δ bifun (inner T-bound / outer outp d doubling)
    b.swap('tr', 8, "outp d outp d T([d, T(z)])", "δ", "T(α)", "rect3 TR-NAT3: bifun δ / T(α)")
    # rect3 BL-θ: inpt g / outp f bifun (inner e·outp d→T(d) / outer outp c→outp d)
    b.swap('lb', 4, "outp d[e, e outp d outp c H_c]", "outp f", "inpt g", "rect3 BL-θ: bifun outp f / inpt g")
    # rect3 BL-ι: coev_e / outp f bifun (inner-wrap / outer outp c→outp d) — sets up two outp f's adjacent
    b.swap('lb', 3, "outp d outp d outp c H_c", "outp f", "coev_e", "rect3 BL-ι: bifun outp f / coev_e")

    return b


def replay():
    """Fresh restart — outer perimeter of prop.Theta_T_alpha after the perfect-rectangle wipe.
    Apply tiles here, prioritizing moves that bring atoms toward the keystone facts:
      - Comonoid homomorphism for f / for g (pentagon collapse).
      - σ-opening (σ = τ∘(id⊗η)) to expose T(T(z)) for algebra-associativity.
      - T-algebra associativity α∘T(α) = α∘μ_z.
      - Monad-mult unit μ∘T(η)=id or μ∘η_T=id.
      - Snake at d ([c,ev]∘coev=id, latent ev_d in T(ev) once inpt f passes τ).
      - η monoidal τ∘(η⊗η)=η_{X⊗Y}.
      - Bifun + naturality of η, μ, τ at f, g, ev, etc.
    """
    b = init_state()
    # Tile 1: outp f / coev_d bifun on TR
    b.swap('tr', 1, "outp c[d, d outp c H_c]", "coev_d", "outp f",
           "Tile 1: bifun outp f / coev_d on (1,2)-(1,3)-(1,4)", b_new_pos=(2,3))
    # Tile 2: outp g / coev_e bifun on LB
    b.swap('lb', 2, "outp d[e, e outp c H_c]", "coev_e", "outp g",
           "Tile 2: bifun outp g / coev_e on (3,1)-(4,1)-(5,1)", b_new_pos=(4,2))
    # Tile 3: inpt f / η bifun on TR (different inner slots)
    b.swap('tr', 3, "outp d[d, d outp c T(H_c)]", "η", "inpt f",
           "Tile 3: bifun inpt f / η on (1,4)-(1,5)-(2,5)", b_new_pos=(2,4))
    # Tile 4: α / δ bifun on TR (α inner T(z)→z, δ outer outp d)
    b.swap('tr', 7, "outp d outp d[d, T(z)]", "δ", "α",
           "Tile 4: bifun α / δ on (4,5)-(5,5)-(6,5)", b_new_pos=(5,4))
    # Tile 5: μ / η bifun on LB (different inner slots)
    b.swap('lb', 10, "outp e[e, T(T(c)) T(H_c)]", "η", "μ",
           "Tile 5: bifun μ / η on (11,1)-(12,1)-(12,2)", b_new_pos=(11,2))
    # Tile 6: inpt g / η bifun on LB (inner e·outp d vs inner outp c)
    b.swap('lb', 6, "outp e[e, e outp d T(outp c) H_c]", "η", "inpt g",
           "Tile 6: bifun inpt g / η on (7,1)-(8,1)-(9,1)", b_new_pos=(8,2))
    # Tile 7: outp f / coev_e bifun on LB (outer outp c→outp d / inner wrap)
    b.swap('lb', 1, "outp c[e, e outp c H_c]", "coev_e", "outp f",
           "Tile 7: bifun outp f / coev_e on (2,1)-(3,1)-(4,2)", b_new_pos=(3,2))
    # Tile 8: η / inpt g bifun on TR (inner H_d slot / inner e outp d slot)
    b.swap('tr', 11, "outp e[e, e outp d T(H_d)]", "η", "inpt g",
           "Tile 8: bifun η / inpt g on TR (8,5)-(9,5)-(10,5)", b_new_pos=(9,4))
    # Tile 9: η / coev_e bifun on TR (inner H_d slot / outer wrap)
    b.swap('tr', 10, "outp e outp d T(H_d)", "η", "coev_e",
           "Tile 9: bifun η / coev_e on TR (7,5)-(8,5)-(9,4)", b_new_pos=(8,4))
    # Tile 10: η / outp g bifun on TR (inner H_d slot / outer outp d→outp e)
    b.swap('tr', 9, "outp d outp d T(H_d)", "η", "outp g",
           "Tile 10: bifun η / outp g on TR (6,5)-(7,5)-(8,4)", b_new_pos=(7,4))
    # Tile 11 [KEYSTONE]: naturality of η at α — (α, η) ≡ (η, T(α))
    b.swap('tr', 8, "outp d outp d T([d, T(z)])", "η", "T(α)",
           "Tile 11 [KEYSTONE]: η-naturality at α on TR (5,4)-(6,5)-(7,4)", b_new_pos=(6,4))
    # Tile 12: T(α) / outp g bifun on TR (inner T-stack / outer outp d→outp e)
    b.swap('tr', 9, "outp e outp d T([d, T(z)])", "outp g", "T(α)",
           "Tile 12: bifun T(α) / outp g on TR (6,4)-(7,4)-(8,4)", b_new_pos=(7,3))
    # Tile 13: T(α) / coev_e bifun on TR (inner T-stack / wrap into [e,e⊗-])
    b.swap('tr', 10, "outp e[e, e outp d T([d, T(z)])]", "coev_e", "T(α)",
           "Tile 13: bifun T(α) / coev_e on TR (7,3)-(8,4)-(9,4)", b_new_pos=(8,3))
    # Tile 14: T(α) / inpt g bifun on TR (inner T-stack tail / inner e outp d slot)
    b.swap('tr', 11, "outp e[e, T(d) T([d, T(z)])]", "inpt g", "T(α)",
           "Tile 14: bifun T(α) / inpt g on TR (8,3)-(9,4)-(10,5)", b_new_pos=(10,4))
    # Tile 15: τ-naturality at [d, α] in slot 2 — (T(α), τ) ≡ (τ, T(α))
    b.swap('tr', 12, "outp e[e, T(d [d, T(z)])]", "τ", "T(α)",
           "Tile 15: τ-nat at [d,α] slot 2 on TR (10,4)-(10,5)-(11,5)", b_new_pos=(11,4))
    # Tile 16: closure-counit ev_d ∘ (id ⊗ [d,α]) = α ∘ ev_d, lifted by T —
    # (T(id ⊗ [d, α]), T(ev_d)) ≡ (T(ev_d), T(α)). Now T(α) is the underlying T-α.
    b.swap('tr', 13, "outp e[e, T(T(z))]", "T(ev_d)", "T(α)",
           "Tile 16: T(closure ε at α): (T([d,α]), T(ev_d)) ≡ (T(ev_d), T(α))",
           b_new_pos=(12,4))
    # Tile 17 [KEYSTONE, deferred]: T-algebra associativity α ∘ T(α) = α ∘ μ_z is
    # available here (T(α) at edge 14, T(T(z)) at cell 14). Hold off on the relabel
    # until we have a concrete use for μ_z that matches LB structure.
    # Tile 18: η / T(inpt f) bifun on LB (H_c slot / T-stack slot)
    b.swap('lb', 9, "outp e[e, T(d outp c) T(H_c)]", "η", "T(inpt f)",
           "Tile 18: bifun η / T(inpt f) on LB (10,1)-(11,1)-(11,2)", b_new_pos=(10,2))
    # Tile 19: η / τ bifun on LB (H_c slot / T-stack laxator slot)
    b.swap('lb', 8, "outp e[e, T(d) T(outp c) T(H_c)]", "η", "τ",
           "Tile 19: bifun η / τ on LB (9,1)-(10,1)-(10,2)", b_new_pos=(9,2))
    # Tile 20: η / inpt g bifun on LB (H_c slot / e outp d Kleisli slot)
    b.swap('lb', 7, "outp e[e, e outp d T(outp c) T(H_c)]", "η", "inpt g",
           "Tile 20: bifun η / inpt g on LB (8,2)-(9,1)-(9,2)", b_new_pos=(9,3))
    # Tile 21: δ / outp g bifun on LB (inner outp c slot / outer outp d→outp e)
    b.swap('lb', 3, "outp d[e, e outp c outp c H_c]", "δ", "outp g",
           "Tile 21: bifun δ / outp g on LB (4,2)-(5,1)-(6,1)", b_new_pos=(5,2))
    # Tile 22: δ / outp f bifun on LB (inner outp c slot / outer outp c→outp d)
    b.swap('lb', 2, "outp c[e, e outp c outp c H_c]", "δ", "outp f",
           "Tile 22: bifun δ / outp f on LB (3,2)-(4,2)-(5,2)", b_new_pos=(4,3))
    return b


def hypothesis_snake_at_d():
    """Hypothesis: TR's coev_d ⨾ ... ⨾ T(ev_d) collapses by snake-at-d to identity,
    leaving the c-side and e-side computations. Test by collapse_range, then chain_diff."""
    b = replay()
    # Identify coev_d (TR edge 1) and T(ev_d) (TR edge 14).
    # Hypothesis: edges 1..14 collapse to "id" — i.e., zero residual edges.
    # This requires cells[1] == cells[15] (start of range == end of range).
    # cells[1] = "outp c outp c H_c", cells[15] = "outp e[e, T(z)]". Not equal — snake to id breaks the chain.
    # So instead: hypothesize that coev_d/T(ev_d) snake leaves a residual chain that travels
    # outp c outp c H_c -> outp e[e, T(z)] via the ATOMS THAT DON'T USE D.
    # Atoms in the d-block (edges 1-14): coev_d, outp f, η, inpt f, τ, T(ev_c), δ, η, T(α),
    #   outp g, coev_e, inpt g, τ, T(ev_d).
    # D-using atoms: coev_d, inpt f, T(α), inpt g, T(ev_d). Five atoms.
    # Non-D atoms: outp f, η, τ, T(ev_c), δ, η, outp g, coev_e, τ. Nine atoms.
    # Residual hypothesis: keep the 9 non-D atoms (in original relative order).
    residual_edges = ["outp f", "η", "τ", "T(ev_c)", "δ", "η", "outp g", "coev_e", "τ"]
    # Need 8 intermediate cells. We'll use placeholder strings; for chain-diff what matters is edges.
    residual_cells = [f"hyp_cell_{i}" for i in range(8)]
    b.collapse_range('tr', 1, 15, residual_edges, residual_cells,
                     "Hypothesis: snake-at-d removes the 5 d-using atoms (coev_d, inpt f, T(α), inpt g, T(ev_d))")
    return b


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'hypothesis':
        b = hypothesis_snake_at_d()
        print("=== HYPOTHESIS: snake-at-d eliminates d-using atoms ===")
        i, tr_res, lb_res = b.chain_diff()
        print(f"matched prefix length: {i}")
        print(f"TR residual ({len(tr_res)}): {tr_res}")
        print(f"LB residual ({len(b.lb_edges) - i}): {b.lb_edges[i:]}")
        print(f"\nFull TR edges: {b.tr_edges}")
        print(f"Full LB edges: {b.lb_edges}")
    elif len(sys.argv) > 1 and sys.argv[1] == 'simple':
        b = replay_simple()
        print(b.show())
        b.write_log("tile_replay_simple.log.jsonl")
        print(f"\n{len(b.log)} steps written to tile_replay_simple.log.jsonl")
    elif len(sys.argv) > 1 and sys.argv[1] == 'inner1':
        b = init_state_inner1()
        print(b.show())
    else:
        b = replay()
        print(b.show())
        b.write_log("tile_replay.log.jsonl")
        print(f"\n{len(b.log)} steps written to tile_replay.log.jsonl")
