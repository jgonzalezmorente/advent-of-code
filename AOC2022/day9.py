from helpers.functions import move_rope, tail_to_head

if __name__ == '__main__':

    inputs = 'inputs/day9/input.txt'
    sample = 'samples/day9/sample.txt'
    sample2 = 'samples/day9/sample2.txt'


    with open( inputs ) as f:
        inputs_ = [ tuple( line.strip().split() ) for line in f ]    

    head = (0, 0)
    tail = (0, 0)
    tails = set()
    tails.add( tail )
    for move in inputs_:        
        for _ in range( int( move[ 1 ] ) ):
            head, tail = move_rope( head, tail, move[ 0 ] )
            tails.add( tail )            

    print( len( tails  ) )

    tails = set()
    rope = [ (0 , 0) for _ in range( 10 ) ]
    tails.add( rope[ -1 ] )
    for move in inputs_:         
        for _ in range( int( move[ 1 ] ) ):
            rope[ 0 ], rope[ 1 ] = move_rope( rope[ 0 ], rope[ 1 ], move[0] )

            for k in range( 2, 10 ):
                rope[ k ] = tail_to_head( rope[ k ], rope[ k - 1 ] )            
            tails.add( rope[ -1 ] )
            
    print( len( tails ) )