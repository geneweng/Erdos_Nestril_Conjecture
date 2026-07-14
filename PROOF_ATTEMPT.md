# Proof Attempt: Delta = 4 Erdős-Nešetřil

Date: 2026-07-14

Goal: prove that every simple graph with maximum degree at most 4 has strong
chromatic index at most 20.

Status: no complete proof yet.  The main progress here is that a connected
edge-critical counterexample is reduced to the 4-regular triangle-free case:
degree-3 vertices are eliminated using the local Hall/recoloring obstruction
plus a finite cross-edge check, and triangles are eliminated by a palette
argument.  The main tools below are:

1. a Gallai-forest constraint on the edges with exactly 20 conflicts, and
2. a Hall-extension obstruction obtained by deleting a degree-3 vertex,
3. a one-edge recoloring saturation lemma for the radius-2 ball, and
4. a dependency-free finite check ruling out cross edges between the three
   arms around a degree-3 vertex, and
5. a triangle-deletion palette contradiction in the 4-regular case.

These are intended to extend the reductions already recorded in
`PROOF_NOTES.md`.

## Plan

1. Work in a minimal counterexample `H`.
2. Translate to the conflict graph `C = L(H)^2`.
3. Use standard critical-graph structure on the degree-20 vertices of `C`.
4. Try to eliminate degree-3 vertices of `H`.
5. If that succeeds, attack the remaining 4-regular case.

The pass below completes Steps 1--4 and reduces the remaining problem to the
4-regular triangle-free case.

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

## Step 5: Executing the Next Targets

This section continues the plan above.  The two targets were:

1. prove that sufficiently many spokes around a degree-3 vertex must be tight;
2. use recoloring in `H - u` to break the forced two-color availability.

The first target does not work as hoped, but it gives useful negative
structure.  The second target gives a stronger saturation condition on the
edges in the local palette split.

### Exact Spoke Count

Let `s = vi w` be a spoke, with `w in Wi`.  Then `s` is a 4--4 edge and has no
common neighbor:

```text
N(vi) = {u} union Wi,
N(w) cap ({u} union Wi \ {w}) = empty.
```

So in the 4--4 budget for `s` we have `t = 0`.  The six outer vertices of
`S(s)` include the degree-3 vertex `u`, the two other vertices of `Wi`, and the
three neighbors of `w` other than `vi`.  Hence the outer degree deficiency
`D_s` is at least 1, coming from `u`.  If `x_s` denotes the number of extra
internal edges in `S(s)` beyond the star edges, then

```text
conflicts(s) = 24 - D_s - x_s,
1 <= D_s + x_s <= 4.
```

Consequently:

```text
s is tight  <=>  D_s + x_s = 4.
```

Thus the local degree budget alone does not force spokes to be tight.  In the
locally tree-like case where the other neighbors of `w` have degree 4 and no
extra internal edges occur in `S(s)`, the spoke has 23 conflicts, not 20.

### Cross Edges Are Very Sparse

Lemma 2 said that every cross edge between different `Wi` arms is non-tight.
For a cross edge `c = w_i w_j`, the 4--4 count gives

```text
conflicts(c) = 24 - 4t_c - D_c - x_c.
```

Since `c` is non-tight but every edge of `H` has at least 20 conflicts,
`conflicts(c) >= 21`, so:

```text
4t_c + D_c + x_c <= 3.
```

In particular:

**Lemma 6.** Every cross edge between two different arms has `t_c = 0` and
`D_c = 0`.  It lies in no triangle, and every outer vertex in its `S(c)` has
degree 4.

### Tight Spokes Are Scarce

Combining Lemma 3 with Lemma 6 gives a useful limitation.

**Lemma 7.** Around a degree-3 vertex, tight spokes can occur in at most two
arms.  Moreover, if two arms contain `r` and `s` tight spokes respectively,
then `(r - 1)(s - 1) <= 3`; in particular two arms cannot both have all three
spokes tight.

Proof.  If there is a tight spoke in each of the three arms, Lemma 3 forces
the three corresponding outer endpoints to be pairwise adjacent.  These three
outer endpoints form a triangle of cross edges, contradicting Lemma 6 because
cross edges have no common neighbor.

Now suppose tight spokes occur in exactly two arms.  Let `A` and `B` be the
sets of their outer endpoints, with `|A| = r` and `|B| = s`.  Lemma 3 forces
all edges of the complete bipartite graph `A--B` to be present.  For any
particular cross edge `ab` with `a in A`, `b in B`, all edges between
`A \ {a}` and `B \ {b}` are extra internal edges in `S(ab)`.  Lemma 6 gives
`x_ab <= 3`, hence `(r - 1)(s - 1) <= 3`.

So at most five of the nine spokes around a degree-3 vertex can be tight.

This rules out the first target as stated: the current local theory does not
force many tight spokes.  It forces the opposite, namely that at least four
spokes are non-tight.

### One-Edge Recoloring Saturation

Return to a 20-coloring `phi` of `H - u` and use the notation from Lemma 5:

```text
P = colors on the nine spokes B,       |P| = 9,
Q = colors on each Oi,                 |Q| = 9,
R = {alpha, beta} = colors missing from every Xi.
```

Thus `P`, `Q`, and `R` partition the 20 colors, and no edge in the local set

```text
L = B union O1 union O2 union O3
```

has a color from `R`.

Let `f` be an edge in `O = O1 union O2 union O3`, and let `q = phi(f) in Q`.
Let `I(f)` be the set of arms `i` for which `f in Oi`.  Since an edge has only
two endpoints, `I(f)` has size 1 or 2.

**Lemma 8.** In every 20-coloring of `H - u`, every edge `f in O` sees every
color in `P union R`.

Proof.  Suppose some color `c in P union R` is absent from the colored conflict
neighborhood of `f`.  Recolor `f` from `q` to `c`; this remains a valid
20-coloring of `H - u`.

If `c in R`, then for every `i in I(f)`, the edge `ei` loses availability of
`c` but gains availability of `q`; every `i notin I(f)` still has the two
available colors `R`.  If `c in P`, then `c` was already blocked for every
`ei` by the spoke using color `c`, while every `i in I(f)` gains availability
of `q`.  In both cases the three missing edges `e1,e2,e3` have lists whose
union has size at least 3 and which satisfy Hall's condition:

```text
i in I(f):      available colors include q and at least one color of R,
i notin I(f):  available colors are R.
```

Since `1 <= |I(f)| <= 2`, we can color one edge with `q` and the remaining
two with the two colors of `R`, or use the analogous choice when `c in R`.
This extends the coloring to `H`, a contradiction.  Therefore every
`c in P union R` must already appear on a conflict of `f`.

This is the clean Kempe-free version of the recoloring obstruction: every
outer edge in the degree-3 ball is saturated by all 11 colors outside `Q`.

Some of these blockers are local.  An edge of `Oi` always conflicts with the
three spokes in arm `i`; a cross edge in `Oi cap Oj` conflicts with the six
spokes in arms `i` and `j`.  Additional spoke blockers can occur through other
allowed joins involving the non-`Wi` endpoint.  The rigorous conclusion is:
for every color in `P` not represented among the local spoke conflicts of `f`,
and for both colors in `R`, Lemma 8 requires a blocker outside the local set
`L`.

This is strong, but still not a contradiction.  The next unresolved step is an
external-blocker counting argument: show that the bounded-degree graph outside
the radius-2 ball cannot supply these blockers for all edges in
`O1 union O2 union O3` while preserving the critical local counts.

## Step 6: Eliminating Degree-3 Vertices

The external-blocker problem above has a useful first resolution: cross edges
between arms cannot exist at all.

### A Stronger One-Edge Recoloring Lemma

Lemma 8 can be strengthened from `P union R` to all colors other than the color
of `f`.

**Lemma 9.** In every 20-coloring of `H - u`, every edge
`f in O1 union O2 union O3` sees all 19 colors other than its own.

Proof.  Lemma 8 handles colors in `P union R`.  Let `q = phi(f) in Q`, and let
`c in Q \ {q}` be absent from the conflict neighborhood of `f`.  Recolor `f`
from `q` to `c`.  This is still a valid 20-coloring of `H - u`.

For every arm `i` with `f in Oi`, the color `q` is now available for the
missing edge `ei`.  The color `c` was not available for `ei` before the
recoloring anyway, because `Oi` is rainbow and contains a different edge of
color `c`.  Arms not containing `f` still have the two available colors
`R = {alpha,beta}`.  Thus the three missing edges have lists whose union
contains `R union {q}`, and Hall's condition holds.  The coloring extends to
`H`, a contradiction.

So every color in `Q \ {q}` also appears in the conflict neighborhood of `f`.

### No Cross Edges

Consider the cross-edge graph `X` on `W1 union W2 union W3`, with parts
`W1,W2,W3` and edges exactly the edges of `H` joining different arms.

From Lemma 6, `X` is triangle-free and every vertex has cross-degree at most
3.  Also, if `ab` is a cross edge between `Wi` and `Wj`, and `Wk` is the third
arm, then Lemma 9 forces `ab` to see the three spoke colors in `Bk`.  The only
way `ab` can conflict with the spoke `vk z`, `z in Wk`, is for `a z` or `b z`
to be a cross edge.  Therefore:

```text
for every cross edge ab between two arms,
N_X(a) union N_X(b) contains all three vertices of the third arm.
```

Together with triangle-freeness, this means the endpoints of each cross edge
cover the third arm without overlap.

The remaining statement is a 9-vertex finite lemma:

**Lemma 10.** The only tripartite graph with three parts of size 3 satisfying
the cross-degree bound, triangle-freeness, and the third-arm coverage rule
above is the empty graph.

This is verified by `check_degree3_cross_edges.py`.  The check is by closure:
if a nonempty valid cross-edge graph existed, start from any one of its edges.
The third-arm coverage rule forces at least one of two possible new edges for
each uncovered third-arm vertex.  Recursing over those forced choices, while
rejecting degree overflow and triangles, would find a nonempty closed valid
subgraph.  The script finds none.

Thus:

**Corollary 11.** There are no cross edges between different arms around a
degree-3 vertex.

### Final Contradiction for a Degree-3 Vertex

Let `f = w x` be any edge of `O_i`, with `w in Wi`.  By Corollary 11, `x` is
not in any other arm and no edge joins `w` to another arm.  Lemma 9 says that
`f` must see all nine spoke colors in `P`.

The three spoke colors in `Bi` are seen locally: `f` conflicts with all three
spokes at `vi`.  Now take a spoke `vj z` in another arm, with `j != i` and
`z in Wj`.  The edge `f = wx` can conflict with `vj z` only if one of the
following edges exists:

```text
w vj,  w z,  x vj,  x z.
```

The first is forbidden by the degree-3 ball structure.  The second is a cross
edge, forbidden by Corollary 11.  The third would put `x` in `Wj`, making
`wx` a cross edge, again forbidden.  Hence the only possible join is `x z`.

Therefore, to see the six spoke colors in the two arms other than `i`, the
single vertex `x` must be adjacent to all six corresponding vertices of
`Wj union Wk`.  But `x` is already adjacent to `w` and `Delta(H) <= 4`, so this
is impossible.

**Theorem 12.** A connected edge-critical counterexample has no degree-3
vertex.  Therefore every connected edge-critical counterexample at `Delta = 4`
is 4-regular.

This completes the first major target identified in `PROOF_NOTES.md`: the
degree-3 case is eliminated.  The remaining hypothetical counterexample is
4-regular, edge-critical, has conflict graph chromatic number 21 and clique
number at most 20, and every edge satisfies the local budget `4t + x <= 4`.

## Step 7: Eliminating Triangles in the 4-Regular Case

Now assume `H` is a 4-regular connected edge-critical counterexample.

For any edge `uv`, the 4-regular count is:

```text
conflicts(uv) = 24 - 4t - x,
```

where `t = |N(u) cap N(v)|` and `x` is the number of extra internal edges in
`S(uv)` beyond the seven star edges.  Since every edge has at least 20
conflicts, `4t + x <= 4`.  In particular, every edge lies in at most one
triangle.  If an edge lies in a triangle, then `t = 1` and `x = 0`, so that
edge is tight.

We prove that no triangle can occur.

Let `abc` be a triangle.  Since every triangle edge is tight, each of
`ab,bc,ca` has exactly 20 conflicts.  Write:

```text
A = N(a) \ {b,c},    B = N(b) \ {a,c},    C = N(c) \ {a,b}.
```

Each of `A,B,C` has size 2.  The condition `x = 0` for the three triangle
edges implies:

* each of `A,B,C` is independent;
* there are no edges between any two of `A,B,C`;
* vertices in `A` are not adjacent to `b` or `c`, vertices in `B` are not
  adjacent to `a` or `c`, and vertices in `C` are not adjacent to `a` or `b`.

Let:

```text
L   = the six edges from {a,b,c} to A union B union C,
O_A = the six edges incident with A other than the two edges from a,
O_B = the six edges incident with B other than the two edges from b,
O_C = the six edges incident with C other than the two edges from c.
```

### Hall Obstruction for the Deleted Triangle

Delete the three triangle edges.  This graph is 20-strong-colorable, by
edge-criticality and restriction from a coloring of `H - ab`.  In any such
20-coloring, let `A_ab,A_bc,A_ca` be the available color sets for the missing
edges `ab,bc,ca`.

Each missing triangle edge has exactly 18 colored conflicts, because it had
20 conflicts in `H` and the other two triangle edges have been deleted.  Hence
each available set has size at least 2.  The three missing edges pairwise
conflict, so if the coloring did not extend to `H`, Hall's theorem forces:

```text
A_ab = A_bc = A_ca = R,
```

where `R` is a common 2-color set.

For the missing edge `ab`, the 18 colored conflicts are exactly:

```text
L union O_A union O_B.
```

Similarly the conflict sets for `ac` and `bc` are:

```text
L union O_A union O_C,
L union O_B union O_C.
```

Since each missing edge has exactly the same two missing colors `R`, each of
these three 18-edge sets must use the same 18 colors, namely all colors outside
`R`, with no repetition.

Let `P` be the six colors used on `L`, and let

```text
S_A = colors on O_A,
S_B = colors on O_B,
S_C = colors on O_C.
```

Then each `S_*` has size 6, and the common complement of `P union R` is a
12-color set `Q`.  The three displayed conflict sets force:

```text
S_A union S_B = Q,
S_A union S_C = Q,
S_B union S_C = Q,
```

and in each union the two sets are disjoint, because the corresponding
18-edge conflict set is rainbow.

The first two equations give `S_B = Q \ S_A = S_C`.  But the third equation
requires `S_B` and `S_C` to be disjoint 6-sets.  This is impossible.

Therefore a 4-regular connected edge-critical counterexample is triangle-free.

**Theorem 13.** Every connected edge-critical counterexample at `Delta = 4`,
if one exists, is 4-regular and triangle-free.

In the remaining case every edge has `t = 0`, so for each edge:

```text
conflicts(e) = 24 - x(e),        0 <= x(e) <= 4.
```

An edge is tight exactly when `x(e) = 4`.  The next target is to use the same
delete-and-extend method on a non-triangular edge, where the obstruction is no
longer a 3-edge clique but a single missing edge whose 20 available blockers
must saturate the local budget.

## Step 8: The Remaining 4-Regular Triangle-Free Obstruction

This step records the exact shape of the remaining problem after Theorem 13.
It does not close the conjecture, but it identifies the next local targets
without hiding the obstruction.

Let `uv` be an edge in the remaining graph.  Write:

```text
A = N(u) \ {v},       B = N(v) \ {u}.
```

Since the graph is triangle-free, `A` and `B` are independent 3-sets.  The
extra internal edges in `S(uv)` are exactly the edges between `A` and `B`.
Thus:

```text
x(uv) = e(A,B) = the number of 4-cycles containing uv,
conflicts(uv) = 24 - x(uv),
0 <= x(uv) <= 4.
```

So a tight edge is exactly an edge in four 4-cycles.

### Single-Edge Deletion

In every 20-coloring of `H - uv`, the conflict neighborhood of `uv` must use
all 20 colors; otherwise the coloring extends to `uv`.  Since this
neighborhood has `24 - x(uv)` edges, the number of surplus color occurrences
is:

```text
(24 - x(uv)) - 20 = 4 - x(uv).
```

Consequently:

* if `x(uv) = 4`, the 20 conflicting edges are rainbow, recovering the frozen
  tight-edge lemma;
* if `x(uv) = 3`, exactly one color is repeated among the 21 conflicts;
* if `x(uv) = 0`, four repetitions are possible among the 24 conflicts.

This explains why non-tight edges are harder than the deleted degree-3 star or
triangle cases: the local color obstruction has room for repetitions.

### Deleting a Star or a 4-Cycle

Two natural four-edge deletions remain:

1. the four edges incident with a vertex, and
2. the four edges of a 4-cycle.

In either case the deleted edges form a `K4` in the conflict graph.  Let the
deleted set be `F`, and let `x_e = x(e)` for `e in F`.  In any 20-coloring of
`H - F`, the available color list `L_e` for a missing edge `e` has size at
least:

```text
|L_e| >= max(0, x_e - 1).
```

Reason: `e` has `24 - x_e` conflicts in `H`, and the other three edges of
`F` all conflict with `e` and have been deleted, leaving at most
`21 - x_e` colored conflicts.

If the four lists `{L_e : e in F}` have a system of distinct representatives,
then the coloring extends over the deleted `K4`.  Therefore, in a critical
counterexample, every 20-coloring of `H - F` must make these four lists fail
Hall's condition.

The most rigid special case is when all four deleted edges are tight
(`x_e = 4`).  Then all four lists have size at least 3.  Four lists of size at
least 3 can fail Hall only in one way:

```text
L_e = R for all e in F,
```

for a common 3-color set `R`.  Equivalently, for every tight-star or tight-4-
cycle deletion, the 17 colored conflicts of each deleted edge must be rainbow
and must use the same 17 colors.

This is the next sharp target.  A contradiction here would either eliminate
vertices incident only with tight edges or eliminate 4-cycles whose four edges
are tight.  The present local analysis does not yet force such a configuration:
graphs like the C5 blowup have `x(e) = 1` on every edge, showing that the
remaining case may avoid tight edges entirely.

## Step 9: Reduced Local Enumeration

To test whether the tight-star/tight-4-cycle target is forced by the remaining
local assumptions, I added `check_regular_trianglefree_profiles.py`.  It uses
`geng` to enumerate connected 4-regular triangle-free graphs, parses graph6
directly, and computes the profile of `x(e)` values.  It also checks two
critical-graph constraints on the associated conflict graph:

1. the Kostochka-Yancey lower bound on the edge density of a 21-critical
   graph, and
2. Gallai's theorem applied to the subgraph induced by tight edges.

The script filters only by the necessary local criticality condition

```text
x(e) <= 4 for every edge e.
```

It does not test colorability.  The point is narrower: determine whether the
remaining local structure already forces a tight star or tight 4-cycle.  It
does not.

Run:

```sh
python3 check_regular_trianglefree_profiles.py 10 12 14 16
```

Output from this pass:

```text
n=10: generated=2, x<=4 survivors=0
  KY-compatible survivors: 0
  tight-edge Gallai-compatible survivors: 0
n=12: generated=12, x<=4 survivors=4
  KY-compatible survivors: 4
  tight-edge Gallai-compatible survivors: 1
  survivors with tight star: 0
  survivors with tight 4-cycle: 2
  survivors with tight star or tight 4-cycle: 2
n=14: generated=220, x<=4 survivors=160
  KY-compatible survivors: 160
  tight-edge Gallai-compatible survivors: 112
  survivors with tight star: 9
  survivors with tight 4-cycle: 25
  survivors with tight star or tight 4-cycle: 26
n=16: generated=16828, x<=4 survivors=14784
  KY-compatible survivors: 14784
  tight-edge Gallai-compatible survivors: 14102
  survivors with tight star: 258
  survivors with tight 4-cycle: 1389
  survivors with tight star or tight 4-cycle: 1411
n=17: generated=193900, x<=4 survivors=177228
  KY-compatible survivors: 177228
  tight-edge Gallai-compatible survivors: 173742
  survivors with tight star: 1983
  survivors with tight 4-cycle: 12675
  survivors with tight star or tight 4-cycle: 12877
```

The Kostochka-Yancey density bound does not remove any of these locally
surviving small graphs.  Gallai's tight-edge condition does remove some:
3 of 4 survivors at order 12, 48 of 160 at order 14, and 682 of 14,784 at
order 16, and 3,486 of 177,228 at order 17.  However, many Gallai-compatible
survivors remain, and most locally surviving small graphs still have neither a
tight star nor a tight 4-cycle.  At order 17, only 12,877 of 177,228 local
survivors have either one.  The tight-`K4` list-extension obstruction from
Step 8 is useful when such a configuration exists, but it is not forced by the
current reductions.

This pushes the next target toward non-tight deletions.  For a deleted star or
4-cycle with edge values `x_1,...,x_4`, the available lists have lower bounds
`x_i - 1`; since many survivors have `x <= 3` on every edge, a proof must use
more than Hall's theorem from list sizes alone.  It must exploit the precise
overlap pattern of the colored conflict neighborhoods.

## Step 10: Reduced Exhaustion for 15 Through 17 Vertices

The structural reductions also make the next small-order exhaustive checks
much cheaper.

The original exhaustive theorem covered all graphs on at most 14 vertices.
After Theorems 12 and 13, a connected edge-critical counterexample on more
vertices must be:

```text
4-regular,
triangle-free,
x(e) <= 4 for every edge.
```

I added `check_reduced_small_orders.py`, which enumerates exactly this reduced
family using `geng`, then greedily colors the strong conflict graph.  A greedy
coloring with at most 20 colors is a constructive certificate that the graph is
not a counterexample.

Run for the first two orders beyond the original exhaustive theorem:

```sh
python3 check_reduced_small_orders.py
```

Output:

```text
n=15: generated=1606, x<=4 survivors=1340, max greedy strong colors=17
  histogram: 10:3 11:59 12:246 13:420 14:365 15:174 16:61 17:12
n=16: generated=16828, x<=4 survivors=14784, max greedy strong colors=18
  histogram: 8:1 9:1 10:27 11:410 12:2919 13:5547 14:4060 15:1456 16:321 17:39 18:3
```

The script now streams `geng` output and accepts a progress interval.  This
allowed the next order to be checked without buffering all generated graphs:

```sh
python3 check_reduced_small_orders.py --progress 50000 17
```

Final output:

```text
n=17: generated=193900, x<=4 survivors=177228, max greedy strong colors=18
  histogram: 9:4 10:159 11:4418 12:32311 13:69157 14:51870 15:16647 16:2477 17:180 18:5
```

I also reran order 17 with the additional critical-graph filters enabled:

```sh
python3 check_reduced_small_orders.py --critical-filters --progress 50000 17
```

Final output:

```text
n=17: generated=193900, x<=4 survivors=177228, max greedy strong colors=18
  KY-compatible survivors: 177228
  tight-edge Gallai-compatible survivors: 173742
  colored after critical filters: 173742
  histogram: 9:4 10:159 11:4409 12:32024 13:68057 14:50577 15:16005 16:2339 17:164 18:4
```

Thus the current critical-graph filters do not eliminate all of the worst
greedy examples at order 17: four Gallai-compatible survivors still use
18 colors under deterministic DSATUR.

Therefore, conditional only on the reductions proved above, there is no
counterexample on 15, 16, or 17 vertices.  Combined with the original exhaustive
search through 14 vertices, the current proof/computation package rules out
counterexamples on at most 17 vertices.

This is still not a general proof.  It does, however, give a much smaller
search target for future computation: start directly from connected
4-regular triangle-free graphs with `x(e) <= 4`, rather than all degree-[3,4]
graphs.

## Step 11: Exact Check of the Hardest Order-17 Greedy Cases

The order-17 reduced sweep above used deterministic DSATUR as a constructive
upper bound.  To check whether the largest greedy values reflect genuine
chromatic difficulty, I added `analyze_reduced_extremes.py`.  It extracts
high-greedy survivors and, for those selected graphs only, runs a dependency-
free exact coloring check on the strong conflict graph.

Run:

```sh
python3 analyze_reduced_extremes.py 17 --critical-filters --threshold 18 --exact --node-budget 500000 --progress 50000
```

The scan finds exactly the four Gallai-compatible order-17 survivors whose
deterministic greedy strong coloring uses 18 colors.  The initial bounded
exact check gives:

```text
case 1: clique=12 exact=13
case 2: clique=12 exact=12..15
case 3: clique=10 exact=13
case 4: clique=11 exact=12
```

Rerunning case 2 directly with a larger budget,

```sh
python3 analyze_reduced_extremes.py --graph6 'P??CAA_SFOJCCwL_T_?Y_@s?' --exact --node-budget 5000000
```

settles it exactly:

```text
clique=12 exact=12
```

Thus none of the four order-17 critical-filtered greedy-18 graphs is close to
being a 21-chromatic conflict graph: their exact conflict chromatic numbers are
`13, 12, 13, 12`.

I then exact-checked the full critical-filtered order-17 layer with greedy
value at least 17:

```sh
python3 analyze_reduced_extremes.py 17 --critical-filters --threshold 17 --exact --summary-only --node-budget 500000 --progress 50000
```

This selects 168 graphs: 164 with greedy value 17 and the four with greedy
value 18.  With the 500,000-node budget, 148 cases settle exactly:

```text
exact histogram: 11:9 11..13:4 11..14:1 11..15:1 12:130 12..13:3 12..14:5 12..15:5 13:9 13..16:1
```

Rerunning only the 20 unresolved graph6 strings with a 5,000,000-node budget
settles 16 more:

```text
exact histogram: 11..13:1 12:8 12..14:2 13:8 13..16:1
```

Thus, among the 168 high-greedy critical-filtered order-17 survivors:

```text
exact 11: 9
exact 12: 138
exact 13: 17
unresolved but <= 13: 1
unresolved but <= 14: 2
unresolved but <= 16: 1
```

In particular every high-greedy order-17 survivor has a certified 16-color
strong coloring, and all fully settled cases have exact value at most 13.

I also added a structural summary mode:

```sh
python3 analyze_reduced_extremes.py 17 --critical-filters --threshold 17 --structure --summary-only --progress 50000
```

For the same 168 selected graphs it reports:

```text
clique histogram: 10:22 11:62 12:83 13:1
alpha histogram: 3:105 4:63
ceil(n/alpha) histogram: 9:63 12:105
degree range histogram: 20..23:26 20..24:122 21..23:4 21..24:14 22..22:1 22..23:1
```

Here `alpha` is the maximum independent-set size in the conflict graph,
equivalently the largest induced matching in the original graph.  Since the
order-17 graphs have 34 edges, the 105 cases with `alpha = 3` already have the
basic lower bound `ceil(34/3) = 12`, matching the most common exact value.
The selected conflict graphs remain dense, with minimum conflict degree at
least 20, but their clique numbers are at most 13 and their exact chromatic
numbers are far below the 21-critical threshold.

Finally, I used the analyzer's witness mode on the four order-17 graphs whose
deterministic greedy coloring used 18 colors:

```sh
python3 analyze_reduced_extremes.py --exact --witness --node-budget 5000000 \
  --graph6 'P???E?oIPg@wdCPgGTDo?q_?' \
  --graph6 'P??CAA_SFOJCCwL_T_?Y_@s?' \
  --graph6 'P??CAA_sBOU_JOU_@Y?l?@Y?' \
  --graph6 'P??CE@_E@Goe?yEoFOAw?x??'
```

The exact color class-size histograms are:

```text
exact 13: size=2:6 size=3:6 size=4:1
exact 12: size=2:2 size=3:10
exact 13: size=2:5 size=3:8
exact 12: size=2:2 size=3:10
```

Thus the two exact-12 examples are explained by decompositions into ten
3-edge induced matchings and two 2-edge induced matchings.  The exact-13
examples are also dominated by 3-edge induced matchings.  This points the next
proof attempt toward finding large induced matchings or color-class trades in
the remaining triangle-free regular case, rather than toward clique/tight-edge
obstructions.

With `--witness-details`, the analyzer prints the actual original edges in
each induced matching, annotated by their `x(e)` values.  The detailed
witnesses show that these color classes are not simply "all tight" or "all
non-tight" classes.  They freely mix edge types.  One greedy-18 example has
`x(e) = 2` on all 34 edges and exact value 13; its witness consists of eight
3-edge induced matchings and five 2-edge induced matchings, all necessarily
using only `x=2` edges.  The exact-12 examples mix `x=0,1,2,3,4` edges across
their 3-edge classes.

So the useful phenomenon is not a special tight-edge decomposition.  It is the
existence of many medium-size induced matchings even inside dense conflict
graphs with minimum degree at least 20.

To test whether this phenomenon can be made algorithmic, I added a packing
mode that repeatedly removes a maximum independent set of the conflict graph,
equivalently a maximum induced matching of the original graph:

```sh
python3 analyze_reduced_extremes.py 17 --critical-filters --threshold 17 --pack --summary-only --progress 50000
```

For the same 168 high-greedy order-17 cases, this simple induced-matching
packing gives:

```text
pack histogram: 12:19 13:76 14:65 15:8
```

Thus all high-greedy order-17 survivors are colored with at most 15 colors by
a direct maximum-induced-matching packing heuristic, without exact coloring
backtracking.  This is weaker than the best exact values, but it is a more
structural certificate: repeatedly finding large induced matchings already
overcomes the deterministic DSATUR artifacts.

This is still not a structural proof, but it shows that the current worst
greedy examples are very far from 21-chromatic conflict graphs.  The next
computational target is to extract a common recoloring or induced-matching
mechanism explaining why these high-greedy survivors collapse so far below 20.
