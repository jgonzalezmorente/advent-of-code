import numpy as np

def read_and_parse_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [list(line.strip()) for line in f]
    except FileNotFoundError:
        print(f'Error: El archivo {file_path} no se encontró')
        return []

def is_within_bounds(shape, x, y):
    return 0 <= x < shape[0] and 0 <= y < shape[1]

def get_neighbors_with_condition(word_search, i, j, char):
    neighbors = []
    for k in range(-1, 2):
        for s in range(-1, 2):
            x, y = i + k, j + s
            if (k != 0 or s != 0) and is_within_bounds(word_search.shape, x, y) and word_search[x, y] == char:
                neighbors.append((x, y))
    return neighbors

def count_pattern_X(word_search):
    indexes_starting_with_X = np.where(word_search == 'X')
    result = 0
    for i, j in zip(indexes_starting_with_X[0], indexes_starting_with_X[1]):
        neighbors = get_neighbors_with_condition(word_search, i, j, 'M')
        for p in neighbors:
            values = []
            for k in range(1, 3):
                q = (p[0] + k * (p[0] - i), p[1] + k * (p[1] - j))
                if is_within_bounds(word_search.shape, q[0], q[1]):
                    values.append(word_search[q[0], q[1]])
            if values == ['A', 'S']:
                result += 1
    return result

def count_pattern_A(word_search):
    indexes_starting_with_A = np.where(word_search == 'A')
    result = 0
    for i, j in zip(indexes_starting_with_A[0], indexes_starting_with_A[1]):
        values = []
        for di, dj in [(-1, 1), (1, -1), (1, 1), (-1, -1)]:
            x, y = i + di, j + dj
            if not is_within_bounds(word_search.shape, x, y):
                break
            values.append(word_search[x, y])
        if (values[:2] == ['M', 'S'] or values[:2] == ['S', 'M']) and (values[2:] == ['M', 'S'] or values[2:] == ['S', 'M']):
            result += 1
    return result

if __name__ == '__main__':
    inputs = 'inputs/day4.txt'
    sample = 'samples/day4.txt'

    word_search = np.array(read_and_parse_file(inputs))

    result_X = count_pattern_X(word_search)
    print(f'Parte 1 (XMAS): {result_X}')

    result_A = count_pattern_A(word_search)
    print(f'Parte 2 (X-MAX): {result_A}')