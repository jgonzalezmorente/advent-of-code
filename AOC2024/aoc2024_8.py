from collections import defaultdict
from itertools import combinations
from math import gcd

class Point:
    def __init__(self, x: int, y: int, value: str):
        self.x = x
        self.y = y
        self.value = value
        self.is_antinode = False

    def is_antenna(self) -> bool:
        return any([self.value.islower(), self.value.isupper(), self.value.isdigit()])

    def __str__(self):
        return f'({self.x}, {self.y}) -> {self.value}'


def read_and_parse_file(file_path):
    city = {}
    antennas = defaultdict(list)
    try:
        with open(file_path, 'r') as f:
            for y, line in enumerate(f):
                for x, value in enumerate(list(line.strip())):
                    point = Point(x, y, value)
                    city[(x,y)] = point
                    if point.is_antenna():
                        antennas[point.value].append(point)

        return city, antennas
    except FileNotFoundError:
        print(f'Error: El archivo {file_path} no se encontró.')
        return None
    except Exception as e:
        print(f"Error inesperado al leer el archivo {file_path}: {e}")
        return None


if __name__ == '__main__':
    inputs = 'inputs/day8.txt'
    sample = 'samples/day8.txt'

    city, antennas = read_and_parse_file(inputs)
    for group in antennas.values():
        for start, end in combinations(group, 2):
            vector = (end.x - start.x, end.y - start.y)
            endpoint = (end.x + vector[0], end.y + vector[1])
            startpoint = (start.x - vector[0], start.y - vector[1])
            if endpoint in city:
                city[endpoint].is_antinode = True
            if startpoint in city:
                city[startpoint].is_antinode = True

    print(sum([point.is_antinode for point in city.values()]))


    city, antennas = read_and_parse_file(inputs)
    for group in antennas.values():
        for start, end in combinations(group, 2):
            divisor = gcd(abs(end.x - start.x), abs(end.y - start.y))
            vector = ((end.x - start.x) // divisor, (end.y - start.y) // divisor)
            endpoint = (end.x, end.y)
            while(endpoint in city):
                city[endpoint].is_antinode = True
                endpoint = (endpoint[0] + vector[0], endpoint[1] + vector[1])

            endpoint = (end.x - vector[0], end.y - vector[1])
            while(endpoint in city):
                city[endpoint].is_antinode = True
                endpoint = (endpoint[0] - vector[0], endpoint[1] - vector[1])

    print(sum([point.is_antinode for point in city.values()]))