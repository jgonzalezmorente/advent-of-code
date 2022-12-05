from helpers.functions import parse_stacks, parse_movements
from functools import reduce
from copy import deepcopy

if __name__ == '__main__':

    inputs = 'inputs/day5/input.txt'
    sample = 'samples/day5/sample.txt'

    with open( inputs ) as f:
        inputs_ = [ line.replace( '\n', '' ) for line in f ]

    n = inputs_.index('') - 1    
    stacks = parse_stacks( inputs_[ : n ] )
    movements = parse_movements( inputs_[ n + 2 : ] )

    stacks_1 = deepcopy( stacks )    
    for move in movements:
        for _ in range( move['count'] ):
            stacks_1[ move['to'] ].append( stacks_1[ move['from'] ].pop() )
    
    print( reduce( lambda acc, stack: acc + stack[-1], stacks_1, '' ) )

    stacks_2 = deepcopy( stacks )
    for move in movements:        
        stacks_2[ move['to'] ].extend( stacks_2[ move['from'] ][-move['count']:] )
        stacks_2[ move['from'] ] = stacks_2[ move['from'] ][:-move['count']]
    
    print( reduce( lambda acc, stack: acc + stack[-1], stacks_2, '' ) )