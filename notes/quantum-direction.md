# Note: taking the framework toward quantum mechanics

**Status.** Orientation note, not a spec. Records where quantum dynamics does and
doesn't fit the `CDLM` framework, and — if someone wants to push it — exactly which
assumption to attack and what it costs. Conclusions below were reached by reading the
lens and framework chapters; line numbers drift, so navigate by `\label`.

---

## 0. The one thing to know

Single-particle wave mechanics already fits. Genuine many-body quantum mechanics does
not, and the obstruction is **not** where it first appears (the cartesian datum). It is
one copy map — the comonoid comultiplication `δ` used inside lens internalization. That
copy is no-cloning. Everything below is unpacking this.

## 1. What already fits: single-particle Schrödinger

A single particle on `K` lattice sites has Hilbert space `ℂ^K = ⊕ᵢ ℂ|xᵢ⟩` — a **direct
sum** of site amplitudes, not a tensor. So the framework's `⊕` is correct here, and
this is essentially an *instance* of the existing smooth datum `Sm`, not a new one:

- take the parameter to be `ℂ^K` viewed as a real reactive space with sharp = the
  complex structure `J` (an antisymmetric sharp; `def.rvect` permits it — symmetry and
  positivity are only added later, for descent and for symplecticity);
- the discrete Laplacian on the wiring graph is the kinetic term, the on-site term is
  the potential, and the total energy `⟨ψ|Ĥ|ψ⟩` is a quadratic form — i.e. a
  **harmonic arrangement** in the paper's exact sense (`prop.closed_conservation`);
- `J` instead of a symmetric sharp turns the second-order wave into first-order
  Schrödinger; `|ψ(x)|²` "on the screen" is a (nonlinear) readout.

Caveat: the built-in Euler/symplectic-Euler integrators are not exactly unitary. A
faithful quantum step wants a **unitary integrator** (Cayley transform / Crank–Nicolson
of `Ĥ`). The framework is built to accept new integrators (`cor.functor`,
`rmk.adam`), so this is in-scope but is a new integrator to construct and prove
monoidal — not free.

## 2. Where it breaks: many particles

`N` indistinguishable particles must be written in **second quantization**, where the
Fock space factorizes **over sites** (not over particles):

```
F  =  ⊗ᵢ Fᵢ ,        Fᵢ = span{|0⟩ᵢ, |1⟩ᵢ, |2⟩ᵢ, …}   ("how many particles at site i")
```

This is good news for the spatial reading: **box = site is exactly right**, and the
interfaces between neighboring boxes are the hopping bonds. The tight-binding /
Bose–Hubbard kinetic term `−J Σ aᵢ† aⱼ` annihilates a particle at `j` and creates one
at `i` — it *hops a particle across the interface*. **The wiring graph is the
tight-binding graph; the paper's graph Laplacian is already the right connectivity.**

What breaks is what the wire carries and how state combines:

- the hopping operator `aᵢ† aⱼ` acts on `Fᵢ ⊗ Fⱼ` and **entangles** the two sites
  (a delocalized particle `|1,0⟩ + |0,1⟩` is mode entanglement *between boxes*);
- the framework's composite state is a **product of sets** `∏ᵢ Fᵢ` (tuples / definite
  configurations), which cannot represent superpositions across sites — those live in
  the **tensor** `⊗ᵢ Fᵢ`, which is not a product of sets.

This is the LOCC no-go, read in the framework's vocabulary: per-box updates = local
operations, classical signals on wires = classical communication, parameters = local
ancillas. **LOCC cannot create entanglement from a separable state**, and the framework
is structurally a LOCC machine.

## 3. The precise obstruction (do not stop at "cartesian")

The datum (`def.rewiring_datum`) asks for a **cartesian** category of spaces `cat M`.
That looks like the wall, but it is only a convenience: by Fox's theorem
(cited near the lens definition), cartesianness freely supplies the two things the
construction actually uses —

1. output objects `c.out` carry a comonoid `(ε, δ)`;
2. forward maps `f.out` are comonoid **homomorphisms**.

None of the real theorems need cartesian. `Lens(cat C)`, the `cat A`-action, and lens
internalization `Θ` (`thm.Theta_T_alpha`) are all stated for symmetric monoidal
(closed) categories with chosen comonoids. The author already decouples the two
explicitly: **`prop.moding` — "Note that `⊗` need not be the cartesian product."**

The genuinely load-bearing use is a single copy. Lens internalization opens with

```
δ : c.out → c.out ⊗ c.out
```

which **copies the output** so it can go both forward (the readout) and backward (into
the potential / update). *That* copy is the no-cloning wall — cartesian just handed it
over for free.

Why relaxing cartesian → "monoidal-with-comonoids" does **not** rescue quantum: in
`(FdHilb, ⊗)` the comonoids are exactly orthonormal bases — "classical structures" in
the sense of Coecke–Pavlović–Vicary — and comonoid homomorphisms are basis-preserving
(classical) maps. So requiring `f.out` to be a comonoid homomorphism forces the output
side into the copyable/classical fragment (the position basis on the lattice). Same
separable sector, reached by a different door.

## 4. The actual frontier: lenses → optics

The move that could matter is not cartesian → monoidal; it is **lenses → optics**.
Optics (Tambara modules / coend presentation) need *no* comonoid structure and are
defined over any monoidal category, including `(Hilb, ⊗)` (which is compact closed,
hence monoidal closed — so the closed structure `Θ` needs is available).

Cost, stated honestly:

- `Θ` — the paper's central construction — is a *lens* theorem built on the copy `δ`.
  It must be rederived for optics, and the copy was doing real work; it is not obvious
  what survives.
- The semantic target `PC` is deterministic (no stochastic morphisms). Even with optics
  in place, measurement, the Born rule, and collapse are out of scope — only **unitary
  evolution of a closed system** is a candidate. A genuinely quantum target would
  replace `PC` (coalgebras in additive `Poly`) with a quantum analog: open systems /
  coalgebras valued in `Hilb` under `⊗_ℂ`, with wires as quantum channels rather than
  classical signal ports.

## 5. Summary table

| layer | classical (this paper) | quantum many-body |
|---|---|---|
| wiring graph (syntax) | graph Laplacian connectivity | **same** — tight-binding/hopping graph |
| box = site state | a point / configuration | local Fock space `Fᵢ` (vector space) |
| combine states | product of sets `∏ᵢ` (separable) | tensor `⊗ᵢ` (entanglement) |
| wire carries | classical readout (position/covector) | particle flux / `aᵢ† aⱼ` (quantum channel) |
| forward map `f.out` | comonoid hom (copyable) | **must drop** the comonoid requirement |
| construction | lenses + `Θ` (uses copy `δ`) | optics (no copy) — `Θ` to be rebuilt |
| target | `PC` (deterministic) | `Hilb`-valued open systems under `⊗_ℂ` |

The single-particle row collapses to the classical column (`⊗ᵢ → ⊕ᵢ`), which is why
§1 works for free and §2 does not.
