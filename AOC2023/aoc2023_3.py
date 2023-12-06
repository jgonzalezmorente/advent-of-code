from typing import Dict, TypeAlias, Tuple, Set
from functools import partial

Point: TypeAlias = Tuple[ int, int ]
Engine: TypeAlias = Dict[ Tuple, str ]
MapEngine: TypeAlias = Set[ Point ]
Parts: TypeAlias = Dict[ Tuple, int ]

def is_part_number( key: Tuple, engine: Engine, points: MapEngine ) -> bool:
    assert key in engine
    if not engine[key].isdigit():
        return False
    neighbors = set()
    for point in key:
        neighbors.add( ( point[0], point[1] + 1 ) )
        neighbors.add( ( point[0], point[1] - 1 ) )
    
    neighbors.add( ( key[-1][0] - 1, key[-1][1] ) )
    neighbors.add( ( key[-1][0] - 1, key[-1][1] + 1 ) )
    neighbors.add( ( key[-1][0] - 1, key[-1][1] - 1 ) )

    neighbors.add( ( key[0][0] + 1, key[0][1] ) )
    neighbors.add( ( key[0][0] + 1, key[0][1] + 1 ) )
    neighbors.add( ( key[0][0] + 1, key[0][1] - 1 ) )

    return not neighbors.isdisjoint( points )


def get_key_part( point: Point, parts: Parts ) -> Tuple | None:
    if ( point, ) in parts.keys():
        return ( point, )
    
    for key in parts.keys():
        if point in key:
            return key
    
    return None

def get_gear_value( key: Tuple, engine: Engine, parts: Parts ) -> int:
    assert key in engine and engine[ key ] == '*' and len( key ) == 1

    p = key[0]
    neighbors = [
        (p[0], p[1] - 1), 
        (p[0], p[1] + 1),

        (p[0] - 1, p[1]), 
        (p[0] - 1, p[1] + 1), 
        (p[0] - 1, p[1] - 1),

        (p[0] + 1, p[1]), 
        (p[0] + 1, p[1] + 1),
        (p[0] + 1, p[1] - 1), 
    ]

    f = partial( get_key_part, parts = parts )

    neighbors_parts_keys = set(filter( lambda key: key != None, map( f, neighbors ) ))
    if len( neighbors_parts_keys ) == 2:
        result = 1        
        for key in neighbors_parts_keys: # type: ignore
            result *= parts[ key ]
        return result
    
    return 0
   

if __name__ == '__main__':

    engine: Engine = {}

    inputs = 'inputs/day3.txt'
    sample = 'samples/day3.txt'

    y = 0
    points = set()
    with open( inputs ) as f:
        for line in f:
            line = line.strip() + '.'
            x = 0
            value = ''
            for c in line:
                if c.isdigit():
                    value += c
                else:
                    if value:
                        key = tuple( ( x - i, y ) for i in range( 1, len( value ) + 1 ) )                        
                        engine[ key ] = value                        
                    if c != '.':
                        value = c
                        engine[ (( x, y ),) ] = value
                        points.add( (x, y))
                    value = ''
                x += 1
            y += 1
    
    parts: Parts = { key: int(engine[key]) for key in engine.keys() if is_part_number( key, engine, points ) }
    print( sum( parts.values() ) )

    fun = partial( get_gear_value, engine = engine, parts = parts )
    print( sum( map(fun, [ k for k, v in engine.items() if v == '*' ]) ) )
    