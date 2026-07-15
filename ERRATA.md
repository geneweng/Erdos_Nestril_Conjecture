# Erratum: Edge-Critical Deletion Is Not Valid for Strong Coloring

Date: 2026-07-15

## Correction

An SME review identified a flaw in the proof notes: a strong coloring of
`H - e` was used as though it were a coloring of the fixed conflict graph
`L(H)^2 - e`.  This is false.

Deleting an edge from `H` can remove conflicts between other edges.  Thus an
induced matching in `H - e` need not be an induced matching in `H`.  Equivalently,

```text
L(H - e)^2 is not generally equal to L(H)^2 - e.
```

Example: in the path `a-b-c-d`, deleting the middle edge `bc` makes `ab` and
`cd` non-conflicting in `H - bc`, so they may receive the same color.  In the
original graph `H`, they conflict through `bc`.

## Withdrawn Claims

The following claims in the proof documents are withdrawn as proof claims:

* edge-minimality of `H` implies `L(H)^2` is vertex-21-critical;
* every edge of an edge-critical `H` has at least 20 conflicts;
* the degree-3 elimination in `PROOF_ATTEMPT.md`;
* the triangle elimination in `PROOF_ATTEMPT.md`;
* the reduction of a counterexample to the 4-regular triangle-free case;
* the proof-certified small-order exclusion that relied on those criticality
  prunes.

The reduced 4-regular triangle-free searches remain useful exploratory data,
but they are conditional on a withdrawn reduction and should not be cited as a
proof of absence of counterexamples.

## What Remains Valid

The following parts are not affected by this issue:

* the definition of strong coloring as coloring the conflict graph `L(G)^2`;
* exact color computations on explicitly supplied graphs;
* solver validation and cross-checks;
* the SAT proof that no graph with `Delta <= 4` contains 21 pairwise-conflicting
  edges, i.e. the strong clique number at `Delta = 4` is exactly 20;
* exploratory search logs, provided they are described as computational
  evidence rather than proof after invalid pruning.

## Correct Replacement Framework

The proof setup should be rebuilt in the fixed conflict graph.

If a counterexample `G` exists, set `C = L(G)^2` and choose an induced subgraph
`C0` that is vertex-21-critical.  Its vertices are a selected edge set
`F subset E(G)`.  Colorings must be colorings of `C0 - X`, not strong colorings
of `G - X`.

Consequences must be restated in this language:

* every selected edge `e in F` has at least 20 neighbors inside `C0`;
* Gallai's theorem applies to vertices of degree 20 in `C0`, not necessarily to
  edges with exactly 20 total conflicts in `G`;
* local counting must count selected conflict neighbors in `F`, not all edges
  of the ambient graph;
* any Hall/list-extension argument must extend a coloring of `C0 - X`.

This is the next proof direction.  It preserves standard critical-graph theory,
but it removes the invalid step from colorings of `H - e` back to colorings of
`H`.
