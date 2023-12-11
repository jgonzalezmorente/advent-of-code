import re
from typing import Dict, Tuple, TypeAlias, List
from math import lcm
from functools import reduce

NetworkType: TypeAlias = Dict[str, Tuple[str, str]]
CycleType: TypeAlias = Dict[ Tuple[ str, int ], int ]

def navigate_network( network: NetworkType, instructions: List[ bool ], current_node: str = 'AAA', target: str = 'ZZZ', steps: int = 0 ) -> int:
    n = len( instructions )
    while current_node != target:
        direction = instructions[ steps % n ]
        current_node = network[ current_node ][ direction ]
        steps += 1
    return steps

def get_cycle( network: NetworkType, instructions: List[ bool ], start_node: str, target: str = 'Z' ) -> CycleType:
    result: CycleType = {}
    n = len( instructions )    
    steps = 0
    current_node = start_node
    while True:
        direction = instructions[ steps % n ]
        current_node = network[ current_node ][ direction ]        
        steps += 1        
        if not current_node.endswith( target ):
            continue

        current_key = ( current_node, steps )
        previous_key = next( ( key for key in result.keys() if key[0] == current_node ), None )

        if not previous_key:
            result[ current_key ] = 0
            continue

        m = steps - previous_key[1]
        if not m % n == 0:
            result[ current_key ] = 0
            continue
        
        result[ previous_key ] = m
        for node in result:
            if node[1] > previous_key[1]:
                result[node] = m
        break
    return result

def extract_nodes( line: str ) -> ( Tuple[ str, ... ] ) | None:
    pattern = r'(\w+)\s*=\s*\((\w*),\s*(\w+)\)'
    match = re.match( pattern, line )
    if match:
        return match.groups()

    return None

if __name__ == '__main__':

    inputs = 'inputs/day8.txt'
    sample = 'samples/day8.txt'

    file = inputs
    
    instructions: List[ bool ]
    network: NetworkType = {}

    with open( file ) as f:
       line = f.readline().strip()
       instructions = [ instr == 'R' for instr in line ]
       f.readline()
       for line in f:
           nodes = extract_nodes( line.strip() )
           if nodes:
            network.update({ nodes[0]: ( nodes[1], nodes[2] ) })       
       
    # Part I
    print( navigate_network( network, instructions ) )

    # Part II
    nodes_ending_A = [ node for node in network.keys() if node.endswith( 'A' ) ]
    values: List[ int ] = []
    for node_ending_a in nodes_ending_A:
        cycle = get_cycle( network, instructions, node_ending_a )
        print( cycle )
        values.append( next(iter(cycle.values())) )        
    print( reduce( lcm, values ) )
    print( lcm(*values) )