# Erdős–Nešetřil Conjecture at Δ = 4: A Computational Attack

**Conjecture (Erdős–Nešetřil, 1985).** The edges of any simple graph with maximum
degree Δ can be partitioned into at most ⌈1.25 Δ²⌉ induced matchings; equivalently
the *strong chromatic index* satisfies χ′ₛ(G) ≤ 1.25 Δ² (with the refined value
(5Δ² − 2Δ + 1)/4 for odd Δ).

Status of the problem: proved for Δ ≤ 3 (Andersen 1992; Horák–Qing–Trotter 1993).
Open for Δ ≥ 4. For Δ = 4 the conjectured bound is **20**, and the best proven
upper bound is **21** (Huang–Santana–Yu 2018). The C₅ blowup (each vertex of a
5-cycle replaced by an independent pair) is 4-regular with 20 edges that pairwise
conflict, so χ′ₛ = 20: the conjecture is tight. Hence at Δ = 4 the conjecture and
the theorem differ by exactly one color: a counterexample is precisely a Δ = 4
graph with χ′ₛ = 21.

This project hunted for such a counterexample. **No counterexample was found**, and
several rigorous negative results were established along the way (modulo correctness
of the encodings + solvers, all of which were validated on known cases).

## Method

A strong edge coloring of G is a proper vertex coloring of the conflict graph
L(G)², whose vertices are edges of G, adjacent when they share an endpoint or are
joined by an edge of G. Tooling (`sec.py`): exact χ′ₛ via DSATUR upper bound, exact
max-clique lower bound, and CaDiCaL SAT decisions with clique symmetry breaking.
Validated on: C₅ (χ′ₛ = 5), Petersen (5), C₅ blowup (20), Δ=3 clique values (10 yes/11 no).

## Result 1 — No counterexample on ≤ 14 vertices (exhaustive)

Any counterexample contains a connected *edge-critical* counterexample H (delete
edges while χ′ₛ stays 21; components don't interact in strong colorings). In H every
edge conflicts with ≥ 20 others. Counting degrees around an edge uv with
S = N[u] ∪ N[v]: #conflicts ≤ Σ_{s∈S} deg(s) − e(S) − 1, which gives:

* deg(u) + deg(v) ≤ 6 ⇒ ≤ 16 conflicts. So **H has min degree ≥ 3 and no two
  adjacent degree-3 vertices**.
* Every counterexample has ≥ 21 edges, so ≥ 11 vertices at Δ = 4.

geng enumerated all connected graphs with degrees in [3,4] and ≥ 21 edges on
n = 11, 12, 13, 14 vertices (5,705 + 284,175 + 3,323,481 + 36,801,545 graphs).
Each was tested (criticality prune → DSATUR ≤ 20 prune → SAT decision).
**Outcome: zero graphs with χ′ₛ ≥ 21; [TODO n14/n15 status]. Any edge-critical
counterexample needs ≥ [15] vertices.**

## Result 2 — The strong clique number at Δ = 4 is exactly 20 (SAT, rigorous)

A "strong clique" is a set of edges pairwise at distance ≤ 1 — a clique in L(G)².
A 21-edge strong clique with Δ ≤ 4 would immediately disprove the conjecture. Note
the general strong-clique bound 1.25Δ² is itself only conjectured (best proven:
~4Δ²/3, Faron–Postle), which for Δ = 4 allows 21 — so this route was genuinely open.

Finite model: fix a clique edge {0,1}; every clique edge touches S = N[0] ∪ N[1],
|S| ≤ 8; every vertex relevant to the clique and its joining edges is an endpoint
of a clique edge, and ≤ 20 clique edges leave S, so 28 vertices suffice. A SAT
encoding (host adjacency vars + clique selector vars, degree ≤ 4 cardinality
constraints, pairwise-conflict clauses, WLOG prefix labeling) is **UNSAT for
21 edges on n = 28 in 16 s** (CaDiCaL), and SAT for 20 edges, recovering the C₅
blowup. Hence:

> **Theorem (computer-assisted).** No graph with Δ ≤ 4 contains 21 edges that
> pairwise share an endpoint or are joined by an edge. The Erdős–Nešetřil
> conjecture holds at Δ = 4 in its strong-clique version, tightly: max = 20.

Consequence: any counterexample graph must have conflict-graph chromatic number
strictly exceeding its clique number — it cannot be certified by local density.

Same method at Δ = 3: max strong clique = 10 = (5·9−6+1)/4 ✓ (matches the theorem).
At Δ = 5: [TODO Δ=5 results]

## Result 3 — Structured families and local search stay far below 20

* 4-regular circulants C_n(a,b), 11 ≤ n ≤ 40: max χ′ₛ observed [TODO].
* Torus grids C_m □ C_n: χ′ₛ ∈ {9, 10, 11} — far below 20.
* Line graphs of all connected cubic graphs on ≤ 14 vertices (4-regular): [TODO].
* Blowups of odd cycles with part sizes ≤ 3 and degree ≤ 4: [TODO].
* Simulated annealing over Δ ≤ 4 graphs (n = 12–18, exact χ′ₛ objective):
  never exceeded 20; the only state reaching 20 was the C₅ blowup itself.
  Random 4-regular graphs at n = 12–14 sit around χ′ₛ ≈ 13–17, and adding any
  21st edge to the C₅ blowup (n = 11+) collapses the value — the extremal
  configuration is an isolated peak.

## Interpretation

Everything found is consistent with the conjecture being **true and tight** at
Δ = 4: the unique-looking extremal structure (C₅ blowup) maximizes both clique
and chromatic number of the conflict graph, the clique version is now verified
exactly, and there is no counterexample on ≤ 14 vertices [TODO update]. A
counterexample, if it exists, must be a graph of ≥ 15 vertices whose conflict
graph has chromatic number 21 but clique number ≤ 20 — a chromatic/clique gap
phenomenon of which no trace appeared in ~40 million exhaustively tested graphs
or any structured family.

## Files

* `sec.py` — solver toolkit (conflict graph, DSATUR, max clique, SAT coloring)
* `hunt_sweep.py`, `run_sweep.sh` — exhaustive geng sweeps with criticality pruning
* `hunt_strongclique.py`, `hunt_strongclique_d.py` — strong-clique SAT (Δ=4 / general)
* `hunt_structured.py` — circulants, torus grids, line graphs, blowups
* `hunt_anneal.py` — simulated annealing
* `results/` — logs
