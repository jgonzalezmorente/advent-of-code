import numpy as np

def read_and_parse_file(file_path):
    with open(file_path, 'r') as f:
        return [int(x) for x in f.readline().strip()]

if __name__ == '__main__':
    inputs = 'inputs/day9.txt'
    sample = 'samples/day9.txt'

    # Part 1
    disk_map = read_and_parse_file(inputs)
    blocks = np.full(sum(disk_map), -1, dtype=int)
    s = 0
    for i, v in enumerate(disk_map):
        if i % 2 == 0:
            file_id = i // 2
            blocks[s:s+v] = file_id
        s += v

    blocks_p1 = blocks.copy()
    idx_free_space = np.where(blocks_p1 == -1)[0]
    idx_files = np.where(blocks_p1 != -1)[0]
    for id_file, id_free_space in zip(idx_files[::-1], idx_free_space):
        blocks_p1[id_free_space] = blocks_p1[id_file]
        blocks_p1[id_file] = -1
        if np.max(np.where(blocks_p1 != -1)[0]) <= np.min(np.where(blocks_p1 == -1)[0]):
            break

    blocks_p1 = blocks_p1[blocks_p1 != -1]
    print(np.dot(blocks_p1, np.arange(len(blocks_p1))))

    # Part 2
    unique_values = np.unique(blocks)
    indices_dict = {value: np.where(blocks == value)[0] for value in unique_values}
    indices_dict = dict(sorted(indices_dict.items(), key=lambda item: item[0], reverse=True))

    free_spaces = indices_dict.pop(-1, [])
    free_space_count = []
    count = 1
    value = free_spaces[0]
    for i in  range(1, len(free_spaces)):
        if free_spaces[i] == free_spaces[i-1] + 1:
            count += 1
        else:
            free_space_count.append(np.array([value, count]))
            value = free_spaces[i]
            count = 1
    free_space_count.append([value, count])

    for file_id, blocks_idx in indices_dict.items():
        fs = next((x for x in free_space_count if x[1] >= len(blocks_idx) and sum(x) <= blocks_idx[0]), None)
        if not fs is None:
            for k in range(len(indices_dict[file_id])):
                indices_dict[file_id][k] = fs[0] + k
            fs[0] += len(indices_dict[file_id])
            fs[1] -= len(indices_dict[file_id])
    s = 0
    for k, v in indices_dict.items():
        s += k * sum(v)
    print(s)
