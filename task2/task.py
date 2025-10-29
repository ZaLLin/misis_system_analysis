import pandas as pd
import numpy as np
from typing import Tuple

def main(s: str, e: str) -> Tuple[float, float]:
    graph = pd.read_csv(s, header=None, dtype=int)
    uniq_list = sorted(set(graph[0]).union(set(graph[1])))

    adjacency_m = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    for u, v in graph.values:
        adjacency_m.loc[u, v] = 1
        adjacency_m.loc[v, u] = 1

    # Степени вершин
    degrees = adjacency_m.sum(axis=1).astype(float)
    total = degrees.sum()
    if total == 0 or len(uniq_list) == 0:
        return 0.0, 0.0

    # Вероятности связей
    probs = degrees / total

    # Энтропия
    H = 0.0
    for p in probs:
        if p > 0:
            H -= p * np.log2(p)

    # Максимальная энтропия и нормированная сложность
    h_max = np.log2(len(uniq_list)) if len(uniq_list) > 1 else 0.0
    h = H / h_max if h_max > 0 else 0.0

    return round(float(H), 1), round(float(h), 1)

