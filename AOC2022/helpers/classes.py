from typing import List, Tuple
from functools import reduce, total_ordering
import operator

@total_ordering
class Directory:
    def __init__( self, name, parent = None  ):
        self.name = name
        self.parent = parent
        self.directories = []
        self.files = []
        self.size = None

    def get_subdirectory( self, name ):
        try:        
            return next( filter( lambda d: d.name == name, self.directories) )
        except:
            return None

    def get_size( self ):
        if not self.size:
            self.size = reduce( lambda acc, f: acc + f['size'] , self.files, 0 ) + reduce( lambda acc, d: acc + d.get_size(), self.directories, 0 )
        return self.size

    def get_subdirectories( self ):
        return reduce( lambda acc, directory: acc + directory.get_subdirectories(), self.directories, self.directories )
    
    def __eq__( self, other ):
        return self.size == other.size

    def __lt__( self, other ):
        return self.size < other.size

class Monkey:

    __instances: List['Monkey'] = []

    @classmethod
    def start_round( cls, part2 = False ):
        module = None
        if part2:
            module = reduce( lambda acc, m: acc * m.divider, cls.__instances, 1 )

        for monkey in cls.__instances:
            monkey.inspect( module )

    @classmethod
    def inspected_items( cls ):
        return [ m.inspected_items for m in cls.__instances ]
    
    def __init__( self ):
        self.starting_items = []        
        self.inspected_items = 0
        self.operator = ''
        self.parameter = ''
        self.divider = 1
        self.monkey_true = 0
        self.monkey_false = 0

        Monkey.__instances.append ( self )

    def operation( self, worry_level ):
        if self.operator == '+':
            op = operator.add
        elif self.operator == '*':
            op = operator.mul            
        else:
            return worry_level

        if self.parameter == 'old':            
            return op( worry_level, worry_level )
        else:
            return op( worry_level, int( self.parameter ) )

    def test( self, worry_level ):
        if worry_level % self.divider == 0:
            Monkey.__instances[ self.monkey_true ].starting_items.append( worry_level )
        else:
            Monkey.__instances[ self.monkey_false ].starting_items.append( worry_level )

    def inspect( self, module = None ):
        for _ in range( len(self.starting_items) ):
            worry_level = self.starting_items.pop(0)
            self.inspected_items += 1
            if not module:
                self.test( self.operation( int( worry_level ) ) // 3  )
            else:            
                self.test( self.operation( int( worry_level ) % module ) )

class Dijkstra:
    def __init__( self,  heightmap ):
        self.heightmap = heightmap
        self.distance = [ None for _ in range( len( heightmap ) ) ]
        self.visited = set()
        self.current_node = None

    def is_neighbor( self, node ):
        return ( ( ( node[0] == self.current_node[0] + 1 and node[1] == self.current_node[1] ) or
                 ( node[0] == self.current_node[0] and node[1] == self.current_node[1] + 1 ) or
                 ( node[0] == self.current_node[0] - 1 and node[1] == self.current_node[1] ) or
                 ( node[0] == self.current_node[0] and node[1] == self.current_node[1] - 1 ) ) and ( node[-1] <= self.current_node[-1] + 1 )
        )

    def neighbors( self ):
        d = self.distance[ self.heightmap.index( self.current_node ) ]
        for neighbor in [ p for p in self.heightmap if self.is_neighbor( p ) and not p in self.visited ]:            
            neighbor_d = d + 1
            i = self.heightmap.index( neighbor )
            if self.distance[ i ] is None or self.distance[ i ] > neighbor_d:
                self.distance[ i ] = neighbor_d

    def set_current_node( self, S = None ):
        self.current_node = None
        if S:
            self.current_node = S
            return

        nodes = []
        for i, d in enumerate( self.distance ):
            if d != None:
                node = self.heightmap[ i ]
                if not node in self.visited:
                    nodes.append( ( node, d ) )
    
        if nodes:
            nodes.sort( key = lambda n : n[-1] )
            self.current_node = nodes[0][0]

    def start_from( self, S ):
        self.set_current_node( S )
        self.visited.add( self.current_node )        
        self.distance[ self.heightmap.index( self.current_node ) ] = 0
 
        while len( self.visited ) < len( self.heightmap ) and self.current_node:
            self.neighbors()
            self.set_current_node()
            self.visited.add( self.current_node )            


class Tree:
    heightmap: List[Tuple[int, int, int]] = []
    target_distances: List[int] = []    

    def __init__( self, node, father = None ):
        self.node = node
        self.father = father
        if father is None:
            self.depth = 0
            self.fathers = []
        else:
            self.fathers = father.fathers
            self.fathers.append( father.node )
            self.depth = father.depth + 1

        self.children = []
        self.target_distances.append( ( self.node, self.depth ) )

    
    def is_child( self, node ):
        return ( ( ( node[0] == self.node[0] + 1 and node[1] == self.node[1] ) or
                 ( node[0] == self.node[0] and node[1] == self.node[1] + 1 ) or
                 ( node[0] == self.node[0] - 1 and node[1] == self.node[1] ) or
                 ( node[0] == self.node[0] and node[1] == self.node[1] - 1 ) ) and ( node[-1] <= self.node[-1] + 1 )
                 and ( not node in self.fathers )
        )

    def search_children( self ):
        self.children = [ Tree( node, father = self ) for node in Tree.heightmap if self.is_child( node ) ]        

    def build( self ):
        self.search_children()
        if len( self.children ) == 0:
            return
        
        for child in self.children:
            child.build()