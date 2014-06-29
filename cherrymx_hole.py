#!/usr/bin/env python
# Everything is always in millimeters, not stupid imperial!
# Jog machine to desired location then run the output generated by this script.

from gcode_base import *
from gcode_profile_polygon import *
from math_base import *


def cherrymx_profile(
                     width=14.0,
                     depth=0.0,
                     notch_depth=0.0,
                     notch_height=0.0,
                     rotate=0.0,
                     pitch=0.0,
                     feedrate=0.0,
                     plungerate=0.0,
                     clearance=0.0,
                     endmill=0.0,
                     direction='',
                     ablpd=True,
                    ): # {{{
    '''Generate gcode for a hole at the current position to hold cherry mx switches.
    '''

    assert isinstance(width, float) and width > 0.0
    assert isinstance(depth, float) and depth > 0.0
    assert notch_depth >= endmill/2
    assert notch_height >= endmill/2
    assert isinstance(rotate, float) and abs(rotate) <= 2*pi
    assert isinstance(pitch, float) and pitch > 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    # Endmill size > 0 assertion not needed as you may want to just generate a
    #   "dumb" path for a different shape of endmill.
    assert isinstance(endmill, float) and endmill < width
    assert isinstance(direction, str) and direction in ['cw', 'ccw']
    assert isinstance(ablpd, bool)
    
    # Calculate points to move to.
    inner_x = width/2 - endmill/2
    outer_x = inner_x + notch_depth
    outer_y = inner_x
    inner_y =  width/2 - notch_height + endmill/2
    
    # Points relative to centre listed in CW direction.
    pts = [
           (-inner_x, +inner_y),
           (-outer_x, +inner_y),
           (-outer_x, +outer_y),
           (+outer_x, +outer_y),
           (+outer_x, +inner_y),
           (+inner_x, +inner_y),
           (+inner_x, -inner_y),
           (+outer_x, -inner_y),
           (+outer_x, -outer_y),
           (-outer_x, -outer_y),
           (-outer_x, -inner_y),
           (-inner_x, -inner_y),
          ]
    
    if direction == 'ccw':
        pts.reverse()
    
    # Rotate points around origin here.
    pts = pts_rotate(pts, [rotate], (0.0, 0.0))
    
    # Initialise gcode lines.
    g = []
    
    # Set units as millimeters.
    g.append('G21')
    
    # Use relative positioning (as opposed to absolute).
    # Required to make this code callable like a function.
    g.append('G91')
    
    g.append(polygon_profile(
                             pts=pts,
                             depth=depth,
                             pitch=pitch,
                             feedrate=feedrate,
                             plungerate=plungerate,
                             clearance=clearance,
                             ablpd=ablpd,
                            ))
    
    return '\n'.join(g)
# }}}


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--width',
                        action='store',
                        default=13.5,
                        type=float,
                        help='hole width')
    
    parser.add_argument('--depth',
                        action='store',
                        default=7.0,
                        type=float,
                        help='hole depth')
    
    parser.add_argument('--notch_depth',
                        action='store',
                        default=1.5,
                        type=float,
                        help='notch depth')
    
    parser.add_argument('--notch_height',
                        action='store',
                        default=4.0,
                        type=float,
                        help='notch height')
    
    parser.add_argument('--rotate',
                        action='store',
                        default=0.0,
                        type=float,
                        help='rotation of hole (radians)')
    
    parser.add_argument('--pitch',
                        action='store',
                        default=1.0,
                        type=float,
                        help='cutting pitch')
    
    parser.add_argument('--feedrate',
                        action='store',
                        default=500.0,
                        type=float,
                        help='feedrate (mm/minute)')
    
    parser.add_argument('--plungerate',
                        action='store',
                        default=500.0,
                        type=float,
                        help='plungerate (mm/minute)')
    
    parser.add_argument('--clearance',
                        action='store',
                        default=5.0,
                        type=float,
                        help='clearance (mm)')
    
    parser.add_argument('--endmill',
                        action='store',
                        default=3.0,
                        type=float,
                        help='endmill diameter (cylindrical)')
    
    parser.add_argument('--direction',
                        action='store',
                        default='cw',
                        choices=['cw', 'ccw'],
                        help='cutting direction')
    
    parser.add_argument('--ablpd',
                        action='store',
                        default=1,
                        type=int,
                        choices=[0, 1],
                        help='Anti Backlash Point Drilling')

    args = parser.parse_args()
    
    # Initialise gcode lines.
    g = []
    
    # Select XY plane.
    g.append('G17')
    
    # Set units as millimeters.
    g.append('G21')
    
    # Assume spindle starts at zero.
    g.append('G91 G0 Z%s' % floatf(args.clearance))
    
    # Cherry profile function should assume spindle at clearance.
    g.append(cherrymx_profile(
                              width=args.width,
                              depth=args.depth,
                              notch_depth=args.notch_depth,
                              notch_height=args.notch_height,
                              rotate=args.rotate,
                              pitch=args.pitch,
                              feedrate=args.feedrate,
                              plungerate=args.plungerate,
                              clearance=args.clearance,
                              endmill=args.endmill,
                              direction=args.direction,
                              ablpd=bool(args.ablpd),
                             ))
    # Cherry profile function should leave spindle at clearance.

    # Put gcode onto STDOUT to let caller do any file redirect.
    print('\n'.join(g))
