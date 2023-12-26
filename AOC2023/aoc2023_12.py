from typing import TypeAlias, List, Tuple
from functools import cache, partial
from itertools import repeat

SpringRow: TypeAlias = Tuple[ str, Tuple[int, ...] ]

def count( spring: SpringRow, factor: int = 1 ) -> int:
    assert( factor >= 1 )

    mask = spring[0] + '.'
    groups = spring[1]

    if factor > 1:
        mask = '?'.join( repeat( spring[0], factor ) ) + '.'
        groups = factor * groups

    @cache
    def dp( pos: int, group_idx: int, remaining: int, is_prev_hash: bool ) -> int:

        def dp_hastag( pos: int, group_idx: int, remaining: int ) -> int:
            return dp( pos + 1, group_idx, remaining - 1, True ) if remaining > 0 else 0

        def dp_point( pos: int, group_idx: int, remaining: int, is_prev_hash: bool ) -> int:
            if is_prev_hash:
                r = groups[ group_idx + 1 ] if group_idx < len( groups ) - 1 else 0
                g = min( group_idx + 1, len( groups ) )
                return dp( pos + 1, g, r, False ) if remaining == 0 else 0
            else:
                return dp( pos + 1, group_idx, remaining, False )

        if pos == len( mask ):            
            return group_idx == len( groups )

        match mask[ pos ]:
            case '#':
                return dp_hastag( pos, group_idx, remaining )
            case '.':
                return dp_point( pos, group_idx, remaining, is_prev_hash )
            case '?':
                return dp_hastag( pos, group_idx, remaining ) + dp_point( pos, group_idx, remaining, is_prev_hash )
            case _:
                return 0
    
    return dp( 0, 0, groups[0], False )

if __name__ == '__main__':

    inputs = 'inputs/day12.txt'
    sample = 'samples/day12.txt'

    file = inputs

    springs: List[ SpringRow ] = []

    with open( file ) as f:
        for line in f:
            record = line.strip().split()
            springs.append( ( record[0], tuple( [ int( x ) for x in record[1].split(',') ] ) ) )     
    
    # Part I
    print( sum( map( count, springs ) ) )

    # Part II
    print( sum( map( partial(count, factor = 5), springs ) ) )


