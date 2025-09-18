import pandas as pd

def main(path):
    graph = pd.read_csv(path, header=None)

    d = {}

    for key, val in graph.values:
        d.setdefault(key, []).append(val)

    uniq_list = list(set(graph[0]).union(set(graph[1])))

    matrix = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)

    for u, neighbors in d.items():
        for v in neighbors:
            matrix.loc[u, v] = 1

    return matrix
