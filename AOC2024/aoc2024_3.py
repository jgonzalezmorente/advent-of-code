from functools import reduce
import re

def read_and_parse_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return ''.join([line.strip() for line in f])
    except FileNotFoundError:
        print(f'Error: El archivo {file_path} no se encontró')

def get_sum_mul(memory):
    pattern = r'mul\((\d+),\s*(\d+)\)'
    matches = re.findall(pattern, memory)
    return reduce(lambda acc, x: acc + int(x[0]) * int(x[1]), matches, 0)

if __name__ == '__main__':
    inputs = 'inputs/day3.txt'
    sample = 'samples/day3.txt'

    memory = read_and_parse_file(inputs)
    print(get_sum_mul(memory))

    pattern = r"don't\(\).*?do\(\)"
    memory = re.sub(pattern, '', memory)
    print(get_sum_mul(memory))