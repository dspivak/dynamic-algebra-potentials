# Dynamic algebra of potentials

LaTeX source and supporting material for the paper *Dynamic algebra of potentials*.

## The paper

- `dynamic-algebra-potentials.tex` — the manuscript (`.pdf` is the rendered output)
- `Library20260419.bib` — bibliography
- `NOTATION.md` — canonical notation table

Build with `pdflatex` + `biber`:

```
pdflatex dynamic-algebra-potentials
biber    dynamic-algebra-potentials
pdflatex dynamic-algebra-potentials
pdflatex dynamic-algebra-potentials
```

## Executable companion

- `dap` — launcher: `./dap` builds and runs an arrangement interactively; `./dap demo` runs the worked examples
- `dap-core/` — the executable companion itself (git submodule, `github.com/dspivak/dap`)

## Other directories

- `sensemaking/` — emergent-language experiments built on the executable companion; includes `sensemaking/attention-suboperad/`, the standalone companion note (attention as a smooth arrangement and the predictive-coding suboperad of `Arr_Sm`) that the experiments are faithful to
- `notes/` — working notes and proposals (e.g. the Riccati section proposal, the gyroscope build/audit record)
- `refs/` — reference PDFs

## For AI agents

- `AGENTS.md` — working conventions for this repository
