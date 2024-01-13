from typing import TypeAlias, Tuple, Dict, List
from abc import ABC, abstractmethod
from copy import deepcopy

N_2: TypeAlias = Tuple[int, int]
DimensionType: TypeAlias = N_2 | None

class Rock(ABC):
    position: N_2
    shape: str

    def __init__(self, x: int, y: int, shape: str) -> None:        
        self.position = (x, y)
        self.shape = shape

    @abstractmethod
    def move( self, direction: N_2 ) -> None:
        pass

    def __eq__(self, rock: object ) -> bool:
        if not isinstance( rock, Rock ):
            return NotImplemented
        return self.shape == rock.shape and self.position == rock.position

class RoundedRock( Rock ):
    def __init__( self, x: int, y: int ) -> None:
        super().__init__(x, y, 'O')

    def move( self, direction: N_2 ) -> None:
        self.position = ( self.position[0] + direction[0], self.position[1] + direction[1] )

class CubeRock( Rock ):
    def __init__(self, x: int, y: int ) -> None:
        super().__init__(x, y, '#')

    def move(self, direction: N_2 ) -> None:
        pass

class Platform:
    rocks: Dict[ N_2, Rock ]
    dimension: DimensionType

    @property
    def total_load( self ) -> int:        
        return sum( map( lambda rock: self.dimension[1] - rock.position[1] if self.dimension and isinstance(rock, RoundedRock) else 0, self.rocks.values() ) )                

    def __init__(self) -> None:
        self.rocks = {}
        self.dimension = None

    def add_rock( self, rock: Rock ) -> None:
        self.rocks[ rock.position ] = rock
        if not self.dimension:
            self.dimension = ( rock.position[0] + 1, rock.position[1] + 1 )
        else:
            self.dimension = ( max( self.dimension[0], rock.position[0] + 1 ), max( self.dimension[1], rock.position[1] + 1 ) )
    
    def __move( self, rock: Rock, direction: N_2 ) -> None:
        del self.rocks[ rock.position ]
        rock.move( direction )
        self.rocks[ rock.position ] = rock

    def move_one_step( self, rock_position: N_2, direction: N_2, chained: bool = False ) -> bool:        
        assert( rock_position in self.rocks and self.dimension and max( abs(direction[0]), abs(direction[1]) ) == 1 )        
        rock = self.rocks[ rock_position ]
        if isinstance( rock, CubeRock ):
            return False

        target_position = ( rock_position[0] + direction[0], rock_position[1] + direction[1] )
        if target_position[0] >= self.dimension[0] or target_position[0] < 0 or target_position[1] >= self.dimension[1] or target_position[1] < 0 or isinstance( self.rocks.get( target_position ), CubeRock ):
            return False
                
        if not target_position in self.rocks:
            self.__move( rock, direction )
            return True

        if not chained:
            return False

        if chained:
            movement_made = self.move_one_step( target_position, direction, chained )
            if not movement_made:
                return False

            self.__move( rock, direction )
            return True
    
    def slide_rock( self, rock_position: N_2, direction: N_2, chained: bool = False ) -> None:
        rock = self.rocks[ rock_position ]
        while self.move_one_step( rock.position, direction, chained ):
            pass
    
    def slide( self, direction: N_2, chained: bool = False ) -> None:
        assert self.dimension
        for y in range(self.dimension[1]):
            for x in range(self.dimension[0]):
                key = self.__get_key( x, y, direction )
                if key in self.rocks:
                    self.slide_rock( key, direction, chained )
    
    def __get_key( self, x: int, y: int, direction ):
        assert self.dimension
        match direction:
            case (0, -1):
                return (x, y)
            case (-1, 0):
                return (x, y)
            case (0, 1):
                return ( x, self.dimension[1] - y - 1 )
            case (1, 0):
                return ( self.dimension[0] - x - 1, y )
    
    def __eq__(self, platform: object) -> bool:
        if not isinstance( platform, Platform ):
            return NotImplemented
        return self.rocks == platform.rocks and self.dimension == platform.dimension        
    
if __name__ == '__main__':
    
    inputs = 'inputs/day14.txt'
    sample = 'samples/day14.txt'

    file = inputs

    original_platform = Platform()    
    with open( file ) as f:
        for y, line in enumerate(f):
            line = line.strip()
            for x, r in enumerate( line ):
                match r:
                    case 'O':
                        original_platform.add_rock( RoundedRock(x, y) )
                    case '#':
                        original_platform.add_rock( CubeRock(x, y) )
    
    # Part I
    platform = deepcopy( original_platform )
    platform.slide((0, -1))
    print( platform.total_load )

    # Part II
    cycle: List[ Platform ] = []
    
    platform = deepcopy( original_platform )    
    while not platform in cycle:        
        cycle.append( deepcopy( platform ) )        
        for direction in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            platform.slide( direction )

    n = cycle.index( platform )    
    m = n + ( 1000000000 - n ) % ( len( cycle ) - n )
    print( cycle[m].total_load )