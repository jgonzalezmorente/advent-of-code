from collections import defaultdict
import numpy as np

def read_and_parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [list(line.strip()) for line in lines]

def is_inside(point, shape):
    return 0 <= point[1] < shape[0] and 0 <= point[0] < shape[1]

def has_loop(guard_map):
    path = defaultdict(list)
    point = start_point.copy()
    direction = directions[guard_map[start_point[1], start_point[0]]]
    while is_inside(point, guard_map.shape):
        if direction in path[tuple(point)]:
            return True
        path[tuple(point)].append(direction)
        next_point = point + np.array(direction)
        if is_inside(next_point, guard_map.shape) and guard_map[next_point[1], next_point[0]] in ['#', 'O']:
            direction = directions[right_turns[directions_inv[direction]]]
        point += np.array(direction)
    return False

def check_loop(idx):
    i, j = idx
    guard_map_ = guard_map_original.copy()
    guard_map_[i, j] = 'O'
    return has_loop(guard_map_)

if __name__ == '__main__':
    inputs = 'inputs/day6.txt'
    sample = 'samples/day6.txt'

    guard_map_original = np.array(read_and_parse_file(sample))
    guard_map = guard_map_original.copy()
    directions = {
        '^': (0, -1),
        '<': (-1, 0),
        'v': (0, 1),
        '>': (1, 0),
    }
    directions_inv = {v: k for k, v in directions.items()}
    right_turns = {
        '^': '>',
        '>': 'v',
        'v': '<',
        '<': '^',
    }
    start_point = np.flip(np.argwhere(np.isin(guard_map, list(directions.keys())))[0])
    point = start_point.copy()
    direction = directions.get(guard_map[point[1], point[0]])
    while is_inside(point, guard_map.shape):
        guard_map[point[1], point[0]] = 'X'
        next_point = point + np.array(direction)
        if is_inside(next_point, guard_map.shape) and guard_map[next_point[1], next_point[0]] == '#':
            direction = directions[right_turns[directions_inv[direction]]]
        point += np.array(direction)
    print(np.count_nonzero(guard_map == 'X'))

    idx = np.where((guard_map == 'X') & ~((np.arange(guard_map.shape[0])[:, None] == start_point[1]) &
                                          (np.arange(guard_map.shape[1]) == start_point[0])))

    print(sum(map(check_loop, zip(idx[0], idx[1]))))
