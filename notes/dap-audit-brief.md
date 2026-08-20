# Auditor brief — `dap-core`

`dap-core/` implements `CDLM.tex`. The claim under audit is **faithfulness**: every
dynamical quantity factors through `Phiconf`/`Phiphase`, and nothing is computed by
hand around the functor. So: does each module compute its cited paper equation —
`rvect.py`↔`def.rvect`, `arrangement.py`↔`eqn.srw_morphism`,
`interpretation.py`↔`eqn.covector_triple`, `wiring.py`↔`prop.suboperads`,
`integrator.py`↔`eqn.conf_integrator` — and is any composite potential written out
rather than emerging from composition?

Not claimed: the MOSFET channel `W` in `logic.py` is a modelling choice; `PC^(K)`
functoriality is open; `logic.py`, `gyroscope*.py`, `pinn.py`, `system_id.py` are
extensions beyond the paper.

One trap: `unilateral` (`def.arrangement_terminology`) is an output-side condition;
`logic.py`'s kernel condition is input-side. Different notions.

Report findings only. `pytest dap/tests` → 95 passed, 1 skipped.
