import re
from helpers.classes import Monkey

if __name__ == '__main__':

    inputs = 'inputs/day11/input.txt'
    sample = 'samples/day11/sample.txt'
    part2 = True

    with open( inputs ) as f:
        for line in f:
            line = line.strip()
            
            if re.match( r'^Monkey \d+:$', line ):            
                monkey = Monkey()
            
            elif re.match( r'Starting items: (\d+,\s)*\d+$', line ):
                monkey.starting_items = re.findall( r'\d+', line )
            
            elif re.match( r'Operation: new = old \S (old)*\d*', line ):
                match = re.search(r'\S (old)*\d*$', line)
                if match:
                    span = match.span()
                    monkey.operator = line[span[0]]
                    monkey.parameter = line[span[0] + 2 : span[1]]

            elif re.match( r'Test: divisible by \d+$', line ):
                match = re.search( r'\d+', line )
                if match:
                    monkey.divider = int( match.group(0) )
            
            elif re.match( r'If true: throw to monkey \d+', line ):
                match = re.search( r'\d+', line )
                if match:
                    monkey.monkey_true = int( match.group(0) )                
            
            elif re.match( r'If false: throw to monkey \d+', line ):
                match = re.search( r'\d+', line )
                if match:
                    monkey.monkey_false = int( match.group(0) )
        
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