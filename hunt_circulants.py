"""All 4-regular circulants C_n(a,b), n=15..40, no dedup."""
import networkx as nx
from sec import strong_chromatic_index

best = []
for n in range(15, 41):
    for a in range(1, n // 2 + 1):
        for b in range(a + 1, n // 2 + 1):
            if 2 * a == n or 2 * b == n:
                continue
            G = nx.circulant_graph(n, [a, b])
            if max(dict(G.degree()).values()) != 4 or not nx.is_connected(G):
                continue
            v, _ = strong_chromatic_index(G, ub_hint=21, exact_clique=False)
            best.append((v, f"C_{n}({a},{b})"))
            if v >= 20:
                print(f"*** chi'_s={v} C_{n}({a},{b})", flush=True)
    print(f"n={n} done, max so far: {max(best)}", flush=True)

best.sort(reverse=True)
print("top:", best[:10])
