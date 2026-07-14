"""Reduced exhaustive check after the proof-attempt reductions.

Using PROOF_ATTEMPT.md, any connected edge-critical counterexample must be
4-regular, triangle-free, and satisfy x(e) <= 4 on every edge, where x(e) is
the number of 4-cycles containing e.

This script enumerates that reduced family for selected orders with `geng` and
greedily strong-colors each survivor.  A greedy coloring with at most 20 colors
is a constructive certificate that the graph is not a counterexample.
Generation is streamed, so larger orders can be monitored with `--progress N`.

Default orders are 15 and 16, the first orders beyond the original <=14 sweep.
"""

from __future__ import annotations

import argparse
import collections
import sys
import time

from check_regular_trianglefree_profiles import edge_x_profile, iter_geng_graphs, parse_graph6


def conflict_graph(adj: list[set[int]]) -> list[set[int]]:
    edges = []
    for u in range(len(adj)):
        for v in adj[u]:
            if u < v:
                edges.append((u, v))

    conflicts = [set() for _ in edges]
    for i, (a, b) in enumerate(edges):
        for j in range(i + 1, len(edges)):
            c, d = edges[j]
            if (
                a == c
                or a == d
                or b == c
                or b == d
                or c in adj[a]
                or d in adj[a]
                or c in adj[b]
                or d in adj[b]
            ):
                conflicts[i].add(j)
                conflicts[j].add(i)
    return conflicts


def dsatur_greedy(conflicts: list[set[int]]) -> int:
    colors: list[int | None] = [None] * len(conflicts)
    uncolored = set(range(len(conflicts)))
    seen_neighbor_colors = [set() for _ in conflicts]

    while uncolored:
        vertex = max(
            uncolored,
            key=lambda v: (len(seen_neighbor_colors[v]), len(conflicts[v]), -v),
        )
        blocked = {colors[w] for w in conflicts[vertex] if colors[w] is not None}
        color = 0
        while color in blocked:
            color += 1
        colors[vertex] = color
        uncolored.remove(vertex)
        for neighbor in conflicts[vertex]:
            if neighbor in uncolored:
                seen_neighbor_colors[neighbor].add(color)

    return max((color for color in colors if color is not None), default=-1) + 1


def summarize(n: int, progress: int = 0) -> None:
    generated = 0
    survivors = 0
    max_greedy = 0
    histogram: collections.Counter[int] = collections.Counter()
    started = time.monotonic()

    for line in iter_geng_graphs(n):
        generated += 1
        adj = parse_graph6(line)
        profile, _ = edge_x_profile(adj)
        if progress and generated % progress == 0:
            elapsed = time.monotonic() - started
            print(
                f"n={n}: generated={generated}, survivors={survivors}, "
                f"max_greedy={max_greedy}, elapsed={elapsed:.1f}s",
                file=sys.stderr,
                flush=True,
            )
        if max(profile, default=0) > 4:
            continue

        survivors += 1
        used = dsatur_greedy(conflict_graph(adj))
        histogram[used] += 1
        max_greedy = max(max_greedy, used)
        if used > 20:
            raise AssertionError(f"greedy used {used} colors on graph6 {line}")

    print(
        f"n={n}: generated={generated}, x<=4 survivors={survivors}, "
        f"max greedy strong colors={max_greedy}"
    )
    print("  histogram:", " ".join(f"{k}:{histogram[k]}" for k in sorted(histogram)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("orders", nargs="*", type=int, help="orders to enumerate")
    parser.add_argument(
        "--progress",
        type=int,
        default=0,
        metavar="N",
        help="print progress after every N generated graphs",
    )
    args = parser.parse_args()

    ns = args.orders if args.orders else [15, 16]
    for n in ns:
        summarize(n, progress=args.progress)


if __name__ == "__main__":
    main()
