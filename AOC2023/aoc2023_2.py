from typing import List, Dict, TypeAlias, Tuple

ColorCubes: TypeAlias = Dict[str, int]

def filter_possible_games( game: Tuple[ int, List[ColorCubes] ]) -> bool:
    bag: ColorCubes = {
        'red': 12,
        'green': 13,
        'blue': 14
    }    
    for round in game[1]:
        for color in round:
            if round[color] > bag[color]:
                return False
    return True

def get_power( game: List[ColorCubes] ) -> int:
    red = []
    green = []
    blue = []
    for round in game:
        red.append( round['red'] )
        green.append( round['green'] )
        blue.append( round['blue'] )
    return max(red) * max(green) * max(blue)

if __name__ == '__main__':

    inputs = 'inputs/day2.txt'
    sample = 'samples/day2.txt'

    games: List[ List[ColorCubes] ] = []

    with open( inputs ) as f:
        for line in f:
            game: List[ ColorCubes ] = []
            for group in line.split(':')[-1].split(';'):
                color_cubes: ColorCubes = {
                    'green': 0,
                    'red': 0,
                    'blue': 0
                }
                for cube in group.split(','):
                    count_color = cube.strip().split()
                    key = count_color[1]
                    value = int( count_color[0] )
                    assert key in color_cubes
                    color_cubes[ key ] = value
                game.append( color_cubes )
            games.append( game )
    
    possible_games = filter( filter_possible_games, enumerate( games ) )
    print( sum( map( lambda game: game[0] + 1, possible_games) ) )
    print( sum(map( get_power, games ) ) )    





            