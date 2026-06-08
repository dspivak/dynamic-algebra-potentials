# PARAMETERIZE_PLAN.md — superseded (historical)

**This is a fossil. Do not execute it.** It was a one-shot build plan from an
early stage of the paper and has been fully superseded by later restructuring.
Its premises no longer hold:

- It assumes one functor `\Phi : \potlens -> \org` built as `cint ∘ leg ∘ dyn`,
  to be parameterized into `\Phi^{symp}` and `\Phi^{grad}`. The paper instead
  factors dynamics as a **polynomial interpretation** `Φ'_interpsm` followed by an
  **integrator** `Ψ_intg`, and ships two functors **`Phiphase`** (Hamilton) and
  **`Phiconf`** (gradient), via `cor.functor` / `thm.dynamics_functor`. The
  `Φ^{symp}/Φ^{grad}` naming never shipped.
- It predates the `pvect -> rvect` ("reactive vector space") and `V -> Q` renames,
  the smooth-chapter split, and the monad-generalized potentials slot.
- It references files that no longer exist (`RIEMANN_GRADIENT_PROPOSAL.md`,
  `VOCAB.md` at the repo root) and labels that have moved (`thm.functor`,
  `lem.para_rho`, `prop.pnla_polynomial`, `potlens`, ...).

For the current design, see `misc/VOCAB.md` and the `dap` package. The original
plan text is preserved in git history (this file before 2026-06-08).
