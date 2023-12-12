from typing import List
from itertools import pairwise

def predict_next_value( history: List[ int ], sign: int = 1, index: int = -1 ) -> int:
    if all( x == 0 for x in history ):
        return 0

    differences = [ b - a for a, b in pairwise( history ) ]    
    value = predict_next_value( differences, sign, index )
    return history[ index ] + sign * value

if __name__ == '__main__':

    inputs = 'inputs/day9.txt'
    sample = 'samples/day9.txt'

    file = inputs

    dataset: List[ List[int] ] = []

    with open( file ) as f:
        dataset = [ [ int(n) for n in line.strip().split() ] for line in f ]
       
    # Part I
    print( sum( [ predict_next_value(x) for x in dataset ] ) )

    # Part II
    print( sum( [ predict_next_value( x, sign = -1, index = 0 ) for x in dataset ] ) )    