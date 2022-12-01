
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
            