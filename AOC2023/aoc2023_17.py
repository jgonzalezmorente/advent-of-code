from heapq import heappush, heappop
from functools import total_ordering
from typing import TypeAlias, Tuple, Dict, List, Optional, Callable
from enum import Enum

class Dir( Enum ):
    E = (1, 0)
    N = (0, -1)
    W = (-1, 0)
    S = (0, 1)

Z_2: TypeAlias = Tuple[int, int]

@total_ordering
class Node:
    position: Z_2
    cost: int
    acc_cost: float
    direction: Optional[Dir]    
    same_dir_count: int
    previous_node: Optional['Node']

    def __init__(self, position: Z_2, cost: int, direction: Dir | None = None, same_dir_count: int = 0) -> None:
        self.position = position
        self.direction = direction
        self.same_dir_count = same_dir_count
        self.cost = cost
        self.acc_cost = 0
        self.previous_node = None
        self.visited = False

    def __lt__(self, node: object) -> bool:
        if not isinstance( node, Node ):
            return NotImplemented
        return self.cost < node.cost

    def __eq__(self, node: object) -> bool:
        if not isinstance( node, Node ):
            return NotImplemented
        return ( self.position, self.direction, self.same_dir_count ) == ( node.position, node.direction, node.same_dir_count )

class Graph:
    min_same_dir: int
    max_same_dir: int
    grid_nodes: Dict[ Z_2, List[ Node ] ]
    distances: Dict[ Tuple[Z_2, Dir | None, int], float ]

    def __init__(self, min_same_dir: int = 0, max_same_dir: int = 3) -> None:
        self.grid_nodes = {}
        self.min_same_dir = min_same_dir
        self.max_same_dir = max_same_dir
        self.distances = {}

    def add(self, point: Z_2, cost: int) -> None:
        if point == (0,0):
            self.grid_nodes[point] = [ Node( point, cost ) ]
            return
        self.grid_nodes[point] = [ Node(point, cost, Dir.E, k + 1) for k in range(self.max_same_dir) ]
        self.grid_nodes[point].extend([ Node(point, cost, Dir.N, k + 1) for k in range(self.max_same_dir)] )
        self.grid_nodes[point].extend([ Node(point, cost, Dir.W, k + 1) for k in range(self.max_same_dir)] )
        self.grid_nodes[point].extend([ Node(point, cost, Dir.S, k + 1) for k in range(self.max_same_dir)] )

    def __get_neighbors_p1( self, node: Node ) -> List[Node]:
        result = []
        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            neighbor_position = ( node.position[0] + dx, node.position[1] + dy )
            if not neighbor_position in self.grid_nodes:
                continue
            direction = ( neighbor_position[0] - node.position[0], neighbor_position[1] - node.position[1] )
            if ( node.direction and ( direction[0] + node.direction.value[0], direction[1] + node.direction.value[1] ) == (0, 0) ):
                continue
            if not node.direction or direction != node.direction.value:
                same_dir_count = 1
            else:
                same_dir_count = node.same_dir_count + 1
            result.extend([ n for n in self.grid_nodes[ neighbor_position ] if n.direction and n.direction.value == direction and n.same_dir_count == same_dir_count])
        return result

    def __get_neighbors_p2( self, node: Node ) -> List[Node]:
        if not node.direction or self.min_same_dir == 0 or node.same_dir_count >= self.min_same_dir:
            return self.__get_neighbors_p1( node )        
        neighbor_position = ( node.position[0] + node.direction.value[0], node.position[1] + node.direction.value[1] )
        if not neighbor_position in self.grid_nodes:
            return []
        return [ n for n in self.grid_nodes[ neighbor_position ] if n.direction and n.direction.value == node.direction.value and n.same_dir_count == node.same_dir_count + 1 ]    

    def get_neighbors(self, node: Node) -> List[Node]:
        if self.min_same_dir == 0:
            return self.__get_neighbors_p1( node )
        return self.__get_neighbors_p2( node )    
        
    def dijkstra( self ) -> None:
        for p in self.grid_nodes:
            for node in self.grid_nodes[p]:                
                self.distances[(p, node.direction, node.same_dir_count)] = float('inf') if p != (0,0) else 0
        
        priority_queue: List[Tuple[float, Node]] = []
        heappush( priority_queue, (0, self.grid_nodes[0,0][0]))

        while priority_queue:
            current_distance, current_node = heappop( priority_queue )
            current_node.visited = True
            for neighbor in [ n for n in self.get_neighbors( current_node ) if not n.visited]:
                distance = current_distance + neighbor.cost
                distance_key = (neighbor.position, neighbor.direction, neighbor.same_dir_count)
                if distance < self.distances[distance_key]:
                    neighbor.previous_node = current_node
                    neighbor.acc_cost = distance
                    self.distances[distance_key] = distance
                    heappush( priority_queue, ( distance, neighbor ))

if __name__ == '__main__':    
    inputs = 'inputs/day17.txt'    
    sample = 'samples/day17.txt'

    file = inputs

    # Part I
    graph = Graph()
    with open( file ) as f:
        for j, line in enumerate(f):
            for i, value in enumerate(line.strip()):
                graph.add( (i, j), int(value))
    graph.dijkstra()
    
    min_distance = min([ v for k, v in graph.distances.items() if k[0] == (i,j)])
    print(min_distance)

    # Part II
    min_same_dir = 4
    graph = Graph( min_same_dir = min_same_dir, max_same_dir = 10 )
    with open( file ) as f:
        for j, line in enumerate(f):
            for i, value in enumerate(line.strip()):
                graph.add( (i, j), int(value))

    graph.dijkstra()
    min_distance = min([ node.acc_cost for node in graph.grid_nodes[i, j] if node.same_dir_count >= min_same_dir and node.acc_cost > 0])
    print( min_distance )
