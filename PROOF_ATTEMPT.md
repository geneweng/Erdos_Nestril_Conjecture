# Proof Attempt: Delta = 4 Erdős-Nešetřil

Date: 2026-07-14

Goal: prove that every simple graph with maximum degree at most 4 has strong
chromatic index at most 20.

Status of this pass: no complete proof.  The useful progress is a sharper
description of what a hypothetical counterexample with a degree-3 vertex must
look like.  The main new tools below are:

1. a Gallai-forest constraint on the edges with exactly 20 conflicts, and
2. a Hall-extension obstruction obtained by deleting a degree-3 vertex.

These are intended to extend the reductions already recorded in
`PROOF_NOTES.md`.

## Plan

1. Work in a minimal counterexample `H`.
2. Translate to the conflict graph `C = L(H)^2`.
3. Use standard critical-graph structure on the degree-20 vertices of `C`.
4. Try to eliminate degree-3 vertices of `H`.
5. If that succeeds, attack the remaining 4-regular case.

The pass below completes Steps 1--3 and makes partial progress on Step 4.

## Step 1: Critical Setup

Assume for contradiction that `H` is a connected edge-critical counterexample:

```text
Delta(H) <= 4,
chi'_s(H) = 21,
chi'_s(H - e) <= 20 for every edge e.
```

Let `C = L(H)^2`.  The vertices of `C` are the edges of `H`, and two vertices
of `C` are adjacent exactly when the corresponding edges of `H` conflict.
Then `C` is vertex-21-critical:

```text
chi(C) = 21,
chi(C - x) <= 20 for every vertex x of C.
```

In particular every vertex of `C` has degree at least 20.  Equivalently, every
edge of `H` conflicts with at least 20 other edges.

For an edge `e = uv` of `H`, put `S(e) = N[u] union N[v]`.  The local count is:

```text
conflicts(e) = sum_{s in S(e)} deg(s) - e(S(e)) - 1.
```

The existing notes already derive:

* `delta(H) >= 3`;
* no two degree-3 vertices are adjacent or share a neighbor;
* every 3--4 edge has exactly 20 conflicts;
* for a 4--4 edge `uv`, if `t = |N(u) cap N(v)|`, `D` is total degree
  deficiency among the outer vertices of `S(uv)`, and `x` is the number of
  extra internal edges in `S(uv)` beyond the star edges, then

```text
4t + D + x <= 4.
```

Call an edge of `H` **tight** if it has exactly 20 conflicts, i.e. if the
corresponding vertex of `C` has degree 20.

## Step 2: Gallai Constraint on Tight Edges

Use the standard Gallai theorem for critical graphs:

> In a `k`-critical graph, the subgraph induced by vertices of degree `k - 1`
> is a Gallai forest: every block is a clique or an odd cycle.

Applied to `C`, this says:

**Lemma 1.** The conflict graph induced by the tight edges of `H` is a Gallai
forest.

Two immediate corollaries will be useful.

**Corollary 1.** Let `e1,e2,e3` be three pairwise-conflicting tight edges.  No
tight edge `f` can conflict with exactly two of `e1,e2,e3`.

Proof.  The three edges `e1,e2,e3` form a triangle in the tight-edge subgraph.
If `f` is adjacent to exactly two vertices of this triangle, those four
vertices form a diamond block in the tight-edge subgraph.  A diamond is neither
a clique nor an odd cycle, contradicting Lemma 1.

**Corollary 2.** Let `e1,e2,e3` be three pairwise-conflicting tight edges.  If
tight edges `f` and `g` both conflict with all of `e1,e2,e3`, then `f` and `g`
must conflict with each other.

Proof.  If `f` and `g` were nonadjacent, then the five vertices
`{e1,e2,e3,f,g}` would lie in one block of the tight-edge subgraph: the triangle
gives two disjoint paths between any pair, and both `f` and `g` attach to all
three vertices of the triangle.  That block is not a clique because `fg` is
missing, and it is not an odd cycle because it contains a triangle with extra
chords.  This contradicts Lemma 1.

This does not prove the conjecture, but it gives a clean way to turn
critical-graph theory into structural constraints inside `H`.

## Step 3: Consequences Near a Degree-3 Vertex

Assume `u` is a degree-3 vertex of `H`.  Let its neighbors be
`v1,v2,v3`, and let

```text
Wi = N(vi) \ {u}.
ei = uvi.
```

From the existing notes:

* the sets `W1,W2,W3` are pairwise disjoint;
* each `Wi` is independent;
* no vertex of `Wi` is adjacent to `vj` for `i != j`;
* every vertex in `{v1,v2,v3} union W1 union W2 union W3` has degree 4;
* each `ei` is tight.

Thus `e1,e2,e3` are three pairwise-conflicting tight edges.

### Cross Edges Between Arms

Suppose `w_i in Wi`, `w_j in Wj`, `i != j`, and `w_i w_j` is an edge.  This
edge conflicts with exactly `ei` and `ej` among `e1,e2,e3`; it does not conflict
with the third edge because the degree-3 ball has the tree-like structure above.

By Corollary 1:

**Lemma 2.** Every cross edge between two different `Wi` arms is non-tight.
Equivalently, every such edge has at least 21 conflicts.

For a 4--4 cross edge this strengthens the local budget from

```text
4t + D + x <= 4
```

to

```text
4t + D + x <= 3.
```

### Tight Spokes

Call the edges from `vi` to `Wi` the spokes of arm `i`.  Every spoke conflicts
with all three of `e1,e2,e3`: it shares an endpoint with one of them and is
joined to the other two through the edge from `u` to its arm center.

If `vi w in arm i` and `vj x in arm j` are tight spokes with `i != j`, then
Corollary 2 forces them to conflict.  The local degree-3 structure rules out
all possible joins except `w x`.

**Lemma 3.** If two spokes in different arms are tight, then their outer
endpoints must be adjacent.  Equivalently, tight spokes in different arms force
cross edges between their `W` endpoints.

This is a concrete structural pressure on any degree-3 vertex.  It is not yet
a contradiction because a spoke need not be tight: a 4--4 spoke can have 21,
22, or 23 conflicts depending on the local budget around it.

## Step 4: Delete the Degree-3 Vertex

Continue with a degree-3 vertex `u` and edges `e1,e2,e3`.

Because `H` is edge-critical, `H - e1` is 20-strong-colorable.  Restrict such a
coloring after also deleting `e2` and `e3`; hence `H - u` is 20-strong-colorable.

For a fixed 20-coloring `phi` of `H - u`, let `Ai` be the set of colors
available for the missing edge `ei`.  In `H - u`, the edge `ei` has exactly 18
colored conflicts: its two conflicts `ej,ek` through `u` have been deleted.
Therefore

```text
|Ai| >= 2 for i = 1,2,3.
```

The three missing edges `e1,e2,e3` pairwise conflict, so extending `phi` to `H`
is exactly the problem of choosing distinct representatives from
`A1,A2,A3`.  By Hall's theorem, this is possible whenever

```text
|A1 union A2 union A3| >= 3.
```

Since `H` is a counterexample, no 20-coloring of `H - u` can extend.  Thus:

**Lemma 4.** In every 20-coloring of `H - u`,

```text
A1 = A2 = A3 = {alpha, beta}
```

for some two colors `alpha,beta` depending on the coloring.

This is substantially stronger than the one-edge frozen-rainbow lemma.

### Palette Consequences

Let

```text
Bi = {vi w : w in Wi}              (the three spokes in arm i)
B  = B1 union B2 union B3          (all nine spokes)
Oi = {edges incident with Wi, except the spokes Bi}.
```

The external conflict set for `ei` in `H - u` is exactly

```text
Xi = B union Oi,
```

with `|B| = 9`, `|Oi| = 9`, and `|Xi| = 18`.

Lemma 4 implies:

**Lemma 5.** In every 20-coloring of `H - u`:

1. each `Xi` uses exactly 18 distinct colors;
2. the same two colors are missing from all three `Xi`;
3. the nine spoke edges `B` are rainbow;
4. for each `i`, the nine edges `Oi` are rainbow;
5. the three sets `O1,O2,O3` use the same 9-color palette, disjoint from the
   9-color palette used on `B`.

Proof.  Since `Ai` has exactly two colors, the 18 colored conflicts in `Xi`
must use the other 18 colors with no repetition.  The sets `Xi` have the common
9-edge subset `B`, so `B` is rainbow.  In `Xi = B union Oi`, the remaining
9 edges `Oi` must be rainbow and use precisely the complement of the colors on
`B`.  This complement is independent of `i`, because the same two colors are
missing from all `Xi`.

## Current Blocker

The natural hope was that Lemma 5 would immediately contradict the local
structure around `u`.  It does not.

The obstruction is specific:

* The palette split in Lemma 5 is rigid, but it is not locally impossible.
* Gallai's tight-edge constraint only controls edges with exactly 20 conflicts.
  Many spokes and outer edges in the degree-3 ball may have 21--24 conflicts,
  so the Gallai forest alone does not force a contradiction.
* To finish the degree-3 case, one needs a recoloring or counting argument
  showing that some 20-coloring of `H - u` violates Lemma 4/Lemma 5.

A simple local witness explains why Lemma 5 alone is insufficient.  Take the
degree-3 ball with no cross edges between the arms, and attach three fresh
outside edges to each vertex of each `Wi` so that the sets `O1,O2,O3` have
nine edges each.  Color the nine spokes `B` with colors `1,...,9`, and color
each of `O1,O2,O3` bijectively with colors `10,...,18`.  Around the deleted
vertex, this realizes exactly the palette split of Lemma 5 and creates no
local strong-coloring conflict.  This toy witness is not a critical graph, but
it shows that the next argument must use either global criticality, Kempe
recoloring, or additional degree constraints outside the radius-2 ball.

The best next targets are:

1. Prove that sufficiently many spokes around a degree-3 vertex must be tight.
   Lemma 3 would then force many cross edges between the `Wi`, potentially
   violating degree limits or Lemma 2.
2. Use Kempe-chain recoloring in `H - u` to alter the color of one spoke while
   preserving the coloring, breaking the forced common two-color availability
   in Lemma 4.
3. Combine Lemma 5 with the Huang-Santana-Yu 21-color proof: their partition
   argument may provide exactly the recoloring freedom needed here.
4. If degree-3 vertices can be eliminated, restart with the 4-regular case,
   where every edge satisfies `4t + x <= 4`, every triangle edge is tight, and
   the same Gallai tight-edge constraints apply to all triangle edges.

## Summary of Partial Progress

This pass did not prove the conjecture.  It did produce two reusable reductions:

* Tight edges in a hypothetical counterexample are constrained by Gallai's
  theorem for 21-critical graphs.
* A degree-3 vertex forces every 20-coloring of `H - u` into an extremely rigid
  9-color/9-color palette split around the radius-2 ball.

The degree-3 case now has a sharper target: prove that the forced palette split
from Lemma 5 cannot persist under valid recolorings of `H - u`.
