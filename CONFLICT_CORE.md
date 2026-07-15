# Conflict-Core Framework After the Edge-Deletion Erratum

Date: 2026-07-15

This note records the replacement framework after `ERRATA.md`.  The key point
is to work entirely inside the fixed conflict graph `C = L(G)^2`.

## Core Lemma

Let `C` be any graph and let `K` be its `k`-core, obtained by repeatedly
deleting vertices of degree less than `k`.

If `K` is `k`-colorable, then `C` is `k`-colorable.

Proof: color `K`.  Add the deleted vertices back in reverse deletion order.
When a vertex is reinserted, it has fewer than `k` neighbors that are already
present, so at most `k - 1` colors are blocked.  One of the `k` colors remains
available.

For the Erdos-Nesetril problem at `Delta = 4`, use `k = 20`.  Therefore any
counterexample `G` must have a conflict graph `C = L(G)^2` whose 20-core is
not 20-colorable.  Equivalently, every vertex-21-critical induced subgraph
`C0 subset C` lies inside the 20-core.

This is the sound replacement for the withdrawn edge-critical prune.  It uses
only colorings of induced subgraphs of the fixed conflict graph.

## Consequences

The core lemma gives a valid computational filter:

1. Generate a graph `G`.
2. Build `C = L(G)^2`.
3. Compute the 20-core `K`.
4. If `K` is empty, certify `G` is 20-strong-colorable.
5. If `K` is 20-colorable, certify `G` is 20-strong-colorable by extension.
6. Only if `K` is not 20-colorable is `G` a counterexample.

The updated `hunt_sweep.py` implements this filter without `networkx` or SAT
dependencies.  It uses the repository's graph6 parser, adjacency-list conflict
graph, greedy DSATUR upper bound, and bounded exact backtracker for the rare
case where the 20-core is not greedily certified.

## Corrected Small-Order Result Through 12 Vertices

Any graph with at most 10 vertices and `Delta <= 4` has at most 20 edges, so it
is trivially 20-strong-colorable by giving every edge its own color.  A
counterexample on at most 12 vertices must therefore have a connected component
on 11 or 12 vertices with at least 21 edges.

The corrected unpruned sweeps are:

```sh
geng -c -q -D4 11 21:22 | python3 hunt_sweep.py core_n11 --progress 10000
geng -c -q -D4 12 21:24 | python3 hunt_sweep.py core_n12 --progress 100000
```

Results:

```text
[core_n11] done: graphs=5705, empty_core=5705, greedy_core_ok=0,
  exact_core_ok=0, undecided=0, hits=0, max_core_size=0, max_core_greedy=0
[core_n11] core_size_hist 0:5705

[core_n12] done: graphs=1032644, empty_core=1032640, greedy_core_ok=4,
  exact_core_ok=0, undecided=0, hits=0, max_core_size=24, max_core_greedy=12
[core_n12] core_size_hist 0:1032640 24:4
[core_n12] core_greedy_hist 10:1 12:3
```

Thus the conjecture is now soundly verified for all graphs with at most 12
vertices.  This proof uses no edge-critical deletion in the original graph.

## Order 13 Status

A corrected unpruned order-13 sweep was started:

```sh
geng -c -q -D4 13 21:26 | python3 hunt_sweep.py core_n13 --progress 1000000
```

It was interrupted after 2,000,000 generated graphs:

```text
[core_n13] seen=1000000 empty_core=999999 greedy_ok=0 exact_ok=0
  undecided=0 hits=0 elapsed=83.6s
[core_n13] seen=2000000 empty_core=1999999 greedy_ok=0 exact_ok=0
  undecided=0 hits=0 elapsed=167.1s
```

No hard 20-core was reported before the interrupt.  A full order-13 run is the
next natural computational target.
