"""Profile the remaining 4-regular triangle-free case.

This dependency-free helper enumerates connected 4-regular triangle-free graphs
with nauty `geng`, computes

    x(uv) = e(N(u) \\ {v}, N(v) \\ {u}),

and reports which graphs survive the necessary criticality condition x(e) <= 4
for every edge.  It also checks two additional necessary conditions for the
conflict graph of a 21-critical counterexample: the Kostochka-Yancey edge
density lower bound and Gallai's theorem on the tight-edge subgraph.

It is not a coloring proof.  It is a quick way to see which local 4-cycle
profiles remain after the reductions in PROOF_ATTEMPT.md.
"""

from __future__ import annotations

import collections
from collections.abc import Iterator
import itertools
import subprocess
import sys


def iter_geng_graphs(n: int) -> Iterator[str]:
    """Yield graph6 lines for connected 4-regular triangle-free graphs."""
    cmd = ["geng", "-c", "-t", "-q", "-d4", "-D4", str(n), f"{2 * n}:{2 * n}"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            line = line.strip()
            if line:
                yield line
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
    except BaseException:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        raise


def parse_graph6(line: str) -> list[set[int]]:
    """Parse graph6 for n <= 62."""
    line = line.strip()
    if not line:
        raise ValueError("empty graph6 line")
    n = ord(line[0]) - 63
    bits = []
    for ch in line[1:]:
        value = ord(ch) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))

    adj = [set() for _ in range(n)]
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i].add(j)
                adj[j].add(i)
            idx += 1
    return adj


def edge_x_profile(adj: list[set[int]]) -> tuple[tuple[int, ...], list[tuple[int, int, int]]]:
    values = []
    edge_data = []
    for u in range(len(adj)):
        for v in adj[u]:
            if u < v:
                a_side = adj[u] - {v}
                b_side = adj[v] - {u}
                x = sum(1 for a in a_side for b in b_side if b in adj[a])
                values.append(x)
                edge_data.append((u, v, x))
    return tuple(sorted(values)), edge_data


def edges_conflict(adj: list[set[int]], e: tuple[int, int], f: tuple[int, int]) -> bool:
    a, b = e
    c, d = f
    return (
        a == c
        or a == d
        or b == c
        or b == d
        or c in adj[a]
        or d in adj[a]
        or c in adj[b]
        or d in adj[b]
    )


def has_tight_star(adj: list[set[int]], edge_x: dict[tuple[int, int], int]) -> bool:
    for v, nbrs in enumerate(adj):
        if all(edge_x[tuple(sorted((v, w)))] == 4 for w in nbrs):
            return True
    return False


def has_tight_4cycle(adj: list[set[int]], edge_x: dict[tuple[int, int], int]) -> bool:
    n = len(adj)
    for a, b, c, d in itertools.combinations(range(n), 4):
        edges = [(a, b), (b, c), (c, d), (a, d)]
        if all(y in adj[x] for x, y in edges):
            if all(edge_x[tuple(sorted(e))] == 4 for e in edges):
                return True
        edges = [(a, b), (b, d), (c, d), (a, c)]
        if all(y in adj[x] for x, y in edges):
            if all(edge_x[tuple(sorted(e))] == 4 for e in edges):
                return True
        edges = [(a, c), (b, c), (b, d), (a, d)]
        if all(y in adj[x] for x, y in edges):
            if all(edge_x[tuple(sorted(e))] == 4 for e in edges):
                return True
    return False


def block_is_clique(block: set[int], graph: list[set[int]]) -> bool:
    size = len(block)
    return all(len(graph[v] & block) == size - 1 for v in block)


def block_is_odd_cycle(block: set[int], graph: list[set[int]]) -> bool:
    size = len(block)
    if size < 3 or size % 2 == 0:
        return False
    return all(len(graph[v] & block) == 2 for v in block)


def biconnected_blocks(graph: list[set[int]]) -> list[set[int]]:
    n = len(graph)
    disc = [-1] * n
    low = [0] * n
    edge_stack: list[tuple[int, int]] = []
    blocks: list[set[int]] = []
    time = 0

    def dfs(v: int, parent: int) -> None:
        nonlocal time
        disc[v] = low[v] = time
        time += 1
        for w in graph[v]:
            if disc[w] == -1:
                edge_stack.append((v, w))
                dfs(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= disc[v]:
                    block = set()
                    while True:
                        a, b = edge_stack.pop()
                        block.add(a)
                        block.add(b)
                        if (a, b) == (v, w):
                            break
                    blocks.append(block)
            elif w != parent and disc[w] < disc[v]:
                edge_stack.append((v, w))
                low[v] = min(low[v], disc[w])

    for v in range(n):
        if disc[v] == -1:
            dfs(v, -1)
    return blocks


def tight_conflict_gallai_ok(adj: list[set[int]], edge_data: list[tuple[int, int, int]]) -> bool:
    tight_edges = [(u, v) for u, v, x in edge_data if x == 4]
    graph = [set() for _ in tight_edges]
    for i, edge in enumerate(tight_edges):
        for j in range(i + 1, len(tight_edges)):
            if edges_conflict(adj, edge, tight_edges[j]):
                graph[i].add(j)
                graph[j].add(i)

    for block in biconnected_blocks(graph):
        if len(block) <= 2:
            continue
        if not (block_is_clique(block, graph) or block_is_odd_cycle(block, graph)):
            return False
    return True


def ky_min_degree_sum(conflict_vertices: int, colors: int = 21) -> int:
    """Kostochka-Yancey lower bound on degree sum of a k-critical graph."""
    numerator = (colors + 1) * (colors - 2) * conflict_vertices - colors * (colors - 3)
    denominator = colors - 1
    return (numerator + denominator - 1) // denominator


def summarize(n: int) -> None:
    generated = 0
    survivors = 0
    profiles: collections.Counter[tuple[int, ...]] = collections.Counter()
    tight_stars = 0
    tight_4cycles = 0
    tight_star_or_4cycle = 0
    ky_compatible = 0
    tight_gallai_compatible = 0
    conflict_vertices = 2 * n
    min_degree_sum = ky_min_degree_sum(conflict_vertices)

    for line in iter_geng_graphs(n):
        generated += 1
        adj = parse_graph6(line)
        profile, edge_data = edge_x_profile(adj)
        if max(profile, default=0) > 4:
            continue
        survivors += 1
        conflict_degree_sum = sum(24 - x for x in profile)
        if conflict_degree_sum >= min_degree_sum:
            ky_compatible += 1
        if tight_conflict_gallai_ok(adj, edge_data):
            tight_gallai_compatible += 1
        profiles[profile] += 1
        edge_x = {tuple(sorted((u, v))): x for u, v, x in edge_data}
        has_star = has_tight_star(adj, edge_x)
        has_4cycle = has_tight_4cycle(adj, edge_x)
        tight_stars += int(has_star)
        tight_4cycles += int(has_4cycle)
        tight_star_or_4cycle += int(has_star or has_4cycle)

    print(f"n={n}: generated={generated}, x<=4 survivors={survivors}")
    print(f"  KY-compatible survivors: {ky_compatible}")
    print(f"  tight-edge Gallai-compatible survivors: {tight_gallai_compatible}")
    print(f"  survivors with tight star: {tight_stars}")
    print(f"  survivors with tight 4-cycle: {tight_4cycles}")
    print(f"  survivors with tight star or tight 4-cycle: {tight_star_or_4cycle}")
    for profile, count in profiles.most_common(8):
        compact = collections.Counter(profile)
        summary = " ".join(f"x={x}:{compact[x]}" for x in sorted(compact))
        print(f"  {count:5d}  {summary}")


def main() -> None:
    ns = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [10, 12, 14]
    for n in ns:
        summarize(n)


if __name__ == "__main__":
    main()
