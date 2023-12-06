from io import TextIOWrapper
from typing import List, Callable, Tuple
from functools import reduce

class Map( dict ):

    __ranges: List[ Tuple[ range, int ] ]

    def __init__( self ):
        super().__init__()
        self.__ranges = []
    
    def __missing__( self, key: int ) -> int:
        value = key
        for r in self.__ranges:
            if key in r[0]:
                value = r[1] + key - r[0][0]
                break
        self[ key ] = value
        return value

    def add_range( self, interval: str ):
        interval_values = interval.split()
        length = int( interval_values[2] )
        source_range_start = int( interval_values[1] )
        dest_range_start = int( interval_values[0] )
        self.__ranges.append( ( range( source_range_start, source_range_start + length ), dest_range_start ) )

    def __project_interval( self, interval: Tuple[ int, int ] ) -> List[ Tuple[int, int] ]:
        result: List[ Tuple[int, int] ] = []
        a = interval[0]
        b = interval[1]
        points: List[int] = []
        points.append( a )
        points.append( b )
        for r in self.__ranges:
            if a < r[0][0] and r[0][0] < b:
                points.append( r[0][0] )
            if a < r[0][-1] and r[0][-1] < b:
                points.append( r[0][-1] )        
        points = list( set( points ) )
        points.sort()       
        for i in range( len( points ) ):
            if i < len( points ) - 1:
                result.append( ( self[points[i]], self[points[i+1] - 1] ) )
        
        return result

    def project_intervals( self, intervals: List[ Tuple[int, int] ] ) -> List[ Tuple[int, int] ]:
        result: List[ Tuple[int, int] ] = []
        for interval in intervals:
            result.extend( self.__project_interval( interval ) )
        return result
    
    def to_fun( self ) -> Callable[[int], int]:
        return lambda key: self[ key ]

def set_map( f: TextIOWrapper, map_: Map ):
    line = None
    while ( line != '' ):
        line = f.readline().strip()
        if line:
            map_.add_range( line )

if __name__ == '__main__':

    inputs = 'inputs/day5.txt'
    sample = 'samples/day5.txt'

    seed_to_soil = Map()
    soil_to_fertilizer = Map()
    fertilizer_to_water  = Map()
    water_to_light = Map()
    light_to_temperature = Map()
    temperature_to_humidity = Map()
    humidity_to_location = Map()

    seeds: List[str]
    with open( inputs ) as f:
        for line in f:
            line = line.strip()
            if line.startswith( 'seeds' ):
                seeds = line.split(': ')[-1].split()

            elif line.startswith( 'seed-to-soil' ):
                set_map( f, seed_to_soil )

            elif line.startswith( 'soil-to-fertilizer' ):
                set_map( f, soil_to_fertilizer )

            elif line.startswith( 'fertilizer-to-water' ):
                set_map( f, fertilizer_to_water )

            elif line.startswith( 'water-to-light' ):
                set_map( f, water_to_light )

            elif line.startswith( 'light-to-temperature' ):
                set_map( f, light_to_temperature )

            elif line.startswith( 'temperature-to-humidity' ):
                set_map( f, temperature_to_humidity )

            elif line.startswith( 'humidity-to-location' ):
                set_map( f, humidity_to_location )

maps = [
    seed_to_soil,
    soil_to_fertilizer,
    fertilizer_to_water,
    water_to_light,
    light_to_temperature,
    temperature_to_humidity,
    humidity_to_location
]
compose = lambda f, g: lambda x: g( f(x) )
seed_to_location = reduce( compose, map( lambda m: m.to_fun(), maps ) )
print( min( [ seed_to_location( int( seed ) ) for seed in seeds ] ) )

intervals = []
for i in range(0, len(seeds), 2 ):
    interval = ( int(seeds[i]), int(seeds[i]) + int(seeds[i+1]) - 1)
    intervals.append( interval )

seed_to_location_intervals = reduce( compose, map( lambda m: m.project_intervals, maps ) )
projected_intervals = seed_to_location_intervals( intervals )
projected_intervals.sort( key = lambda x: x[0] )
print( projected_intervals[0][0] )