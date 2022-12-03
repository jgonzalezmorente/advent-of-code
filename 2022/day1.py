from helpers.functions import split_lists_numbers

if __name__ == '__main__':

    inputs = 'inputs/day1/input.txt'
    sample = 'samples/day1/sample.txt'


    with open( inputs ) as f:    
        inputs_ = [ line.strip() for line in f ]
    
    calories = split_lists_numbers( inputs_ )
    sum_list = list( map( sum, calories )  )
  
    print(max(sum_list))

    sum_list.sort( reverse = True )    
    print(sum(sum_list[:3]))