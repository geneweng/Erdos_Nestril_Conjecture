"""Analyze high-greedy survivors in the reduced 4-regular triangle-free search.

This script is meant for the remaining case in PROOF_ATTEMPT.md.  It scans
connected 4-regular triangle-free graphs from `geng`, keeps graphs satisfying
x(e) <= 4, optionally applies the KY density and tight-edge Gallai filters, and
prints the graphs whose deterministic DSATUR strong coloring uses at least a
chosen threshold.

For the selected graphs it can also run a small exact coloring check on the
strong conflict graph.  The exact checker is dependency-free and intended for
the few high-greedy survivors, not for full-family exact coloring.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
import sys
import time

from check_reduced_small_orders import conflict_graph, dsatur_greedy
from check_regular_trianglefree_profiles import (
    edge_x_profile,
    iter_geng_graphs,
    ky_min_degree_sum,
    parse_graph6,
    tight_conflict_gallai_ok,
)


def profile_summary(profile: tuple[int, ...]) -> str:
    compact = collections.Counter(profile)
    return " ".join(f"x={x}:{compact[x]}" for x in sorted(compact))


def adjacency_masks(graph: list[set[int]]) -> list[int]:
    masks = []
    for nbrs in graph:
        mask = 0
        for w in nbrs:
            mask |= 1 << w
        masks.append(mask)
    return masks


def maximum_clique(graph: list[set[int]]) -> list[int]:
    """Exact maximum clique by branch-and-bound Bron-Kerbosch."""
    adj = adjacency_masks(graph)
    all_vertices = (1 << len(graph)) - 1
    best: list[int] = []

    def vertices(mask: int):
        while mask:
            bit = mask & -mask
            yield bit.bit_length() - 1
            mask ^= bit

    def expand(clique: list[int], candidates: int, excluded: int) -> None:
        nonlocal best
        if not candidates and not excluded:
            if len(clique) > len(best):
                best = clique.copy()
            return
        if len(clique) + candidates.bit_count() <= len(best):
            return

        pivot_pool = candidates | excluded
        if pivot_pool:
            pivot = max(vertices(pivot_pool), key=lambda v: (candidates & adj[v]).bit_count())
            branch = candidates & ~adj[pivot]
        else:
            branch = candidates

        while branch:
            bit = branch & -branch
            v = bit.bit_length() - 1
            expand(clique + [v], candidates & adj[v], excluded & adj[v])
            candidates ^= bit
            excluded |= bit
            branch ^= bit
            if len(clique) + candidates.bit_count() <= len(best):
                return

    expand([], all_vertices, 0)
    return best


@dataclass
class ColorCheck:
    result: bool | None
    nodes: int


def k_colorable(
    graph: list[set[int]],
    k: int,
    clique: list[int],
    node_budget: int,
) -> ColorCheck:
    """Return whether `graph` is k-colorable, or None if the budget expires."""
    if len(clique) > k:
        return ColorCheck(False, 0)

    n = len(graph)
    colors = [-1] * n
    degrees = [len(nbrs) for nbrs in graph]
    for color, vertex in enumerate(clique):
        colors[vertex] = color

    nodes = 0

    def blocked_mask(vertex: int) -> int:
        mask = 0
        for nbr in graph[vertex]:
            color = colors[nbr]
            if color != -1:
                mask |= 1 << color
        return mask

    def search(used: int) -> bool | None:
        nonlocal nodes
        nodes += 1
        if node_budget and nodes > node_budget:
            return None

        choice = -1
        choice_blocked = 0
        best_key = (-1, -1)
        for vertex in range(n):
            if colors[vertex] != -1:
                continue
            blocked = blocked_mask(vertex)
            available_limit = min(used + 1, k)
            allowed = ((1 << available_limit) - 1) & ~blocked
            if allowed == 0:
                return False
            key = (blocked.bit_count(), degrees[vertex])
            if key > best_key:
                best_key = key
                choice = vertex
                choice_blocked = blocked

        if choice == -1:
            return True

        existing_allowed = [c for c in range(used) if not (choice_blocked >> c) & 1]
        color_order = existing_allowed
        if used < k:
            color_order = color_order + [used]

        for color in color_order:
            colors[choice] = color
            result = search(max(used, color + 1))
            colors[choice] = -1
            if result is True:
                return True
            if result is None:
                return None
        return False

    return ColorCheck(search(len(clique)), nodes)


@dataclass
class ExactResult:
    lower: int
    upper: int
    exact: bool
    checks: list[str]
    clique_size: int


@dataclass
class CaseSummary:
    graph6: str
    greedy: int
    tight_edges: int
    profile: str
    clique_size: int | None
    exact_status: str | None


def exact_chromatic_range(
    graph: list[set[int]],
    upper: int,
    node_budget: int,
) -> ExactResult:
    clique = maximum_clique(graph)
    lower = len(clique)
    checks: list[str] = []

    for k in range(upper - 1, lower - 1, -1):
        check = k_colorable(graph, k, clique, node_budget)
        if check.result is True:
            checks.append(f"{k}:yes/{check.nodes}")
            upper = k
            continue
        if check.result is False:
            checks.append(f"{k}:no/{check.nodes}")
            lower = k + 1
            return ExactResult(lower, upper, lower == upper, checks, len(clique))
        checks.append(f"{k}:unknown/{check.nodes}")
        return ExactResult(lower, upper, False, checks, len(clique))

    return ExactResult(lower, upper, lower == upper, checks, len(clique))


def passes_critical_filters(
    n: int,
    adj: list[set[int]],
    profile: tuple[int, ...],
    edge_data: list[tuple[int, int, int]],
) -> bool:
    conflict_degree_sum = sum(24 - x for x in profile)
    if conflict_degree_sum < ky_min_degree_sum(2 * n):
        return False
    return tight_conflict_gallai_ok(adj, edge_data)


def report_case(
    case_no: int,
    line: str,
    profile: tuple[int, ...],
    conflicts: list[set[int]],
    greedy: int,
    exact: bool,
    node_budget: int,
    emit: bool = True,
) -> str | None:
    tight_edges = sum(1 for x in profile if x == 4)
    if emit:
        print(f"case {case_no}: graph6={line}", flush=True)
        print(
            f"  greedy={greedy} tight_edges={tight_edges} profile={profile_summary(profile)}",
            flush=True,
        )
    if not exact:
        return None

    result = exact_chromatic_range(conflicts, greedy, node_budget)
    status = str(result.upper) if result.exact else f"{result.lower}..{result.upper}"
    if emit:
        print(
            f"  clique={result.clique_size} exact={status} "
            f"checks={' '.join(result.checks) or 'none'}",
            flush=True,
        )
    return status


def analyze(
    n: int,
    threshold: int,
    critical_filters: bool,
    exact: bool,
    node_budget: int,
    progress: int,
    summary_only: bool,
) -> None:
    generated = 0
    local_survivors = 0
    filtered_survivors = 0
    selected = 0
    greedy_hist: collections.Counter[int] = collections.Counter()
    exact_hist: collections.Counter[str] = collections.Counter()
    unresolved: list[CaseSummary] = []
    started = time.monotonic()

    for line in iter_geng_graphs(n):
        generated += 1
        adj = parse_graph6(line)
        profile, edge_data = edge_x_profile(adj)
        if progress and generated % progress == 0:
            elapsed = time.monotonic() - started
            print(
                f"n={n}: generated={generated}, x<=4={local_survivors}, "
                f"filtered={filtered_survivors}, selected={selected}, "
                f"elapsed={elapsed:.1f}s",
                file=sys.stderr,
                flush=True,
            )
        if max(profile, default=0) > 4:
            continue
        local_survivors += 1
        if critical_filters and not passes_critical_filters(n, adj, profile, edge_data):
            continue
        filtered_survivors += 1

        conflicts = conflict_graph(adj)
        greedy = dsatur_greedy(conflicts)
        greedy_hist[greedy] += 1
        if greedy < threshold:
            continue

        selected += 1
        status = report_case(
            selected,
            line,
            profile,
            conflicts,
            greedy,
            exact,
            node_budget,
            emit=not summary_only,
        )
        if status is not None:
            exact_hist[status] += 1
            if ".." in status:
                clique = maximum_clique(conflicts)
                unresolved.append(
                    CaseSummary(
                        graph6=line,
                        greedy=greedy,
                        tight_edges=sum(1 for x in profile if x == 4),
                        profile=profile_summary(profile),
                        clique_size=len(clique),
                        exact_status=status,
                    )
                )

    print(
        f"summary n={n}: generated={generated}, x<=4={local_survivors}, "
        f"filtered={filtered_survivors}, selected={selected}"
    )
    print("  greedy histogram:", " ".join(f"{k}:{greedy_hist[k]}" for k in sorted(greedy_hist)))
    if exact:
        print("  exact histogram:", " ".join(f"{k}:{exact_hist[k]}" for k in sorted(exact_hist)))
    if unresolved:
        print("  unresolved cases:")
        for case in unresolved:
            print(
                f"    graph6={case.graph6} greedy={case.greedy} clique={case.clique_size} "
                f"exact={case.exact_status} tight_edges={case.tight_edges} profile={case.profile}"
            )


def analyze_graph6_inputs(lines: list[str], exact: bool, node_budget: int) -> None:
    exact_hist: collections.Counter[str] = collections.Counter()
    for index, line in enumerate(lines, start=1):
        adj = parse_graph6(line)
        profile, _ = edge_x_profile(adj)
        conflicts = conflict_graph(adj)
        greedy = dsatur_greedy(conflicts)
        status = report_case(index, line, profile, conflicts, greedy, exact, node_budget)
        if status is not None:
            exact_hist[status] += 1
    if exact:
        print("exact histogram:", " ".join(f"{k}:{exact_hist[k]}" for k in sorted(exact_hist)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("order", nargs="?", type=int, help="order to enumerate")
    parser.add_argument("--graph6", action="append", default=[], help="analyze one graph6 string")
    parser.add_argument("--threshold", type=int, default=18, help="minimum greedy color count")
    parser.add_argument("--critical-filters", action="store_true")
    parser.add_argument("--exact", action="store_true", help="run exact coloring on selected cases")
    parser.add_argument("--summary-only", action="store_true", help="suppress selected case details")
    parser.add_argument(
        "--node-budget",
        type=int,
        default=200000,
        help="recursive node budget per exact k-colorability check; 0 means no budget",
    )
    parser.add_argument(
        "--progress",
        type=int,
        default=0,
        metavar="N",
        help="print progress after every N generated graphs",
    )
    args = parser.parse_args()

    if args.graph6:
        analyze_graph6_inputs(args.graph6, exact=args.exact, node_budget=args.node_budget)
        return
    if args.order is None:
        parser.error("order is required unless --graph6 is supplied")

    analyze(
        args.order,
        threshold=args.threshold,
        critical_filters=args.critical_filters,
        exact=args.exact,
        node_budget=args.node_budget,
        progress=args.progress,
        summary_only=args.summary_only,
    )


if __name__ == "__main__":
    main()
