from helpers.functions import get_first_marker

if __name__ == '__main__':

    inputs = 'inputs/day6/input.txt'
    sample = 'samples/day6/sample.txt'

    with open( inputs ) as f:
        datastream = f.readline()

    print( get_first_marker( datastream ) )
    print( get_first_marker( datastream, 14 ) )