import re
import numpy as np
from functools import lru_cache

def read_and_parse_file(file_path):
    result = []
    with open(file_path, 'r') as f:
        current_block = []
        for line in f:
            numbers = re.findall(r'\d+', line.strip())
            current_block.extend(map(int, numbers))
            if 'Prize' in line:
                result.append(current_block)
                current_block = []
    return result

def calc_tokens_linalg(nums):
    A = np.array([nums[:2], nums[2:4]]).T
    b_ = np.array(nums[4:6])
    try:
       x = np.linalg.solve(A, b_)
    except np.linalg.LinAlgError:
        return 0

    if np.allclose(np.mod(x, 1), 0):
        x_int = x.astype(int)
        if np.any((x_int > 100) | (x_int < 0)):
            return 0
        return(np.dot(x_int, np.array([3, 1])))
    else:
        return 0

def calc_tokens_bf(nums):
    A = np.array([nums[:2], nums[2:4]]).T
    b_ = np.array(nums[4:6])

    gcd = (np.gcd.reduce(A, axis=1))
    if not (np.all(np.mod(b_, gcd) == np.zeros(2))):
        return 0

    A = A // gcd[:, None]
    b_ = b_ // gcd

    results = []
    for x in range(101):
        for y in range (101):
            if np.array_equal(np.dot(A, np.array([x, y])), b_):
                results.append(3 * x + y)
    return 0 if not results else min(results)

@lru_cache(maxsize=None)
def gcd_bezout(a, b):
    r = a % b
    if r == 0:
        return b, 0, 1
    c = a // b
    d, x, y = gcd_bezout(b, r)
    return d, y, x - c * y

def calc_tokens(nums, delta=0):
    a, b, c = nums[0], nums[2], nums[4]
    e, f, g = nums[1], nums[3], nums[5]
    c += delta
    g += delta
    d, r, s = gcd_bezout(a, b)
    if c % d != 0:
        return 0
    a, b, c = a // d, b // d, c // d
    x, y = r * c, s * c
    det = a * f - b * e
    u = g - e * x - f * y
    if u % det != 0:
        return 0
    t = u // det
    x -= t * b
    y += t * a
    if (x < 0 or y < 0):
        return 0
    return 3 * x + y

if __name__ == '__main__':
    inputs = 'inputs/day13.txt'
    sample = 'samples/day13.txt'

    prize_location = read_and_parse_file(inputs)

    print(sum(map(calc_tokens, prize_location)))
    print(sum(map(lambda nums: calc_tokens(nums, 10000000000000), prize_location)))
