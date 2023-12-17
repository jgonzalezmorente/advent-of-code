from typing import Tuple, Dict, Set, List
from typing import TypeAlias
from functools import reduce

Z_2: TypeAlias = Tuple[int, int]
PipeNetworkType: TypeAlias = Dict[ Z_2, str ]

class Loop:
    pipe_network: PipeNetworkType = {}
    __position: Z_2
    direction_vector: Z_2
    path: List[ Z_2 ]    

    def __init__( self, start_point: Z_2 ) -> None:
        self.path = [ start_point ]
        self.__init_point()        

    @property
    def position( self ) -> Z_2:
        return self.__position
    
    @position.setter
    def position( self, point: Z_2 ):
        self.__position = point
        self.path.append( self.__position )

    def __init_point( self ) -> None:
        point = ( self.path[0][0], self.path[0][1] - 1 )
        north = Loop.pipe_network.get( point )
        if north and north in [ '|', '7', 'F' ]:
            self.position = point
            match north:
                case '|':
                    self.direction_vector = (0, -1)
                case '7':
                    self.direction_vector = (-1, -1)
                case 'F':
                    self.direction_vector = (1, -1)
            return
        
        point = ( self.path[0][0], self.path[0][1] + 1 )
        south = Loop.pipe_network.get( point )
        if south and south in [ '|', 'L', 'J' ]:
            self.position = point
            match south:
                case '|':
                    self.direction_vector = (0, 1)
                case 'L':
                    self.direction_vector = (1, 1)
                case 'J':
                    self.direction_vector = (-1, 1)
            return

        point = ( self.path[0][0] + 1, self.path[0][1] )
        east = Loop.pipe_network.get( point )
        if east and east in [ '-', 'J', '7' ]:
            self.position = point
            match east:
                case '-':
                    self.direction_vector = (1, 0)
                case 'J':
                    self.direction_vector = (1, -1)
                case '7':
                    self.direction_vector = (1, 1)
            return

        point = ( self.path[0][0], self.path[0][1] + 1 )
        west = Loop.pipe_network.get( point )
        if west and west in [ '-', 'L', 'F' ]:
            self.position = point
            match west:
                case '-':
                    self.direction_vector = (-1, 0)
                case 'L':
                    self.direction_vector = (-1, -1)
                case 'F':
                    self.direction_vector = (-1, 1)
            return

    def __str__( self ) -> str:
        return f'{Loop.pipe_network[ self.position ]}{ self.position } (vector: { self.direction_vector })'
        
    def __iter__( self ) -> 'Loop':
        return self
    
    def __next__( self ):        
        match Loop.pipe_network[ self.position ]:
            case '|':
                next_direction_vector = ( 0, self.direction_vector[1] )
            case '-':
                next_direction_vector = ( self.direction_vector[0], 0 )
            case 'L':
                if self.direction_vector[1] == 1:
                    next_direction_vector = ( 1, 0 )
                elif self.direction_vector[0] == -1:
                    next_direction_vector = ( 0, -1 )
            case 'J':
                if self.direction_vector[1] == 1:
                    next_direction_vector = ( -1, 0 )
                elif self.direction_vector[0] == 1:
                    next_direction_vector = ( 0, -1 )
            case '7':
                if self.direction_vector[0] == 1:
                    next_direction_vector = ( 0, 1 )
                elif self.direction_vector[1] == -1:
                    next_direction_vector = ( -1, 0 )
            case 'F':
                if self.direction_vector[0] == -1:
                    next_direction_vector = ( 0, 1 )
                elif self.direction_vector[1] == -1:
                    next_direction_vector = ( 1, 0 )
            case 'S':
                 raise StopIteration
            case _:
                raise Exception
            
        next_position = ( self.position[0] + next_direction_vector[0], self.position[1] + next_direction_vector[1] )

        self.position = next_position
        self.direction_vector = next_direction_vector        

        return self

if __name__ == '__main__':

    inputs = 'inputs/day10.txt'
    sample = 'samples/day10.txt'

    file = inputs
    
    start_point: Z_2
    with open( file ) as f:
        for row, line in enumerate(f):
            for column, value in enumerate( line.strip() ):
                point = ( column, row )
                if value == 'S':
                    start_point = point
                Loop.pipe_network[ point ] = value        
       
    # Part I
    loop = Loop( start_point )
    list( loop )    
    steps = ( len(loop.path) - 1 ) // 2
    print( steps )

    # Part II
    area = 0
    for k in range( len( loop.path ) - 1 ):
        area += ( loop.path[k+1][0] - loop.path[k][0] ) * loop.path[k][1]
    
    area = abs( area )
    print( area - steps + 1 )



    