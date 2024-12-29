from itertools import chain
from typing import Dict

class Plot:
    def __init__(self, x, y):
        self.point = (x, y)

    def __eq__(self, value):
        if isinstance(value, Plot):
            return self.point == value.point
        return False

    @property
    def corners(self):
        x, y = self.point
        return [(x + dx, y + dy) for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1)]]

class Region:
    def __init__(self, plant_type, initial_plot):
        self.plant_type = plant_type
        self.perim = 0
        self.plots = []
        self.left_sides = []
        self.right_sides = []
        self.top_sides = []
        self.bottom_sides = []
        self.add(initial_plot)

    @property
    def area(self):
        return len(self.plots)

    @property
    def price(self):
        return self.area * self.perim

    def intersects_to(self, plot: Plot):
        #return not set(chain.from_iterable(p.corners for p in self.plots)).isdisjoint(plot.corners)
        _, _, _, _, count = self.get_adjacent(plot)
        return count > 0

    def get_adjacent(self, plot: Plot):
        corners = plot.corners
        top = {corners[0], corners[1]}
        right = {corners[1], corners[2]}
        bottom = {corners[2], corners[3]}
        left = {corners[3], corners[0]}
        return top, right, bottom, left, sum(
            side in set_side for side, set_side in zip(
                [top, right, bottom, left],
                [self.bottom_sides, self.left_sides, self.top_sides, self.right_sides]
            )
        )

    def add(self, plot: Plot):
        self.plots.append(plot)
        top, right, bottom, left, count = self.get_adjacent(plot)
        self.perim += (4 - 2 * count)
        self.top_sides.append(top)
        self.right_sides.append(right)
        self.bottom_sides.append(bottom)
        self.left_sides.append(left)

def read_and_parse_file(file_path):
    garden: Dict[str, Region] = {}
    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            for x, value in enumerate(line.strip()):
                plot = Plot(x, y)
                initial_region = Region(value, plot)
                if not value in garden:
                    garden[value] = [initial_region]
                else:
                    intersecting_regions = []
                    disjoin_regions = []
                    for region in garden[value]:
                        if region.intersects_to(plot):
                            intersecting_regions.append(region)
                        else:
                            disjoin_regions.append(region)
                    region_union = None
                    if intersecting_regions:
                        region_union = intersecting_regions[0]
                        for r in intersecting_regions[1:]:
                            region_union.plots.extend(r.plots)
                            region_union.perim += r.perim
                            region_union.top_sides.extend(r.top_sides)
                            region_union.right_sides.extend(r.right_sides)
                            region_union.bottom_sides.extend(r.bottom_sides)
                            region_union.left_sides.extend(r.left_sides)
                        region_union.add(plot)
                    else:
                        disjoin_regions.append(initial_region)
                    garden[value] = disjoin_regions + [region_union] if region_union else disjoin_regions
    return garden


if __name__ == '__main__':
    inputs = 'inputs/day12.txt'
    sample = 'samples/day12.txt'

    garden = read_and_parse_file(inputs)
    print(sum(region.price for region in chain.from_iterable(garden.values())))