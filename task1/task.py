import pandas as pd
from typing import List, Tuple

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    graph = pd.read_csv(s, header=None, dtype=int)
    uniq_list = sorted(set(graph[0]).union(set(graph[1])))

    # Матрица смежности
    adjacency_m = pd.DataFrame(False, index=uniq_list, columns=uniq_list, dtype=bool)
    for u, v in graph.values:
        adjacency_m.loc[u, v] = True
        adjacency_m.loc[v, u] = True

    # r1 — прямое управление
    r1_m = adjacency_m.copy()
    for i in uniq_list:
        if adjacency_m.loc[i, e]:
            for j in uniq_list:
                if j != e:
                    r1_m.loc[j, i] = False
        for k in uniq_list:
            r1_m.loc[k, e] = False

    # r2 — прямое подчинение
    r2_m = adjacency_m & (~r1_m)

    # r3 — опосредованное управление
    r3_m = pd.DataFrame(False, index=uniq_list, columns=uniq_list, dtype=bool)
    for i in uniq_list:
        if r1_m.loc[e, i]:
            r3_m.loc[e] |= r1_m.loc[i]

    for j in uniq_list:
        if r1_m.loc[e, j]:
            local_e = j
            for k in uniq_list:
                if r1_m.loc[local_e, k]:
                    r3_m.loc[local_e] |= r1_m.loc[k]

    # r4 — опосредованное подчинение
    r4_m = pd.DataFrame(False, index=uniq_list, columns=uniq_list, dtype=bool)
    for i in uniq_list:
        for j in uniq_list:
            if r2_m.loc[i, j] and j != e:
                r4_m.loc[i] |= r2_m.loc[j]

    # r5 — соподчинение
    r5_m = pd.DataFrame(False, index=uniq_list, columns=uniq_list, dtype=bool)
    l = []
    for i in uniq_list:
        if r2_m.loc[:, i].sum() > 1:
            for j in uniq_list:
                if r2_m.loc[j, i]:
                    l.append(j)
            for el1 in l:
                for el2 in l:
                    if el1 != el2:
                        r5_m.loc[el1, el2] = True
            l.clear()

    return (
        r1_m.values.tolist(),
        r2_m.values.tolist(),
        r3_m.values.tolist(),
        r4_m.values.tolist(),
        r5_m.values.tolist()
    )
