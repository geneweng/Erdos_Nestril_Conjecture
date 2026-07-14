# Erdős–Nešetřil Conjecture: Computational Attack at Δ = 4

**Conjecture (Erdős–Nešetřil, 1985).** The edges of any simple graph with maximum
degree Δ can be partitioned into at most 1.25 Δ² induced matchings — equivalently,
the *strong chromatic index* satisfies χ′ₛ(G) ≤ 1.25 Δ².

Proved for Δ ≤ 3; **open for Δ ≥ 4**. At Δ = 4 the conjectured bound is **20**
and the best proven upper bound is **21** (Huang–Santana–Yu 2018), so a
counterexample is precisely a Δ = 4 graph with χ′ₛ = 21. The C₅ blowup
(each vertex of a 5-cycle replaced by an independent pair) is 4-regular with 20
pairwise-conflicting edges, so the bound is tight.

This repo is a systematic computational hunt for such a counterexample.
**No counterexample was found**; along the way we obtained rigorous negative
results — see [REPORT.md](REPORT.md) for the full write-up. Highlights:

* **No counterexample exists on ≤ 14 vertices** (exhaustive: ~40M graphs after
  provable criticality pruning; n = 15 in progress).
* **The strong clique number of Δ ≤ 4 graphs is exactly 20** (SAT, with a
  rigorous 28-vertex reduction): the "clique version" of the conjecture holds
  tightly at Δ = 4, so any counterexample needs conflict-graph chromatic number
  strictly above clique number.
* Structured families (circulants, torus grids, line graphs of cubic graphs,
  cycle blowups) and simulated annealing all stay well below 20; the C₅ blowup
  is an isolated peak.

## Key idea

A strong edge coloring of G is a proper vertex coloring of the conflict graph
L(G)² (vertices = edges of G; adjacent iff they share an endpoint or are joined
by an edge). All exact χ′ₛ computations reduce to graph coloring, decided with
the CaDiCaL SAT solver plus clique symmetry breaking.

## Setup

```sh
python3 -m venv .venv
.venv/bin/pip install networkx python-sat
brew install nauty          # for geng (exhaustive generation)
```

## Files

| File | Purpose |
|---|---|
| `sec.py` | Core toolkit: conflict graph, DSATUR/clique bounds, SAT coloring, exact χ′ₛ. Run directly for sanity checks. |
| `hunt_sweep.py` + `run_sweep.sh` | Exhaustive sweep: `./run_sweep.sh <n> <maxedges> <workers>` enumerates all connected graphs with degrees in [3,4] and ≥ 21 edges via `geng`, flags any χ′ₛ ≥ 21. |
| `hunt_strongclique.py` | SAT search for a 21-edge strong clique at Δ = 4 (`python hunt_strongclique.py <n> [target]`). |
| `hunt_strongclique_d.py` | Same, generalized: `python hunt_strongclique_d.py <D> <target> [N]`. |
| `hunt_structured.py` / `hunt_structured2.py` / `hunt_circulants.py` | Structured families: circulants, torus grids, line graphs of cubic graphs, odd-cycle blowups. |
| `hunt_anneal.py` | Simulated annealing over Δ ≤ 4 graphs: `python hunt_anneal.py <n> <seed> <steps>`. |
| `test_crosscheck.py` | Validation: SAT-based χ′ₛ vs. brute-force backtracking on 60 random graphs. |
| `results/` | Logs from all runs. |
| `REPORT.md` | Full write-up: methods, pruning lemmas, results, interpretation. |

## Reproducing the headline results

```sh
.venv/bin/python sec.py                        # sanity: C5=5, C5 blowup=20, Petersen=5
.venv/bin/python test_crosscheck.py            # solver cross-validation
.venv/bin/python hunt_strongclique.py 28       # UNSAT: no 21-edge strong clique, Δ≤4
.venv/bin/python hunt_strongclique_d.py 3 11   # UNSAT: matches known Δ=3 value
./run_sweep.sh 11 22 4                         # exhaustive n=11 (seconds)
```
