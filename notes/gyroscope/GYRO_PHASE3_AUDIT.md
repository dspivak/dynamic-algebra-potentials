# Audit brief: `dap` Phase 3 — the faithful gyroscope machine

**What to review:** the uncommitted Phase-3 work in the `dap-core` submodule (repo
root), branch `faithful-machine` (off `orgk-rk4`), captured in
`GYRO_PHASE3_REVIEW.patch` (this folder; 12 files). It builds the Bull & Achour
gyroscope-and-springs classifier entirely from the paper's constructions.

**Recommended reviewer:** Opus, high/max reasoning. There is real categorical and
naturality content here; **run the tests and try to break the claims**, don't just read.

---

## The frame (audit against THIS goal, nothing else)

The goal (the north star) is a **standalone expressiveness
demo**: show that a real published ML-physics machine **factors through the paper's
dynamics functor `Phi`**, equation-faithfully and assembled from the paper's own
constructions, with the **springs→0 ablation** as the one genuinely interesting result.
It is **NOT** a paper result and **NOT** a benchmark — there is deliberately **no
external accuracy claim**, and the data is purely synthetic.

So judge: *is the math right, does it genuinely factor through the framework, and is
every claim honestly scoped?* — **not** "does it match the blog's 0.834."

---

## Part A — the math (run it; reproduce the numbers)

### A1. Quadratic-drag 1-form (`integrator.quadratic_drag_kick`, `gyro_phase_integrator`)
The blog's air drag `~ -|v| v` as a 1-form `omega_drag = (|v| v, 0)`, per gyro. The
claim rests on **`rmk.adam`** (.tex ~line 2854): restricting `Q` to a subcategory
weakens *naturality* (allowed — "lives over a smaller Q") but **monoidality over `⊕`
cannot be negotiated** (compositionality). Verify, via `test_drag_one_form.py`:
- **monoidal over `⊕`** (block-diagonal per gyro) — the non-negotiable part; drag passes;
- **natural only over per-gyro `O(2)`**, and the restriction is **real** — the test shows
  a non-orthogonal per-gyro map breaks naturality. Confirm `|v|` is `O(2)`-invariant but
  not invariant under a general sharp-equivariant iso, so the subcategory is exactly the
  orthogonal one (top of `rmk.adam`'s chain). Flag any overstatement.

### A2. Hex springs from the prism wiring (`wiring.py`: `vdim` + `onsite`; `test_vector_graph.py`)
`compose_graph`/`harmonic_vertex`/`graph_wire` are generalized from scalar `R^1` to
`R^vdim` vertices + an on-site potential. Verify:
- the **`R^2` graph Laplacian `Σ_e (κ/2)|q_tgt − q_src|^2` EMERGES** from composition on a
  hex topology, matching the independent oracle (it is *not* a hand-written `U`);
- the on-site term adds per vertex; **`vdim=1` is byte-unchanged** (the paper's scalar
  graph test `test_graph_laplacian.py` still passes — confirm);
- the prism routing handles `vdim`-blocks correctly (`comp_perm`).

### A3. RK4-phase integrator (`rk4.rk4_gyro_integrator`, `Phirk4gyro`; `test_rk4_gyro.py`)
RK4 on the phase ODE `q̇ = sharp(ξ)`, `ξ̇ = −dU − drag·F(v) − γ⊙(Jv)`, as an `org^(4)`
morphism (the K=4 `IntegratorK` pushed through `orgK_from_integrator`). Verify:
- it is **genuinely 4th order on the phase system** — reproduce the global error vs the
  exact flow `e^{AT}`; ratios should approach 16 (reported 16.6→16.1). If it is secretly
  2nd/3rd order, say so;
- one macro-tick **equals a hand-rolled RK4 step including the drag and per-gyro γ**;
- it really runs through the framework: each of the 4 rounds emits a stage position and
  `dU = ξ_Q` comes from the interpretation's backward pass (not hand-computed) — the
  drag/γ are added in the stages. Confirm this is the case, not a bypass.

### A4 / A5 / A6 (smaller; `test_faithful_physics.py`, `test_faithful_machine.py`)
- **Rod gravity** `−g√(L²−|q|²)`: restoring well, nonlinear stiffening, small-tilt limit
  `(g/L)q`. Confirm; note the `|q| < L` validity constraint is honored in tests.
- **Per-gyro γ**: a vector `gamma` precesses each gyro at its own rate, with **no integrator
  change** (it broadcasts against `J v`). Confirm.
- **NaN fix**: `quadratic_drag_kick` uses a double-`where` so `|v| v` is differentiable at
  `v = 0` (rollout starts at rest). Confirm it (a) leaves `|v| v` **exact** away from 0 and
  (b) gives the **correct gradient (0)** at `v = 0` — not an `eps` fudge that perturbs the value.

---

## Part B — the factorization (the central claim; try hardest to break this)

`gyroscope_faithful.faithful_arrangement` builds the open-port classifier **on
`compose_graph`**. Verify (`test_faithful_machine.py` + reading):
- the classifier's potential **is** the wired `R^2` Laplacian + rod gravity − drive
  (matched to an oracle) — i.e. the **spring coupling comes from the prism wiring**, not a
  hand-written `U`. This is what makes the springs ablation a wiring fact;
- the rollout **genuinely runs through** `Phirk4gyro` → `orgK_from_integrator` →
  `smooth_interpretation`, with the force `= jax.grad(U)` (the framework's backward pass).
  Try to find a place where the physics is hand-computed outside the functor;
- **Honest judgment call for you to make** (not pre-decided): the spring coupling and rod
  gravity *emerge from composition*, but the **drive (`−⟨n_in, q_in⟩`) and the output
  readout are added by hand** as the open I/O interface. Is that the right line — "the
  coupling is categorical, the I/O is the interface" — or does the hand-added interface
  undercut the factorization claim? Say what you think, and whether the prose claims more
  than this.

---

## Part C — the springs→0 ablation (the headline; reproduce it)

`test_faithful_machine.test_springs_zero_collapses_information_flow`. With springs, the
input signal reaches the output gyros and depends on the input; freeze the stiffness
(`log_kappa → −∞`) and the output gyros stay at rest **regardless of the input**. Verify:
- it reproduces, and the mechanism is genuinely *wiring* — input gyros (left column) and
  output gyros (right column) are disjoint, so with no spring path no force reaches the
  output (which starts at equilibrium where `∇U = 0`). Confirm this is the reason, not an
  artifact of the particular init/seed;
- is "stays at rest" exact, or merely `< 1e-9` (stiffness frozen to `~4e-44`, not exactly
  0)? Note which; either is fine if stated honestly.

---

## Part D — honesty / scoping

- **No accuracy claim anywhere.** The trainability test asserts only that the **loss
  decreases** (an earlier weak/lucky 0.64 val-acc was deliberately dropped). Confirm no
  accuracy assertion or boast crept into code, tests, or docstrings.
- Beyond-paper pieces (drag 1-form, gyroscopic 1-form, RK4-as-`org^(K)` without a
  functoriality proof) are **banner-labeled** with their caveats. Confirm.
- The grep `grep -rni "reproduc\|0.834\|matches the blog\|state of the art" dap` should
  surface no overclaim.

**Known & intentional deviations — do NOT flag these as bugs** (they are the design under
the "no accuracy claim" goal): small scale (3×3 hex, not ~100-gyro/261-spring); uniform
mass/stiffness (not per-gyro per-edge); short synthetic strokes (not 8-pt/100-step
PenDigits); the drive/readout are the hand-added I/O interface; RK4 is non-symplectic.

**Not yet done (intentionally — audit is requested first):** the README **deviation
table** + a demo line + the commit are pending. So absence of README documentation of the
faithful machine is expected, not a finding — but if you think a deviation MUST be in that
table, list it.

---

## How to run

```bash
cd dap-core
.venv/bin/python -m pytest dap/tests -q          # expect 75 passed, 1 skipped
.venv/bin/python -m pytest dap/tests/test_faithful_machine.py dap/tests/test_rk4_gyro.py \
    dap/tests/test_vector_graph.py dap/tests/test_drag_one_form.py \
    dap/tests/test_faithful_physics.py -q        # the Phase-3 tests
```
Reproduce independently: the RK4-phase h^4 ratios vs `e^{AT}`; the `R^2` Laplacian
emergence vs your own oracle; the springs-on vs springs-off output readout.

## Deliver

A per-item verdict (pass / fail / overclaim), **distinguishing real defects from the
intended deviations above**. Be adversarial: try to break the factorization (find
hand-computed physics outside the functor), falsify the 4th-order or the Laplacian
emergence, and find any accuracy/overclaim. The factorization (Part B) and the ablation
(Part C) are the load-bearing claims — weigh them hardest.

## Pointers

- Paper: `dynamic-algebra-potentials.tex`. Labels: `rmk.adam` (~2854), `rmk.multistage`
  (~2118), `sec.graph_laplacian`, `prop.one_forms_vector_space`, `def.cot`.
- Plan + goal: stated in "The frame" above (the prior `GYRO_BUILD_HANDOFF.md` was
  folded into the repo reorg). Phases 1–2 are committed on the dap branch `orgk-rk4`
  (public). Blog: https://unconv.ai/blog/machine-learning-with-dynamics/.
