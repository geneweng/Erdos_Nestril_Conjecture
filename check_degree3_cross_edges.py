"""Finite check for the degree-3 proof attempt.

In the notation of PROOF_ATTEMPT.md, look only at possible cross edges between
the three sets W1, W2, W3, each of size 3.

The local lemmas imply that any such cross-edge graph X must satisfy:

1. X is tripartite with parts of size 3.
2. every vertex has cross-degree at most 3;
3. X is triangle-free;
4. for every edge ab between two parts, the endpoints a and b together are
   adjacent to all three vertices of the third part.

This script verifies that the only graph satisfying these rules is the empty
graph.  The search is by closure rather than by all 2^27 tripartite graphs:
if a nonempty valid graph existed, starting from any one of its edges and
following the forced choices in rule 4 would produce a nonempty closed valid
subgraph, which this search would find.
"""

PARTS = [tuple(range(0, 3)), tuple(range(3, 6)), tuple(range(6, 9))]
ALL_EDGES = tuple(
    tuple(sorted((a, b)))
    for i in range(3)
    for j in range(i + 1, 3)
    for a in PARTS[i]
    for b in PARTS[j]
)


def part(v):
    return v // 3


def adjacency(edges):
    adj = [set() for _ in range(9)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def add_edge(edges, a, b):
    if a == b or part(a) == part(b):
        return None
    new_edges = set(edges)
    new_edges.add(tuple(sorted((a, b))))
    adj = adjacency(new_edges)
    if any(len(adj[v]) > 3 for v in range(9)):
        return None
    for a0 in PARTS[0]:
        for b0 in PARTS[1]:
            for c0 in PARTS[2]:
                if b0 in adj[a0] and c0 in adj[a0] and c0 in adj[b0]:
                    return None
    return frozenset(new_edges)


def first_uncovered_requirement(edges):
    adj = adjacency(edges)
    for a, b in sorted(edges):
        third_part = ({0, 1, 2} - {part(a), part(b)}).pop()
        for c in PARTS[third_part]:
            a_sees_c = c in adj[a]
            b_sees_c = c in adj[b]
            if a_sees_c and b_sees_c:
                return None
            if not a_sees_c and not b_sees_c:
                return a, b, c
    return "closed"


def search(edges, seen, solutions):
    if edges is None or edges in seen:
        return
    seen.add(edges)
    requirement = first_uncovered_requirement(edges)
    if requirement is None:
        return
    if requirement == "closed":
        solutions.append(edges)
        return
    a, b, c = requirement
    search(add_edge(edges, a, c), seen, solutions)
    search(add_edge(edges, b, c), seen, solutions)


def main():
    seen = set()
    solutions = [frozenset()]
    for edge in ALL_EDGES:
        search(frozenset([edge]), seen, solutions)

    nonempty = [s for s in set(solutions) if s]
    assert not nonempty, sorted(nonempty, key=lambda s: (len(s), sorted(s)))[:3]
    print("ok: the empty graph is the only valid cross-edge pattern")


if __name__ == "__main__":
    main()
