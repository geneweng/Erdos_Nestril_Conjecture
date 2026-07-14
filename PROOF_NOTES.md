# Toward a Proof of the Erdős–Nešetřil Conjecture at Δ = 4

**Claim to prove.** Every simple graph G with Δ(G) ≤ 4 has strong chromatic index
χ′ₛ(G) ≤ 20.

**Status.** Not proved here (it has been open since 1985), and that outcome was
expected. What follows are the *partial results established in this project* —
several with complete human-readable proofs, two computer-assisted — which
together reduce the conjecture at Δ = 4 to a sharply constrained minimal case,
plus an analysis of why the remaining gap resists current techniques.

Throughout: edges e, f *conflict* if they share an endpoint or are joined by an
edge of G. For e = uv let S(e) = N[u] ∪ N[v]. The conflict graph C = L(G)² has
the edges of G as vertices, conflicts as adjacency, and χ′ₛ(G) = χ(C).

Since Huang–Santana–Yu (2018) proved χ′ₛ ≤ 21 for Δ = 4, a counterexample is
exactly a graph with χ′ₛ = 21: **the entire conjecture at Δ = 4 is one color.**

---

## 1. Reduction to a critical graph

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

## 2. Structure of a critical counterexample (proved)

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

## 4. No small counterexample (computer-assisted theorem)

**Theorem F.** The conjecture holds for every graph with Δ ≤ 4 on at most 14
vertices.

*Method.* A counterexample on ≤ 14 vertices contains a connected edge-critical
counterexample H on ≤ 14 vertices, which by Lemma B has all degrees in {3, 4}
and ≥ 21 edges. geng enumerated all such graphs for n = 11–14 — 5,705 +
284,175 + 3,323,481 + 36,801,545 = 40,414,906 graphs. Each was screened by the
edge-conflict criterion of Lemma A (a Lemma-A-violating graph cannot be
critical, and the critical subgraph itself appears elsewhere in the
enumeration), then DSATUR; any graph whose greedy strong coloring needed ≥ 21
colors would be decided exactly by SAT. None reached the SAT stage with a
21-color greedy; in fact no graph even required 20 greedy colors. ∎

So any counterexample has ≥ 15 vertices — and being nearly 4-regular
(Corollary D), at least ~30 edges, with conflict graph of ≥ 30 vertices,
chromatic number 21, clique number ≤ 20, and minimum degree ≥ 20 (Lemma A).

## 5. Why the last color is hard (assessment)

By Lemma C, Δ(C) ≤ 24. The known landscape for coloring C:

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
K₂₁-free conflict graph arising from a near-4-regular, nearly triangle-free
graph on ≥ 15 vertices satisfying Lemmas A–D. Two honest routes forward:

1. **Extend Theorem F by exhaustion** (n = 15 is ~4×10⁸ candidate graphs after
   Lemma-B pruning — days of CPU, feasible; n = 16 an order more). This can
   only ever push the bound, not close the conjecture.
2. **Sharpen the HSY analysis using Lemmas B–D**: their proof of ≤ 21 already
   does heavy local case analysis; the rigidity of degree-3 neighborhoods
   (B.3, D) and the 4t + D + x ≤ 4 budget (C) eliminate many of their
   configurations at the 20-color level. Whether the remaining cases close is
   beyond what was checked here — this is where a genuine proof attempt should
   concentrate.

## 6. Conclusion

The conjecture at Δ = 4 survived a multi-front computational attack unscathed,
and the evidence for it is now stronger in two rigorous ways: it holds exactly
in the clique relaxation (Theorem E, tight at 20), and it has no counterexample
on ≤ 14 vertices (Theorem F). Every heuristic signal — the isolation of the
C₅-blowup peak, the collapse of χ′ₛ under any local perturbation, structured
families plateauing at 13–16 — points the same way. We believe the conjecture
is true at Δ = 4, with the C₅ blowup as the unique extremal configuration, and
the gap between 20 and 21 is precisely a global chromatic/clique gap problem
that current local techniques cannot see.
