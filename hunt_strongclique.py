"""SAT search: does a graph with Delta<=4 contain 21 edges that pairwise
conflict (share an endpoint or are joined by an edge)?

Such a "strong clique" of size 21 would force chi'_s >= 21 > 20 = 1.25*16,
disproving Erdos-Nesetril at Delta=4.

Model: we search for a graph G on n vertices, ALL of whose edges pairwise
conflict, with >= 21 edges and Delta(G) <= 4.  (If a host graph has a
21-edge strong clique, the subgraph formed by those 21 edges is itself such
a graph: pairwise conflicts may use joining edges, but a joining edge
between two clique edges has both endpoints covered... NOTE: a joining edge
need not itself belong to the clique.  So we search for a graph G with an
edge subset K, |K| >= 21, pairwise conflicting IN G; other edges of G may
serve as joiners but also contribute to degrees.  Since removing non-clique
edges only removes joiners, we must keep them; hence: variables for the
host graph's adjacency AND a selector per potential edge.)

WLOG (up to isomorphism), for the base clique edge (0,1):
  - N(0) subset {1,2,3,4};  N(1) subset {0,2,...,7}
  - every clique edge touches S subset {0..7}; vertices >= 8 have neighbors
    only in S (an edge between two vertices >= 8 could never be selected,
    and as a joiner it would be useless: it joins edges via its endpoints'
    adjacencies... a joining edge must connect endpoints OF clique edges,
    and all clique-edge endpoints are in S or adjacent to S).  We cap n=18:
    outside vertices need >= 2 selected edges each and <= 20 selected edges
    leave S... (see analysis in report).
"""

import sys
import itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical195

N = int(sys.argv[1]) if len(sys.argv) > 1 else 18

pool = IDPool()
pairs = list(itertools.combinations(range(N), 2))


def E(a, b):  # host graph adjacency
    return pool.id(("e", min(a, b), max(a, b)))


def K(a, b):  # edge selected into the strong clique
    return pool.id(("k", min(a, b), max(a, b)))


cnf = []

# selected => present
for a, b in pairs:
    cnf.append([-K(a, b), E(a, b)])

# base clique edge (0,1)
cnf.append([K(0, 1)])

# WLOG: N(0) subset {1,2,3,4}, N(1) subset {0,2..7}
for j in range(5, N):
    cnf.append([-E(0, j)])
for j in range(8, N):
    cnf.append([-E(1, j)])
# WLOG prefix form: N(0)\{1} is a prefix of {2,3,4}; fresh neighbors of 1
# (those not shared with 0) take a prefix of {5,6,7}.
cnf.append([-E(0, 4), E(0, 3)])
cnf.append([-E(0, 3), E(0, 2)])
cnf.append([-E(1, 7), E(1, 6)])
cnf.append([-E(1, 6), E(1, 5)])

# Every selected edge must conflict with (0,1): touch S = N[0] u N[1].
# vertex v in S iff v in {0,1} or E(0,v) or E(1,v); S subset {0..7}.
# So a selected edge {a,b} with a,b >= 2 needs a or b in N(0) u N(1):
for a, b in pairs:
    if a >= 2:
        clause = [-K(a, b)]
        for x in (a, b):
            if x <= 4:
                clause.append(E(0, x))
            if x <= 7:
                clause.append(E(1, x))
        cnf.append(clause)

# vertices >= 8: only adjacent to 2..7 (edges among >=8 are useless: they
# cannot be selected -- their endpoints are non-adjacent to 0 and 1 -- and
# as joiners they join edges whose endpoints they are adjacent to; but a
# joiner between selected edges e,f only matters via adjacency E(x,y) with
# x in e, y in f, and all selected-edge endpoints lie in {0..7} or are
# adjacent to S... endpoints of selected edges CAN be >= 8 (edge from S to
# outside).  A joiner between two outside endpoints x,y >= 8 WOULD matter.
# So we must NOT forbid those edges.  Only forbid nothing; rely on degree
# constraints.  (Kept: E(0,j)=E(1,j)=0 above, which is genuine WLOG.)

# pairwise conflict for selected edges: for disjoint pairs (a,b),(c,d):
# K(a,b) & K(c,d) -> some host edge joins them (or shares endpoint - not
# disjoint here): E(a,c) | E(a,d) | E(b,c) | E(b,d)
for (a, b), (c, d) in itertools.combinations(pairs, 2):
    if len({a, b, c, d}) == 4:
        cnf.append([-K(a, b), -K(c, d), E(a, c), E(a, d), E(b, c), E(b, d)])

# degree <= 4 in host graph
for v in range(N):
    lits = [E(v, u) for u in range(N) if u != v]
    cnf.extend(CardEnc.atmost(lits=lits, bound=4, vpool=pool,
                              encoding=EncType.seqcounter).clauses)

# at least 21 selected edges
klits = [K(a, b) for a, b in pairs]
cnf.extend(CardEnc.atleast(lits=klits, bound=int(sys.argv[2]) if len(sys.argv) > 2 else 21, vpool=pool,
                           encoding=EncType.seqcounter).clauses)

print(f"n={N}: {pool.top} vars, {len(cnf)} clauses; solving...", flush=True)
with Cadical195(bootstrap_with=cnf) as s:
    if s.solve():
        model = set(l for l in s.get_model() if l > 0)
        edges = [(a, b) for a, b in pairs if E(a, b) in model]
        sel = [(a, b) for a, b in pairs if K(a, b) in model]
        print("SAT!  host edges:", edges)
        print("strong clique:", sel)
    else:
        print(f"UNSAT: no Delta<=4 graph on {N} vertices has a 21-edge strong clique (under WLOG constraints)")
