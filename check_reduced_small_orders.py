"""Conditional reduced-family check after the withdrawn proof-attempt reductions.

ERRATA.md withdraws the proof that any connected counterexample must be
4-regular, triangle-free, and satisfy x(e) <= 4 on every edge.  This script
still enumerates that family because it remains useful exploratory data, but
its output is not a proof-certified exclusion of counterexamples.

This script enumerates that reduced family for selected orders with `geng` and
greedily strong-colors each survivor.  A greedy coloring with at most 20 colors
is a constructive certificate that the generated graph is not a counterexample.
Generation is streamed, so larger orders can be monitored with `--progress N`.
Use `--critical-filters` to color only graphs that also pass the
Kostochka-Yancey density and tight-edge Gallai necessary conditions.

Default orders are 15 and 16, the first orders beyond the original <=14 sweep.
"""

from __future__ import annotations

import argparse
import collections
import sys
import time

from check_regular_trianglefree_profiles import (
    edge_x_profile,
    iter_geng_graphs,
    ky_min_degree_sum,
    parse_graph6,
    tight_conflict_gallai_ok,
)


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


def summarize(n: int, progress: int = 0, critical_filters: bool = False) -> None:
    generated = 0
    survivors = 0
    ky_compatible = 0
    tight_gallai_compatible = 0
    colored = 0
    max_greedy = 0
    histogram: collections.Counter[int] = collections.Counter()
    min_degree_sum = ky_min_degree_sum(2 * n)
    started = time.monotonic()

    for line in iter_geng_graphs(n):
        generated += 1
        adj = parse_graph6(line)
        profile, edge_data = edge_x_profile(adj)
        if progress and generated % progress == 0:
            elapsed = time.monotonic() - started
            message = (
                f"n={n}: generated={generated}, x<=4={survivors}, "
                f"colored={colored}, max_greedy={max_greedy}, elapsed={elapsed:.1f}s"
            )
            if critical_filters:
                message = (
                    f"n={n}: generated={generated}, x<=4={survivors}, "
                    f"KY={ky_compatible}, Gallai={tight_gallai_compatible}, "
                    f"colored={colored}, max_greedy={max_greedy}, elapsed={elapsed:.1f}s"
                )
            print(message, file=sys.stderr, flush=True)
        if max(profile, default=0) > 4:
            continue

        survivors += 1
        if critical_filters:
            conflict_degree_sum = sum(24 - x for x in profile)
            if conflict_degree_sum < min_degree_sum:
                continue
            ky_compatible += 1
            if not tight_conflict_gallai_ok(adj, edge_data):
                continue
            tight_gallai_compatible += 1

        colored += 1
        used = dsatur_greedy(conflict_graph(adj))
        histogram[used] += 1
        max_greedy = max(max_greedy, used)
        if used > 20:
            raise AssertionError(f"greedy used {used} colors on graph6 {line}")

    print(
        f"n={n}: generated={generated}, x<=4 survivors={survivors}, "
        f"max greedy strong colors={max_greedy}"
    )
    if critical_filters:
        print(f"  KY-compatible survivors: {ky_compatible}")
        print(f"  tight-edge Gallai-compatible survivors: {tight_gallai_compatible}")
        print(f"  colored after critical filters: {colored}")
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
    parser.add_argument(
        "--critical-filters",
        action="store_true",
        help="color only graphs that also pass KY density and tight-edge Gallai filters",
    )
    args = parser.parse_args()

    ns = args.orders if args.orders else [15, 16]
    for n in ns:
        summarize(n, progress=args.progress, critical_filters=args.critical_filters)


if __name__ == "__main__":
    main()
