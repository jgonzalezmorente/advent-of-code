from functools import reduce

def calc_area(band):
    return reduce(lambda area, i: area + (band[i][0] - band[i-1][0]) * band[i][1] ,range(1, len(band)), 0)

def get_next_square(current_square, direction, length):
    match direction:
        case 'U':
            return tuple((x, y + length) for (x, y) in current_square)
        case 'D':
            return tuple((x, y - length) for (x, y) in current_square)
        case 'L':
            return tuple((x - length, y) for (x, y) in current_square)
        case 'R':
            return tuple((x + length, y) for (x, y) in current_square)

def process_trench(file, p2=False):
    trench = [
        {'square': ((0, 0), (1, 0), (1, 1), (0, 1)), 'color': '', 'direction': '', 'length': 0}
    ]
    if p2:
        directions = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    with open(file) as f:
        for line in f:
            direction, length, color = line.strip().split()
            length = int(length)
            color = color.strip('()')
            if p2:
                direction = directions.get(color[-1])
                length = int(color[1:-1], 16)
            current_square = trench[-1]['square']
            trench[-1]['direction'] = direction
            trench[-1]['length'] = length
            next_square = get_next_square(current_square, direction, length)
            existing_square = next((t for t in trench if t.get('square') == next_square), None)
            if existing_square:
                existing_square['color'] = color
            else:
                trench.append({
                    'square': next_square,
                    'color': color,
                    'direction': '',
                    'length': 0,
                })
    return trench

def build_bands(trench):
    band1, band2 = [], []
    for i, t in enumerate(trench):
        p = trench[i - 1]
        match (p['direction'], t['direction']):
            case ('U', 'L') | ('D', 'R') | ('L', 'U') | ('R', 'D'):
                a = t['square'][0]
                b = t['square'][2]
            case ('U', 'R') | ('D', 'L') | ('L', 'D') | ('R', 'U'):
                a = t['square'][1]
                b = t['square'][3]
        if not band1 and not band2:
            band1.append(a)
            band2.append(b)
        elif band1 and band2:
            if (band1[-1][0] == a[0] or band1[-1][1] == a[1]):
                band1.append(a)
                band2.append(b)
            else:
                band1.append(b)
                band2.append(a)
    return band1, band2

if __name__ == '__main__':
    inputs = 'inputs/day18.txt'
    sample = 'samples/day18.txt'

    p2 = True

    file = inputs
    trench = process_trench(file, p2)
    band1, band2 = build_bands(trench)
    area = max(calc_area(band1), calc_area(band2))
    print(f'Volumen laguna: {area}')

