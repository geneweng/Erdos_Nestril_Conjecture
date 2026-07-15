# Handoff: Erdos-Nesetril Delta 4 Project

Date: 2026-07-15

This is the pause point after the SME correction and the first corrected
post-erratum computational push.

## Current State

The conjecture remains open at `Delta = 4`.  The repository now clearly
separates:

* rigorous results that survive the SME correction;
* exploratory/conditional data from the withdrawn edge-critical reduction.

The key correction is in `ERRATA.md`: a strong coloring of `H - e` is not a
coloring of the fixed conflict graph `L(H)^2 - e`, because deleting `e` can
remove conflicts among other edges.  Therefore the earlier edge-critical
reduction, the degree-3 elimination, the triangle elimination, and the
4-regular triangle-free reduction are withdrawn as proof claims.

## Rigorous Results Currently Recorded

1. **Strong clique theorem.**
   No graph with `Delta <= 4` contains 21 pairwise-conflicting edges.  The
   strong clique number is exactly 20, attained by the `C5` blowup.

2. **Corrected conflict-core verification through 13 vertices.**
   Work in the fixed conflict graph `C = L(G)^2`.  If the 20-core of `C` is
   20-colorable, then `C` is 20-colorable by greedy extension through the
   core-deletion order.  This avoids all invalid `G - e` reasoning.

   Corrected sweep totals:

   ```text
   n=11: graphs=5,705, empty 20-core=5,705, hits=0
   n=12: graphs=1,032,644, empty 20-core=1,032,640,
         nonempty cores=4, max core greedy colors=12, hits=0
   n=13: graphs=37,111,262, empty 20-core=37,111,243,
         nonempty cores=19, max core greedy colors=15, hits=0
   ```

   This soundly verifies the conjecture through 13 vertices.

## Important Files

* `ERRATA.md` explains the SME correction and the replacement framework.
* `CONFLICT_CORE.md` states the fixed-conflict-graph core lemma and records the
  corrected sweeps through order 13.
* `hunt_sweep.py` is the corrected dependency-free sweep.  It reads graph6,
  builds `L(G)^2`, takes the 20-core, and only exact-checks the rare core not
  certified by greedy coloring.
* `run_sweep.sh` now runs the corrected sweep over `Delta <= 4` connected
  graphs with enough edges; it no longer applies the withdrawn `-d3` prune.
* `results/conflict_core_sweeps_n11_n12.txt` records the corrected n=11,12
  runs.
* `results/conflict_core_sweep_n13.txt` records the full 8-partition n=13 run.
* `PROOF_NOTES.md`, `PROOF_ATTEMPT.md`, and `REPORT.md` are archival unless
  read together with `ERRATA.md`.

## Exploratory Data Still Useful, But Not Proof

The conditional 4-regular triangle-free sweeps and packing experiments remain
useful for pattern finding, but they rely on the withdrawn reduction and should
not be cited as proof-certified exclusions.

Key exploratory result:

* conditional order-17 high-greedy layer packs into at most 13 induced
  matchings after randomized maximum-induced-matching tie-breaking.

## Exact Commands Used Most Recently

Corrected order-13 sweep was run in 8 partitions:

```sh
geng -c -q -D4 13 21:26 PART/8 \
  | python3 hunt_sweep.py core_n13_pPART --progress 1000000
```

Aggregate from the 8 partitions:

```text
graphs=37111262
empty_core=37111243
greedy_core_ok=19
exact_core_ok=0
undecided=0
hits=0
max_core_size=26
max_core_greedy=15
core_size_hist 0:37111243 26:19
core_greedy_hist 12:4 13:7 14:7 15:1
```

Validation before the latest commit:

```sh
git diff --check
python3 -m py_compile hunt_sweep.py analyze_reduced_extremes.py \
  check_reduced_small_orders.py check_regular_trianglefree_profiles.py \
  check_degree3_cross_edges.py sec.py
```

## Next Best Steps

1. **Make `hunt_sweep.py` log nonempty cores even when greedy certifies them.**
   The n=13 run found only 19 nonempty 20-cores, but their graph6 strings were
   not saved because they were greedily certified.  Saving them would allow
   structural analysis of why the core is so rare.

2. **Prepare a resumable order-14 corrected sweep.**
   Order 13 already generated 37,111,262 connected graphs.  Order 14 should be
   run in many partitions with per-partition logs committed or resumable.

3. **Analyze the conflict-core threshold structurally.**
   A counterexample must have a non-20-colorable 20-core in `L(G)^2`.  The next
   proof direction is to show that the 20-core is sparse/rare or always
   20-colorable under `Delta <= 4`, without using edge-deletion criticality.

4. **Rebuild local lemmas in the selected-edge language.**
   Work with a vertex-21-critical induced subgraph `C0 subset L(G)^2`, whose
   vertices are a selected edge set `F subset E(G)`.  Count selected conflict
   neighbors in `F`, not total conflicts in `G`.

5. **Keep the old conditional reductions quarantined.**
   They are still useful for intuition, but the proof path should start from
   `C0` and the 20-core certificate.

## Current Git State At Pause

Latest pushed commit before this handoff note:

```text
12357f3 Verify conflict-core sweep through order 13
```

After adding this handoff note, the intended commit is:

```text
Save project handoff summary
```
