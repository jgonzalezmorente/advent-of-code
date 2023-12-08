from typing import List, Tuple
from math import ceil, floor, sqrt
from functools import reduce

def ways_beat_record( race: Tuple[int, int] ) -> int:
    s = race[0]
    d = race[1]
    disc = s**2 - 4*d
    if ( disc < 0 ):
        return 0
    t_1 = ( s - sqrt( disc ) ) / 2
    t_2 = ( s + sqrt( disc ) ) / 2

    return ( min(s - 1, ceil(t_2) - 1) - max(1, floor(t_1) + 1 ) + 1 )    

if __name__ == '__main__':

    inputs = 'inputs/day6.txt'
    sample = 'samples/day6.txt'

    times: List[ int ] = []
    distances: List[ int ]    

    with open( inputs ) as f:        
        times = [ int( x ) for x in f.readline().split(':')[-1].strip().split() ]
        distances = [ int( x ) for x in f.readline().split(':')[-1].strip().split() ]

    races: List[ Tuple[int, int] ] = list( zip( times, distances ) )

    #Part I
    print( reduce( lambda x, y : x*y, map( ways_beat_record, races ) ) )

    #Part II
    time = int(reduce( lambda x, y: x + y, map( str, times ) ))
    distance = int(reduce( lambda x, y: x + y, map( str, distances ) ))
    print(ways_beat_record( (time, distance) ))

