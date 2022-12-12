import re
from helpers.classes import Monkey

if __name__ == '__main__':

    inputs = 'inputs/day11/input.txt'
    sample = 'samples/day11/sample.txt'
    part2 = True

    with open( inputs ) as f:
        for line in f:
            line = line.strip()
            
            if re.match( '^Monkey \d+:$', line ):            
                monkey = Monkey()
            
            elif re.match( 'Starting items: (\d+,\s)*\d+$', line ):
                monkey.starting_items = re.findall( '\d+', line )
            
            elif re.match( 'Operation: new = old \S (old)*\d*', line ):
                span = re.search('\S (old)*\d*$', line).span()
                monkey.operator = line[span[0]]
                monkey.parameter = line[span[0] + 2 : span[1]]

            elif re.match( 'Test: divisible by \d+$', line ):
                monkey.divider = int( re.search( '\d+', line ).group(0) )
            
            elif re.match('If true: throw to monkey \d+', line ):
                monkey.monkey_true = int( re.search( '\d+', line ).group(0) )                
            
            elif re.match('If false: throw to monkey \d+', line ):
                monkey.monkey_false = int( re.search( '\d+', line ).group(0) )
        
    if not part2:
        for _ in range( 20 ):
            Monkey.start_round()
    else:
        for _ in range( 10000 ):
            Monkey.start_round( part2 )
    
    
    inspected_items = Monkey.inspected_items()
    print( inspected_items )
    inspected_items.sort( reverse = True )
    print( inspected_items[0] * inspected_items[1] )