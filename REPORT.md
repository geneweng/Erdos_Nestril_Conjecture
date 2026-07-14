# Erdős–Nešetřil at Δ = 4: Counterexample Hunt — Final Report

**Conjecture (Erdős–Nešetřil, 1985).** χ′ₛ(G) ≤ 1.25 Δ² for every simple graph G
of maximum degree Δ, where χ′ₛ is the strong chromatic index (minimum number of
induced matchings partitioning E). Proved for Δ ≤ 3; open for Δ ≥ 4.

At Δ = 4 the conjectured bound is **20**; the proven bound is **21**
(Huang–Santana–Yu 2018); the C₅ blowup C₅[2] (each vertex of a 5-cycle replaced
by an independent pair; 4-regular, 10 vertices, 20 edges, all pairwise
conflicting) shows 20 is attained. **A counterexample is exactly a Δ ≤ 4 graph
with χ′ₛ = 21.** This project hunted for one.

**Verdict: no counterexample found — and two rigorous negative results.**
Companion document: [PROOF_NOTES.md](PROOF_NOTES.md) (structural lemmas with
proofs, and an assessment of the path to a full proof).

## Tooling and validation

χ′ₛ(G) = χ(L(G)²) where the conflict graph L(G)² joins edges at distance ≤ 1.
Exact values: DSATUR upper bound, max-clique lower bound, CaDiCaL SAT decisions
with clique symmetry breaking (`sec.py`). Validation:

* C₅ → 5, Petersen → 5, C₅[2] → 20, K₅ → 10, K₄,₄ → 16 (all known values);
* Δ = 3 strong-clique maximum reproduced: 10 achievable, 11 UNSAT (matches the
  proven Δ = 3 theorem);
* SAT-based χ′ₛ equals brute-force backtracking on 60 random graphs
  (`test_crosscheck.py`).

## Result 1 — No counterexample on ≤ 14 vertices (exhaustive)

Any counterexample contains a connected edge-critical one, whose every edge has
≥ 20 conflicting edges; degree counting then forces all degrees in {3, 4} and
no adjacent degree-3 pairs (Lemmas A–B in PROOF_NOTES.md). geng enumeration of
all connected degree-[3,4] graphs with ≥ 21 edges, with the criticality prune,
DSATUR filter, and SAT decisions:

| n | graphs tested | χ′ₛ ≥ 21 | DSATUR ≥ 20 |
|---|---|---|---|
| 11 | 5,705 | 0 | 0 |
| 12 | 284,175 | 0 | 0 |
| 13 | 3,323,481 | 0 | 0 |
| 14 | 36,801,545 | 0 | 0 |
| **total** | **40,414,906** | **0** | **0** |

Not a single graph even pushed the greedy coloring to 20 colors. A partial
n = 15 sweep (~1 CPU-day of the ~430M-graph space) was aborted by request with
no hits. **Any counterexample has ≥ 15 vertices.**

## Result 2 — Strong clique number at Δ = 4 is exactly 20 (SAT, rigorous)

A 21-edge strong clique (edges pairwise conflicting) would disprove the
conjecture instantly, and the general strong-clique bound (≈ 4Δ²/3 proven)
does not exclude it. We settled it: after a rigorous reduction to host graphs
on ≤ 28 vertices with WLOG labeling, CaDiCaL proves UNSAT in 16 s; target 20 is
SAT and recovers C₅[2]. See PROOF_NOTES.md §3.

> No graph with Δ ≤ 4 has 21 pairwise-conflicting edges; the maximum is 20.

Consequence: a counterexample's conflict graph must have χ = 21 > ω — a global
chromatic/clique-gap obstruction, invisible to local density.

At Δ = 5 the analogous probe (does a 30-edge strong clique exist? the refined
odd-Δ conjecture says max = 29) was still running when this report was written;
the instance (39-vertex host, 304k clauses) had not resolved after ~1 h.
[Update here when it finishes.]

## Result 3 — Structured families plateau far below 20

747 structured Δ = 4 graphs, exact where the budgeted SAT converged
(brackets `[lb,ub]` otherwise):

| family | count | max χ′ₛ (exact) | max upper bound |
|---|---|---|---|
| circulants C_n(a,b), n = 11–40 | ~620 | 13 | 16 (undecided brackets at n=16) |
| torus grids C_m □ C_n, 3 ≤ m ≤ n ≤ 8 | 15 | 12 | 12 |
| line graphs of cubic graphs ≤ 14 vertices | 112+ | 13 | 13 |
| odd-cycle blowups (parts ≤ 3, Δ ≤ 4) | dozens | 20 (C₅[2] itself) | 20 |
| named graphs (K₅, K₄,₄, Q₄, Chvátal, …) | — | 16 (K₄,₄) | 16 |

## Result 4 — Local search confirms C₅[2] is an isolated peak

Simulated annealing over Δ ≤ 4 graphs (n = 12–18, exact χ′ₛ objective,
add/remove/rewire moves, 3,000 steps × 6 runs): random starts plateau at
χ′ₛ = 15–17; runs seeded at C₅[2] never improve on 20 — every mutation
(including every way of adding a 21st edge and more vertices) collapses the
value. The extremal configuration behaves as a strict, isolated local maximum
of χ′ₛ over the whole search space, consistent with the conjectured uniqueness
of the extremal graph.

## Interpretation

Everything points to the conjecture being **true and tight at Δ = 4**:

1. The clique relaxation is now a theorem (max strong clique = 20, attained
   only by the extremal-type configuration in our searches).
2. No counterexample exists through 14 vertices, with a criticality theory
   (min degree 3, scattered degree-3 vertices, ≤ 1 triangle per edge,
   4t + D + x ≤ 4 local sparsity) that makes small counterexamples impossible
   and large ones extremely rigid.
3. Every constructive family and every stochastic search saturates at or below
   17 except the unique known extremal graph at exactly 20.

The remaining gap (21 → 20) is a pure "last color" problem. The most promising
route we see is combining our critical-graph lemmas with the Huang–Santana–Yu
case analysis at the 20-color level (PROOF_NOTES.md §5).

## Reproducibility

All searches: `sec.py` (toolkit), `hunt_sweep.py`/`run_sweep.sh` (exhaustive),
`hunt_strongclique.py`/`hunt_strongclique_d.py` (clique SAT),
`hunt_structured.py`/`hunt_bounded.py`/`hunt_circulants.py` (families),
`hunt_anneal.py` (annealing), `test_crosscheck.py` (validation), logs in
`results/`. Environment: Python 3.13, networkx, python-sat (CaDiCaL 1.9.5),
nauty geng, macOS, 12 cores. Total compute ≈ 6 CPU-hours plus the aborted
n = 15 partial sweep.
