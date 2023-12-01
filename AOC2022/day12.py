
from helpers.classes import Dijkstra

if __name__ == '__main__':

    inputs = 'inputs/day12/input.txt'
    sample = 'samples/day12/sample.txt'

    with open( inputs ) as f:
        inputs_ = [ line.replace( '\n', '' ) for line in f ]

    heights = 'SabcdefghijklmnopqrstuvwxyzE'

    heightmap = []    
    for y, row in enumerate( inputs_ ):        
        for x, z in enumerate( row ):
            point = ( x, y, heights.index(z) )
            if z == 'S':                
                S = point
            elif z == 'E':                
                E = point
 
            heightmap.append( point )
    
    # dijkstra = Dijkstra( heightmap )
    # dijkstra.start_from( S )
    # print( f'Part 1: { dijkstra.distance[ heightmap.index( E )] }')

    distances = []
    initial_points = list( filter( lambda p: p[-1] in [0, 1], heightmap ) )
    for i, p in enumerate( initial_points ):
        print(f'Point { i + 1 } of { len(initial_points) }')
        dijkstra = Dijkstra( heightmap )
        dijkstra.start_from( p )
        if dijkstra.distance[ heightmap.index( E ) ]:
            distances.append( dijkstra.distance[ heightmap.index( E ) ] )
            print ( min(distances) )

    print( f'Part 2: { min(distances) }' )





