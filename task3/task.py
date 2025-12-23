import json
import numpy as np

def build_mat(rank, n):
    # приводим ранжировку к списку групп
    groups = []
    for x in rank:
        groups.append(x if isinstance(x, list) else [x])

    m = np.zeros((n, n), dtype=int)

    # заполняем матрицу предпочтений
    for i, gi in enumerate(groups):
        for j, gj in enumerate(groups):
            if i <= j:
                for a in gi:
                    for b in gj:
                        m[a - 1][b - 1] = 1

    for i in range(n):
        m[i][i] = 1

    return m

def close_transitive(m):
    # транзитивное замыкание
    n = len(m)
    res = m.copy()

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if res[i][k] and res[k][j]:
                    res[i][j] = 1

    return res

def find_groups(m):
    # ищем эквивалентные элементы
    n = len(m)
    used = [False] * n
    groups = []

    for i in range(n):
        if used[i]:
            continue

        cur = []
        for j in range(n):
            if m[i][j] and m[j][i]:
                cur.append(j + 1)
                used[j] = True

        groups.append(cur)

    return groups


def main(a_json, b_json):
    a = json.loads(a_json)
    b = json.loads(b_json)

    # собираем все объекты
    objs = set()
    for r in (a, b):
        for x in r:
            if isinstance(x, list):
                objs.update(x)
            else:
                objs.add(x)

    n = max(objs)

    # матрицы для двух экспертов
    A = build_mat(a, n)
    B = build_mat(b, n)

    AT = A.T
    BT = B.T

    # согласие и его обратная версия
    AB = np.logical_and(A, B).astype(int)
    AB_t = np.logical_and(AT, BT).astype(int)

    # ядро противоречий
    kernel = []
    for i in range(n):
        for j in range(i + 1, n):
            if AB[i][j] == 0 and AB_t[i][j] == 0:
                kernel.append([i + 1, j + 1])

    # итоговая матрица порядка
    C = AB.copy()

    # пары из ядра считаем эквивалентными
    for i, j in kernel:
        i -= 1
        j -= 1
        C[i][j] = 1
        C[j][i] = 1

    # эквивалентность и замыкание
    E = np.logical_and(C, C.T).astype(int)
    E = close_transitive(E)

    # получаем кластеры
    clusters = find_groups(E)

    # порядок между кластерами
    k = len(clusters)
    order = np.zeros((k, k), dtype=int)

    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            x = clusters[i][0] - 1
            y = clusters[j][0] - 1
            if C[x][y]:
                order[i][j] = 1

    # простая топологическая сортировка
    used = [False] * k
    seq = []

    def dfs(v):
        used[v] = True
        for u in range(k):
            if order[v][u] and not used[u]:
                dfs(u)
        seq.append(v)

    for i in range(k):
        if not used[i]:
            dfs(i)

    seq.reverse()

    # собираем финальную ранжировку
    result = []
    for i in seq:
        g = clusters[i]
        result.append(g[0] if len(g) == 1 else g)

    return json.dumps({
        "kernel": kernel,
        "consistent_ranking": result
    })
