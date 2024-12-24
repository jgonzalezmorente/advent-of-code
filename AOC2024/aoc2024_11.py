from functools import lru_cache

def read_and_parse_file(file_path):
    with open(file_path, 'r') as f:
        return [int(x) for x in f.readline().strip().split()]

def blink(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif (len(str(stone)) % 2 == 0):
            stone_str = str(stone)
            n = len(stone_str) // 2
            new_stones.append(int(stone_str[:n]))
            new_stones.append(int(stone_str[n:]))
        else:
            new_stones.append(2024 * stone)
    return new_stones

@lru_cache(maxsize=None)
def calc_num_stones(value, depth, level=1):
    if level == depth + 1:
        return 1
    if value == 0:
        return calc_num_stones(1, depth, level = level + 1)
    value_str = str(value)
    if (len(value_str) % 2 == 0):
        n = len(value_str) // 2
        return calc_num_stones(int(value_str[:n]), depth, level = level + 1) + calc_num_stones(int(value_str[n:]), depth, level = level + 1)
    return calc_num_stones(2024 * value, depth, level = level + 1)

if __name__ == '__main__':
    inputs = 'inputs/day11.txt'
    sample = 'samples/day11.txt'

    stones = read_and_parse_file(inputs)
    for _ in range(25):
        stones = blink(stones)
    print(len(stones))

    stones = read_and_parse_file(inputs)
    print(sum(map(lambda stone: calc_num_stones(stone, 75), stones)))
