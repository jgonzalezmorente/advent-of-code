from functools import reduce, total_ordering

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
