# Base functions for generating and manipulating gcode.

from math_base import *

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


def point_drill_abs(
                    pt=(0.0, 0.0),
                    depth=3.0,
                    plungerate=500.0,
                    clearance=5.0,
                   ):
    '''Generate gcode for a drill operation at a single point.
Returns spindle to clearance.
Assume in absolute (G90) mode.
    '''
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    g = []
    g.append('G0 Z%s' % floatf(clearance))
    g.append('G0 X%(x)s Y%(y)s' % {
                                   'x': floatf(pt[0]),
                                   'y': floatf(pt[1]),
                                  })
    g.append('G0 Z0')
    g.append('G1 Z%(z)s F%(f)s' % {
                                   'z': floatf(depth * -1),
                                   'f':floatf(plungerate),
                                  })
    g.append('G1 Z0 F%s' % floatf(plungerate))
    g.append('G0 Z%s' % floatf(clearance))
    
    return '\n'.join(g)


def points_drill_abs(
                    pts=[(0.0, 0.0)],
                    depth=3.0,
                    plungerate=500.0,
                    clearance=5.0,
                   ):
    '''Generate gcode for a drill operations at multiple points.
Returns spindle to clearance.
Assume in absolute (G90) mode.
    '''
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    g = [point_drill_abs(pt, depth, plungerate, clearance) for pt in pts]
    return '\n'.join(g)


def point_drill_rel(
                    pt=(0.0, 0.0),
                    depth=3.0,
                    plungerate=500.0,
                    clearance=5.0,
                   ):
    '''Generate gcode for a drill operation at a single point.
Assume spindle at clearance.
Returns spindle to clearance.
Assume in relative (G91) mode.
    '''
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    g = []
    g.append('G0 X%(x)s Y%(y)s' % {
                                   'x': floatf(pt[0]),
                                   'y': floatf(pt[1]),
                                  })
    g.append('G0 Z%s' % floatf(clearance * -1))
    g.append('G1 Z%(z)s F%(f)s' % {
                                   'z': floatf(depth * -1),
                                   'f':floatf(plungerate),
                                  })
    g.append('G1 Z%(z)s F%(f)s' % {
                                   'z': floatf(depth),
                                   'f':floatf(plungerate),
                                  })
    g.append('G0 Z%s' % floatf(clearance))
    
    return '\n'.join(g)


def points_drill_rel(
                    pts=[(0.0, 0.0)],
                    depth=3.0,
                    plungerate=500.0,
                    clearance=5.0,
                   ):
    '''Generate gcode for a drill operations at multiple points.
Assume spindle at clearance.
Returns spindle to clearance and starting XY.
Assume in relative (G91) mode.
    '''
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    
    # Use points to calculate the relative movements.
    rels = vectors_between_pts(pts)
        
    g = [point_drill_rel(pt, depth, plungerate, clearance) for pt in rels]
    return '\n'.join(g)

