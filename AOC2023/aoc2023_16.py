import sys
from typing import Tuple, Dict, Set, List
from copy import deepcopy

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
    points: Dict[Tuple[int, int], Point]
    current_position: Tuple[int, int]
    size: Tuple[int, int]

    @property
    def total_energized( self ) -> int:
        return len([ point for point in self.points.values() if point.energized ])

    def __init__(self) -> None:
        self.points = {}
        self.size = (0, 0)
    
    def add_point( self, point: Point ) -> None:
        self.points[ ( point.x, point.y ) ] = point
        if point.x + 1 > self.size[0]:
            self.size = ( point.x + 1, self.size[1] )
        if point.y + 1 > self.size[1]:
            self.size = ( self.size[0], point.y + 1 )
        
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
    contraption_copy = deepcopy( contraption )
    contraption_copy.energize()
    print( contraption_copy.total_energized )
    
    # Part 2    
    top   = [ ( ( i, -1 ), ( 0, 1 ) ) for i in range(contraption.size[0] ) ]        
    down  = [ ( ( i, contraption.size[1] ), ( 0, -1 ) ) for i in range(contraption.size[0] ) ]        
    left  = [ ( ( -1, i ), ( 1, 0 ) ) for i in range(contraption.size[1] ) ]        
    right = [ ( ( contraption.size[0], i ), ( -1, 0 ) ) for i in range(contraption.size[1] ) ]
    
    border_direction = top + down + left + right

    values: List[int] = []
    for initial_point, direction in border_direction:
        contraption_copy = deepcopy( contraption )
        contraption_copy.energize( direction = direction, current_position = initial_point )
        values.append( contraption_copy.total_energized )
    
    print(max(values) )