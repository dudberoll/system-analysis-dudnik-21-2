import pandas as pd
import math
def entropy(mat, n, k):
    entropy = 0
    for i in range(n):
        for j in range(k):
            value = mat[i][j]
            if value > 0:
                entropy -= (value / (n - 1)) * math.log2(value / (n - 1))
    return entropy

def main(file_path: str):
    # исключаем первый столбец (это индексы)
    df = pd.read_csv(file_path)
    mat = df.iloc[:, 1:].to_numpy()  # Преобразуем в NumPy матрицу

    n = len(mat)  # узлы
    k = len(mat[0])  # отношения
    # энтропия
    entropyy = entropy(mat, n, k)

    print(entropyy)

main('../task2/output.csv')
