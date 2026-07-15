"""Sound exhaustive sweep over graph6 input for Delta <= 4.

Usage:
  geng -c -q -D4 <n> 21:<maxm> | python3 hunt_sweep.py <tag>

For each graph this works in the fixed conflict graph C = L(G)^2:

1. remove vertices of degree < 20 to get the 20-core K;
2. if K is 20-colorable, then C is 20-colorable by greedy extension through
   the core-deletion order;
3. if greedy coloring does not certify K, run the dependency-free exact
   20-colorability checker on K.

This is the corrected replacement for the withdrawn edge-critical prune.  It
never uses a strong coloring of G-e.
"""

from __future__ import annotations

import argparse
import collections
import sys
import time

from analyze_reduced_extremes import k_colorable, maximum_clique
from check_reduced_small_orders import conflict_graph, dsatur_greedy
from check_regular_trianglefree_profiles import parse_graph6


def core_deletion_order(
    graph: list[set[int]],
    k: int,
) -> tuple[list[int], list[set[int]], list[int]]:
    """Return original core vertices, induced k-core, and deleted vertices."""
    n = len(graph)
    remaining = [True] * n
    queued = [False] * n
    degree = [len(nbrs) for nbrs in graph]
    stack = [v for v, deg in enumerate(degree) if deg < k]
    for v in stack:
        queued[v] = True

    deleted: list[int] = []
    while stack:
        v = stack.pop()
        if not remaining[v]:
            continue
        remaining[v] = False
        deleted.append(v)
        for w in graph[v]:
            if not remaining[w]:
                continue
            degree[w] -= 1
            if degree[w] < k and not queued[w]:
                queued[w] = True
                stack.append(w)

    core_vertices = [v for v in range(n) if remaining[v]]
    index = {v: i for i, v in enumerate(core_vertices)}
    core = [set() for _ in core_vertices]
    for v in core_vertices:
        for w in graph[v]:
            if w in index:
                core[index[v]].add(index[w])
    return core_vertices, core, deleted


def hist_line(counter: collections.Counter[int]) -> str:
    return " ".join(f"{key}:{counter[key]}" for key in sorted(counter))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", nargs="?", default="sweep")
    parser.add_argument("--k", type=int, default=20)
    parser.add_argument(
        "--node-budget",
        type=int,
        default=200000,
        help="recursive node budget per exact core check; 0 means no budget",
    )
    parser.add_argument("--progress", type=int, default=0, metavar="N")
    args = parser.parse_args()

    near_path = f"results/core_near_{args.tag}.g6"
    hit_path = f"results/CORE_HIT_{args.tag}.g6"

    count = 0
    empty_core = 0
    greedy_core_ok = 0
    exact_core_ok = 0
    undecided = 0
    hits = 0
    max_core_size = 0
    max_core_greedy = 0
    core_size_hist: collections.Counter[int] = collections.Counter()
    core_greedy_hist: collections.Counter[int] = collections.Counter()
    started = time.monotonic()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        count += 1
        if args.progress and count % args.progress == 0:
            elapsed = time.monotonic() - started
            print(
                f"[{args.tag}] seen={count} empty_core={empty_core} "
                f"greedy_ok={greedy_core_ok} exact_ok={exact_core_ok} "
                f"undecided={undecided} hits={hits} elapsed={elapsed:.1f}s",
                file=sys.stderr,
                flush=True,
            )

        adj = parse_graph6(line)
        conflicts = conflict_graph(adj)
        _, core, _ = core_deletion_order(conflicts, args.k)
        core_size = len(core)
        core_size_hist[core_size] += 1
        max_core_size = max(max_core_size, core_size)

        if core_size == 0:
            empty_core += 1
            continue

        used = dsatur_greedy(core)
        core_greedy_hist[used] += 1
        max_core_greedy = max(max_core_greedy, used)
        if used <= args.k:
            greedy_core_ok += 1
            continue

        check = k_colorable(core, args.k, maximum_clique(core), args.node_budget)
        if check.result is True:
            exact_core_ok += 1
            with open(near_path, "a") as near_file:
                near_file.write(
                    f"{line} core={core_size} greedy={used} exact20=yes/{check.nodes}\n"
                )
            continue
        if check.result is None:
            undecided += 1
            with open(near_path, "a") as near_file:
                near_file.write(
                    f"{line} core={core_size} greedy={used} exact20=unknown/{check.nodes}\n"
                )
            continue

        hits += 1
        with open(hit_path, "a") as hit_file:
            hit_file.write(f"{line} core={core_size} greedy={used} exact20=no/{check.nodes}\n")
        print(f"*** COUNTEREXAMPLE: {line}", flush=True)

    print(
        f"[{args.tag}] done: graphs={count}, empty_core={empty_core}, "
        f"greedy_core_ok={greedy_core_ok}, exact_core_ok={exact_core_ok}, "
        f"undecided={undecided}, hits={hits}, max_core_size={max_core_size}, "
        f"max_core_greedy={max_core_greedy}",
        flush=True,
    )
    print(f"[{args.tag}] core_size_hist {hist_line(core_size_hist)}", flush=True)
    print(f"[{args.tag}] core_greedy_hist {hist_line(core_greedy_hist)}", flush=True)


if __name__ == "__main__":
    main()
