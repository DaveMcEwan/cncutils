#!/usr/bin/env python

from gcode_base import *
from math_base import *


def polygon_profile(
                    pts=[],
                    depth=0.0,
                    pitch=0.0,
                    feedrate=0.0,
                    plungerate=0.0,
                    clearance=0.0,
                    ablpd=True,
                   ):
    '''Generate gcode for a polygon composed of straight lines between given points.
    '''

    assert isinstance(pts, list) and len(pts) > 0
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(pitch, float) and pitch > 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    
    # Use points to calculate the relative movements.
    rels = vectors_between_pts(pts)
    
    # Build list of cut depths.
    cuts = [(depth % pitch)] + [pitch for l in range(int(depth / pitch))]
    
    g = []
    
    # Assume spindle is at clearance and zeroXY.
    # Move to start XY.
    g.append('G0 X%(x)s Y%(y)s' % {
                                   'x': floatf(pts[0][0]),
                                   'y': floatf(pts[0][1]),
                                  })
    
    # Anti-BackLash Point Drill
    # Move round points and drill at each, ending back at start XY.
    if ablpd:
        g.append(points_drill_rel(pts=pts,
                              depth=depth,
                              plungerate=plungerate,
                              clearance=clearance))
    
    # Move down to Z0 at start XY
    g.append('G0 Z-%s' % floatf(clearance))
    
    # For each cut pass generate the relative gcode.
    for i, c in enumerate(cuts):
        g.append('(cut%d)' % i)
        g.append('G1 Z%(z)s F%(f)s' % {
                                       'z': floatf(c * -1),
                                       'f':floatf(plungerate),
                                      })
        g.append(points_path(pts=rels, feedrate=feedrate))
    
    # Move back to start position
    g.append('G0 Z%s' % floatf(clearance + depth))
    g.append('G0 X%(x)s Y%(y)s' % {
                                   'x': floatf(pts[0][0] * -1),
                                   'y': floatf(pts[0][1] * -1),
                                  })
    
    return '\n'.join(g)

