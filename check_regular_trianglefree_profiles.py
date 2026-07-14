"""Profile the remaining 4-regular triangle-free case.

This dependency-free helper enumerates connected 4-regular triangle-free graphs
with nauty `geng`, computes

    x(uv) = e(N(u) \\ {v}, N(v) \\ {u}),

and reports which graphs survive the necessary criticality condition x(e) <= 4
for every edge.

It is not a coloring proof.  It is a quick way to see which local 4-cycle
profiles remain after the reductions in PROOF_ATTEMPT.md.
"""

from __future__ import annotations

import collections
import itertools
import subprocess
import sys


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


def summarize(n: int) -> None:
    proc = subprocess.run(
        ["geng", "-c", "-t", "-q", "-d4", "-D4", str(n), f"{2 * n}:{2 * n}"],
        check=True,
        capture_output=True,
        text=True,
    )
    generated = 0
    survivors = 0
    profiles: collections.Counter[tuple[int, ...]] = collections.Counter()
    tight_stars = 0
    tight_4cycles = 0
    tight_star_or_4cycle = 0

    for line in proc.stdout.splitlines():
        if not line:
            continue
        generated += 1
        adj = parse_graph6(line)
        profile, edge_data = edge_x_profile(adj)
        if max(profile, default=0) > 4:
            continue
        survivors += 1
        profiles[profile] += 1
        edge_x = {tuple(sorted((u, v))): x for u, v, x in edge_data}
        has_star = has_tight_star(adj, edge_x)
        has_4cycle = has_tight_4cycle(adj, edge_x)
        tight_stars += int(has_star)
        tight_4cycles += int(has_4cycle)
        tight_star_or_4cycle += int(has_star or has_4cycle)

    print(f"n={n}: generated={generated}, x<=4 survivors={survivors}")
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
