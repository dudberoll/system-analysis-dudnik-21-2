import numpy as np
import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['nodes']

def main():
    nodes = read_json('task1task1/data.json')
    node_list = list(nodes.keys())
    n = len(node_list)
    adj_matrix = np.zeros((n, n))

    # заполняем матрицу
    for p, c in nodes.items():
        parent_idx = node_list.index(p)
        for child in c:
            child_idx = node_list.index(child)
            adj_matrix[parent_idx][child_idx] = 1

    print("Матрица смежности:")
    print(adj_matrix)


if __name__ == "__main__":
   main()
