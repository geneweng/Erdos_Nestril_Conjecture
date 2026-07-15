# Toward a Proof of the Erdős–Nešetřil Conjecture at Δ = 4

> **Erratum, 2026-07-15.** The edge-critical reduction in Sections 1--2 is
> withdrawn.  A strong coloring of `H - e` is not generally a coloring of the
> fixed conflict graph `L(H)^2 - e`, because deleting `e` can remove conflicts
> among other edges.  Consequently the local critical-graph structure derived
> from edge-minimality is not proof-valid as written.  See
> [ERRATA.md](ERRATA.md) for the corrected conflict-critical framework.

**Claim to prove.** Every simple graph G with Δ(G) ≤ 4 has strong chromatic index
χ′ₛ(G) ≤ 20.

**Status.** Not proved here (it has been open since 1985). After the erratum
above, the edge-critical structural reductions in this file should be read as
archival failed proof attempts, not established lemmas. The exact computations
on explicit graphs and the strong-clique SAT theorem remain valid.

Throughout: edges e, f *conflict* if they share an endpoint or are joined by an
edge of G. For e = uv let S(e) = N[u] ∪ N[v]. The conflict graph C = L(G)² has
the edges of G as vertices, conflicts as adjacency, and χ′ₛ(G) = χ(C).

Since Huang–Santana–Yu (2018) proved χ′ₛ ≤ 21 for Δ = 4, a counterexample is
exactly a graph with χ′ₛ = 21: **the entire conjecture at Δ = 4 is one color.**

---

## 1. Withdrawn Reduction to an Edge-Critical Graph

The section below is retained for context, but the central inference is invalid
for strong coloring.  Edge-minimality of `H` does not imply vertex-criticality
of `L(H)^2`.

If any counterexample exists, take one, and repeatedly delete edges while
χ′ₛ = 21. Since strong colorings of disjoint unions are independent per
component (χ′ₛ of a union is the max over components), the result contains a
**connected, edge-critical** graph H: χ′ₛ(H) = 21 and χ′ₛ(H − e) ≤ 20 for
every edge e.

**Lemma A.** In H, every edge conflicts with at least 20 other edges.

*Proof.* Otherwise color H − e with 20 colors; e conflicts with ≤ 19 edges,
which block ≤ 19 colors, so e can be colored — contradicting χ′ₛ(H) = 21. ∎

**Counting identity.** For any vertex set S: the number of edges with at least
one endpoint in S equals Σ_{s∈S} deg(s) − e(S), where e(S) counts edges inside
S. An edge f conflicts with e iff f has an endpoint in S(e), so

  conflicts(e) = Σ_{s∈S(e)} deg(s) − e(S(e)) − 1.

## 2. Withdrawn Structure of an Edge-Critical Counterexample

The statements in this section depend on Lemma A, which depends on the invalid
edge-deletion inference above.  They are therefore withdrawn as proof claims.

Write d(v) for degrees; all ≤ 4. Let e = uv with t = |N(u) ∩ N(v)|.

**Lemma B (degrees).** In H:
1. δ(H) ≥ 3.
2. No edge joins two degree-3 vertices.
3. If d(u) = 3, d(v) = 4 and uv ∈ E(H), then: t = 0; |S(uv)| = 7; the only
   edges inside S(uv) are uv and the five other edges at u and v; and all five
   vertices of (N(u) ∪ N(v)) ∖ {u, v} have degree exactly 4.

*Proof.* (1) If d(u) = 1 with neighbor v of degree d: S(uv) has ≤ d + 1
vertices besides u; Σdeg ≤ 1 + d + 4(d−1) = 5d − 3 and e(S) ≥ d (the star at
v), so conflicts ≤ 4d − 4 ≤ 12 < 20. If d(u) = 2: |S| ≤ d + 3,
Σdeg ≤ 2 + d + 4·d = 5d + 2, e(S) ≥ d + 1 (stars at u and v), so
conflicts ≤ 4d ≤ 16 < 20. Both contradict Lemma A.

(2) d(u) = d(v) = 3: Σdeg(S) ≤ 3 + 3 + 4(4 − t) = 22 − 4t, e(S) ≥ 5, so
conflicts ≤ 16 − 4t < 20.

(3) Σdeg(S) ≤ 3 + 4 + 4(5 − t) − D = 27 − 4t − D where D ≥ 0 is the total
degree deficiency of the five outer vertices, and e(S) ≥ 6 + x with x ≥ 0 the
internal edges beyond the six star edges. Then
conflicts ≤ 27 − 4t − D − (6 + x) − 1 = 20 − 4t − D − x ≥ 20 forces
t = D = x = 0. ∎

**Lemma C (local sparsity at 4–4 edges).** If d(u) = d(v) = 4, let x be the
number of edges inside S(uv) other than uv and the six star edges, and D the
total degree deficiency of the six outer vertices. Then

  **4t + D + x ≤ 4.**

In particular every edge of H lies in at most one triangle, and an edge in a
triangle admits no other internal edge or deficiency in its neighborhood.

*Proof.* |S| = 8 − t, Σdeg(S) = 32 − 4t − D, e(S) = 7 + x, so
conflicts = 24 − 4t − D − x ≥ 20. ∎

**Corollary D (degree-3 vertices are scattered).** Distinct degree-3 vertices
of H are non-adjacent and share no common neighbor (distance ≥ 3 apart in
particular). Hence, counting each degree-3 vertex's three private degree-4
neighbors, n₄ ≥ 3 n₃.

*Proof.* Non-adjacent by B.2. If u ≠ u′ have degree 3 and share a neighbor v,
apply B.3 to uv: every vertex of (N(u) ∪ N(v)) ∖ {u, v} — which contains
u′ — has degree 4, a contradiction. ∎

Consequently H is 4-regular except for a scattered independent set of degree-3
vertices, is nearly triangle-free (Lemma C), and around every degree-3 vertex
the second neighborhood is rigidly prescribed by B.3.

**Lemma D′ (the ball around a degree-3 vertex).** Let u have degree 3 in H,
with neighbors v₁, v₂, v₃ and Wᵢ = N(vᵢ) ∖ {u}. Then:
1. N(u) is independent and N(vᵢ) ∩ N(vⱼ) = {u} for i ≠ j;
2. no triangle and no 4-cycle of H passes through u;
3. the radius-2 ball B₂(u) contains exactly 1 + 3 + 9 = 13 vertices, the sets
   Wᵢ are pairwise disjoint and each is independent, and every vertex of
   B₂(u) ∖ {u} has degree exactly 4;
4. the only edges inside B₂(u) are the 12 "tree" edges u vᵢ and vᵢ w (w ∈ Wᵢ),
   plus possibly edges between different Wᵢ, Wⱼ.

*Proof.* Apply B.3 to each edge u vᵢ: x = 0 forbids every non-star edge inside
S(u vᵢ) = {u, v₁, v₂, v₃} ∪ Wᵢ. An edge vⱼ vₖ is internal to S(u v₁), so N(u)
is independent. An edge vⱼ w with w ∈ Wᵢ is internal to S(u vᵢ), so
Wᵢ ∩ N(vⱼ) = ∅, giving N(vᵢ) ∩ N(vⱼ) = {u}; this also makes the Wᵢ pairwise
disjoint (a common vertex would be a common neighbor) and rules out any 4-cycle
u vᵢ w vⱼ u. Edges inside Wᵢ are internal to S(u vᵢ), so each Wᵢ is
independent. Degrees are 4 by B.3. Cross edges Wᵢ–Wⱼ are the only pairs not
internal to any S(u vₖ). ∎

So each degree-3 vertex forces a rigid 13-vertex, locally tree-like
configuration whose twelve outer vertices are all 4-valent — consistent with
(and explaining) the absence of small counterexamples.

**Lemma E (frozen rainbow).** Let e be an edge of H with *exactly* 20
conflicts — by B.3 every 3–4 edge qualifies. Then in **every** 20-coloring of
H − e:
1. the 20 edges conflicting with e receive 20 distinct colors, and
2. every edge f conflicting with e is itself frozen: the edges conflicting
   with f (in H − e) carry all 19 colors other than f's.

*Proof.* (1) Otherwise some color is absent from e's conflict set; give it
to e, contradicting χ′ₛ(H) = 21. (2) Otherwise recolor f with a color c′
missing from its conflict set (c′ ≠ color(f)); by (1) f's old color occurred
only on f among e's conflicts, so it is now free for e — again a 20-coloring
of H. ∎

Lemma E is the seed of a rigidity cascade: each of the 20 edges around a 3–4
edge must see all 20 colors, which by the same counting as Lemma A pins their
neighborhoods' degree sums and internal edges near their extremes, propagating
the rigidity of B.3/D′ outward. We did not complete a contradiction from this
cascade (see §5), but it is the natural entry point for a human proof that
critical counterexamples are 4-regular.

## 3. The clique barrier (computer-assisted theorem)

The cheapest conceivable counterexample would be 21 edges that pairwise
conflict — a 21-clique in C, forcing χ ≥ 21 immediately. Whether strong
cliques can exceed 1.25 Δ² is itself open in general (the best proven general
bound, ≈ 4Δ²/3, allows 21 at Δ = 4). We closed this route:

**Theorem E.** No graph with Δ ≤ 4 contains 21 pairwise-conflicting edges.
The maximum is 20, attained by the C₅ blowup. Hence ω(L(G)²) ≤ 20 = 1.25 Δ²:
the strong-clique version of the conjecture holds at Δ = 4, tightly.

*Method.* Fix a clique edge (0,1). Every clique edge has an endpoint in
S = N[0] ∪ N[1], |S| ≤ 8; every vertex incident to a clique edge or to a
joining edge is an endpoint of a clique edge; at most 20 clique edges leave S.
So up to relabeling any such configuration embeds in a host graph on 28
vertices with N(0) ⊆ {1,2,3,4}, N(1) ⊆ {0,2,…,7}. A SAT encoding (adjacency
variables + clique-selector variables, degree-≤4 cardinality constraints,
pairwise-conflict clauses, prefix symmetry breaking) is UNSAT (CaDiCaL, 16 s).
Validation: target 20 is SAT and recovers the C₅ blowup; at Δ = 3 the same
encoding gives max = 10 (SAT) and 11 (UNSAT), matching the proven Δ = 3 value;
the χ′ₛ solver itself agrees with brute-force backtracking on 60 random graphs. ∎

**Corollary.** Any counterexample H has χ(C) = 21 > 20 ≥ ω(C): its conflict
graph is a K₂₁-free 21-chromatic graph. The counterexample cannot be certified
by local edge density; it would have to be a genuinely global coloring
obstruction.

## 4. Withdrawn: No Small Counterexample Claim

**Withdrawn claim.** This section was originally presented as a proof that the
conjecture holds for every graph with Δ ≤ 4 on at most 14 vertices.  The search
data remain recorded, but the proof certification relied on the withdrawn
edge-critical pruning from Sections 1--2.

*Historical method.* Under the withdrawn edge-critical reduction, geng
enumerated connected degree-[3,4] graphs for n = 11–14 — 5,705 + 284,175 +
3,323,481 + 36,801,545 = 40,414,906 graphs. Each was screened by the withdrawn
edge-conflict criterion of Lemma A, then DSATUR; any graph whose greedy strong
coloring needed ≥ 21 colors would be decided exactly by SAT. None reached the
SAT stage with a 21-color greedy; in fact no graph in that pruned family even
required 20 greedy colors.

The conclusion that any counterexample has at least 15 vertices is withdrawn.

## 4½. Graph classes where the conjecture is proved (Δ = 4)

**Theorem G (planar graphs).** Every planar graph with Δ ≤ 4 satisfies
χ′ₛ ≤ 20.

*Proof.* By Vizing's theorem E(G) partitions into 5 matchings M₁,…,M₅. Fix a
matching M and form Hₘ: vertices are the edges of M, adjacent when some edge
of G joins them (matched edges are vertex-disjoint, so conflicts are exactly
joins). Hₘ is obtained from a contraction minor of G (contract each matched
edge, discard unmatched vertices), hence planar, hence 4-colorable by the Four
Color Theorem. A proper 4-coloring of Hₘ splits M into 4 induced matchings.
Doing this for each Mᵢ gives 5 × 4 = 20 induced matchings. ∎

This instantiates the Faudree–Gyárfás–Schelp–Tuza bound χ′ₛ ≤ 4Δ + 4 for
planar graphs, which meets the Erdős–Nešetřil bound exactly at Δ = 4.
Fittingly, the extremal graph C₅[2] is *non-planar* (verified), so no tension.
Random planar Δ ≤ 4 graphs tested here peaked at χ′ₛ = 12.

**Theorem H (chordal graphs).** Every chordal graph with Δ ≤ 4 satisfies
χ′ₛ ≤ 20.

*Proof.* For chordal G, the conflict graph L(G)² is chordal (Cameron 1989,
"Induced matchings"), hence perfect, so χ(L(G)²) = ω(L(G)²) ≤ 20 by
Theorem E. ∎ (We corroborated χ = ω on 200 random chordal Δ ≤ 4 instances,
where every generated conflict graph was itself chordal.)

Thus the independent graph-class results currently recorded here are the
planar case, the chordal case, and the clique relaxation for all graphs.  The
small-order claim is withdrawn pending an unpruned or conflict-critical
replacement.

## 5. Why the last color is hard (assessment)

For any graph with `Delta(G) <= 4`, the conflict graph `C = L(G)^2` has maximum
degree at most 24.  The known landscape for coloring C:

* Greedy/Brooks-type: χ(C) ≤ 24 — three colors short of useless; the trivial
  bound 2Δ(Δ−1)+1 = 25 is what Brooks-style arguments give at Δ = 4.
* Huang–Santana–Yu (2018): χ(C) ≤ 21, via an intricate structural analysis
  specific to Δ = 4. This is the current frontier.
* Probabilistic sparse-neighborhood arguments (Molloy–Reed 1997 and successors,
  down to 1.772 Δ², Hurley–de Joannis de Verclos–Kang 2021) need Δ large;
  at Δ = 4 they give nothing below the trivial bound.
* Bounds interpolating between ω and Δ (e.g. Reed's conjectured
  χ ≤ ⌈(Δ+1+ω)/2⌉, which is not proven in general) would give 23 here even if
  available — still short. Our Theorem E (ω ≤ 20) cannot be leveraged into
  χ ≤ 20 by any known ω-sensitive machinery.

The residual problem is exactly a "last color" question, structurally similar
to the hardest step in edge-coloring theorems: rule out a 21-chromatic,
K₂₁-free conflict graph arising as an induced subgraph of some `L(G)^2`.

After the erratum, the honest route forward is:

1. Choose a vertex-21-critical induced subgraph `C0 subset L(G)^2`.
2. Translate critical-graph constraints on `C0` back to the selected edge set
   in `G`.
3. Count selected conflict neighbors, not total conflicts in `G`.
4. Rebuild any Hall/list-extension step as an extension of a coloring of
   `C0 - X`, not as a strong coloring of `G - X`.

The HSY proof of the 21-color bound remains the natural comparison point, but
the local reductions in Sections 1--2 must first be rebuilt in this
conflict-critical language.

## 6. Conclusion

The conjecture at Δ = 4 survived the computational searches performed here,
but after the erratum only the clique relaxation is a rigorous theorem recorded
in this file.  The heuristic signals remain favorable: the isolation of the
C₅-blowup peak, the collapse of χ′ₛ under local perturbation, and structured
families plateauing below 20.  The proof gap is still a global chromatic/clique
gap problem, but future arguments must use conflict-critical induced subgraphs
rather than edge-critical deletions in the original graph.
