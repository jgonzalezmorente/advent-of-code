from typing import Dict, List, Counter as CounterType
from functools import total_ordering
from collections import Counter
from enum import Enum

class HandType( Enum ):
    UNKNOW = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7

@total_ordering
class Hand( object ):
    cards: str
    bid_amount: int
    cards_counter: CounterType[int]
    second_ordering_rule: Dict[ str, int ]

    @property
    def type( self ) -> HandType:
        if self.cards_counter[ 5 ] == 1:
            return HandType.FIVE_OF_KIND
        elif self.cards_counter[ 4 ] == 1 and self.cards_counter[ 1 ] == 1:
            return HandType.FOUR_OF_KIND
        elif self.cards_counter[ 3 ] == 1 and self.cards_counter[ 2 ] == 1:
            return HandType.FULL_HOUSE
        elif self.cards_counter[ 3 ] == 1 and self.cards_counter[ 1 ] == 2:
            return HandType.THREE_OF_KIND
        elif self.cards_counter[ 2 ] == 2 and self.cards_counter[ 1 ] == 1:
            return HandType.TWO_PAIR
        elif self.cards_counter[ 2 ] == 1 and self.cards_counter[ 1 ] == 3:
            return HandType.ONE_PAIR
        elif self.cards_counter[ 1 ] == 5:
            return HandType.HIGH_CARD
        else:
            return HandType.UNKNOW

    def __init__( self, hand_data: str ):
        self.second_ordering_rule = { '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13 }
        hand_data_ = hand_data.split()
        self.cards = hand_data_[0]
        self.bid_amount = int( hand_data_[1] )
        self.cards_counter = Counter( Counter( self.cards ).values() ) 
    
    def __eq__( self, hand: object ) -> bool:
        if not isinstance( hand, Hand ):
            return NotImplemented

        return self.cards == hand.cards
    
    def __lt__( self, other: 'Hand' ) -> bool:
        if self.type != other.type:
            return self.type.value < other.type.value
        return [ self.second_ordering_rule[ i ] for i in self.cards ] <= [ self.second_ordering_rule[ i ] for i in other.cards ]
    
    def __str__( self ) -> str:
        return f'{ self.cards } ({ self.bid_amount })'

class HandPart2( Hand ):
    def __init__( self, hand_data: str ):
        self.second_ordering_rule = { 'J': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'Q': 10, 'K': 11, 'A': 12 }
        hand_data_ = hand_data.split()
        self.bid_amount = int( hand_data_[1] )

        self.cards = hand_data_[0]
        cards_ = self.cards
        if 'J' in cards_:
            num_cards = len( cards_ )
            cards_ = ''.join([ card for card in cards_ if card != 'J' ])
            if cards_:
                most_common = Counter( cards_ ).most_common( 1 )[ 0 ][ 0 ]
            else:
                most_common = 'A'
            num_jokers = num_cards - len( cards_ )
            cards_ += num_jokers * most_common
        self.cards_counter = Counter( Counter( cards_ ).values() )

if __name__ == '__main__':

    inputs = 'inputs/day7.txt'
    sample = 'samples/day7.txt'

    file = inputs
        
    # Part I
    hands: List[ Hand ]
    with open( file ) as f:
        hands = [ Hand( line.strip() ) for line in f ]

    hands.sort()
    print(sum( [ x[0].bid_amount * x[1] for x in zip( hands, range( 1, len( hands ) + 1 ) ) ] ) )

    # Part II
    hands_part2: List[ HandPart2 ]
    with open( file ) as f:
        hands_part2 = [ HandPart2( line.strip() ) for line in f ]

    hands_part2.sort()
    print(sum( [ x[0].bid_amount * x[1] for x in zip( hands_part2, range( 1, len( hands_part2 ) + 1 ) ) ] ) )
