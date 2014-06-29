# Base functions for generating and manipulating gcode.


def floatf(f=0.0):
    '''Format floats in gcode to a minimal form.
    '''
    return ('%0.4f' % f).rstrip('0').rstrip('.')


def points_path(pts=[], feedrate=0.0):
    '''Generate gcode to make linear paths between a list of given points. 
Due to the way gcode works, this is good for both relative and absolute modes.
    '''

    assert isinstance(pts, list) and len(pts) > 0
    assert isinstance(feedrate, float) and feedrate > 0.0
    
    g = []
    g.append('F%s' % floatf(feedrate))
    for p in pts:
        g.append('G1 X%(x)s Y%(y)s' % {
                                       'x': floatf(p[0]),
                                       'y': floatf(p[1]),
                                      })
    return '\n'.join(g)


def helix_path(
               radius=0.0,
               depth=0.0,
               feedrate=0.0,
               direction='cw',
              ):
    assert isinstance(radius, float) and radius > 0.0
    assert isinstance(depth, float) and depth >= 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(direction, str) and direction in ['cw', 'ccw']
    
    if direction == 'cw':
        g_dir = 'G2'
    elif direction == 'ccw':
        g_dir = 'G3'
    
    return '%(dir)s X0 Y0 Z%(z)s I0 J%(j)s F%(f)s' % {
                                                      'dir': g_dir,
                                                      'f': floatf(feedrate),
                                                      'z': floatf(depth * -1),
                                                      'j': floatf(radius),
                                                     }

