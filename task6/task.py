import json
def calculate_membership(value, fuzzy_set):
    """Вычисляет степени принадлежности для заданного значения в нечетком множестве."""
    membership_degrees = {}
    for term, points in fuzzy_set.items():
        membership = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 <= value <= x2:
                if x1 == x2:
                    membership = max(y1, y2)
                else:
                    membership = y1 + (y2 - y1) * (value - x1) / (x2 - x1)
                break
        membership_degrees[term] = membership
    return membership_degrees

def calculate_centroid(fuzzy_result, output_set):
    """Вычисляет центр тяжести для дефаззификации результата."""
    numerator = 0
    denominator = 0
    for term, degree in fuzzy_result.items():
        if degree > 0:
            points = output_set[term]
            centroid = sum([x for x, y in points]) / len(points)
            numerator += degree * centroid
            denominator += degree
    return numerator / denominator if denominator != 0 else 0


def main(input_file, regulator_file, transition_file, input_value):
    """Основная функция для выполнения нечеткого вывода и дефаззификации."""
    # Считываем входные нечеткие множества из JSON файлов
    with open(input_file, 'r', encoding='utf-8') as f:
        fuzzy_input_set = json.load(f)
    with open(regulator_file, 'r', encoding='utf-8') as f:
        fuzzy_output_set = json.load(f)
    with open(transition_file, 'r', encoding='utf-8') as f:
        transition_rules = json.load(f)

    # Вычисляем степени принадлежности для входного значения
    fuzzy_input_degrees = calculate_membership(input_value, fuzzy_input_set)
    print("Фаззифицированное значение:", fuzzy_input_degrees)

    # Применяем правила переходов для получения выходных степеней принадлежности
    fuzzy_output_degrees = {}
    for input_term, degree in fuzzy_input_degrees.items():
        if input_term in transition_rules:
            output_term = transition_rules[input_term]
            fuzzy_output_degrees[output_term] = max(fuzzy_output_degrees.get(output_term, 0), degree)
    print("Результат после применения правил переходов:", fuzzy_output_degrees)

    # Дефаззификация результата с помощью метода центра тяжести
    defuzzified_output = calculate_centroid(fuzzy_output_degrees, fuzzy_output_set)
    print("Дефаззифицированное значение:", defuzzified_output)

    return defuzzified_output


if __name__ == "__main__":
    input_value = 19.3

    input_file = "Input Sets.json"
    regulator_file = "Regulator Sets.json"
    transition_file = "Transition Rules.json"

    main(input_file, regulator_file, transition_file, input_value)
