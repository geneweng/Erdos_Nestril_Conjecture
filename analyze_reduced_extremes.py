"""Analyze high-greedy survivors in the reduced 4-regular triangle-free search.

This script is meant for the remaining case in PROOF_ATTEMPT.md.  It scans
connected 4-regular triangle-free graphs from `geng`, keeps graphs satisfying
x(e) <= 4, optionally applies the KY density and tight-edge Gallai filters, and
prints the graphs whose deterministic DSATUR strong coloring uses at least a
chosen threshold.

For the selected graphs it can also run a small exact coloring check on the
strong conflict graph.  The exact checker is dependency-free and intended for
the few high-greedy survivors, not for full-family exact coloring.

It can also color selected cases by repeatedly removing a maximum induced
matching, giving a constructive packing heuristic to compare with DSATUR.  A
small randomized tie-breaking mode tests whether poor packings come only from
which maximum induced matching is removed first.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
import math
import random
import sys
import time

from check_reduced_small_orders import dsatur_greedy
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


def edge_list(adj: list[set[int]]) -> list[tuple[int, int]]:
    return [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]


def conflict_graph(adj: list[set[int]]) -> list[set[int]]:
    edges = edge_list(adj)
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


def maximum_cliques_limited(
    graph: list[set[int]],
    limit: int,
    rng: random.Random | None = None,
) -> list[list[int]]:
    """Collect up to `limit` maximum cliques by Bron-Kerbosch search."""
    if limit < 1:
        return []

    adj = adjacency_masks(graph)
    all_vertices = (1 << len(graph)) - 1
    best_size = 0
    best: list[list[int]] = []

    def vertices(mask: int) -> list[int]:
        result = []
        while mask:
            bit = mask & -mask
            result.append(bit.bit_length() - 1)
            mask ^= bit
        return result

    def record(clique: list[int]) -> None:
        nonlocal best_size, best
        size = len(clique)
        if size > best_size:
            best_size = size
            best = [clique.copy()]
        elif size == best_size and len(best) < limit:
            best.append(clique.copy())

    def expand(clique: list[int], candidates: int, excluded: int) -> None:
        if not candidates and not excluded:
            record(clique)
            return
        if len(clique) + candidates.bit_count() < best_size:
            return
        if len(best) >= limit and len(clique) + candidates.bit_count() <= best_size:
            return

        pivot_pool = candidates | excluded
        if pivot_pool:
            pivot = max(vertices(pivot_pool), key=lambda v: (candidates & adj[v]).bit_count())
            branch = candidates & ~adj[pivot]
        else:
            branch = candidates

        branch_vertices = vertices(branch)
        if rng is not None:
            rng.shuffle(branch_vertices)

        for v in branch_vertices:
            bit = 1 << v
            if not candidates & bit:
                continue
            expand(clique + [v], candidates & adj[v], excluded & adj[v])
            candidates ^= bit
            excluded |= bit
            if len(clique) + candidates.bit_count() < best_size:
                return
            if len(best) >= limit and len(clique) + candidates.bit_count() <= best_size:
                return

    expand([], all_vertices, 0)
    return best


def complement_graph(graph: list[set[int]]) -> list[set[int]]:
    n = len(graph)
    vertices = set(range(n))
    return [vertices - {v} - graph[v] for v in range(n)]


def induced_subgraph(graph: list[set[int]], vertices: list[int]) -> list[set[int]]:
    index = {v: i for i, v in enumerate(vertices)}
    subgraph = [set() for _ in vertices]
    for v in vertices:
        for w in graph[v]:
            if w in index:
                subgraph[index[v]].add(index[w])
    return subgraph


@dataclass
class StructureSummary:
    clique: int
    alpha: int
    color_lb: int
    min_degree: int
    max_degree: int
    degree_sum: int


def structure_summary(graph: list[set[int]]) -> StructureSummary:
    clique = len(maximum_clique(graph))
    alpha = len(maximum_clique(complement_graph(graph)))
    degrees = [len(nbrs) for nbrs in graph]
    return StructureSummary(
        clique=clique,
        alpha=alpha,
        color_lb=math.ceil(len(graph) / alpha),
        min_degree=min(degrees, default=0),
        max_degree=max(degrees, default=0),
        degree_sum=sum(degrees),
    )


@dataclass
class ColorCheck:
    result: bool | None
    nodes: int
    coloring: list[int] | None = None


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
    solution: list[int] | None = None

    def blocked_mask(vertex: int) -> int:
        mask = 0
        for nbr in graph[vertex]:
            color = colors[nbr]
            if color != -1:
                mask |= 1 << color
        return mask

    def search(used: int) -> bool | None:
        nonlocal nodes, solution
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
            solution = colors.copy()
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

    result = search(len(clique))
    return ColorCheck(result, nodes, solution if result is True else None)


@dataclass
class ExactResult:
    lower: int
    upper: int
    exact: bool
    checks: list[str]
    clique_size: int
    coloring: list[int] | None = None


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
    best_coloring: list[int] | None = None

    for k in range(upper - 1, lower - 1, -1):
        check = k_colorable(graph, k, clique, node_budget)
        if check.result is True:
            checks.append(f"{k}:yes/{check.nodes}")
            upper = k
            best_coloring = check.coloring
            continue
        if check.result is False:
            checks.append(f"{k}:no/{check.nodes}")
            lower = k + 1
            return ExactResult(lower, upper, lower == upper, checks, len(clique), best_coloring)
        checks.append(f"{k}:unknown/{check.nodes}")
        return ExactResult(lower, upper, False, checks, len(clique), best_coloring)

    return ExactResult(lower, upper, lower == upper, checks, len(clique), best_coloring)


def color_class_summary(coloring: list[int]) -> str:
    class_sizes = collections.Counter(coloring)
    size_hist = collections.Counter(class_sizes.values())
    return " ".join(f"size={size}:{size_hist[size]}" for size in sorted(size_hist))


def class_size_summary(classes: list[list[int]]) -> str:
    size_hist = collections.Counter(len(cls) for cls in classes)
    return " ".join(f"size={size}:{size_hist[size]}" for size in sorted(size_hist))


def maximum_induced_matching_pack(
    graph: list[set[int]],
    candidate_limit: int = 1,
    rng: random.Random | None = None,
) -> list[list[int]]:
    """Color by repeatedly removing a maximum independent set."""
    remaining = list(range(len(graph)))
    classes: list[list[int]] = []
    while remaining:
        subgraph = induced_subgraph(graph, remaining)
        complement = complement_graph(subgraph)
        if candidate_limit <= 1:
            independent_set = maximum_clique(complement)
        else:
            choices = maximum_cliques_limited(complement, candidate_limit, rng)
            if not choices:
                choices = [maximum_clique(complement)]
            independent_set = rng.choice(choices) if rng is not None else choices[0]
        color_class = [remaining[i] for i in independent_set]
        classes.append(color_class)
        used = set(color_class)
        remaining = [v for v in remaining if v not in used]
    return classes


def pack_sort_key(classes: list[list[int]]) -> tuple[int, list[int]]:
    return len(classes), [-len(cls) for cls in classes]


def best_maximum_induced_matching_pack(
    graph: list[set[int]],
    trials: int,
    candidate_limit: int,
    seed: int,
) -> list[list[int]]:
    if trials <= 1:
        rng = random.Random(seed) if candidate_limit > 1 else None
        return maximum_induced_matching_pack(graph, candidate_limit, rng)

    best: list[list[int]] | None = None
    for trial in range(trials):
        rng = random.Random(seed + trial)
        classes = maximum_induced_matching_pack(graph, candidate_limit, rng)
        if best is None or pack_sort_key(classes) < pack_sort_key(best):
            best = classes
    assert best is not None
    return best


def color_class_details(
    adj: list[set[int]],
    edge_data: list[tuple[int, int, int]],
    coloring: list[int],
) -> list[str]:
    x_by_edge = {tuple(sorted((u, v))): x for u, v, x in edge_data}
    groups: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)
    for edge, color in zip(edge_list(adj), coloring, strict=True):
        groups[color].append(edge)

    lines = []
    for color in sorted(groups):
        edges = sorted(groups[color])
        xs = [x_by_edge[edge] for edge in edges]
        x_summary = profile_summary(tuple(sorted(xs)))
        edge_summary = " ".join(f"{u}-{v}:x{x_by_edge[(u, v)]}" for u, v in edges)
        lines.append(f"    color {color}: size={len(edges)} {x_summary} edges={edge_summary}")
    return lines


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
    adj: list[set[int]],
    profile: tuple[int, ...],
    edge_data: list[tuple[int, int, int]],
    conflicts: list[set[int]],
    greedy: int,
    exact: bool,
    node_budget: int,
    structure: bool,
    witness: bool,
    witness_details: bool,
    pack: bool,
    pack_trials: int,
    pack_candidates: int,
    pack_seed: int,
    emit: bool = True,
) -> tuple[str | None, StructureSummary | None, int | None]:
    tight_edges = sum(1 for x in profile if x == 4)
    if emit:
        print(f"case {case_no}: graph6={line}", flush=True)
        print(
            f"  greedy={greedy} tight_edges={tight_edges} profile={profile_summary(profile)}",
            flush=True,
        )

    struct = structure_summary(conflicts) if structure else None
    if emit and struct is not None:
        print(
            f"  omega={struct.clique} alpha={struct.alpha} "
            f"ceil(n/alpha)={struct.color_lb} "
            f"conflict_degree={struct.min_degree}..{struct.max_degree} "
            f"degree_sum={struct.degree_sum}",
            flush=True,
        )
    if not exact:
        pack_colors = None
        if pack:
            packed_classes = best_maximum_induced_matching_pack(
                conflicts,
                pack_trials,
                pack_candidates,
                pack_seed + 1000003 * case_no,
            )
            pack_colors = len(packed_classes)
            if emit:
                suffix = (
                    f" pack_trials={pack_trials} pack_candidates={pack_candidates}"
                    if pack_trials > 1 or pack_candidates > 1
                    else ""
                )
                print(
                    f"  pack_colors={pack_colors} "
                    f"pack_classes={class_size_summary(packed_classes)}{suffix}",
                    flush=True,
                )
        return None, struct, pack_colors

    result = exact_chromatic_range(conflicts, greedy, node_budget)
    status = str(result.upper) if result.exact else f"{result.lower}..{result.upper}"
    if emit:
        print(
            f"  clique={result.clique_size} exact={status} "
            f"checks={' '.join(result.checks) or 'none'}",
            flush=True,
        )
        if witness and result.coloring is not None:
            print(f"  color_classes={color_class_summary(result.coloring)}", flush=True)
            if witness_details:
                print("  color_class_details:", flush=True)
                for detail_line in color_class_details(adj, edge_data, result.coloring):
                    print(detail_line, flush=True)
    pack_colors = None
    if pack:
        packed_classes = best_maximum_induced_matching_pack(
            conflicts,
            pack_trials,
            pack_candidates,
            pack_seed + 1000003 * case_no,
        )
        pack_colors = len(packed_classes)
        if emit:
            suffix = (
                f" pack_trials={pack_trials} pack_candidates={pack_candidates}"
                if pack_trials > 1 or pack_candidates > 1
                else ""
            )
            print(
                f"  pack_colors={pack_colors} "
                f"pack_classes={class_size_summary(packed_classes)}{suffix}",
                flush=True,
            )
    return status, struct, pack_colors


def analyze(
    n: int,
    threshold: int,
    critical_filters: bool,
    exact: bool,
    node_budget: int,
    progress: int,
    summary_only: bool,
    structure: bool,
    witness: bool,
    witness_details: bool,
    pack: bool,
    pack_trials: int,
    pack_candidates: int,
    pack_seed: int,
) -> None:
    generated = 0
    local_survivors = 0
    filtered_survivors = 0
    selected = 0
    greedy_hist: collections.Counter[int] = collections.Counter()
    exact_hist: collections.Counter[str] = collections.Counter()
    clique_hist: collections.Counter[int] = collections.Counter()
    alpha_hist: collections.Counter[int] = collections.Counter()
    color_lb_hist: collections.Counter[int] = collections.Counter()
    degree_range_hist: collections.Counter[tuple[int, int]] = collections.Counter()
    pack_hist: collections.Counter[int] = collections.Counter()
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
        status, struct, pack_colors = report_case(
            selected,
            line,
            adj,
            profile,
            edge_data,
            conflicts,
            greedy,
            exact,
            node_budget,
            structure,
            witness,
            witness_details,
            pack,
            pack_trials,
            pack_candidates,
            pack_seed,
            emit=not summary_only,
        )
        if pack_colors is not None:
            pack_hist[pack_colors] += 1
        if struct is not None:
            clique_hist[struct.clique] += 1
            alpha_hist[struct.alpha] += 1
            color_lb_hist[struct.color_lb] += 1
            degree_range_hist[(struct.min_degree, struct.max_degree)] += 1
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
    if structure:
        print("  clique histogram:", " ".join(f"{k}:{clique_hist[k]}" for k in sorted(clique_hist)))
        print("  alpha histogram:", " ".join(f"{k}:{alpha_hist[k]}" for k in sorted(alpha_hist)))
        print(
            "  ceil(n/alpha) histogram:",
            " ".join(f"{k}:{color_lb_hist[k]}" for k in sorted(color_lb_hist)),
        )
        print(
            "  degree range histogram:",
            " ".join(
                f"{lo}..{hi}:{degree_range_hist[(lo, hi)]}"
                for lo, hi in sorted(degree_range_hist)
            ),
        )
    if pack:
        print("  pack histogram:", " ".join(f"{k}:{pack_hist[k]}" for k in sorted(pack_hist)))
    if unresolved:
        print("  unresolved cases:")
        for case in unresolved:
            print(
                f"    graph6={case.graph6} greedy={case.greedy} clique={case.clique_size} "
                f"exact={case.exact_status} tight_edges={case.tight_edges} profile={case.profile}"
            )


def analyze_graph6_inputs(
    lines: list[str],
    exact: bool,
    node_budget: int,
    structure: bool,
    witness: bool,
    witness_details: bool,
    pack: bool,
    pack_trials: int,
    pack_candidates: int,
    pack_seed: int,
) -> None:
    exact_hist: collections.Counter[str] = collections.Counter()
    for index, line in enumerate(lines, start=1):
        adj = parse_graph6(line)
        profile, edge_data = edge_x_profile(adj)
        conflicts = conflict_graph(adj)
        greedy = dsatur_greedy(conflicts)
        status, _, _ = report_case(
            index,
            line,
            adj,
            profile,
            edge_data,
            conflicts,
            greedy,
            exact,
            node_budget,
            structure,
            witness,
            witness_details,
            pack,
            pack_trials,
            pack_candidates,
            pack_seed,
        )
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
    parser.add_argument("--structure", action="store_true", help="report clique/independence summaries")
    parser.add_argument("--witness", action="store_true", help="print exact coloring class-size histograms")
    parser.add_argument("--witness-details", action="store_true", help="print edge-level color classes")
    parser.add_argument("--pack", action="store_true", help="color by repeatedly removing maximum induced matchings")
    parser.add_argument("--pack-trials", type=int, default=1, help="randomized maximum-matching pack trials")
    parser.add_argument(
        "--pack-candidates",
        type=int,
        default=1,
        help="maximum matching alternatives collected at each packing step",
    )
    parser.add_argument("--pack-seed", type=int, default=0, help="seed for randomized packing")
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

    if args.witness and not args.exact:
        parser.error("--witness requires --exact")
    if args.witness_details and not args.witness:
        parser.error("--witness-details requires --witness")
    if args.pack_trials < 1:
        parser.error("--pack-trials must be at least 1")
    if args.pack_candidates < 1:
        parser.error("--pack-candidates must be at least 1")
    if (args.pack_trials != 1 or args.pack_candidates != 1 or args.pack_seed != 0) and not args.pack:
        parser.error("--pack-trials, --pack-candidates, and --pack-seed require --pack")

    if args.graph6:
        analyze_graph6_inputs(
            args.graph6,
            exact=args.exact,
            node_budget=args.node_budget,
            structure=args.structure,
            witness=args.witness,
            witness_details=args.witness_details,
            pack=args.pack,
            pack_trials=args.pack_trials,
            pack_candidates=args.pack_candidates,
            pack_seed=args.pack_seed,
        )
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
        structure=args.structure,
        witness=args.witness,
        witness_details=args.witness_details,
        pack=args.pack,
        pack_trials=args.pack_trials,
        pack_candidates=args.pack_candidates,
        pack_seed=args.pack_seed,
    )


if __name__ == "__main__":
    main()
