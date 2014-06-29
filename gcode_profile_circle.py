# Functions for profiling circles.

from gcode_base import *


def profile_circle(
                   diameter=0.0,
                   depth=0.0,
                   pitch=0.0,
                   feedrate=0.0,
                   offset=0.0,
                   direction='cw',
                   roughing=0.0,
                  ):
    '''Generate gcode for a circle at the current position using a helix.
    '''
    assert isinstance(diameter, float) and diameter > 0.0
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(pitch, float) and pitch > 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(direction, str) and direction in ['cw', 'ccw']
    assert isinstance(roughing, float) and roughing >= 0.0
    # +ve offset is always on RHS of movement, -ve on LHS.
    assert isinstance(offset, float)
    if direction == 'cw':
        radius = diameter/2 - offset
    else:
        radius = diameter/2 + offset
    assert radius > roughing
    
    rough_radius = radius - roughing
    
    g = []
    
    # Select XY plane.
    g.append('G17')
    
    # Offset from centre of hole to start spiral
    g.append('G0 Y%s' % floatf(rough_radius * -1))
    
    # First shallow loop for remainder.
    # This loop will be less than the specified pitch.
    remainder_pitch = depth % pitch
    g.append(helix_path(rough_radius, remainder_pitch, feedrate, direction))
    
    # Main helix.
    for l in range(int(depth / pitch)):
        g.append(helix_path(rough_radius, pitch, feedrate, direction))
    
    # Even out the bottom.
    g.append(helix_path(rough_radius, 0.0, feedrate, direction))
    
    # Fill radius with finishing pass.
    if roughing != 0.0:
        g.append('G0 Y%s' % floatf(roughing * -1))
        g.append(helix_path(radius, 0.0, feedrate*0.7, direction))
    
    # Go back to original position.
    g.append('G0 Z%s' % floatf(depth))
    g.append('G0 Y%s' % floatf(radius))
    
    return '\n'.join(g)

