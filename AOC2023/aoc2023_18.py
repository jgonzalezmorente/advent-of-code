from functools import reduce

def calc_area(band):
    return reduce(lambda area, i: area + (band[i][0] - band[i-1][0]) * band[i][1] ,range(1, len(band)), 0)

if __name__ == '__main__':
    inputs = 'inputs/day18.txt'
    sample = 'samples/day18.txt'

    file = inputs
    trench = [
        {'square': ((0, 0), (1, 0), (1, 1), (0, 1)), 'color': '', 'direction': '', 'length': 0}
    ]

    # Part I
    with open(file) as f:
        for line in f:
            line = line.strip()
            direction, length, color = line.split()
            length = int(length)
            color = color.strip('()')
            current_square = trench[-1]['square']
            trench[-1]['direction'] = direction
            trench[-1]['length'] = length
            match direction:
                case 'U':
                    next_square = tuple((x, y + length) for (x, y) in current_square)
                case 'D':
                    next_square = tuple((x, y - length) for (x, y) in current_square)
                case 'L':
                    next_square = tuple((x - length, y) for (x, y) in current_square)
                case 'R':
                    next_square = tuple((x + length, y) for (x, y) in current_square)
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

    band1 = []
    band2 = []
    for i, t in enumerate(trench):
        p = trench[i - 1]
        match (p['direction'], t['direction']):
            case('U', 'L'):
                a = t['square'][0]
                b = t['square'][2]

            case('U', 'R'):
                a = t['square'][1]
                b = t['square'][3]

            case('D', 'L'):
                a = t['square'][1]
                b = t['square'][3]

            case('D', 'R'):
                a = t['square'][0]
                b = t['square'][2]

            case('L', 'U'):
                a = t['square'][0]
                b = t['square'][2]

            case('L', 'D'):
                a = t['square'][1]
                b = t['square'][3]

            case('R', 'U'):
                a = t['square'][1]
                b = t['square'][3]

            case('R', 'D'):
                a = t['square'][0]
                b = t['square'][2]

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

    area = max(calc_area(band1), calc_area(band2))
    print(area)




