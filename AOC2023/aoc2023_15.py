import re
from typing import List
from functools import reduce
from enum import Enum

class OperationType( Enum ):
    UNKNOW = 0
    REMOVE = 1
    INSERT = 2

def get_hash( string: str ) -> int:
    return reduce( lambda current_value, character: ( current_value + ord( character ) ) * 17 % 256, string, 0 )

class Lens:
    label: str
    operation: OperationType
    focal_lenth: int

    @property 
    def box_number( self ) -> int:
        return get_hash( self.label )

    def __init__( self, step: str ) -> None:    
        self.label = ''
        self.operation = OperationType.UNKNOW
        self.focal_lenth = 0

        pattern = r'^(.+?)(-|=\d+)$'
        groups = re.search( pattern, step )
        assert( groups )
        self.label = groups.group(1)
        match( groups.group(2)[0] ):
            case '-':
                self.operation = OperationType.REMOVE
            case '=':
                self.operation = OperationType.INSERT
                self.focal_lenth = int( groups.group(2)[1:])
    
    def __eq__(self, lens: object) -> bool:
        if not isinstance( lens, Lens ):
            return NotImplemented
        return self.label == lens.label
    
    def __str__(self) -> str:
        return f'[{ self.label } { self.focal_lenth}]'

class Box:    
    lenses: List[ Lens ]
    number: int | None

    def __init__(self) -> None:
        self.lenses = []
        self.number = None

    def perform_operation( self, number: int, lens: Lens ) -> None:
        self.number = number
        match lens.operation:
            case OperationType.REMOVE:
                self.lenses = [ l for l in self.lenses if l != lens ]
            case OperationType.INSERT:
                if lens in self.lenses:
                    self.lenses[ self.lenses.index( lens ) ] = lens
                else:
                    self.lenses.append( lens )
            case _:
                pass
    
    def get_power( self ) -> int:        
        box_number = 0 if self.number is None else self.number + 1
        return reduce( lambda acc, l: acc + box_number * ( l[0] + 1 ) * l[1].focal_lenth ,enumerate( self.lenses ), 0 )

    
    def __str__(self) -> str:
        return f'Box { self.number }: { reduce( lambda acc, lens: acc + ' ' + str( lens ), self.lenses, '' )}'

if __name__ == '__main__':
    
    inputs = 'inputs/day15.txt'
    sample = 'samples/day15.txt'

    file = inputs
    
    with open( file ) as f:
        steps = f.readline().strip().split(',')

    # Part I
    print(sum( map( get_hash, steps ) ))

    boxes: List[ Box ] = [ Box() for _ in range(256) ]

    for step in steps:
        lens = Lens( step )        
        box_number = lens.box_number
        box = boxes[ box_number ]
        box.perform_operation( box_number, lens )
        
        # print (f'\nAfter { step }:')
        # for box in boxes:
        #     if box.lenses:
        #         print( box )
    
    
    # Part 2
    print( sum( map( lambda box: box.get_power(), filter( lambda box: box.lenses, boxes) ) ))






    
