from typing import List, Type

class MirrorLine:
    compare_with_smudge: bool = False
    __smudge_detected: bool = False
    data: str

    @classmethod
    def reset_smudge_detected( cls: Type['MirrorLine'] ) -> None:
        if cls.compare_with_smudge:
            cls.__smudge_detected = False

    @classmethod
    def smudge_detected( cls: Type['MirrorLine'] ) -> bool:
        return cls.__smudge_detected

    def __init__(self, data: str) -> None:
        self.data = data

    def __eq__( self, mirrorLine: object ) -> bool:
        if not isinstance( mirrorLine, MirrorLine ):
            return NotImplemented
        if self.data == mirrorLine.data:
            return True
        if not MirrorLine.compare_with_smudge or MirrorLine.__smudge_detected:
            return False        
        MirrorLine.__smudge_detected = len( set( enumerate( self.data ) ).difference( set( enumerate( mirrorLine.data ) ) ) ) == 1
        return MirrorLine.__smudge_detected

class Mirror:
    lines: List[ MirrorLine ]

    def __init__( self ) -> None:
        self.lines = []

    def add_line( self, line: MirrorLine ):
        self.lines.append( line )
    
    def check_reflection( self, inf: int, sup: int ) -> bool:
        pattern = self.lines[ inf: sup ]
        if not pattern or ( len( pattern ) == 2 and pattern[0] == pattern[-1] ):
            return True
        if len( pattern ) == 1 or pattern[0] != pattern[-1]:            
            return False
        return self.check_reflection( inf + 1, sup - 1 )
    
    def get_horizontal_reflection_line( self ) -> int:
        for i, value in enumerate( self.lines ):
            MirrorLine.reset_smudge_detected()
            if ( i != len( self.lines ) - 1 ) and ( value == self.lines[-1] ) and self.check_reflection( i + 1, -1 ):
                if MirrorLine.compare_with_smudge == False or ( MirrorLine.compare_with_smudge and MirrorLine.smudge_detected() ):
                    return ( i + 1 + ( len( self.lines ) - i - 1 ) // 2 )            
            MirrorLine.reset_smudge_detected()
            if ( i != 0 and value == self.lines[0] and self.check_reflection( 1, i ) ):
                if MirrorLine.compare_with_smudge == False or ( MirrorLine.compare_with_smudge and MirrorLine.smudge_detected() ):
                    return 1 + ( i // 2 )
        return 0
    
    def transpose( self ) -> 'Mirror':
        transposed_mirror = Mirror()
        for i in range( len( self.lines[0].data ) ):
            column = [ line.data[i] for line in self.lines ]
            transposed_mirror.add_line( MirrorLine( ''.join( column ) ) )
        return transposed_mirror
    
    def get_reflection_value( self ):
        reflection_line = 100 * self.get_horizontal_reflection_line()
        if reflection_line == 0:
            reflection_line = self.transpose().get_horizontal_reflection_line()
        return reflection_line

if __name__ == '__main__':
    
    inputs = 'inputs/day13.txt'
    sample = 'samples/day13.txt'

    file = inputs

    mirrors: List[ Mirror ] = []
    mirror = Mirror()
    with open( file ) as f:
        for line in f:
            line = line.strip()
            if line:
                mirror.add_line( MirrorLine( line ) )
            else:
                mirrors.append( mirror )
                mirror = Mirror()
    mirrors.append( mirror )

    # Part I
    print( sum( map( lambda mirror: mirror.get_reflection_value(), mirrors ) ) )

    # Part II
    MirrorLine.compare_with_smudge = True
    print( sum( map( lambda mirror: mirror.get_reflection_value(), mirrors ) ) )