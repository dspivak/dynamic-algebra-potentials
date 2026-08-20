# Agent Instructions

This repository contains a mathematics paper in LaTeX. Treat the user as the author.

## Working Style

- Preserve the author's spelling, notation, tone, and local terminology.
- Do not normalize prose, punctuation, or regional spelling unless explicitly asked.
- When the author's intent is obvious, make the next sensible editorial fix rather than the narrowest literal edit.
- When a local change creates an obvious nearby inconsistency, fix that too.
- Ask for clarification only when the ambiguity is real or the choice is mathematically risky.

## Edit protocol: reversible `%` markers

Every edit to a `.tex` file in this repo arrives marked, so the original wording is
exactly recoverable from the file itself and the author can accept or strip it by hand.

**The whole protocol in one example.** To change `decorated cospans` to
`cospans and corelations` inside a 900-character paragraph line, put a line break
immediately *before* and immediately *after* those two words — nothing else moves:

```
...long unchanged text, ending: Coya categorified bond graphs using
%decorated cospans
cospans and corelations %
and assigned two functorial semantics..., long unchanged text continuing...
```

1. **The unit of edit is the changed fragment** — not the line, not the sentence.
   Break the long source line exactly at the fragment's boundaries first, so the
   fragment sits alone. That step is pure reflow, no markers, output unchanged.
   NEVER SKIP IT. It is not paragraph reflow: do not rewrap prose to ~90 chars,
   do not break at sentence boundaries for tidiness; unchanged text keeps its
   shape (long lines stay long).
2. Every inserted line ends with ` %` — space before the `%`, so the compiled
   output is identical to a plain newline.
3. Never delete a line outright; prefix it with `%`.
4. A line carries a marker **only if its wording actually changed**. N changed
   fragments in a paragraph ⇒ N `%`-pairs (commented original, then replacement
   ending ` %`); every other line is the author's text, verbatim and bare. A
   replacement line containing any unchanged words means step 1 was done as
   reflow instead of fragment isolation — not allowed, however tidy it looks.
5. A marker must land at a genuine line end / line start, never mid-original-line.
   After every edit, check the tail of the edited line: a trailing ` %` dropped
   mid-line comments out — silently erases — the live text after it.
6. Extend the fragment to the nearest word boundary rather than stranding
   punctuation (isolate `state that updates until X.`, replace with `state. %`;
   never leave `.` alone on a line, which compiles as `state .`).

Seeing earlier chunks already flattened (markers stripped, text inline) does NOT
mean the convention is off — that is the author having accepted them.

**Afterward, always quote the resulting source block back with line numbers**, not
a summary of what changed: he approves how the edit reads in place. Then stop.
Downstream consequences, new gaps, and things spotted for later chunks wait until
after approval — raising them in the same message buries what he is reviewing.
Once a chunk is approved, commit it: one commit per chunk, never batched, never
before approval.

## Math Editing

- Check statements against the local definitions and surrounding arguments before replying.
- Distinguish carefully between different monoidal structures and categorical structures in the paper.
- Do not invent references, labels, or claims to smooth over a gap; either add the real thing or remove the unsupported mention.
- Prefer concise, mathematically precise prose over chatty explanation.

## LaTeX

- Preserve the author's existing macro/style choices.
- Keep edits minimal and local unless a broader rewrite is requested.
- When changing a displayed formula or lemma statement, check the proof for any required parallel updates.
- To compile, use TeX Live from `/Library/TeX/texbin`:
  `env PATH=/Library/TeX/texbin:$PATH /Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode CDLM.tex`
  Bare `latexmk` may fail because `/Library/TeX/texbin` is not always on `PATH`.
  `notes/divisible_strings.tex` compiles with `pdflatex` alone (thebibliography, no biber).

## Categorical style

- Prefer categorical statements.  When a result is secretly a naturality,
  functoriality, (co)limit, or universal-property statement, say it that
  way: a compatible family of commuting squares is a natural
  transformation; a dense compatible family with a unique bounded
  extension is a colimit; closure under composition plus an induction is
  functoriality; a canonical-up-to-unique-iso object is a universal
  property.
- Conversely, delete content the category theory already implies: once a
  statement is phrased categorically, do not restate its consequences
  (uniqueness, compatibility, associativity) as separate claims.
- Explicit formulas belong in definitions, proofs, or discussion, not in
  theorem statements; a formula-heavy proposition is usually a
  computation serving exactly one later proof, and should live there.

## Labels and environments

- Cross-reference labels use underscores, never hyphens:
  `lem.extended_recurrence`, not `lem.extended-recurrence`.
- Definitions (and examples and remarks) end with the `$\lozenge$` marker:
  the `definition` environment is the `pushQED` wrapper around
  `definitionx`, as in CDLM's preamble.
- Statements of theorems, lemmas, and definitions are self-contained:
  recall every symbol they use (with a `\cref` to its definition) rather
  than relying on running-text conventions from earlier sections.

## Term tracking

- CDLM.tex and notes/divisible_strings.tex use the `\trackTerm`/`\defineTerm`
  hyperlink machinery.  Every newly defined named operation, functor, or
  category gets a `\trackTerm` registration in the preamble and a
  `\defineTerm` at its definition site, so that every later use hyperlinks
  back.  Single Greek letters with local scope are exempt.
- Never run automated text sweeps over the `\trackTerm` preamble block: a
  sweep rewrites the registration lines themselves.
