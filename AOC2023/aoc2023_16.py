import sys
from typing import Tuple, Dict, Set

sys.setrecursionlimit(10000)

class Point:
    x: int
    y: int
    value: str
    energized: bool
    directions: Set[ Tuple[int, int] ]

    def __init__(self, x: int, y: int, value: str) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.energized = False
        self.directions = set()

class Contraption:
    points: Dict[ Tuple[int, int], Point ]
    current_position: Tuple[int, int]

    def __init__(self) -> None:
        self.points = {}        
    
    def add_point( self, point: Point ) -> None:
        self.points[ ( point.x, point.y ) ] = point
        
    def energize( self, direction: Tuple[int, int] = (1, 0), current_position: Tuple[int, int] = (-1, 0) ) -> None:
        
        next_position = ( current_position[0] + direction[0], current_position[1] + direction[1] )        
        if not next_position in self.points:
            return
        next_point = self.points[ next_position ]
        if next_point.energized and direction in next_point.directions:
            return
        next_point.energized = True
        next_point.directions.add( direction )

        match( next_point.value ):
            case '/':
                if direction == (1, 0):
                    self.energize( (0, -1), next_position )
                if direction == (0, 1):
                    self.energize( (-1, 0), next_position )
                if direction == (-1, 0):
                    self.energize( (0, 1), next_position )
                if direction == (0, -1):
                    self.energize( (1, 0), next_position )
                    
            case '\\':
                if direction == (1, 0):
                    self.energize( (0, 1), next_position )
                if direction == (0, 1):
                    self.energize( (1, 0), next_position )
                if direction == (-1, 0):
                    self.energize( (0, -1), next_position )
                if direction == (0, -1):
                    self.energize( (-1, 0), next_position )

            case '|':
                if direction == (1, 0):
                    self.energize( (0, -1), next_position )
                    self.energize( (0, 1), next_position )
                if direction == (0, 1):
                    self.energize( (0, 1), next_position )
                if direction == (-1, 0):
                    self.energize( (0, -1), next_position )
                    self.energize( (0, 1), next_position )
                if direction == (0, -1):
                    self.energize( (0, -1), next_position )
                
            case '-':
                if direction == (1, 0):
                    self.energize( (1, 0), next_position )      
                if direction == (0, 1):
                    self.energize( (-1, 0), next_position )
                    self.energize( (1, 0), next_position )
                if direction == (-1, 0):
                    self.energize( (-1, 0), next_position )                    
                if direction == (0, -1):
                    self.energize( (-1, 0), next_position )
                    self.energize( (1, 0), next_position )
            
            case '.':
                self.energize( direction, next_position )

if __name__ == '__main__':
    
    inputs = 'inputs/day16.txt'
    sample = 'samples/day16.txt'

    file = inputs

    contraption = Contraption()
    with open( file ) as f:
        for j, line in enumerate(f):            
            for i, value in enumerate(line.strip()):
                contraption.add_point( Point( i, j, value ) )
    
    # Part I
    contraption.energize()
    print( len([ point for point in contraption.points.values() if point.energized ]) )
    
    # Part 2