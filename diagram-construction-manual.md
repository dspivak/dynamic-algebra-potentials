# Diagram Construction Manual

A working guide for building pasting diagrams that prove coherence equations. Written from experience filling in `Theta(id_c) = id` and `Theta(g∘f) = Theta(g)∘Theta(f)`.

## The setup

You're proving an equation between two long composites in a category. Draw both composites as the **two boundary paths** of a single big diagram, sharing start and end nodes. Everything inside is the **open hole**: the region you must tile, where each tile is one named coherence fact.

## The core process

1. **State the obligation.** Identify the two composites and their shared endpoints.

2. **Atomize the boundary.** Each boundary arrow performs **exactly one nonidentity operation** — all other tensor/internal-hom structure is identity. If your displayed definitions use composites (e.g., a coKleisli identity, a strength σ that's defined as `τ ∘ (id ⊗ η)`), expand them so that single-atom arrows live on the boundary. Bold the nonidentity part of each label so it's visually checkable.

3. **Choose a layout.** Decide whether the two boundary chains run as two columns down the page, or as an L-shape (one going down then right, the other right then down) so they share top-left and bottom-right corners. Estimate page width (each column needs roughly enough space for a `coev`-sized arrow label) and pick column count to fit. **Use juxtaposition for tensor and shorthand `H_X = [X, z]` etc. to keep cells short.**

4. **The boundary changes after every tile.** This is the central concept. The open hole is bounded at any moment by **two long composites** from shared start to shared end. When you add a tile, those two composites get rerouted: one boundary path now runs through the new interior node introduced by the tile.

5. **To add a tile, find two adjacent atoms on the current boundary, on independent slots.** Bifunctoriality is the workhorse: if atom A acts on tensor slot 1 and atom B acts on slot 2, they commute. Add a NEW interior node where one atom is applied alone, then close the square with the other atom. Coev/ev-naturality is the analogue when one atom wraps a slot in `[X, –]`.

6. **Topological validity check before committing a tile.** A planar pasting diagram allows each edge to be on the boundary of at most TWO 2-cells (one on each side). Before placing a new tile, verify:
   - **Every non-fresh edge of the tile is either on the open-hole boundary or shared with exactly one existing tile** — never with two. An edge already shared between two existing tiles is "saturated" and cannot be a third tile's edge.
   - **Every non-fresh vertex is still adjacent to the open hole.** A vertex surrounded by completed tiles is "trapped" and shouldn't be reused as a new tile's corner — the new tile can't push the boundary anywhere.
   - **At least one edge of the new tile must be on the current open-hole boundary.** Otherwise you're filling a sliver between existing tiles, not extending into the hole.
   If any of these fails, pick a different tile.

7. **Use the empty space.** Interior cells (cols/rows not on the boundary) are available for new nodes. Don't crowd new nodes against the boundary — push into the middle when the structure of the equation lets you. Diagonal arrows (`[dr]`, `[ddl]`, `[ull]`, etc.) let new interior nodes connect to non-adjacent boundary cells.

   **Tracing the inner boundary (forward-arrows-only formula).** The open hole's inner boundary runs between a **split point** and a **merge point** — these bookend the boundary and are shared by the two composite paths. The split point is (1,1): the two outgoing arrows there ([r] and [d]) start the two distinct paths. The merge point is the cell where the two paths re-converge into a shared final edge — that shared edge is interior to the closing tile (not on the boundary), so the merge cell itself is the last entry. The terminal node *past* the merge edge is **not** in the boundary.

   Between the split and merge points, each path dips into the hole by a *mirror* greedy rule:
   - **Topright** (upper composite): from (1,1) take `[r]` (RHS chain start). At every subsequent cell take the forward outgoing arrow whose target has the **smallest** column (ties broken by smallest row).
   - **Leftbottom** (lower composite): from (1,1) take `[d]` (LHS chain start). At every subsequent cell take the forward outgoing arrow whose target has the **largest** column (ties broken by largest row).

   Geometric intuition: the open hole sits between the two paths. Topright walks the upper-right perimeter — the hole is to its lower-left, so each branching dips *left* (smallest col). Leftbottom walks the lower-left perimeter — the hole is to its upper-right, so each branching dips *right* (largest col). Forced edges (single forward arrow) just continue the path.

8. **Each tile = one named fact** from your vocabulary. For closed monoidal + monoidal monad + T-monoid:
   - comonoid counit / coassoc / homomorphism (when an outp factor is comonoidal)
   - coev / ev naturality in either argument at a specific morphism
   - closure triangles (snake): `ev ∘ coev = id`, `[c, ev] ∘ coev = id`
   - η monoidal: `τ ∘ (η ⊗ η) = η_{X⊗Y}` (subsumes both strength unit laws)
   - η natural at any specific `f`: `T(f) ∘ η = η ∘ f`
   - definition of strength: `σ = τ ∘ (id ⊗ η)` and the left version
   - algebra unit `α ∘ η_z = id_z`, algebra associativity `α ∘ T(α) = α ∘ μ_z`
   - bifunctoriality of `[–, –]`, of `⊗`, of `T`, of `[c, –]` when c-slot is fixed

9. **Open up composite morphisms via their definitions** when no clean tile fits. `σ = τ ∘ (id⊗η)` is the canonical example: replacing one σ-arrow with two arrows through a new intermediate node often reveals bifunctoriality squares that weren't visible when σ was a black box. Same for `α_H` lifted to internal-homs, the snake `[c, ev] ∘ coev = id`, etc. Apply this to internal arrows, not just boundary.

10. **Curved arrows for shortcut identifications.** When a single named fact equates two paths from A to B, draw a curved arrow A→B for the shortcut and a chain of straight arrows for the long route — one tile then justifies the curve. Also for "same object at two positions" (an equal-arrow with bend).

11. **Boundary vs filler maps.** Boundary atoms must trace back to the displayed definition you're proving — they aren't free to be invented. Filler maps (the ones inside new interior nodes) need a tile justification. This distinction stops you from sneaking in atoms that aren't part of the obligation.

12. **Compile after every change.** Wrong cell count, wrong arrow direction, or a duplicate node name are easier to catch in the PDF than in the source. Source-only review is not enough.

## Tikzcd recipes

**Tile labels via named arrow midpoints** (robust to layout edits):
```latex
\ar[r, "label", ""{description, name=A1, anchor=center, inner sep=0}]
% after the matrix body:
\arrow[phantom, from=A1, to=A2, "(i)"{description}]
```

**Triangles with equal hypotenuse** — use object aliases:
```latex
|[alias=tl]| ...   |[alias=ce]| ...
\arrow[phantom, from=tl, to=ce, "(iv)"{description}, bend left=30]
```

**Short arrows with no room for over/under labels.** Don't use `description` — it places the label inside the arrow path, but a one-cell-span arrow has no room. Use over (default `"label"`) or under (`"label"'`) and let neighboring labels sit on opposite sides.

**Multi-step direction strings** like `[ddr]`, `[dlll]`, `[ddrr]`, `[ull]` are valid in tikzcd — combine `d/u/l/r` letters in any order for diagonals across multiple cells.

## Anti-patterns

- **Sliver tiles** that share both incoming edges with existing tiles. They capture a node but don't push the boundary inward.
- **Big bent long arrows** trying to close a hole without intermediate nodes — usually means a missing node.
- **Vague tile labels** ("by closure", "by strength") — always reduce to a specific named fact.
- **Hiding atoms inside composite labels** (e.g., a coKleisli identity abbreviated as just `id`, hiding `(id⊗ε)∘η`).
- **Stripping labels to bold while structure is in flux** — type-checking is your error-finder; do this last.
- **Mentally transposing** an entire composite. Don't. Insert the relevant `coev` / `ev` arrows as concrete edges; let the diagram do the work.
- **Tiles you can't justify with one named fact.** If you need two facts, it's two tiles.

## Working pace

Most tiles are bifunctoriality / naturality squares, mostly mechanical once the layout is set. Aim for one tile per edit, compile, glance, next. Reshaping the layout is the main creative act; tiling is the assembly line. Be fast — iterating with compile-after-every-edit catches errors faster than thinking does.

## Tile-replay tracker (`tile_tracker.py`)

The boundary at any moment is two paths from a shared start to a shared end. The tracker keeps these as Python lists with edge labels between consecutive cells, and exposes two operations:

- `swap(side, idx_a, b_new, e1, e2, fact)` — replaces `a -[old_e1]-> b -[old_e2]-> c` with `a -[e1]-> b_new -[e2]-> c`. Applied when a 2-cell (bifunctoriality, naturality, etc.) lets you exchange two adjacent atoms. Tabooes `b_new`; lifts taboo on `a` and `c` (their incident boundary edges changed).
- `collapse(side, idx_a, e_ac, fact)` — replaces `a -[old_e1]-> b -[old_e2]-> c` with `a -[e_ac]-> c`, dropping `b`. For degenerate tiles where the composite reduces (e.g., `α ∘ η = id`, `[c, ev] ∘ coev = id`). No taboo placed.

**Taboo rule.** Each `swap` marks `b_new`. The mark prevents the *next* swap from immediately reintroducing the cell that was just removed. The mark lifts automatically when any incident boundary edge changes — i.e., when the cell becomes the `a` or `c` of a later swap. Taboos can persist for many steps if no later tile touches that cell; that is fine.

**Initial state.** The script's `init_state()` returns the unfilled-rectangle boundary: the two outer composite chains of the displayed obligation in atomized form. For the composition diagram in `prop.Theta_T_alpha`, the TR side has 16 cells / 15 atoms and the LB side 15 cells / 14 atoms, both ending at `outp e[\inpt e, T(z)]`. (The final `α` to `outp e\,H_e` is past the merge and not part of the boundary.)

**Replay protocol.** When you add a tile in the LaTeX source, mirror it with one `swap` (or `collapse`) call in the script in the same order. The script's log file (`tile_replay.log.jsonl`) is the authoritative record of moves; read it back to recover the sequence of swaps and verify that no tile undoes its predecessor. A tile is suspect if (a) its `b_new` is currently tabooed, (b) the same `b_new` was tabooed and untabooed cyclically, or (c) the tile reproduces a swap already applied in an earlier diagram (e.g., re-swapping atoms that the top diagram already swapped). Always run the replay end-to-end after adding a swap; an unexpected `taboo violation` from the script means the math probably has a cycle.

**Source.** The full script lives at `tile_tracker.py`; the core class is reproduced here so the manual is self-contained.

```python
import json
from dataclasses import dataclass, field


@dataclass
class Boundary:
    topright: list                 # cells along upper composite (in order)
    leftbottom: list               # cells along lower composite (in order)
    tr_edges: list                 # tr_edges[i] = label of edge topright[i] -> topright[i+1]
    lb_edges: list
    taboo: set = field(default_factory=set)
    log: list = field(default_factory=list)

    @classmethod
    def init(cls, tr_cells, tr_edges, lb_cells, lb_edges):
        assert len(tr_edges) == len(tr_cells) - 1
        assert len(lb_edges) == len(lb_cells) - 1
        assert tr_cells[0] == lb_cells[0], "paths must share the start cell"
        assert tr_cells[-1] == lb_cells[-1], "paths must share the end cell"
        return cls(list(tr_cells), list(lb_cells), list(tr_edges), list(lb_edges))

    def _path(self, side):
        if side == 'tr':
            return self.topright, self.tr_edges
        if side == 'lb':
            return self.leftbottom, self.lb_edges
        raise ValueError(f"side must be 'tr' or 'lb', got {side!r}")

    def swap(self, side, idx_a, b_new, e1, e2, fact):
        cells, edges = self._path(side)
        if not 0 <= idx_a <= len(cells) - 3:
            raise IndexError(f"idx_a={idx_a} out of range for path of length {len(cells)}")
        a, b, c = cells[idx_a], cells[idx_a + 1], cells[idx_a + 2]
        if b_new in self.taboo:
            raise ValueError(f"taboo violation: {b_new!r} is currently tabooed")
        old_e1, old_e2 = edges[idx_a], edges[idx_a + 1]
        cells[idx_a + 1] = b_new
        edges[idx_a] = e1
        edges[idx_a + 1] = e2
        self.taboo.add(b_new)
        self.taboo.discard(a)
        self.taboo.discard(c)
        self.log.append({
            'step': len(self.log) + 1, 'op': 'swap', 'side': side, 'fact': fact,
            'before': [a, old_e1, b, old_e2, c],
            'after':  [a, e1, b_new, e2, c],
            'taboo_added': b_new,
        })

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
```

The project-specific `init_state()` (cells/edges of the outer perimeter) and `replay()` (the sequence of `swap`/`collapse` calls) live in `tile_tracker.py` proper, since they grow with each tile added.

## Workflow: tile-by-tile keystone-driven proofs

This section distills the rhythm that emerged during tiles 8-16 of `prop.Theta_T_alpha`. Tiles 1-7 were exploratory: each tile required hunting through the LaTeX to figure out where the boundary was, what was adjacent, and whether the resulting cell would even be drawable. Tiles 8-16 went roughly 3-5x faster. The differences are mechanical, not creative — once the loop is in place, most tiles take a minute.

### The tight loop

Every tile follows the same four-step loop, in order, with no skipping:

1. **Edit the script first.** Add a `b.swap(...)` line in `replay()` with the new `b_new`, edge labels, and `b_new_pos`. Do not touch the LaTeX yet.
2. **Run the script.** `python3 tile_tracker.py` validates: taboo not violated, position arrows non-degenerate, fact string spells out which atom moved past which on which slots. If the script crashes, the proposed tile is wrong (or wrongly indexed) — fix before going further.
3. **Edit the LaTeX.** Open the new interior node, redraw the two outgoing arrows of the swap, mark the existing cell that was displaced.
4. **Compile.** Read the PDF, not just the source. Wrong arrow directions and missing nodes show up immediately as overlapping labels or stray edges.

Two things make the loop tight: the script catches geometric errors *before* LaTeX, and LaTeX catches typesetting errors *before* the next tile. The script and the diagram are the same proof in two presentations; they have to agree at every step. If they don't, stop and reconcile.

### Position bookkeeping: `b_new_pos` and `_arrow_dir`

Every cell now carries an `(row, col)` coordinate (`tr_pos`, `lb_pos`). When you call `swap`, the keyword arg `b_new_pos` is mandatory. The script then computes:

- `arrow_a_to_new = _arrow_dir(a_pos, b_new_pos)`
- `arrow_new_to_c = _arrow_dir(b_new_pos, c_pos)`

These are tikzcd direction strings (`d`, `dr`, `ddl`, `r`, etc.) that tell you exactly what to type in the LaTeX. If either resolves to `'self'` (i.e., `b_new_pos` coincides with `a_pos` or `c_pos`), the swap is rejected. This is the single biggest reliability win: previously a typo like `[d]` instead of `[dr]` would compile fine and produce a silently wrong diagram. Now the script refuses the move, and the log records the arrow directions so the LaTeX edit is mechanical transcription.

Concrete example from Tile 11 (the keystone, see below):

```
b.swap('tr', 8, "outp d outp d T([d, T(z)])", "η", "T(α)",
       "Tile 11 [KEYSTONE]: η-naturality at α on TR (5,4)-(6,5)-(7,4)",
       b_new_pos=(6,4))
```

`a_pos = (5,4)`, `b_new_pos = (6,4)`, `c_pos = (7,4)` — so the script logs `a_to_new = 'd'`, `new_to_c = 'd'`. The LaTeX edit is then unambiguous: the new node sits at `(6,4)`, with `\ar[d, "η"]` going in and `\ar[d, "T(α)"]` going out.

### Descriptive script labels vs. compact LaTeX labels

The script's cell strings are *semantic* and verbose: `"outp d outp d T([d, T(z)])"`. The LaTeX label is the same content rendered with macros: `\outp d\,\outp d\,\Fun T([\inpt d,\Fun T(z)])`. The script's edge labels are similar — `"T(α)"` for what LaTeX writes as `\Fun T(\alpha)`, `"T(ev_d)"` for `\Fun T(\ev)` (the LaTeX often drops the `_d` subscript, since the slot makes it unambiguous, but the script keeps it for tracking).

The split is deliberate. The LaTeX is for the reader; brevity and macro-uniformity matter. The script is for you, mid-proof; explicitness about *which* `ev` or *which* slot you're tracking matters more than brevity. When you write `"T(α)"` in the script and `\Fun T(\alpha)` in LaTeX, you're trusting that the verbose form in the script will catch a confusion the compact LaTeX would hide. This pays off most when the same atom (e.g., `η`) appears in three different slots simultaneously.

### Keystones and slides

A **keystone** tile is one that introduces a *new atom* the boundary didn't previously contain — not a permutation of existing atoms via bifunctoriality, but an honest naturality move that injects new content. In the present diagram, Tile 11 is the first keystone:

> Tile 11: `(α, η) ≡ (η, T(α))` by η-naturality at α.

Before Tile 11, the boundary had `α` followed by `η` in adjacent positions. After Tile 11, those are replaced by `η` followed by `T(α)`. The atom `T(α)` is new — it is not on the perimeter of the obligation, and no bifun rearrangement could have produced it. Keystones are the load-bearing tiles of the proof; everything else is plumbing.

Once a keystone has fired and a new atom is on the boundary, the next several tiles are typically a **slide**: bifunctoriality moves the new atom forward (or backward) through atoms acting on independent slots, until it reaches a position where the *next* keystone can fire. Tiles 12-16 are exactly this slide:

| Tile | Move | Slot logic |
|------|------|------------|
| 12 | `T(α) / outp g` bifun | T-stack inner / outer outp d→outp e |
| 13 | `T(α) / coev_e` bifun | T-stack inner / outer wrap into `[e,e⊗-]` |
| 14 | `T(α) / inpt g` bifun | T-stack tail / inner e·outp d slot |
| 15 | `(T(α), τ) ≡ (τ, T(α))` τ-nat at `[d,α]` slot 2 | strength-naturality, second keystone |
| 16 | `(T([d,α]), T(ev_d)) ≡ (T(ev_d), T(α))` | T applied to closure-counit (third keystone) |

After Tile 16, `T(α)` has slid all the way from its origin (post-α on the right) to a position adjacent to the existing `α` on the LB side — the exact configuration where T-algebra associativity `α ∘ T(α) = α ∘ μ_z` can fire as the *fourth* keystone.

Recognizing this rhythm — keystone, then slide, then keystone — is the difference between "what tile next?" (slow) and "I need T(α) at position (12,4) so I can hit T-alg-assoc, what's between here and there?" (fast). Plan the slide *before* placing the keystone, so you know the keystone is worth firing.

### Per-tile reasoning: before vs. after

For each tile (especially slides), the reasoning is uniform:

1. **Identify the two adjacent atoms** on the current boundary at the splice point. Call them A and B.
2. **For each, name the slot it acts on.** A acts on the outer functor / `[c,-]` wrap / inner T-stack head / etc.; B acts on a *different* slot.
3. **Verify bifun-compatibility.** The two slots must be independent: tensor slots in `X ⊗ Y`, head/tail in `T(X) Y`, outer-vs-inner in `[X, Y Z]`. If both atoms touch the same slot, bifun is the wrong tool — you need a real naturality (a keystone), not a slide.
4. **Compute the new cell.** A applied alone, then B; or B applied alone, then A. The "before" cell is what you had; the "after" cell is what you're swapping in.
5. **Pick a position.** Usually one cell off the current boundary, in the open hole.

The fact-string in the script records all of this in one line: e.g., `"Tile 13: bifun T(α) / coev_e on TR (7,3)-(8,4)-(9,4)"`. Read it later and you can reconstruct *why* the tile was legal without looking at the LaTeX.

### Anti-patterns specific to this workflow

- **Skipping the script edit.** If you go LaTeX-first, you lose the position validation and the taboo check. Editing the script first is non-negotiable.
- **Dropping `b_new_pos`.** The script tolerates absent positions (legacy tiles), but every new tile should specify `b_new_pos` so the arrow directions are checked.
- **Vague slot descriptions.** A fact like `"bifun η / outp f"` is not enough — say *which* `η` (inner H_c wrap? inner outp c→T(outp c)?) and *which* `outp f` (outer outp c→outp d? inner-d slot?). When the same atom appears multiple times, only the slot disambiguates, and only the slot tells you whether bifun is even applicable.
- **Firing a keystone without a planned slide.** If you don't know where the new atom needs to end up, don't introduce it — keystones are expensive and create work. The right sequence is: identify the *next* keystone target, plan the slide backwards from there, then fire the current keystone.
