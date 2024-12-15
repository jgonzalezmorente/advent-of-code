from copy import deepcopy
def read_and_parse_file(file_path):
    equations = []
    with open(file_path, 'r') as f:
        for line in f:
            result, numbers = line.strip().split(':')
            equations.append((int(result), [int(x) for x in numbers.split()]))
    return equations

def equation_is_valid(result, numbers, p2=False):
    if not numbers:
        return False
    if len(numbers) == 1:
        return result == numbers[0]
    if len(numbers) == 2:
        results = [numbers[0] + numbers[1], numbers[0] * numbers[1]]
        if not p2:
            return result in results
        results.append(int(str(numbers[0]) + str(numbers[1])))
        return result in results

    n = numbers.pop(0)
    m = numbers.pop(0)
    numbers_prod = numbers.copy()
    numbers_concat = numbers.copy()
    numbers.insert(0, n + m)
    numbers_prod.insert(0, n * m)
    is_valid = equation_is_valid(result, numbers, p2) or equation_is_valid(result, numbers_prod, p2)
    if not p2:
        return is_valid
    numbers_concat.insert(0, int(str(n) + str(m)))
    return is_valid or equation_is_valid(result, numbers_concat, p2)


if __name__ == '__main__':
    inputs = 'inputs/day7.txt'
    sample = 'samples/day7.txt'

    equations = read_and_parse_file(inputs)
    result = sum([result for result, numbers in deepcopy(equations) if equation_is_valid(result, numbers)])
    print(result)

    result = sum([result for result, numbers in equations if equation_is_valid(result, numbers, True)])
    print(result)
