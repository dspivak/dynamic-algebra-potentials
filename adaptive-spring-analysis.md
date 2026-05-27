# Adaptive spring dynamics: working out line 2855

## Setup

The **adaptive spring** is `wire^adapt_K : □^⊗K → □`, an SRW morphism with:

- **Parameter space**: `(V', ♯_κ) = (ℝ^{K-1}, ♯_κ)` — one stiffness `κ_j` per internal bond
- **Output/input maps**: same as `wire_K` (output = `x_K`, input routing = shift)
- **Potential**: `U'(κ, x, x₀) = Σ_{j=1}^{K-1} (κ_j/2)(x_{j+1} - x_j)²`

Each particle `Part` has parameter `(ℝ, p ↦ p/m)`, output `x`, potential
`U_Part(x, y) = (κ_fixed/2)(x - y)²`.

### The composite `wire^adapt_K(Part,...,Part)`

**Parameter space**: `V = ℝ^{K-1} ⊕ ℝ^K` with coordinates `(κ₁,...,κ_{K-1}, x₁,...,x_K)`

**Sharp**: `♯ = ♯_κ ⊕ (p ↦ p/m)` (the κ-sector sharp `♯_κ` is left open)

**Total potential** (wiring potential + particle potentials, with `y_i ↦ x_{i-1}` substituted):

```
U(κ, x, x₀) = Σ_{j=1}^{K-1} (κ_j/2)(x_{j+1} - x_j)²  +  Σ_{i=1}^K (κ_fixed/2)(x_i - x_{i-1})²
```

Combining by bond: define the effective stiffness on bond `(j, j+1)`:

```
K₀ = κ_fixed                     (boundary bond, left)
K_j = κ_fixed + κ_j   (j=1,...,K-1)   (internal bonds, adaptive)
K_K = κ_fixed                     (boundary bond, right—from ξ_N)
```

Then `U = Σ_{j=0}^{K-1} (K_j/2)(x_{j+1} - x_j)²`.

---

## Gradients

**Stiffness gradient** (the "learning signal" from the paper):

```
∂U/∂κ_j = (1/2)(x_{j+1} - x_j)²           for j = 1,...,K-1
```

Always non-negative. This is the strain energy on bond `j`.

**Position gradient** (elastic restoring force, with sign):

```
∂U/∂x_i = K_{i-1}(x_i - x_{i-1}) - K_i(x_{i+1} - x_i)     for 1 ≤ i ≤ K
```

where `K₀ = κ_fixed`, `K_j = κ_fixed + κ_j` for internal bonds,
and the boundary bond contributes via `ξ_N` at `i = K`.

---

## Dynamics under Φ_phase

State: `s = (κ, x, π, p) ∈ T*(ℝ^{K-1} ⊕ ℝ^K)`

From equation (5.2) [eq. (eqn.state_update)], the update is
`(x, ξ) → (x + ♯(ξ), ξ - ξ_V)`, so:

```
κ_j' = κ_j + ♯_κ(π_j)
x_i' = x_i + p_i/m
π_j' = π_j - (1/2)(x_{j+1} - x_j)²
p_i' = p_i - [K_{i-1}(x_i - x_{i-1}) - K_i(x_{i+1} - x_i)]   (interior)
p_K' = p_K - K_{K-1}(x_K - x_{K-1}) - ξ_N
```

With pinned boundaries (`x₀ = 0`, `ξ_N = κ_fixed · x_K`), the position
update is the discrete wave equation with **variable spring constants** `K_j`:

```
p_i' = p_i + K_i(x_{i+1} - x_i) - K_{i-1}(x_i - x_{i-1})
```

The stiffness-momentum pair `(κ_j, π_j)` evolves as:

```
κ_j' = κ_j + ♯_κ(π_j)
π_j' = π_j - (1/2)(x_{j+1} - x_j)²
```

**Key observation**: The "force" on `π_j` is `-(1/2)(Δx_j)² ≤ 0`, always
non-positive. So `π_j` is always pushed downward.

---

## The pathology with constant sharp on κ

Take `♯_κ(π) = π/M_κ` (constant, like an inverse mass for stiffness). Then:

```
κ_j' = κ_j + π_j/M_κ
π_j' = π_j - (1/2)(Δx_j)²
```

This is a particle in a potential that is **linear** in `κ_j`. Since `∂U/∂κ_j
= (1/2)(Δx)²` is always non-negative, the force on `π` is always ≤ 0, so:

- `π_j` drifts steadily negative
- `κ_j` accelerates downward
- Eventually `κ_j` goes through 0 (springs go slack), then negative (repulsive!)
- The system blows up

In continuous time, the Hamiltonian

```
H = Σ π_j²/(2M_κ) + Σ p_i²/(2m) + U(κ, x)
```

is conserved, but the potential `U` is **unbounded below** in the `κ`-direction
(when `Δx ≠ 0`): taking `κ_j → -∞` releases infinite potential energy. So the
system converts potential energy to kinetic energy without bound.

**Diagnosis**: The potential `(κ_j/2)(Δx)²` is linear in `κ_j`, so it acts
like gravity—a constant force pulling stiffness downward. There's no restoring
force to keep `κ` bounded.

---

## Fix 1: Variable sharp (multiplicative dynamics)

### Specification

Take `♯_κ` to be **position-dependent**: `♯_{κ_j}(π_j) = κ_j · π_j / M_κ`.

This is a valid reactive vector space structure on `ℝ^{K-1}` (the sharp map
is smooth and linear in the covector `π_j`). It is **not** constant: the
"effective mass" of `κ_j` is `M_κ/κ_j`, so stiffer springs respond more
quickly.

### Dynamics

```
κ_j' = κ_j + κ_j · π_j / M_κ = κ_j(1 + π_j/M_κ)
π_j' = π_j - (1/2)(x_{j+1} - x_j)²
```

**The stiffness updates multiplicatively**: each step scales `κ_j` by
`(1 + π_j/M_κ)`. For small `|π_j/M_κ|`, this is `κ_j · exp(π_j/M_κ)`.

**Consequences**:
- If `κ_j` starts positive and `|π_j| < M_κ`, then `κ_j` stays positive.
- The dynamics lives in log-space: `log(κ_j)' = log(κ_j) + π_j/M_κ` (approx).
- So `d²/dt²(log κ_j) ≈ -(1/2M_κ)(Δx_j)²`, i.e., the log-stiffness
  decelerates at a rate set by the strain.
- The stiffness decays toward 0 but never crosses 0 (in continuous time, and
  in discrete time for small enough steps).

**Physical interpretation**: The springs gradually relax under strain. Stretched
bonds get exponentially weaker. This models **stress relaxation** in
viscoelastic materials: strain energy is dissipated by softening the coupling.

**Tradeoff**: This dynamics is NOT Hamiltonian (the sharp is not constant, so
Remark 5.16 does not apply). There is no conserved energy. The system is
dissipative: stiffness decays to 0 as long as there is any strain.

### Φ_conf variant (even simpler)

Under `Φ_conf` with variable sharp `♯_{κ_j}(ξ) = -η_κ · κ_j · ξ`:

```
κ_j(t+1) = κ_j(t) · (1 - (η_κ/2)(x_{j+1}(t) - x_j(t))²)
```

One-line update: **multiplicative gradient descent on stiffness**. Each spring
constant is scaled down by a factor proportional to its strain energy. This is
exactly natural gradient descent / mirror descent in log-coordinates.

For the position sector, use `♯_x = -η_x · id` (gradient descent):

```
x_i(t+1) = x_i(t) + η_x[K_i(x_{i+1}-x_i) - K_{i-1}(x_i-x_{i-1})]
```

This is a **discrete heat equation with variable diffusion coefficient**. The
positions diffuse toward equilibrium, and the spring constants decay wherever
there's strain.

Combined: a coupled diffusion-softening system. Physical model: **plastic
deformation**. The material relaxes, deforms, and softens simultaneously. As
the strain goes to 0, the softening stops, and the system reaches a new
equilibrium with reduced stiffness.

---

## Fix 2: Quadratic potential (oscillatory stiffness)

### Specification

Change the wiring potential from `(κ_j/2)(Δx)²` to `(κ_j²/2)(Δx)²`:

```
U'(κ, x, x₀) = Σ_{j=1}^{K-1} (κ_j²/2)(x_{j+1} - x_j)²
```

Keep the sharp constant: `♯_κ(π) = π/M_κ`.

The effective spring constant on bond `j` is now `κ_fixed + κ_j²` (always ≥ κ_fixed).

### Gradients

```
∂U'/∂κ_j = κ_j(x_{j+1} - x_j)²
```

Note: this is proportional to `κ_j` itself, not just the strain. So the "force"
changes sign with `κ_j`.

### Dynamics under Φ_phase

```
κ_j' = κ_j + π_j/M_κ
π_j' = π_j - κ_j(x_{j+1} - x_j)²
```

For fixed strain `Δx_j`, this is a **harmonic oscillator in κ_j**:

```
d²κ_j/dt² = -(Δx_j)²/M_κ · κ_j
```

with angular frequency `ω_j = |Δx_j|/√M_κ`.

**The stiffness oscillates harmonically**, with frequency set by the strain!

**Consequences**:
- Stretched bonds oscillate faster (higher frequency)
- Unstretched bonds don't oscillate (frozen at `κ_j = const`)
- The effective coupling `κ_j²` pulsates between 0 and its maximum
- The system IS Hamiltonian (constant sharp, symmetric): energy is conserved

**Physical interpretation**: Each bond has an internal oscillatory degree of
freedom—a **phonon** living on the bond itself. The bond oscillation frequency
is set by the strain, creating a coupling between acoustic phonons (the `x`
waves) and these "bond phonons" (the `κ` oscillations). This models
**phonon-phonon interaction** in a lattice.

In this picture:
- The `(x, p)` sector describes acoustic waves (particle vibrations)
- The `(κ, π)` sector describes optical-branch phonons (bond vibrations)
- The coupling `κ_j²(Δx_j)²` mixes the two branches

**The Hamiltonian**:

```
H = Σ_j π_j²/(2M_κ) + Σ_i p_i²/(2m) + Σ_j (κ_j²/2)(Δx_j)² + Σ_i (κ_fixed/2)(Δx_i)²
```

This is bounded below (by 0), so the dynamics is stable. Energy conservation
gives: when acoustic phonons excite a bond (large `|Δx_j|`), the bond phonon
speeds up; when the bond phonon has large `|κ_j|`, the effective spring constant
`κ_j²` is large, which scatters the acoustic phonon. **The two sectors exchange
energy through a quartic interaction `κ_j²(Δx_j)²`.**

---

## Comparison

| Feature | As written (κ, const ♯) | Variable ♯ (κ·π) | κ² potential |
|---------|-------------------------|-------------------|-------------|
| Change from paper | none | one-line ♯ | one-line U |
| Dynamics | drift to -∞ | multiplicative decay to 0 | harmonic oscillation |
| Stiffness sign | crosses 0, goes negative | stays positive | effective κ² ≥ 0 |
| Energy conservation | yes but unbounded | no | yes, bounded |
| Physical model | — (pathological) | stress relaxation / plasticity | phonon-phonon interaction |
| Functor | Φ_phase | Φ_phase or Φ_conf | Φ_phase |

---

## Assessment: what's most interesting?

### Variable sharp (Fix 1)

**Pitch**: "A spring material that softens multiplicatively under strain."

- **Why you'd want it**: Models materials that weaken under stress (fatigue,
  plastic deformation, stress relaxation). Also connects to natural gradient
  descent / mirror descent in optimization.
- **What it does**: Stretched springs get exponentially weaker; unstretched
  springs stay frozen. The chain gradually relaxes to uniform displacement.
- **Why it works**: The variable sharp `♯_κ = κ · id` makes stiffness update
  in log-space. Since `log(κ)` sees a one-signed force, `κ` decays
  monotonically toward 0 but never crosses.
- **Specification**: One line: change the sharp on `ℝ^{K-1}` from constant
  to `♯_{κ_j}(π) = κ_j π / M_κ`.

Uses the paper's key innovation (variable sharp) in a natural way. Showcases
the difference between constant and variable reactive structure.

### Quadratic potential (Fix 2)

**Pitch**: "A spring material with oscillating stiffness—phonons on the bonds."

- **Why you'd want it**: Models lattice dynamics with internal bond degrees of
  freedom. Creates acoustic/optical phonon branch coupling. Rich emergent
  behavior from a minimal specification.
- **What it does**: Each bond has a stiffness that oscillates at a frequency
  set by the local strain. Stretched bonds vibrate faster. Energy flows between
  particle motion and bond oscillation.
- **Why it works**: The potential `κ²(Δx)²/2` is quadratic in both `κ` and
  `Δx`, giving harmonic restoring forces in both sectors. The quartic coupling
  term mixes them.
- **Specification**: One line: change `κ_j` to `κ_j²` in the potential.

This is a more standard physics move (choose a different Lagrangian) but
produces richer, stable, energy-conserving dynamics. It doesn't showcase the
variable-sharp feature.

### Recommendation

**For showcasing the formalism**: Fix 1 (variable sharp). It demonstrates that
the choice of reactive structure—the same data that encodes learning rates in
gradient descent and inverse mass in Hamiltonian dynamics—can qualitatively
change the material behavior. "Constant sharp gives plastic deformation that
runs away; variable sharp gives controlled softening." This is a one-sentence
argument for why the sharp map matters beyond being a mathematical convenience.

**For physics interest**: Fix 2 (κ² potential). It gives the richest dynamics
(energy-conserving, two coupled oscillatory sectors, phonon-phonon interaction)
from the simplest change. But it's a standard physics move (change the
Lagrangian) that doesn't exercise the paper's novel machinery.

**Combined possibility**: Use the κ² potential AND variable sharp. This gives
oscillatory dynamics in log-space:

```
log(κ_j)' ≈ log(κ_j) + π_j/M_κ
π_j' = π_j - κ_j(Δx_j)²
```

But this might be over-specifying; the individual fixes each have a clean story.

---

## Appendix: two-particle example (K = 2)

For concreteness, take `K = 2` (two particles, one adaptive bond). Pin
`x₀ = 0`, `x₃ = 0`.

State: `(κ, x₁, x₂, π, p₁, p₂)`

**Constant sharp (as written):**
```
κ' = κ + π/M_κ
x₁' = x₁ + p₁/m
x₂' = x₂ + p₂/m
π' = π - (1/2)(x₂ - x₁)²
p₁' = p₁ + (κ_fixed + κ)(x₂ - x₁) - κ_fixed · x₁
p₂' = p₂ - (κ_fixed + κ)(x₂ - x₁) - κ_fixed · x₂
```

Example trajectory (m = M_κ = 1, κ_fixed = 1, init: x = (1, -1), p = 0, κ = 1, π = 0):

```
t=0: κ=1, x=(1,-1), π=0, p=(0,0)
     Δx = -2, strain² = 4
     Force: p₁' = 2(−2) − 1 = −5,  p₂' = −2(−2) − (−1) = 5
     π' = −2
t=1: κ=1, x=(1,-1), π=−2, p=(−5,5)
     [κ hasn't changed yet because π was 0]
t=2: κ=−1, x=(−4,4), π=−2−(1/2)(8)²=−34, p=...
     [κ already negative! Springs now repulsive on bond 1]
```

The stiffness crosses zero within 2 steps. Pathological.

**Variable sharp** `♯_κ(π) = κπ/M_κ`:
```
t=0: κ=1, π=0 → κ'=1·(1+0)=1
t=1: κ=1, π=−2 → κ'=1·(1−2)=−1  [still crosses 0 for large π!]
```

Hmm—the variable sharp only guarantees positivity for **small** `|π/M_κ|`.
With `M_κ = 1` and the force pushing `π` to `−2`, we cross immediately.
Taking `M_κ = 10` (heavy stiffness): `κ' = 1·(1 − 2/10) = 0.8`. Better!
The stiffness decay rate is controlled by `M_κ`.

**κ² potential** (with constant sharp):
```
κ' = κ + π/M_κ
π' = π - κ(x₂ - x₁)²
```
At `t=0`: `π' = 0 - 1·4 = -4`, `κ' = 1 + 0 = 1`
At `t=1`: `π' = -4 - 1·(Δx')²`, `κ' = 1 + (-4)/M_κ`

For `M_κ = 10`: `κ' = 1 - 0.4 = 0.6`, still positive. And the restoring
force `−κ(Δx)²` changes sign when `κ` crosses 0, pushing it back positive.
The effective stiffness `κ²` is always non-negative regardless.

---

## Bottom line

The adaptive spring **as written** (constant sharp, linear potential) has
unstable stiffness dynamics: `κ` drifts to `−∞` because the potential is
linear in `κ`.

**Best fix for showcasing the paper**: variable sharp `♯_κ = κ · id / M_κ`.

**Best fix for physics**: quadratic potential `κ²(Δx)²/2`.

**Best fix for "cool, easy to specify, easy to explain"**: I'd say the
**quadratic potential**. Here's the elevator pitch:

> "Replace the spring constant with its square in the elastic energy. Now each
> bond has an internal degree of freedom that oscillates—like a phonon living
> on the bond. Stretched bonds oscillate faster. The system is Hamiltonian, the
> energy is conserved, and you get coupled acoustic-optical phonon dynamics
> from a one-character change."

But the **variable sharp** is the deeper story for the paper, because it
demonstrates why the sharp map is more than mathematical scaffolding.
