from functools import reduce
from collections import Counter

if __name__ == '__main__':

    inputs = 'inputs/day10/input.txt'
    sample = 'samples/day10/sample.txt'    

    with open( inputs ) as f:
        inputs_ = [ tuple(line.strip().split()) for line in f ]

    counter = Counter( map( lambda i: i[0], inputs_) )
    total_cycles = counter['noop'] + counter['addx'] * 2 
    cycles = [ { 'cycle': c + 1, 'register': 0  } for c in range( total_cycles ) ]

    pointer = 0
    register = 1
    for i in inputs_:
        if i[0] == 'addx':
            cycles[ pointer ]['register'] = register
            cycles[ pointer + 1 ]['register'] = register
            pointer += 2
            register += int( i[1] )

        elif i[0] == 'noop':
            cycles[ pointer ]['register'] = register
            pointer += 1

    
    cycles_sol = filter( lambda c: ( c['cycle'] - 20 ) % 40 == 0 and c['cycle'] <= 220,  cycles )
    print( reduce( lambda acc, c: acc + c['cycle'] * c['register'], cycles_sol, 0 ) )