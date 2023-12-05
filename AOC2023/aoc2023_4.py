from typing import TypedDict, List

class ScratchCard( TypedDict ):
    winning_numbers: int
    copies: int

if __name__ == '__main__':

    inputs = 'inputs/day4.txt'
    sample = 'samples/day4.txt'

    cards = []
    
    with open( inputs ) as f:
        for line in f:
            line = line.strip()
            card = line.split(': ')[1].split(' | ')
            winning_numbers = card[0].split()
            my_numbers = card[1].split()
            cards.append( ( [ int( n ) for n in winning_numbers ], [ int( n ) for n in my_numbers ]))
        
    winning_cards = list(map( lambda card: list(filter( lambda n: n in card[1],card[0])), cards ))
    points_cards = list( map( lambda card: 2**(len(card)-1) if len(card) > 0 else 0, winning_cards))
    print( sum(points_cards) )    
    
    scratchcards: List[ ScratchCard ] = [ { 'winning_numbers': len(card), 'copies': 1 } for card in winning_cards ]

    for i, c in enumerate(scratchcards):        
        if c['winning_numbers'] > 0:
            copies = c['copies']
            for c in scratchcards[(i+1): c['winning_numbers'] + i + 1]:
                c['copies'] += copies

    print( sum( map( lambda x: x['copies'], scratchcards ) ) )    