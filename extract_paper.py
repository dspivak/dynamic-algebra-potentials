#!/usr/bin/env python3
"""Extract labeled results and types from the paper.

Run once as a preprocessing pass. Outputs paper_graph.json and TYPES.md.
"""
import re
import json

TEX_PATH = "/Users/davidspivak/VersionControl/dynamic-algebra-potentials/dynamic-algebra-potentials.tex"
OUT_JSON = "/Users/davidspivak/VersionControl/dynamic-algebra-potentials/paper_graph.json"
OUT_MD = "/Users/davidspivak/VersionControl/dynamic-algebra-potentials/TYPES.md"

with open(TEX_PATH, 'r') as f:
    lines = f.readlines()
text = "".join(lines)

ENV_KINDS = {
    "definition": "def",
    "proposition": "prop",
    "lemma": "lem",
    "theorem": "thm",
    "corollary": "cor",
    "example": "ex",
    "remark": "rmk",
    "notation": "not",
}

# Build cumulative offsets so we can map char-offset -> 1-indexed line number.
line_offsets = [0]
for ln in lines:
    line_offsets.append(line_offsets[-1] + len(ln))

def offset_to_line(offset):
    lo, hi = 0, len(line_offsets) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if line_offsets[mid] <= offset:
            lo = mid + 1
        else:
            hi = mid
    return lo

# Track structure: chapter, section, subsection at each line
chapter_at = [None] * (len(lines) + 2)
section_at = [None] * (len(lines) + 2)
subsection_at = [None] * (len(lines) + 2)

cur_chap = cur_sec = cur_sub = None
chap_re = re.compile(r'^\\chapter\{([^}]*)\}(?:\\label\{([^}]+)\})?')
sec_re = re.compile(r'^\\section\{([^}]*)\}(?:\\label\{([^}]+)\})?')
sub_re = re.compile(r'^\\subsection\{([^}]*)\}(?:\\label\{([^}]+)\})?')

for i, ln in enumerate(lines, start=1):
    m = chap_re.match(ln)
    if m:
        cur_chap = {"title": m.group(1), "label": m.group(2)}
        cur_sec = None
        cur_sub = None
    m = sec_re.match(ln)
    if m:
        cur_sec = {"title": m.group(1), "label": m.group(2)}
        cur_sub = None
    m = sub_re.match(ln)
    if m:
        cur_sub = {"title": m.group(1), "label": m.group(2)}
    chapter_at[i] = cur_chap
    section_at[i] = cur_sec
    subsection_at[i] = cur_sub

# ==== Task 1: results ====
results = []
begin_re = re.compile(r'\\begin\{(' + "|".join(ENV_KINDS.keys()) + r')\}')
for m in begin_re.finditer(text):
    kind = m.group(1)
    start = m.start()
    end_re = re.compile(r'\\(begin|end)\{' + re.escape(kind) + r'\}')
    depth = 1
    pos = m.end()
    end_pos = None
    for em in end_re.finditer(text, pos):
        if em.group(1) == 'begin':
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end_pos = em.end()
                break
    if end_pos is None:
        continue
    body = text[start:end_pos]
    # Accept the canonical prefix; also accept "lemma." for kind=="lemma"
    accepted_prefixes = [ENV_KINDS[kind] + "."]
    if kind == "lemma":
        accepted_prefixes.append("lemma.")
    label_matches = re.findall(r'\\label\{([^}]+)\}', body)
    label = None
    for lm in label_matches:
        if any(lm.startswith(p) for p in accepted_prefixes):
            label = lm
            break
    if label is None:
        continue

    line_start = offset_to_line(start)
    line_end = offset_to_line(end_pos - 1)

    proof_tex = None
    after = text[end_pos:]
    aftstrip = re.match(r'\s*', after)
    proof_start_off = end_pos + (aftstrip.end() if aftstrip else 0)
    if text[proof_start_off:proof_start_off+13] == '\\begin{proof}':
        proof_re = re.compile(r'\\(begin|end)\{proof\}')
        depth = 1
        pos = proof_start_off + 13
        for em in proof_re.finditer(text, pos):
            if em.group(1) == 'begin':
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    proof_tex = text[proof_start_off:em.end()]
                    break

    combined = body + ("\n" + proof_tex if proof_tex else "")

    cref_deps = []
    for cm in re.finditer(r'\\[cC]ref\{([^}]+)\}', combined):
        for ref in cm.group(1).split(','):
            ref = ref.strip()
            if ref:
                cref_deps.append(ref)

    eqref_deps = []
    for em2 in re.finditer(r'\\eqref\{([^}]+)\}', combined):
        for ref in em2.group(1).split(','):
            ref = ref.strip()
            if ref:
                eqref_deps.append(ref)

    cite_deps = []
    for cm in re.finditer(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', combined):
        for ref in cm.group(1).split(','):
            ref = ref.strip()
            if ref:
                cite_deps.append(ref)

    chap = chapter_at[line_start] or {"title": None, "label": None}
    sec = section_at[line_start] or {"title": None, "label": None}
    sub = subsection_at[line_start]

    results.append({
        "label": label,
        "kind": kind,
        "chapter": chap,
        "section": sec,
        "subsection": sub,
        "line_start": line_start,
        "line_end": line_end,
        "statement_tex": body,
        "proof_tex": proof_tex,
        "cref_deps": cref_deps,
        "eqref_deps": eqref_deps,
        "cite_deps": cite_deps,
    })

results.sort(key=lambda r: r["line_start"])

# ==== Task 2: types ====
types = []

type_macro_patterns = [
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\Cat\{[^}]+\})\}'), 'category'),
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\Fun\{[^}]+\})\}'), 'functor'),
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\mathbb\{[^}]+\})\}'), 'structure'),
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\mathcal\{[^}]+\})\}'), 'structure'),
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\mathfrak\{[^}]+\})\}'), 'structure'),
    (re.compile(r'\\newcommand\{(\\[A-Za-z]+)\}\{(\\mathsf\{[^}]+\})\}'), 'structure'),
]

# Roughly preamble = lines before \begin{document} (line 487 in this file)
preamble_end_line = None
for i, ln in enumerate(lines, start=1):
    if ln.strip().startswith(r'\begin{document}'):
        preamble_end_line = i
        break
if preamble_end_line is None:
    preamble_end_line = 487

preamble = "".join(lines[:preamble_end_line])
postamble = "".join(lines[preamble_end_line:])
pre_len = len(preamble)

found_macros = {}  # macro_name -> (kind, body)
for pat, kind in type_macro_patterns:
    for m in pat.finditer(preamble):
        name = m.group(1)
        body = m.group(2)
        if name not in found_macros:
            found_macros[name] = (kind, body)

def find_first_use_global_offset(macro):
    pat = re.compile(re.escape(macro) + r'(?![A-Za-z])')
    m = pat.search(postamble)
    if m:
        return pre_len + m.start()
    return None

def label_at_offset(offset):
    line = offset_to_line(offset)
    for r in results:
        if r["line_start"] <= line <= r["line_end"]:
            return r["label"]
    sub = subsection_at[line]
    if sub and sub.get("label"):
        return sub["label"]
    sec = section_at[line]
    if sec and sec.get("label"):
        return sec["label"]
    chap = chapter_at[line]
    if chap and chap.get("label"):
        return chap["label"]
    return None

def one_line_at(offset, width=240):
    rel = offset - pre_len
    snippet = postamble[max(0, rel):rel + width]
    snippet = re.sub(r'\s+', ' ', snippet)
    return snippet.strip()

for name, (kind, body) in sorted(found_macros.items()):
    off = find_first_use_global_offset(name)
    if off is None:
        continue
    intro = label_at_offset(off)
    desc = one_line_at(off)
    types.append({
        "name": name,
        "symbol": body,
        "kind": kind,
        "introduced_in": intro,
        "one_line_description": desc[:200],
    })

# \emph{...} first-introductions
emph_seen = {}
for m in re.finditer(r'\\emph\{([^}]+)\}', postamble):
    phrase = m.group(1).strip()
    if phrase in emph_seen:
        continue
    global_off = pre_len + m.start()
    intro = label_at_offset(global_off)
    desc = one_line_at(global_off, 240)
    emph_seen[phrase] = {
        "name": phrase,
        "symbol": None,
        "kind": "structure",
        "introduced_in": intro,
        "one_line_description": desc[:200],
    }

for phrase, entry in emph_seen.items():
    if len(phrase) > 80:
        continue
    if phrase.lower() in ("proof.", "proof"):
        continue
    types.append(entry)

# ==== Sanity: dangling crefs ====
all_doc_labels = set(re.findall(r'\\label\{([^}]+)\}', text))
dangling = []
for r in results:
    for d in r["cref_deps"]:
        if d not in all_doc_labels:
            dangling.append({"from": r["label"], "missing": d})

# ==== Write JSON ====
out = {"results": results, "types": types}
with open(OUT_JSON, 'w') as f:
    json.dump(out, f, indent=2)

# ==== Write TYPES.md ====
by_kind = {}
for t in types:
    by_kind.setdefault(t["kind"], []).append(t)

md = []
md.append("# Types module (auto-extracted draft)")
md.append("")
md.append("This file is auto-extracted from `dynamic-algebra-potentials.tex` and lists the named mathematical structures the paper introduces. It is intended to be hand-curated and to serve as the shared vocabulary for the upcoming code implementation.")
md.append("")
md.append("Each bullet has the form `- **\\name** (introduced in \\cref{label}) -- one-line description.`")
md.append("")

kind_order = ["category", "functor", "structure", "operation", "other"]
kind_titles = {
    "category": "Categories",
    "functor": "Functors",
    "structure": "Structures",
    "operation": "Operations",
    "other": "Other",
}
seen_kinds = set(by_kind.keys())
ordered = [k for k in kind_order if k in seen_kinds] + [k for k in seen_kinds if k not in kind_order]

for k in ordered:
    md.append(f"## {kind_titles.get(k, k.title())}")
    md.append("")
    items = by_kind[k]
    items.sort(key=lambda t: (0 if t["name"].startswith("\\") else 1, t["name"].lower()))
    for t in items:
        nm = t["name"]
        if t.get("symbol"):
            display = f"**`{nm}`** (= `{t['symbol']}`)"
        else:
            display = f"**{nm}**"
        intro = t["introduced_in"] or "?"
        desc = t["one_line_description"].replace("\n", " ")
        md.append(f"- {display} (introduced in \\cref{{{intro}}}) -- {desc}")
    md.append("")

with open(OUT_MD, 'w') as f:
    f.write("\n".join(md))

# ==== Report ====
from collections import Counter
counts = Counter(r["kind"] for r in results)
print("=== RESULT COUNTS ===")
for k, v in counts.most_common():
    print(f"  {k}: {v}")
print(f"Total results: {len(results)}")
print(f"Total types: {len(types)}")
print(f"Dangling crefs: {len(dangling)}")
if dangling:
    for d in dangling[:50]:
        print(f"  {d['from']} -> {d['missing']}")

def sample_of(kind):
    for r in results:
        if r["kind"] == kind:
            return r
    return None

print("\n=== SAMPLES ===")
for k in ("definition", "proposition", "theorem"):
    s = sample_of(k)
    if s:
        compact = {kk: (vv if kk not in ("statement_tex","proof_tex") else (vv[:120] + "..." if vv else None)) for kk, vv in s.items()}
        print(f"\n--- {k} sample ---")
        print(json.dumps(compact, indent=2)[:1500])
