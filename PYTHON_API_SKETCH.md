# Python API Sketch for `potlens`

A design doc for a small Python package that implements the dynamics functor $\Phi\colon\mathbf{PotLens}\to\mathbf{Org}$ from `dynamic-algebra-potentials.tex`. The goal of v1 is the smallest API that captures the math: instantiate $\mathbf{PotLens}$-morphisms, wire them together with finset-level lenses, apply $\Phi$, and step the resulting Moore coalgebra. Manifolds are restricted to $\mathbb{R}^d$.

## 1. Choice of autodiff backend: JAX

We use **JAX**. Three reasons:

1. The math is functional: every map in `eqn.para_potential_lens_maps` is a *pure* function of `(v, m_out, n_in)`. JAX's `jax.vjp` directly returns the linear pullback $(T_p f)^\top$ which is exactly what `eqn.bigtheta` is asking for; no `requires_grad`, no graph state.
2. State updates `(v + sharp_V(p), p - xi_V)` are immutable rebinds, matching the paper's notation `state_update`.
3. `jax.tree_util` gives us a free, structurally-typed representation of paired vector spaces and direction tuples (`xi_V, xi_M, xi_N_in`) — the "cotangent splitting" footnote on line 2289 becomes literal Python tree-zip.

PyTorch tradeoff: more familiar, but `torch.autograd.grad` is awkward for VJPs of multi-output functions and the stateful tape obscures the lens structure. We could keep the API backend-agnostic (a thin `_ad` shim with `vjp` and `grad`), which we do — but ship the JAX implementation first.

For a category-theorist reader: think of `jax.vjp(f, x)` as returning the pair `(f(x), (Tf|_x)^T)` where the second component is a function from cotangents-at-`f(x)` to cotangents-at-`x`. That's the only JAX feature we use.

## 2. Core types

Everything is `Array = jax.Array`, with shapes documented but not statically checked. `Pytree` is any JAX-registered tree of arrays (supports product spaces $V\times \outp{M}\times \inpt{N}$ for free).

```python
from typing import Callable, NamedTuple, Protocol
from jax import Array

# A paired vector space: an Array shape spec + the sharp.
class PVect(NamedTuple):
    shape: tuple[int, ...]                    # e.g. (K,) for V = R^K
    sharp: Callable[[Array], Array]           # V* -> V; identity-typed since R^d ~ (R^d)*

# A potlens object: a pair of shapes (R^d_in, R^d_out). v1 supports only R^d.
class LensOb(NamedTuple):
    in_shape:  tuple[int, ...]                # M_in
    out_shape: tuple[int, ...]                # M_out

# A potlens morphism (V, sharp_V, out_f, in_f, U): V . LensOb_M -> LensOb_N
class PotLensMap(NamedTuple):
    V:      PVect
    src:    LensOb                            # M
    tgt:    LensOb                            # N
    out_f:  Callable[[Array, Array], Array]            # (v, m_out)        -> n_out
    in_f:   Callable[[Array, Array, Array], Array]     # (v, m_out, n_in)  -> m_in
    U:      Callable[[Array, Array, Array], Array]     # (v, m_out, n_in)  -> R, scalar
```

Field names match the paper: `out_f` is $\outp f$, `in_f` is $\inpt f$. A user reading §`subsec.dynamics_functor` line by line should see one Python field per math symbol. No subclasses, no factories, no builders — a `NamedTuple` is the API.

A **covector field** $\omega_M\in\Omega(\inpt M)$ is represented as a closure `omega: Array -> Array` mapping a point $\inpt m$ to a covector at $\inpt m$; identifying $T^*_{\inpt m}\mathbb{R}^d\cong\mathbb{R}^d$ via `eqn.tangent_vec`, this is just a function `R^d -> R^d`. (See open question Q1 for non-trivial $\inpt M$.)

## 3. The dynamics functor $\Phi$

```python
class Stepper(Protocol):
    def initial(self) -> Array: ...                       # an initial state x = (v, p)
    def __call__(self, x: Array, m_out: Array, omega_M: Callable) \
        -> tuple[Array, Callable, Callable[[Array, Array], tuple[Array, Array, Array]]]:
        """Returns (n_out, omega_N, response).
           response(xi_N, n_in) -> (xi_M, m_in, x_next)."""
```

That is, `Phi(f)` returns a function with the **two-stage** Moore signature

```python
def Phi(f: PotLensMap) -> Stepper:
    def step(x, m_out, omega_M):
        v, p = _split_TstarV(x, f.V)
        n_out = f.out_f(v, m_out)
        # omega_N from eqn.omegaprime
        def omega_N(n_in):
            in_f_partial = lambda nn: f.in_f(v, m_out, nn)
            _, vjp_in = jax.vjp(in_f_partial, n_in)
            U_partial  = lambda nn: f.U(v, m_out, nn)
            return vjp_in(omega_M(in_f_partial(n_in)))[0] + jax.grad(U_partial)(n_in)
        def response(xi_N, n_in):
            m_in = f.in_f(v, m_out, n_in)
            # eqn.bigtheta: a single VJP of (out_f, in_f, U) at (v, m_out, n_in)
            #   gives (xi_V, xi_M, xi_N_in) componentwise via cotangent splitting.
            xi_V, xi_M, _ = _vjp_potential(f, v, m_out, n_in, xi_N, omega_M(m_in))
            x_next = _state_update(v, p, xi_V, f.V.sharp)        # eqn.state_update
            return xi_M, m_in, x_next
        return n_out, omega_N, response
    return step
```

**Why this signature, not a flatter one.** The paper's `eqn.state_update` is genuinely two-stage: the readout $(\outp n,\omega_N)$ depends only on the input *position* $(\outp m,\omega_M)$, and the input *direction* $(\xi_N,\inpt n)$ is consumed only to produce the output direction and the next state. Collapsing that into a single `step((x, m_out, omega_M, xi_N, n_in))` would (a) hide the position/direction asymmetry, (b) force the user to evaluate $\omega_N$ at exactly one $\inpt n$ per tick, killing the "covector field as function" semantics, and (c) destroy parallel reuse: a wiring lens consuming `omega_N` will evaluate it at *several* points (see §6, second-pass wave example, where particle $i+1$'s $\omega$ is evaluated at $v_i$). The two-stage signature mirrors `eqn.org_wiring_concise` exactly.

`_state_update(v, p, xi_V, sharp_V)` returns `(v + sharp_V(p), p - xi_V)`, i.e. `eqn.state_update` with the $\sharp_X$ on $T^*V$ inlined (the `eqn.sharp_X` swap-and-negate is absorbed into the addition `(v', -xi') = sharp_X(xi', p')`, so the user never sees it).

## 4. Wiring composition

A wiring is a $\mathbf{PotLens}$-morphism with `V = PVect((), lambda _: 0.)` and `U = 0`. The natural way to *build* one is from a finset-level lens via $\mathbb{R}^-$:

```python
class FinsetLens(NamedTuple):
    n_in: int
    n_out_each: tuple[int, ...]      # arities of the K inner boxes' out-ports
    # out_f: which inner output feeds the outer output (length n_out_outer)
    out_f: tuple[int, ...]
    # in_f: each inner input is fed by either the outer input or some inner output
    in_f: tuple[int, ...]            # values in {0,...,n_in-1} ∪ {n_in,...,n_in+sum_inner_out-1}

def wiring_from_finset(phi: FinsetLens, src: tuple[LensOb, ...], tgt: LensOb) -> PotLensMap:
    """Apply R^- to a finset lens (lemma.lens_rr) and trivial-parameterize."""
    ...
```

Composition uses the symmetric-monoidal-category structure of $\mathbf{PotLens}$ from `subsec.dynamics_functor`:

```python
def compose(wiring: PotLensMap, inners: tuple[PotLensMap, ...]) -> PotLensMap:
    """K-ary composition wiring(inner_1, ..., inner_K). Returns a 0-ary morphism
    if `wiring` has a 0-ary outer. Implements the Para composition: parameters
    direct-sum, and (out_f, in_f, U) get glued via the productor of the R-monad
    (eqn.monoid_productor) — i.e. U_total = U_wiring + sum_i U_inner_i pulled back."""
```

Two functions, full stop: `wiring_from_finset` (the $\Lens{\mathbb{R}^-}$ functor on a chosen finset lens) and `compose` (the categorical composite in $\mathbf{PotLens}$). Crucially, `compose` is implemented at the $\mathbf{PotLens}$ level, *not* by composing steppers — that's the whole point of the first-pass derivation in §`sec.spring_first_pass`.

We additionally provide `Phi_compose_in_org(wiring_stepper, *inner_steppers)` that performs composition at the $\mathbf{Org}$ level (second pass, §`sec.spring_second_pass`); this is mainly a regression test for `Phi(compose(...)) == Phi_compose_in_org(Phi(wiring), *map(Phi, inners))` on random states.

## 5. Worked example: $K$-particle wave equation

Compare directly to lines 2384–2456 of the paper.

```python
import jax.numpy as jnp

# --- The particle: V = R, sharp = p/m, out_f = id, U = (kappa/2)(x-y)^2.
def particle(m: float, kappa: float) -> PotLensMap:
    return PotLensMap(
        V    = PVect(shape=(), sharp=lambda p: p / m),
        src  = LensOb((), ()),                              # 0-ary: R^0 -> R^0
        tgt  = LensOb((), ()),                              # the box R/R
        out_f = lambda v, _m_out: v,                        # f^out(x) = x
        in_f  = lambda v, _m_out, _n_in: jnp.zeros(()),     # vacuous (M_in is R^0)
        U     = lambda v, _m_out, n_in: 0.5 * kappa * (v - n_in)**2,
    )

# --- The wiring: K particles in series. Outer out is the rightmost particle;
#     inner i's "previous neighbor" comes from particle (i-1)'s output, with i=1
#     receiving the outer input v_0.
def chain_wiring(K: int) -> PotLensMap:
    phi = FinsetLens(
        n_in       = 1,
        n_out_each = (1,) * K,
        out_f      = (K - 1,),                              # outer out = inner K's out
        in_f       = (0,) + tuple(range(1, K))              # inner i's in = inner (i-1)'s out, except i=0 reads outer in
                     ,
    )
    return wiring_from_finset(phi, src=(LensOb((), ()),) * K, tgt=LensOb((), ()))

# --- Compose in PotLens, apply Phi.
chain = compose(chain_wiring(K=7), tuple(particle(m=1.0, kappa=1.0) for _ in range(7)))
step  = Phi(chain)                  # a Stepper

# --- Run.
x = jnp.zeros((7,)), jnp.array([1.0, 0, 0, 0, 0, 0, 0])    # one unit of momentum on particle 1
v_left   = 0.0                                              # left wall, eqn.wave_bc
omega_M  = lambda n_in: jnp.zeros_like(n_in)                # external omega is zero
for t in range(1000):
    v_K_out, omega_N, respond = step(x, m_out=jnp.zeros(()), omega_M=omega_M)
    xi_N = 1.0 * (v_K_out - 8 * 1.0)                        # right wall, kappa*(v_K - L*(K+1))
    _, _, x = respond(xi_N, n_in=jnp.array(v_left))
```

The 7-particle chain in 16 lines. The `particle`/`chain_wiring`/`compose`/`Phi` four-step structure is exactly the four-step structure of §`sec.spring_first_pass`.

## 6. Follow-on experiments (sketches)

**2D lattice wave equation (`sec.nd_wave`).** Replace the box `LensOb((), ())` with `LensOb((d,), (d,))` for $d=2$, replace the chain finset-lens with the `FinsetLens` of a square-grid neighbor relation (each interior box has 4 neighbors), and use `U(v, m_out, n_in) = 0.5*kappa*jnp.sum((v - n_in)**2)`. Observe a Gaussian bump propagating circularly at speed $\sqrt{\kappa/m}$. Tests: rotational symmetry of the dispersion relation; energy conservation up to symplectic-Euler drift.

**$N$-body gravity (`sec.nbody`).** Same particle, $d=3$, but now the wiring is the *complete-graph* `FinsetLens`: each box outputs its position and receives positions of all $N-1$ others. Replace the harmonic potential by `U = -G * jnp.sum(m_i*m_j / jnp.linalg.norm(v - n_in_j))` over the received-neighbor list. The same `compose` + `Phi` reproduces symplectic-Euler $N$-body. Tests: Kepler orbit closure for $N=2$; Sun–Earth–Moon stability over $10^4$ steps.

**Heavy-ball on a quadratic loss (`sec.heavy_ball`).** A *single* 0-ary morphism with `V = R^k`, `sharp = lambda p: p/m`, vacuous `M_in = M_out = R^0`, and `U(v, _, _) = 0.5 * v @ A @ v - b @ v`. No wiring. The stepper is autonomous. Sweep $m$ from small (gradient descent) to large (oscillatory) and plot convergence rate vs eigenvalue spread of $A$ — a direct demonstration that the choice of $\sharp_V$ is the optimizer.

## 7. Open design questions (resolve before coding)

1. **Covector fields when $\inpt M\neq\mathbb{R}^d$.** v1 fixes $\inpt M=\mathbb{R}^d$ and represents $\omega\in\Omega(\inpt M)$ as a closure. If we ever want $\inpt M$ a manifold (e.g. $S^1$, configuration of a rigid body), `omega: m -> T*_m M` cannot be just `R^d -> R^d` and we'd need a chart-aware tangent-bundle representation. Decision: punt to v2; document the restriction.

2. **Should `omega_N` be returned eagerly evaluated at a grid, or lazily as a closure?** Lazy is mathematically right (matches `eqn.omegaprime`) and matches the wiring's evaluation pattern (§`sec.spring_second_pass` evaluates $\omega_{i+1}$ at $v_i$). But naive closures aren't `jit`-friendly because they capture `v, m_out`. Resolution candidate: provide both, with `omega_N` a closure by default and a helper `eager_omega_N(grid)` for benchmarking. Needs a JAX-friendly idiom (likely `partial` + `jit` with `static_argnums`).

3. **How to represent the finset-level wiring lens.** The `FinsetLens` flat-tuple format above is concrete but low-level. Two alternatives: (a) a thin DSL (`SeriesChain(K)`, `Grid2D(W, H)`, `CompleteGraph(N)`); (b) PEP-style explicit construction from a wiring-diagram graph object. Recommendation: ship (a) and the flat tuple; defer the graph DSL.

4. **Where does $\sharp_X$ live?** Inside `_state_update` (current sketch, hidden) or surfaced as a method on `PVect`? Hidden is simpler and matches the paper's footnote treating it as a derived object. Surfacing it would let advanced users plug in non-canonical symplectic structures, which the paper does not need.

5. **State representation: tuple `(v, p)` vs. flat `T^*V` array?** The paper writes $x=(v,p)\in V\oplus V^*$. A flat representation costs nothing because $V=\mathbb{R}^k$, but `(v, p)` matches the paper. Recommendation: use a `NamedTuple TStarV(v, p)` and make `_split_TstarV` trivial.

6. **`compose` correctness witness.** We claimed `Phi(compose(w, fs)) == Phi_compose_in_org(Phi(w), *map(Phi, fs))`. This is `theorem.functor` + functoriality of $\Phi$. Should we ship a property-based test (Hypothesis) on random small cases, or only test the wave-equation instance? Recommendation: both, but the random one is what catches sign-convention bugs.

7. **Naming.** `out_f`/`in_f` mirror $\outp f$/$\inpt f$ but read awkwardly in Python. Alternatives: `f_out`/`f_in`, `forward`/`backward`. Author preference?

8. **Manifolds beyond $\mathbb{R}^d$ in v1.** No. Document clearly in the README.
