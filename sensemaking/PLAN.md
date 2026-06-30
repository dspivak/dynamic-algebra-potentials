# Sense-making / emergent-language experiment — PLAN

## Purpose

Test whether addressed, discrete, reusable communication — "a learned language",
or in the sense-making framing "a sense" — *emerges* as the low-rate, stable
structure of **nested predictive arrangements under a capacity bound**, and do so
entirely inside the DAP formalism, with every computation **factoring through the
fully-specified KQV attention suboperad of `sarr`**.

Companion documents:
- `attention-suboperad.tex` — the paper-faithful source for the KQV head.
- `AUDIT.md` — the adversarial auditor charter (run before every milestone is reported done).

## Methodological stance (anti-Goodhart)

LLMs tend to produce work that *passes the stated check* rather than work that is
*correct*. The defenses here are architectural, not promissory:

1. **Membership by construction.** Every experimental arrangement is a term in the
   free operad on KQV generators, realized in `sarr` by the functor `F`. "Factors
   through KQV" is a structural fact, checkable by tracing the generator tree — not
   a claim to be trusted. A computation that cannot be expressed with KQV
   generators + operad operations is reported as a *finding*, never routed around.
2. **Operad laws are tested numerically.** Associativity and unit of substitution,
   `Sigma_N`-equivariance, and functoriality of `F`
   (`compile ∘ substitute == dap_compose ∘ compile`) are property tests. A
   non-operadic `compile` fails them.
3. **Faithfulness is line-checkable.** The head's `out_f`, `in_f`, `U` are
   implemented from the exact equations of `attention-suboperad.tex`
   (`eq.attn`, `eq.pool`, `eq.Uattn`, carrier `Q` of `con.head`); the auditor
   compares code to equations.
4. **Independent audit.** A skeptical auditor (`AUDIT.md`) plus an external-provider
   audit (codex) verify 1–3 and hunt the specific cheats listed in `AUDIT.md`.
   The in-house auditor is a *first-pass adversary only* — same provider, shared
   blind spots — so the external audit is the real gate.

## The invariant (the suboperad / environment boundary)

- **suboperad layer** = the boxes: KQV head generators + operadic substitution +
  lens tensor. *Nothing here may contain a computation that is not a KQV generator
  or a sanctioned operad operation.*
- **environment layer** = the world/drive + the loss wiring + metrics.
- The boundary is explicit in the code layout (`sensemaking/kqv/` vs
  `sensemaking/world/` vs `sensemaking/experiments/`). The auditor checks the
  boundary is not crossed.

## Task 0 — Fully specify the KQV attention suboperad  *(FIRST; everything factors through this)*

0a. **Spec** (`sensemaking/kqv/SPEC.md`, math): the generator (types + the three
    maps faithful to `con.head`: carrier `Q = Vect(R^E, R^{d_q}⊕R^{d_k}⊕R^{d_v}) ⊕
    Vect(R^{d_v}, R^E)`, i.e. `(Wq,Wk,Wv,Wo)`; `out_f` = `eq.pool`; `in_f` =
    `eq.attn` with the `*`-index for the outer input; `U` = `eq.Uattn`, type
    `Q×out_M×in_N→R`); the operad operations (substitution = depth, lens tensor =
    width, `Sigma_N` action); the generated suboperad (`obs.generate`: heads
    generate, do not close); the functor `F : KQV → sarr`; interpretation by
    `Phiconf`/`Phiphase` into `pc`.
0b. **Code** (`sensemaking/kqv/head.py`): `attention_head(N, E, d, d_v, ...) ->
    SmoothArrangement` built from the equations; QKVO weights live in the reactive
    `Q`; the optimizer is the sharp `sharp_Q` (`rmk.optimizer`) or a regularizer
    added to `U` (writer monad adds potentials) — never an optimizer/penalty
    outside the formalism.
0c. **Law tests** (`sensemaking/kqv/test_operad_laws.py`): substitution
    associativity + unit; `Sigma_N`-equivariance of routing (`obs.equivariance`);
    functoriality of `F`; Moore-condition type check (`out_f` has no `in_N` arg,
    `rmk.moore`); potential-type check (`obs.erroreunit`); residual-width check
    (`out_M=in_M=R^E`, `obs.residual`).
0d. **Audit** Task 0 (run `AUDIT.md`). Fix. Report. **Recommend external codex
    audit here** — the whole edifice factors through this object.
0e. *(added after the external audit)* property-based composition auditor
    (`kqv/test_property_composition.py`: random trees, independent recursive oracle
    vs `realize`); the `KQVSystem` provenance wrapper (experiments carry + expose a
    `KQVTerm` trace); `SPEC.md` documents conditional well-posedness of the dynamics.

## Task 1 — Operadic nesting to arbitrary depth (N, N', N'', …)

- Free-operad **term tree**: node = KQV head (arity = #children); leaf = 0-ary box
  (prior-learner, `ex.zeroary`); depth unbounded.
- `compile(tree) -> SmoothArrangement` via operadic substitution (dap
  `compose_seq` / `tensor_arrangements` / wiring). Uniform `R^E` interface makes
  any head substitutable into any box.
- Tests: depth ≥ 4, mixed arities, `N'=0` leaves, large `N`; compiled `Q` =
  direct sum of node `Q`s; runs under `Phiconf` and `Phiphase`; unseen tree shapes
  compile and run (capacity for generalization is structural, not enumerated).

## Task 2 — World + partial-observability harness

- World (outer box): hidden slow latent `s(t)` (season) + fast observable `l(t)`
  whose statistics depend on `s` + weather noise `sigma`. Injected as the
  time-dependent `in_dir_from` closure into the down-leg `in_N` (per dap API).
- `N` inner boxes each receive a *different noisy partial slice* of `l`; no single
  slice determines `s`, the pool does. (Distributed partial observability is the
  engine that makes communication necessary, not merely helpful.)
- **Realized regime (locked in `world/standard.py` after the Task-2 audit).** The
  world is `Phiphase(world_arrangement)` (a coupled oscillator: slow season + 48 fast
  weather modes tethered to it). Sensing: `N=48` one-mode sensors with high
  independent sensor noise. The **strong every-box gate** holds across 8 weather
  seeds: even the *best* single sensor decodes `s` at R^2 <= 0.42, the typical one
  <= 0.18, while pooling all 48 gives R^2 ~ 0.76 and beats every single sensor by
  >= 0.34. Tradeoff (documented, not hidden): suppressing even the best sensor needs
  enough noise that pooled sits near the noise floor (~0.76), not ~0.9.
- **Second caveat (codex Task-2 finding): necessity is decoder-window-relative.** The
  season is slow and periodic, so a single sensor with a *long* temporal window (e.g.
  50) can extrapolate it (best_single climbs to ~0.75). The gate window (10) is matched
  to the experiment's SHORT-MEMORY boxes (per-step spatial attention, no long temporal
  accumulator), for which communication is genuinely necessary. **Task-3 constraint:**
  keep the boxes short-memory; decoder-window-robust necessity would instead need an
  *aperiodic (chaotic)* season (a future world variant). Tested in `test_world.py`.
- The boxes are KQV arrangements from Task 1; the prediction task is the head's
  canonical potential `U` (`obs.erroreunit`), not a bespoke add-on. Clean
  suboperad/environment boundary.
- **Provenance contract** (`AUDIT.md` C0): the experiment builds a `KQVTerm`, wraps
  it as a `KQVSystem`, and interprets only `system.arrangement`. No raw
  `SmoothArrangement` is ever interpreted in the experiment layer, so "factors
  through KQV" stays verifiable by inspecting `system.trace()`.

## Task 3 — Stage 1 experiment (smallest falsifiable): is the channel used?

- Flat (`N'=0`), `N=48` sensors (the strong-gate regime; swept in robustness checks),
  `Phiconf` workhorse.
- **Pre-registered PASS:** with capacity bound + distributed views, the channel is
  used (rate > 0) and both `I(message; s)` and prediction beat the *no-capacity*
  and *full-observability* controls, across ≥ 8 seeds.
- **Informative FAIL:** channel collapses (posterior collapse), or structure also
  appears in the controls (then capacity/distribution is not the cause).
- Controls (all implemented, all genuinely different from treatment):
  no-capacity, full-observability, shuffled-needs, init-baseline, conf-vs-phase.

## Task 4+ — Climb the sense-making arc

- Compression → symbols (timescale split; rate-distortion frontier in `beta`).
- Addressing (needs `N ≥ 3` + heterogeneous needs; success = routing `alpha`
  recovers the hidden dependency graph; interventional + ablation tests).
- The "click" = hysteresis = bistability (sudden jump in order parameters during
  the flow; hysteresis loop under a parameter sweep). Unifies the essay's "click",
  Dama's phase change, and "a symbol is a well".
- Weak supersession (behavior runs on the internalized `s`, raw input demoted to
  error signal). Strong supersession (repurposing) marked as horizon — likely a
  second, slower timescale, out of v1 scope.
- Nesting `N' > 0` for modularity and the generalization tests (the same learned
  generators compose into *unseen* trees and still work = substitution-invariance
  = compositionality).

## Phase R (LIVE, 2026-06-29) — the abstraction tower and the top-latent fix

**Reframe.** Sense-making realized as an operadic KQV tower of abstraction levels.
*This supersedes the necessity-gate framing of Tasks 2–3, diagnosed dead (it rewards
averaging, and a sense is not an average; commit 1b851d6).* Data clamped at the
BOTTOM (open source), sense read at the TOP, relaxed under `Phiconf` = hierarchical
predictive coding (`slo.pc`). Currently single-datum *weight* relaxation (not yet
multi-datum/temporal). Demo: `experiments/sense_demo.py` (commit 7285d57); every
arrangement a `KQVTerm` via `KQVSystem` (provenance per C0).

**Empirical state (depth sweep, this session).** Open tower, 16 bottom slots fixed
(data dim 64 in every row), `Phiconf`, η=0.05, seed 0, 150 steps:

| arities | depth | heads | %relax ΣU | ‖sense‖ | cos(senseA,senseB) |
|---|---|---|---|---|---|
| `[16]` | 1 | 1 | 0% | 0.058 | +0.895 |
| `[4,4]` | 2 | 5 | 23% | 0.916 | +0.424 |
| `[2,2,4]` | 3 | 7 | 10% | 0.195 | +0.828 |
| `[2,2,2,2]` | 4 | 15 | 17% | 0.007 | +0.844 |

Depth 1 collapses (silent); depth 2 forms a non-silent, datum-dependent sense; depth
3–4 regress, and depth 4 *re-collapses* (‖sense‖→0) even as ΣU keeps falling. Runtime
≈ ×2.5 per added depth (≈ O(#heads); per-head cost ~const), so log-runtime is ~linear
in depth. **Caveat:** single seed, 150 steps; depth-3/4 are likely under-converged.

**Diagnosis (primary, morphism-level).** `relax_bottom` feeds the root a zero apex
(`apex=0`; `boundary` returns `(0, apex_ctx)`). The root's potential (`eq.Uattn`) is
then `U = ½‖h − Ω·0‖² = ½‖h‖²` (Ω = Wo Wv, `rmk.circuits`) — an instruction to *be
silent*. The sense is read off those same children, so it is pulled to 0. **Conjecture:**
depth amplifies the zero-pull (each level inherits it) → the depth-4 re-collapse. The
single-level mechanism is certain; the depth-amplification is to be verified.

**Revised design (the target).** A *single* bidirectional predictive-coding tower
(untied = Rao–Ballard), not an encoder plus a bolted-on decoder. The same tower read two
ways: **forward / bottom-up** = inference (infer the causes that explain the clamped
data); **backward / top-down** = generation — the top-down prediction pass *is* the
"program" that re-emits the bottom inputs. "Makes sense of its world" = a short top code
regenerates the world. Five coupled choices:

1. **Relax activations, not just weights.** Make the per-level activations (causes)
   `z_ℓ` *inferred state* the dynamics moves, with `z_0` clamped to data. Sense = the
   inferred **top activation** `z_top`, not a one-shot `out_f` read. This is the genuine
   "inferred, not provided" sense.
2. **Two timescales, one flow (no explicit alternation).** Relax `Q = weights ⊕
   activations` under one conf-update; activations fast (large η), weights slow (small η).
   The large η-gap makes activations equilibrate inside each weight step (= inference)
   while the slow drift is learning — the per-level η-gradient, now across the
   weight/activation split. Adiabatic — keep the gap genuinely large.
3. **Untied predictor.** Fill `eq.Uattn`'s *schematic* `pred(W,n)` with its **own**
   generative weight, separate from the read-out OV `Ω = Wo Wv`. (The shared Ω was the
   *code's* concrete choice, not paper-enforced — `eq.Uattn` leaves `pred` schematic.)
   Untied = classical Rao–Ballard (`rmk.corners`).
4. **Momentum on weights, not activations.** Φdamped / Nesterov on the slow weights
   (accelerates; helps escape the all-zero stationary point); plain or critically-damped
   conf-update on the fast activations (oscillation would break the "settled" assumption
   the weight step relies on).
5. **Bottleneck at `z_top`** (low-dim) — else reconstruction is a trivial copy, not a
   sense (the capacity-bound theme).

**Anti-collapse status (vetted, still binding).** Clamped data makes the all-zero config
non-optimal, but that does NOT prove descent escapes it: (i) if `Ω → 0` the gradient on
`z_top` vanishes and all-zero is a *stationary point* (momentum on weights, choice 4, is
the lever); (ii) explanation can hide in weights / lower messages — nothing pins `z_top`
to the datum without (iii) a `z_top` prior `½‖z_top − μ‖²` (the deferred `prior_box`
potential) to break the gauge freedom (`Ω z` rescaling) and pin the sense.

**Faithfulness.** The *regime* is named in the paper: untied = Rao–Ballard PC
(`rmk.corners`); `Φconf` = predictions-down/errors-up; `pred` schematic so untying is
allowed (`eq.Uattn`); parameters-as-state-by-one-flow (`rmk.params`); the lens is
`eq.arr`. **The one extension:** activations as *relaxed state* — a fast carrier in `Q`
beyond `con.head`'s QKVO. Same block as before (the vetter's candidate (b) needs a spec
revision); **route (2)** — a formal activation/prior generator proven to factor through
`sarr` — is preferred. So: faithful in regime, blocked on exactly one formalization (the
activation carrier).

**Tests (pre-registered).**
- **Baseline (cheap first check):** a bolted-on autoencoder — KQV encoder tower → low-dim
  bottleneck → KQV generator tower — trained to reconstruct the clamped data. Question:
  can a bottleneck code regenerate the world *at all*? (Two systems; sanity check only.)
- **Target:** the *single* bidirectional tower above; its top-down pass regenerates the
  clamped data; sense = inferred `z_top`.
- **Stationary-point test (vetter; run FIRST).** Does the silent state persist under
  random AND near-zero inits? Near-zero is adversarial. Monitor `‖Ω‖` and the generative
  weight — if collapse tracks norm→0, that is mechanism (i); a `z_top`/activation prior is
  the lever.
- **Metrics:** reconstruction error; compression (bottleneck dim vs data dim);
  datum-dependence (cos of `z_top` across two data); timescale separation actually
  achieved.
- **PASS:** non-trivial reconstruction at a real bottleneck; `z_top` datum-dependent (cos
  well below 1); no silent stationary point at near-zero init.
- **FAIL (informative):** only trivial-copy reconstruction (no compression), or `z_top`
  collapses ⇒ the untied / activation-inference design isn't the cure; look to
  over-squashing in `eq.pool` or the carrier.
- **Gate.** Pick the activation-carrier route (1/2/3) before the target counts as
  faithful; until then it tests mechanism only.

**Provenance/faithfulness (must hold).** Everything a `KQVTerm` via `KQVSystem`; no raw
`SmoothArrangement` interpreted in the experiment layer (C0). the activation carrier resolved
against a faithfulness route (1/2/3) before it counts as "inside the suboperad."
η-gradient only as data of the sharp (A5); no optimizer/penalty outside `U`/`sharp_Q`.

## Phase R — results & reframe (2026-06-29)

Generator 3 BUILT and faithful (`kqv/cell.py`; G1–G5 + operad laws pass). The tower ran
(`experiments/activation_tower.py`). Outcome, honestly:

- **Near-zero init is retired as the bar (user's call).** The dead zone is pervasive and
  depth-amplified; near-zero freezes the whole tower; that is a cold-start artifact of
  bilinear/PC systems, not a property of the suboperad. Use **random init**, where the tower
  escapes.
- **The result that matters is structural, not a pass/fail.** From random init `z_top` is
  datum-dependent but tiny, and only ~⅓ of the data is reconstructed — because the head's
  prediction `Ω·n` is one broadcast `R^E` vector, so a head can only explain what its `N`
  inputs *share* (~`1/N`; for i.i.d. data the mean). **i.i.d. data has nothing to compress**;
  the test data, not the head, was the bug. (Full write-up: `kqv/SPEC.md` **Findings**.)
- **Reframe of the architecture:** heads *summarize shared structure*, cells *reconstruct*;
  compress only at `z_top`, not at every interface. The forward path forward: **Generator 4 —
  the residual head** (`kqv/SPEC.md`): each box predicts its children from its own state and
  emits a *compressed residual* (`out_f`), so higher levels work on the unexplained part and
  find longer-range causes. Moore-legal because the subtracted prediction is the box's own
  state, not the top-down `n`.

**Next pre-registered test (Phase R′).** Hierarchically-structured data (long-range
correlations carried by low-dim multi-scale causes); residual cells between levels; measure
whether a distant correlated pair (box 3 in medium A, box 6 in medium B, same grandparent) is
predicted **better because** its residual structure climbed the tree (vs. a flat / no-hierarchy
control). PASS = the cross-group coupling appears only with the hierarchy. This, and the
faithfulness of Generator 4's design, are what **codex** audits and **bets** on
(`AUDIT.md` **Bet**, `CODEX_BRIEF.md`).

## Audit cadence

- **In-house auditor (`AUDIT.md`): I run it automatically at the end of every Task,
  before reporting the Task done.** No action needed from the user.
- **External codex auditor (user-run): recommended at (1) end of Task 0 — the
  formal object, highest leverage; and (2) after the first claimed result
  (Stage 1).** More often on request. `AUDIT.md` + `kqv/SPEC.md` are kept as
  stable, well-scoped targets so the external run is cheap and independent.
- The in-house auditor does not substitute for the external one.

## Open decisions (for the user)

- Code location: proposed `sensemaking/` at repo root, importing `dap-core`
  (keeps speculative code out of the public dap submodule). Confirm or redirect.
- Will you run codex at the Task 0 gate, or should I also prepare a codex-specific
  brief (a frozen spec + check-list it can run without my context)?
