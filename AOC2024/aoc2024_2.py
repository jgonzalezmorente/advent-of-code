from functools import partial

def read_and_parse_file(file_path):
    with open(file_path, 'r') as f:
        return [[int(n) for n in line.strip().split()] for line in f]

def sign(x):
    return (x > 0) - (x < 0)

def validate_report(report):
    first_sign = sign(report[1] - report[0])
    false_indexes = [
        i for i in range(1, len(report))
        if not (sign(report[i] - report[i-1]) == first_sign and
                report[i] != report[i-1] and
                1<= abs(report[i] - report[i-1]) <= 3)
    ]
    return false_indexes

def is_safe(report, p2=False):
    false_indexes = validate_report(report)
    if not p2:
        return len(false_indexes) == 0

    if len(false_indexes) == 0:
        return True

    for j in range(len(report)):
        modified_report = report[:j] + report[j+1:]
        if is_safe(modified_report):
            return True
    return False

if __name__ == '__main__':
    inputs = 'inputs/day2.txt'
    sample = 'samples/day2.txt'

    reports = read_and_parse_file(inputs)
    print(f'Parte I: {sum(map(is_safe, reports))}')
    print(f'Parte II: {sum(map(partial(is_safe, p2=True), reports))}')