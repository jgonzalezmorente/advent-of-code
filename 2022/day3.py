from helpers.functions import get_compartiments, get_priority
from functools import reduce

if __name__ == '__main__':

    inputs = 'inputs/day3/input.txt'
    sample = 'samples/day3/sample.txt'

    with open( inputs ) as f:    
        inputs_ = [ line.strip() for line in f ]
    
    intersections = [ get_compartiments( i )[-1][0] for i in inputs_ ] 
    print( sum(map( get_priority, intersections )) )    
    
    inputs_sets = list(map( set, inputs_ ))
    k_max = ( len( inputs_ ) // 3 )
    sum_priorities = 0
    for k in range( k_max ):
        badge = reduce( lambda x, y: x & y, inputs_sets[3*k:3*(k+1)] ).pop()
        sum_priorities += get_priority( badge )

    print( sum_priorities )        
        

