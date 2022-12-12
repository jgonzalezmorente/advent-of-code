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

    __instances = []

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
        self.paramter = ''
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