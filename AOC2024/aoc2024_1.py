from functools import reduce
from collections import Counter

def read_and_parse_file(file_path):
    list1, list2 = [], []
    with open(file_path, 'r') as f:
        for line in f:
            values = line.strip().split()
            list1.append(int(values[0]))
            list2.append(int(values[1]))
    return list1, list2

def calculate_difference_sum(list1, list2):
    return reduce(lambda acc, x: acc + abs(x[1] - x[0]), zip(sorted(list1), sorted(list2)), 0)

def calculate_sum_products_frequencies(list1, list2):
    counter2 = Counter(list2)
    return reduce(lambda acc, x: acc + x * counter2.get(x, 0), list1, 0)

if __name__ == '__main__':
    inputs = 'inputs/day1.txt'
    sample = 'samples/day1.txt'

    list1, list2 = read_and_parse_file(inputs)
    if not list1 or not list2:
        print('No hay datos')
        exit

    print(f'Parte I: {calculate_difference_sum(list1, list2)}')
    print(f'Parte II: {calculate_sum_products_frequencies(list1, list2)}')

