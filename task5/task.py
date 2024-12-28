import numpy as np
import json
def read_json(file_path):
    """Считываем JSON файл и возвращаем данные под ключом 'data'."""
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        return json_data['data']


def write_json(data, file_path):
    """Записываем данные в JSON файл с отступами для читаемости."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def build_relation_matrix(ranking, size):
    """Создаем матрицу отношений на основе заданного ранжирования."""
    relation_matrix = np.zeros((size, size), dtype=int)
    np.fill_diagonal(relation_matrix, 1)

    for index, group in enumerate(ranking):
        if isinstance(group, int):
            group = [group]

        # Устанавливаем отношения внутри текущей группы
        for item_i in group:
            for item_j in group:
                relation_matrix[item_i - 1][item_j - 1] = 1

        # Устанавливаем отношения между текущей группой и всеми предыдущими группами
        for item_i in group:
            for prev_group in ranking[:index]:
                if isinstance(prev_group, int):
                    prev_group = [prev_group]
                for item_j in prev_group:
                    relation_matrix[item_j - 1][item_i - 1] = 1

    return relation_matrix


def find_discrepancies(matrix_a, matrix_b):
    """Находим противоречия между двумя матрицами отношений."""
    size = matrix_a.shape[0]
    discrepancies = []
    for i in range(size):
        for j in range(size):
            # Противоречие типа A → B и B ↛ A
            if (matrix_a[i, j] == 1 and matrix_b[i, j] == 0 and
                matrix_a[j, i] == 0 and matrix_b[j, i] == 1):
                discrepancies.append((i + 1, j + 1))
            # Противоречие типа B → A и A ↛ B
            elif (matrix_a[i, j] == 0 and matrix_b[i, j] == 1 and
                  matrix_a[j, i] == 1 and matrix_b[j, i] == 0):
                discrepancies.append((j + 1, i + 1))
    return discrepancies


def find_core(discrepancies):
    """Формируем ядро противоречий из списка найденных противоречий."""
    core = []
    added_elements = set()

    for x, y in discrepancies:
        if any(x in group or y in group for group in core):
            for group in core:
                if x in group or y in group:
                    if x not in group:
                        group.append(x)
                    if y not in group:
                        group.append(y)
                    break
        else:
            core.append([x, y])

        added_elements.update([x, y])

    return core


def main(file_a, file_b, output_file):
    """Основная функция для выполнения программы по нахождению ядра противоречий."""
    # Считываем ранжирования из JSON файлов
    ranking_a = read_json(file_a)
    ranking_b = read_json(file_b)

    # Определяем максимальный размер для матриц отношений
    size_a = sum(len(group) if isinstance(group, list) else 1 for group in ranking_a)
    size_b = sum(len(group) if isinstance(group, list) else 1 for group in ranking_b)
    max_size = max(size_a, size_b)

    # Строим матрицы отношений для обоих ранжирований
    relation_matrix_a = build_relation_matrix(ranking_a, max_size)
    print("Матрица A:")
    print(relation_matrix_a)

    relation_matrix_b = build_relation_matrix(ranking_b, max_size)
    print("Матрица B:")
    print(relation_matrix_b)

    # Находим противоречия между матрицами
    discrepancies = find_discrepancies(relation_matrix_a, relation_matrix_b)
    print(f"Противоречия: {discrepancies}")

    # Формируем ядро противоречий
    core = find_core(discrepancies)
    print(f"Ядро противоречий: {core}")

    # Записываем результат в выходной JSON файл
    write_json({"core": core}, output_file)


if __name__ == "__main__":
    main("a.json", "b.json", "core.json")
