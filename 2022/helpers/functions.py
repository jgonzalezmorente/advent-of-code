import numpy as np


def split_lists_numbers( list ):
    output = []
    partial_list = []
    for l in list:
        l = l.strip()
        if l:
            partial_list.append( int( l ) )
        else:
            output.append( partial_list )
            partial_list = []

    output.append( partial_list )
    return output

def get_score( r ):

    # A, X -> Piedra
    # B, Y -> Papel
    # C, Z -> Tijera    

    values = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    game_score = {
        'AX': 3, # Piedra - Piedra => Empate
        'AY': 6, # Piedra - Papel => Gano
        'AZ': 0, # Piedra - Tijera => Pierdo
        'BX': 0, # Papel - Piedra => Pierdo
        'BY': 3, # Papel - Papel => Empate
        'BZ': 6, # Papel - Tijera => Gano
        'CX': 6, # Tijera - Piedra => Gano
        'CY': 0, # Tijera - Papel => Pierdo
        'CZ': 3  # Tijera - Tiejra => Empate
    }    

    return game_score[r] + values[r[1]]
            
def get_move( r ):

    moves = {
        'AX': 'AZ', # Piedra - perder => Tijera
        'AY': 'AX', # Piedra - empatar  => Piedra
        'AZ': 'AY', # Piedra - ganar => Papel
        'BX': 'BX', # Papel - perder => Piedra
        'BY': 'BY', # Papel - empatar => Papel
        'BZ': 'BZ', # Papel - ganar => Tijera
        'CX': 'CY', # Tijera - perder => Papel
        'CY': 'CZ', # Tijera - empatar => Tijera
        'CZ': 'CX'  # Tijera - ganar => Piedra
    }

    return moves[r]

def get_compartiments( rucksack ):
    m = ( len(rucksack) // 2 )
    compartiment_1 = rucksack[:m]
    compartiment_2 = rucksack[m:]
    intersection = list( set(compartiment_1) & set(compartiment_2) )
    return compartiment_1, compartiment_2, intersection

def get_priority( letter ):
    s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return s.index( letter ) + 1

def section_to_set( section ):
    lims = section.split('-')
    return set(range(int(lims[0]), int(lims[1])+1))

def sections_to_pairs_sets( sections ):
    sections_list = sections.split(',')
    return [ section_to_set(sections_list[0]), section_to_set(sections_list[1]) ]

def parse_stacks( stacks ):
    
    num_stacks = ( len(stacks[0]) + 1 ) // 4

    result = []
    for _ in range(num_stacks):
         result.append([])
    
    for s in stacks:
        for k in range(num_stacks):
            crate = s[ 1 + 4 * k ].strip()
            if crate:
                result[k].insert( 0, crate )
    
    return result

def parse_movements( movements ):
    result = []
    for move in movements:
        l = move.split()    
        result.append( { 'count': int(l[1]), 'from': int(l[3]) - 1, 'to': int(l[5]) - 1 } )
    return result

def get_first_marker( datastream, length = 4 ):
    for i in range( length, len(datastream) + 1 ):
        if len( set(datastream[i - length : i]) ) == length:
            return i
    
def tree_is_visible( height, west, east, north, south ):
    
    if ( west.size * east.size * north.size * south.size ) == 0:
        return True

    return ( max( west ) < height or max( east ) < height or max( north ) < height or max( south ) < height )
    
def tree_score_direction( height, direction ):
    return np.where( direction >= height )[0][0] + 1 if np.where( direction >= height )[0].size > 0 else direction.size

def tree_score( height, west, east, north, south ):
    return ( tree_score_direction( height, np.flip( west ) ) * 
             tree_score_direction( height, east ) * 
             tree_score_direction( height, np.flip( north ) ) *
             tree_score_direction( height, south ) ) 


def together( knot1, knot2 ):
    return max( abs( knot1[0] - knot2[0] ), abs( knot1[1] - knot2[1] ) ) < 2
    
def tail_to_head( tail , head ):

    if together( head, tail ):
        return tail
    else:
        x = tail[ 0 ]
        if head[ 0 ] > tail[ 0 ]:
            x = tail[ 0 ] + 1
        elif head[ 0 ] < tail[ 0 ]:
            x = tail[ 0 ] - 1
            
        y = tail[ 1 ]                
        if head[ 1 ] > tail[ 1 ]:
            y = tail[ 1 ] + 1
        elif head[ 1 ] < tail[ 1 ]:
            y = tail[ 1 ] - 1

        return (x, y)

def move_rope( head, tail, move ):
    if move == 'R':
        new_head = ( head[0] + 1, head[1] )
    elif move == 'L':
        new_head = ( head[0] - 1, head[1] )
    elif move == 'U':
        new_head = ( head[0], head[1] + 1 )
    elif move == 'D':
        new_head = ( head[0], head[1] - 1 )

    if together( new_head, tail ):
        return new_head, tail
    else:
        return new_head, head    
    




