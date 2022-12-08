import numpy as np
from helpers.functions import tree_is_visible, tree_score

if __name__ == '__main__':

    inputs = 'inputs/day8/input.txt'
    sample = 'samples/day8/sample.txt'

    with open( inputs ) as f:
        inputs_ = np.array([ list( map( int, list( line.replace( '\n', '' ) ) ) ) for line in f ])

    visible = [ 
        tree_is_visible( 
            inputs_[i, j],             
            inputs_[ i, :j ],          
            inputs_[ i, ( j + 1 ): ],  
            inputs_[ :i, j ],          
            inputs_[ ( i + 1 ): , j ] ) for i in range( inputs_.shape[0] ) for j in range( inputs_.shape[1] ) ]

    print( sum(visible) )

    scores = [ 
        tree_score( 
            inputs_[i, j],             
            inputs_[ i, :j ],          
            inputs_[ i, ( j + 1 ): ],  
            inputs_[ :i, j ],          
            inputs_[ ( i + 1 ): , j ] ) for i in range( inputs_.shape[0] ) for j in range( inputs_.shape[1] ) ]

    print( max( scores ) )
 

