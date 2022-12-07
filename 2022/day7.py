from functools import reduce
from helpers.classes import Directory

if __name__ == '__main__':

    inputs = 'inputs/day7/input.txt'
    sample = 'samples/day7/sample.txt'

    root = Directory( '/' )
    current_directory = None

    with open( inputs ) as f:
        for line in f:
            line = line.strip().split()

            if line[0] == '$':
                if line[1] == 'cd':                    
                    if line[2] == '/':
                        current_directory = root
                    elif line[2] == '..':
                        current_directory = current_directory.parent
                    else:
                        current_directory = current_directory.get_subdirectory( line[2] )               

            elif line[0] == 'dir':
                current_directory.directories.append( Directory(line[1], current_directory ) )

            else:
                current_directory.files.append({ 'size': int(line[0] ), 'name': line[1] })

    total_size = root.get_size()    
    
    directories = root.get_subdirectories() + [root]
    desired_directories = filter( lambda d: d.get_size() <= 100000, directories )
    size = reduce( lambda acc, d: acc + d.get_size(), desired_directories, 0 )
    print(size)

    required_size = 30000000 - ( 70000000 - total_size )
    directory_delete = min([ d for d in directories if d.size >= required_size ])
    print(directory_delete.size)