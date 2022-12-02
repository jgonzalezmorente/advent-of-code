from helpers.functions import get_score, get_move

if __name__ == '__main__':

    inputs = 'inputs/day2/input.txt'
    sample = 'samples/day2/sample.txt'


    with open( inputs ) as f:    
        inputs_ = [ line.strip().replace(' ', '') for line in f ]

    print(sum( map( get_score, inputs_ ) ))
    print(sum( map( get_score, map( get_move, inputs_ ) )))


    



    