import pandas as pd

def main(path):
    graph = pd.read_csv(path, header=None, dtype=int)
    uniq_list = sorted(set(graph[0]).union(set(graph[1])))
    matrix = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    for u, v in graph.values:
        matrix.loc[u, v] = 1
        matrix.loc[v, u] = 1
    return matrix
