from collections import defaultdict, deque

def read_and_parse_file(file_path):
    topographic_map = {}
    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            for x, value in enumerate(line.strip()):
                topographic_map[(x,y)] = int(value)
    size = (x,y)
    return topographic_map, size

def score(start, graph, topographic_map):
    start_value = topographic_map.get(start, None)
    if start_value != 0:
        return 0
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = 0
    while queue:
        node = queue.popleft()
        if topographic_map[node] == 9:
            result += 1
            continue
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result

def score_all_paths(start, graph, topographic_map):
    start_value = topographic_map.get(start, None)
    if start_value != 0:
        return 0
    queue = deque([[start]])
    all_paths = []
    while queue:
        path = queue.popleft()
        node = path[-1]
        if topographic_map[node] == 9:
            all_paths.append(path)
            continue
        for neighbor in graph[node]:
            if neighbor not in path:
                queue.append(path + [neighbor])
    return len(all_paths)

if __name__ == '__main__':
    inputs = 'inputs/day10.txt'
    sample = 'samples/day10.txt'

    topographic_map, size = read_and_parse_file(inputs)

    graph = defaultdict(list)
    for x, y in topographic_map:
        graph[(x,y)] = [(x + dx, y + dy) for dx, dy in {(0, -1), (1, 0), (0, 1), (-1, 0)} if 0 <= x + dx <= size[0] and 0 <= y + dy <= size[1]]
        graph[(x,y)] = [p for p in graph[(x,y)] if topographic_map[p] == topographic_map[(x,y)] + 1]

    result = sum(map(lambda node: score(node, graph, topographic_map), topographic_map))
    print(result)

    result = sum(map(lambda node: score_all_paths(node, graph, topographic_map), topographic_map))
    print(result)

