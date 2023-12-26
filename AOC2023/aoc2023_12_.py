import re
from typing import TypeAlias, List, Tuple
from functools import cache
from itertools import repeat

import time

ConditionRecord: TypeAlias = Tuple[ str, Tuple[List[ int ], int] ]

@cache
def get_partitions( length: int, target: int ) -> List[ List[ int ] ]:    
    assert( target >= 0 )
    if length == 1:
        return [ [ target ] ]
    if target == 0:
        return [ length * [0] ]
    partitions = []    
    for k in range( target + 1 ):
        partitions.extend( [ [k] + p for p in get_partitions( length - 1, target - k ) ] )
    return partitions

def get_matches( groups: List[int], target: int, mask: str ) -> List[str]:    
    matches = []
    partitions = get_partitions( len( groups ), target )
    print( len( partitions ))
    for p in partitions:
        condition = '.'.join([ ( x * '.' + y * '#' ) for (x, y) in zip(p, groups) if x > 0 or y > 0 ])        
        if re.match(mask, condition):
            matches.append( condition )
    return matches

if __name__ == '__main__':

    start = time.time()

    inputs = 'inputs/day12.txt'
    sample = 'samples/day12.txt'

    file = sample

    condition_records: List[ ConditionRecord ] = []    

    with open( file ) as f:        
        for line in f:
            record = line.strip().split()
            mask = '?'.join( repeat( record[0], 3 ) )
            #mask = record[0]
            groups = [int(x) for x in 3*record[1].split(',')] + [0]
            regex = mask.replace( '.', '\\.' ).replace('?', '[#.]')
            condition_records.append( ( regex, ( groups, len( mask ) - sum( groups ) - len ( groups ) + 2 ) ) )

    part1 = 0
    for condition_record in condition_records:
        groups = condition_record[-1][0]
        target = condition_record[-1][1]
        mask = condition_record[0]
        matches = get_matches( groups, target, mask )
        part1 += len( matches )
    print( part1 )

    end = time.time()
    print( end - start )