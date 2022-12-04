from helpers.functions import sections_to_pairs_sets

if __name__ == '__main__':

    inputs = 'inputs/day4/input.txt'
    sample = 'samples/day4/sample.txt'

    with open( inputs ) as f:    
        inputs_ = [ line.strip() for line in f ]    

    print( sum (map( lambda s: s[0].issubset(s[1]) or s[1].issubset(s[0]), [ sections_to_pairs_sets( i ) for i in inputs_ ] ) ) )
    print( sum (map( lambda s: s[0].intersection(s[1]) != set(), [ sections_to_pairs_sets( i ) for i in inputs_ ] ) ) )


