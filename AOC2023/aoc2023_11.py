from typing import TypeAlias, List, Dict, Tuple, Set
from functools import reduce

Image: TypeAlias = List[ List[str] ]
Map: TypeAlias =  Dict[ str, Tuple[ int, int ] ]
Pairs: TypeAlias = Set[ Tuple[str, str]]

def expand_image_by_rows( image: Image, factor: int = 2 ) -> Image:
    expanded_image: Image = []
    for row in image:
        expanded_image.append( row )
        if all( x == '.' for x in row ):            
            for _ in range( factor - 1 ):
                expanded_image.append( row )
    return expanded_image

def expand_image_by_columns( image: Image, factor: int = 2 ) -> Image:
    transposed_image = []
    expanded_image = []
    for i in range( len( image[0] ) ):
        column = [ row[i] for row in image ]
        transposed_image.append( column )
        if all( x == '.' for x in column ):
            for _ in range( factor - 1 ):
                transposed_image.append( column )
    for j in range( len( transposed_image[0] ) ):
        expanded_image.append([ column[j] for column in transposed_image ])
    return expanded_image

def expand_image( image: Image, factor: int = 2 ) -> Image:
    return expand_image_by_columns( expand_image_by_rows( image, factor ), factor )

def get_universe( image: Image ) -> Map:
    universe_map: Map = {}
    for j, row in enumerate( image ):
        for i, pixel in enumerate( row ):
            if pixel != '.':
                universe_map[ pixel] = (i, j )
    return universe_map

def get_pairs( universe_map: Map ) -> Pairs:
    pairs: Pairs = set()
    for r in universe_map:
        for s in universe_map:
            if r != s and not ( s, r ) in pairs:                
                pairs.add( ( r, s ) )
    return pairs

def get_empty_rows_and_columns( pair: Tuple[str, str], universe_map: Map, image: Image ) -> int:    
    result = 0
    galaxy_a = universe_map[ pair[0] ]
    galaxy_b = universe_map[ pair[1] ]
    for i in range( min( galaxy_a[1], galaxy_b[1] ) + 1, max( galaxy_a[1], galaxy_b[1] ) ):
        row = image[i]
        if all( x == '.' for x in row ):
            result += 1
    for j in range( min( galaxy_a[0], galaxy_b[0] ) + 1, max( galaxy_a[0], galaxy_b[0] ) ):
        column = [ row[j] for row in image ]
        if all( x == '.' for x in column ):
            result += 1    
    return result

if __name__ == '__main__':

    inputs = 'inputs/day11.txt'
    sample = 'samples/day11.txt'
    
    file = inputs
    
    original_image: Image = []
    n: int = 0
    with open( file ) as f:
        for line in f:
            new_line = []
            for x in line.strip():
                if x == '#':
                    n += 1
                    new_line.append( str( n ) )
                else:
                    new_line.append( x )
            original_image.append( new_line )

    # Part I
    expanded_image = expand_image( original_image )
    universe_map = get_universe( expanded_image )
    
    pairs = get_pairs( universe_map )
    distance = reduce( lambda acc, pair: acc + abs( universe_map[pair[1]][0] - universe_map[pair[0]][0] ) + abs( universe_map[pair[1]][1] - universe_map[pair[0]][1] ), pairs, 0 )
    print( distance )

    # Part II
    universe_map = get_universe( original_image )
    pairs = get_pairs( universe_map )
    distance = reduce( lambda acc, pair: acc + abs( universe_map[pair[1]][0] - universe_map[pair[0]][0] ) + abs( universe_map[pair[1]][1] - universe_map[pair[0]][1] ), pairs, 0 )    
    factor = sum( map( lambda pair: get_empty_rows_and_columns( pair, universe_map, original_image ), pairs ) )
    print( distance + 999999 * factor )