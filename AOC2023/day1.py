from typing import Tuple 

def get_first_last_numbers( input: str ) -> Tuple[int, int]:
    names = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]
    digits = range(1, 10)
    mapping = { key : value for key, value in zip( names, digits ) }
    mapping.update( { key: value for key, value in zip( map( str, digits ), digits )})
    
    first_number = 0
    last_number = 0
    length = len( input )
    for i in range( length ):
        for key in mapping:
            if first_number == 0:
                if input[i:].startswith( key ):
                    first_number = mapping[ key ]
            if last_number == 0:
                if input[:(length - i)].endswith( key ):
                    last_number = mapping[ key ]
            if first_number != 0 and last_number != 0:
                return( first_number, last_number )
            
    return( first_number, last_number )

if __name__ == '__main__':

    inputs = 'inputs/day1.txt'
    sample = 'samples/day1.txt'
    
    with open( inputs ) as f:
        calibration_document = [ line.strip() for line in f ]

    def to_b10( tuple: Tuple[int, int]) -> int:
        return 10 * tuple[0] + tuple[1]

    print(sum(map( lambda x:  to_b10( get_first_last_numbers( x )), calibration_document )))

  
    