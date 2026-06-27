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
