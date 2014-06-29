# Base math functions for manipulating geometry.
# Intended to be used as from math_base import * as this gets all the python
#   math functions too.

from math import *


def pts_to_rels(pts=[]):
    '''Return vectors between points on 2 dimensions.
    '''
    assert isinstance(pts, list) and len(pts) > 0
    l_pts = len(pts)
    rels = [(pts[(i+1) % l_pts][0] - pts[i][0],
             pts[(i+1) % l_pts][1] - pts[i][1]) for i in range(l_pts)]
    return rels


def pt_rotate(p=(0.0, 0.0), angle=0.0, center=(0.0, 0.0)):
    '''Return given point rotated around a center point.
Angle should be in radians.
Only works is 2 dimensions
    '''
    # Get vector from center to point and use to get relative polar coordinate.
    v_cart = (p[0] - center[0], p[1] - center[1])
    semiturn = pi * int(p[0] < center[0])
    # Length of vector needs to stay constant for new point.
    v_pol_l = sqrt(v_cart[0]**2 + v_cart[1]**2)
    v_pol_a = atan(v_cart[1] / v_cart[0]) + semiturn
    # Add rotation angle then convert back to cartesian vector.
    n_pol_a = v_pol_a + angle
    n_cart = (v_pol_l*cos(n_pol_a), v_pol_l*sin(n_pol_a))
    # Add in the centre offset to get original offset from center.
    r = (n_cart[0] + center[0], n_cart[1] + center[1])
    return r


def pts_rotate(pts=[], angle=0.0, center=(0.0, 0.0)):
    '''Return given points rotated around a center point.
Angle should be in radians.
Only works is 2 dimensions
    '''
    assert isinstance(pts, list) and len(pts) > 0
    assert isinstance(angle, float) and abs(angle) <= 2*pi
    return [pt_rotate(p=p, angle=angle, center=center) for p in pts]

