import pandas as pd

# Функция принимает Е - путь к csv и er - корневой узел
def task_1(E, er):
    # Создадим пустой список для будущих матриц
    lists = []

    # Прочтем файл
    graph = pd.read_csv(E, header=None, dtype=int)

    # Вычленим все уникальные узлы в список
    uniq_list = sorted(set(graph[0]).union(set(graph[1])))

    # Строим симметричную матрицу смежности 
    adjacency_m = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    for u, v in graph.values:
        adjacency_m.loc[u, v] = 1
        adjacency_m.loc[v, u] = 1
    lists.append(adjacency_m.values.tolist())

    # Строим матрицу инцидентности r1 - прямое управление
    r1_m = adjacency_m.copy()
    for i in uniq_list:
        if adjacency_m.loc[i, er] == 1:
            for j in uniq_list:
                if j != er:
                    r1_m.loc[j, i] = 0
        for k in uniq_list:
            r1_m.loc[k, er] = 0

    lists.append(r1_m.values.tolist())


    # Строим матрицу инцидентности r2 - прямое подчинение
    r2_m = adjacency_m - r1_m
    lists.append(r2_m.values.tolist())

    # Строим матрицу инцидентности r3 - опосредованное управление
    r3_m = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    for i in uniq_list:
        if r1_m.loc[er, i] == 1:
            r3_m.loc[er] += r1_m.loc[i]
    
    for j in uniq_list:
        if r1_m.loc[er, j] == 1:
            local_er = j
            for k in uniq_list:
                if r1_m.loc[local_er, k] == 1:
                    r3_m.loc[local_er] += r1_m.loc[k]

    lists.append(r3_m.values.tolist())
    
    # Строим матрицу инцидентности r4 - опосредованное подчинение
    r4_m = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    for i in uniq_list:
        for j in uniq_list:
            if r2_m.loc[i, j] == 1 and j != er:
                r4_m.loc[i] = r2_m.loc[j]

    lists.append(r4_m.values.tolist())

    # Строим матрицу инцидентности r5 - соподчинение
    r5_m = pd.DataFrame(0, index=uniq_list, columns=uniq_list, dtype=int)
    l = []

    for i in uniq_list:
        if r2_m.loc[:, i].sum() > 1:
            for j in uniq_list:
                if r2_m.loc[j, i] == 1:
                    l.append(j)
            for el1 in l:
                for el2 in l:
                    if el1 != el2:
                        r5_m.loc[el1, el2] = 1
            l.clear()

    lists.append(r5_m.values.tolist())
            
    # Возвращение списка полученных матриц
    return lists
