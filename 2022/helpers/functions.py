
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