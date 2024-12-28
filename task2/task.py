import csv
import pandas as pd
import numpy as np
def create_tree(edges, n):
    tree = {i: [] for i in range(1, n + 1)}

    for parent, child in edges:
        tree[parent].append(child)

    return tree
def calculate_r1(tree,n):

    # Вычисляем r1 - количество потомков для каждого узла
    r1 = [0] * n
    for node in tree:
        r1[node - 1] = len(tree[node])

    return r1


def calculate_r2(edges, n):
    # Инициализируем список, где будем хранить количество родителей для каждого узла
    r2 = [0] * n

    # Проходим по списку рёбер и обновляем количество родителей для каждого узла
    for parent, child in edges:
        r2[child - 1] = 1  # Устанавливаем, что у узла child есть 1 родитель

    return r2


def calculate_r3(edges, n):

    # Вычисляем r3 - количество внуков для каждого узла
    r3 = [0] * n
    for node in range(1, n + 1):
        # Считаем количество внуков
        grandchildren = 0
        for child in tree[node]:
            grandchildren += len(tree[child])  # Дети детей - это внуки
        r3[node - 1] = grandchildren

    return r3


def calculate_r4(edges, n):
    # Создаем словарь для хранения родителей
    parents = {i: None for i in range(1, n + 1)}

    # Заполняем родителей из списка рёбер
    for parent, child in edges:
        parents[child] = parent

    # Вычисляем r4 - количество дедов для каждого узла
    r4 = [0] * n
    for node in range(1, n + 1):
        grandparent = parents.get(parents[node], None)  # Находим родителя родителя (деда)
        if grandparent is not None:
            r4[node - 1] = 1  # Если у узла есть дед, ставим 1, иначе 0

    return r4


def calculate_r5(tree, n):

    # Вычисляем r5 - количество братьев для каждого узла
    r5 = [0] * n
    for node in range(1, n + 1):
        parent = None
        # Ищем родителя узла
        for p in tree:
            if node in tree[p]:
                parent = p
                break
        if parent is not None:
            # Количество братьев - общее количество детей минус один (сам узел)
            r5[node - 1] = len(tree[parent]) - 1

    return r5

def read_edges_from_csv(filename):
    edges = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # Преобразуем строки в целые числа и добавляем в список рёбер
            edges.append((int(row[0]), int(row[1])))
    return edges

# Входные данные
# edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
edges = read_edges_from_csv('task2.csv')
n = 5  # Количество узлов
tree = create_tree(read_edges_from_csv('task2.csv'), n)

# Вычисляем r1,r2,r3,r4,r5
result_r1 = calculate_r1(tree, n)
result_r2 = calculate_r2(edges, n)
result_r3 = calculate_r3(tree, n)
result_r4 = calculate_r4(edges, n)
result_r5 = calculate_r5(tree, n)
final = [result_r1, result_r2, result_r3, result_r4, result_r5]

# Создаем DataFrame из массива
df = pd.DataFrame(final, columns=['1', '2', '3', '4', '5'], index=['A', 'B', 'C', 'D', 'E'])
df=df.T
df.to_csv('output.csv', index=True)
