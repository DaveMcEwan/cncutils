# Base math functions for manipulating geometry.
# Intended to be used as from math_base import * as this gets all the python
#   math functions too.

from math import *


def vectors_between_pts(pts=[]):
    '''Return vectors between points on N dimensions.
Last vector is the path between the first and last point, creating a loop.
    '''
    assert isinstance(pts, list) and len(pts) > 0
    l_pts = len(pts)
    l_pt_prev = None
    for pt in pts:
        assert isinstance(pt, tuple)
        l_pt = len(pt)
        assert l_pt > 1
        for i in pt:
            assert isinstance(i, float)
        if l_pt_prev is not None:
            assert l_pt == l_pt_prev
        l_pt_prev = l_pt
    
    return [tuple([pts[(i+1) % l_pts][j] - pts[i][j] for j in range(l_pt)]) \
            for i in range(l_pts)]


def pt_between_pts(a=(0.0, 0.0), b=(0.0, 0.0), t=0.5):
    '''Return the point between two points on N dimensions.
    '''
    assert isinstance(a, tuple)
    assert isinstance(b, tuple)
    l_pt = len(a)
    assert l_pt > 1
    assert l_pt == len(b)
    for i in a:
        assert isinstance(i, float)
    for i in b:
        assert isinstance(i, float)
    assert isinstance(t, float)
    assert 0 <= t <= 1
    
    return tuple([ ((b[i] - a[i]) * t) + a[i] for i in range(l_pt) ])


def distance_between_pts(a=(0.0, 0.0), b=(0.0, 0.0)):
    '''Return the distance between two points on N dimensions (Euclidean distance).
    '''
    assert isinstance(a, tuple)
    assert isinstance(b, tuple)
    l_pt = len(a)
    assert l_pt > 1
    assert l_pt == len(b)
    for i in a:
        assert isinstance(i, float)
    for i in b:
        assert isinstance(i, float)
    
    return sqrt(sum([(b[i] - a[i])**2 for i in range(l_pt)]))


def pt_rotate(pt=(0.0, 0.0), angle=[0.0], center=(0.0, 0.0)):
    '''Return given point rotated around a center point in N dimensions.
Angle is list of rotation in radians for each pair of axis.
    '''
    assert isinstance(pt, tuple)
    l_pt = len(pt)
    assert l_pt > 1
    for i in pt:
        assert isinstance(i, float)
    assert isinstance(angle, list)
    l_angle = len(angle)
    assert l_angle == l_pt-1
    for i in angle:
        assert isinstance(i, float)
        assert abs(i) <= 2*pi
    assert isinstance(center, tuple)
    assert len(center) == l_pt
    for i in center:
        assert isinstance(i, float)
    
    # Get vector from center to point and use to get relative polar coordinate.
    v_cart = [pt[i] - center[i] for i in range(l_pt)]
    
    # Length of vector needs to stay constant for new point.
    v_pol_l = [sqrt(v_cart[i]**2 + v_cart[i+1]**2) for i in range(l_angle)]
    v_pol_a = [atan(v_cart[i+1] / v_cart[i]) + pi*int(pt[i] < center[i]) \
               for i in range(l_angle)]
    
    # Add rotation angle then convert back to cartesian vector.
    n_pol_a = [v_pol_a[i] + angle[i] for i in range(l_angle)]
    n_cart = [v_pol_l[0] * cos(n_pol_a[0])] + [v_pol_l[i] * sin(n_pol_a[i])\
                                               for i in range(l_angle)]
    
    # Add in the centre offset to get original offset from c.
    r = [n_cart[i] + center[i] for i in range(l_pt)]
    return tuple(r)


def pts_rotate(pts=[], angle=[0.0], center=(0.0, 0.0)):
    '''Return given points rotated around a center point in N dimensions.
Angle is list of rotation in radians for each pair of axis.
    '''
    assert isinstance(pts, list) and len(pts) > 0
    l_pt_prev = None
    for pt in pts:
        assert isinstance(pt, tuple)
        l_pt = len(pt)
        assert l_pt > 1
        for i in pt:
            assert isinstance(i, float)
        if l_pt_prev is not None:
            assert l_pt == l_pt_prev
        l_pt_prev = l_pt
    assert isinstance(angle, list)
    l_angle = len(angle)
    assert l_angle == l_pt-1
    for i in angle:
        assert isinstance(i, float)
    assert isinstance(center, tuple)
    assert len(center) == l_pt
    for i in center:
        assert isinstance(i, float)
    
    return [pt_rotate(pt, angle, center) for pt in pts]


def pt_shift(pt=(0.0, 0.0), shift=[0.0, 0.0]):
    '''Return given point shifted in N dimensions.
    '''
    assert isinstance(pt, tuple)
    l_pt = len(pt)
    assert l_pt > 1
    for i in pt:
        assert isinstance(i, float)
    assert isinstance(shift, list)
    l_sh = len(shift)
    assert l_sh == l_pt
    for i in shift:
        assert isinstance(i, float)

    return tuple([pt[i] + shift[i] for i in range(pt)])


def pts_shift(pts=[], shift=[0.0, 0.0]):
    '''Return given points shifted in N dimensions.
    '''
    assert isinstance(pts, list) and len(pts) > 0
    l_pt_prev = None
    for pt in pts:
        assert isinstance(pt, tuple)
        l_pt = len(pt)
        assert l_pt > 1
        for i in pt:
            assert isinstance(i, float)
        if l_pt_prev is not None:
            assert l_pt == l_pt_prev
        l_pt_prev = l_pt
    assert isinstance(shift, list)
    l_sh = len(shift)
    assert l_sh == l_pt
    for i in shift:
        assert isinstance(i, float)
    
    return [pt_shift(pt, shift) for pt in pts]


def pt_reflect(pt=(0.0, 0.0), plane=[None, None]):
    '''Return given point reflected around planes in N dimensions.
There must be the same number of planes as dimensions, but the value of each
  plane may be None to indicate no reflection.
    '''
    assert isinstance(pt, tuple)
    l_pt = len(pt)
    assert l_pt > 1
    for i in pt:
        assert isinstance(i, float)
    assert isinstance(plane, list)
    l_pl = len(plane)
    assert l_pl == l_pt
    for i in plane:
        assert isinstance(i, float) or i is None
    
    return [pt[i] if plane[i] is None else (2*plane[i] - pt[i]) for i in range(l_pt)]


def pts_reflect(pts=[], plane=[None, None]):
    '''Return given point reflected around planes in N dimensions.
There must be the same number of planes as dimensions, but the value of each
  plane may be None to indicate no reflection.
    '''
    assert isinstance(pts, list) and len(pts) > 0
    l_pt_prev = None
    for pt in pts:
        assert isinstance(pt, tuple)
        l_pt = len(pt)
        assert l_pt > 1
        for i in pt:
            assert isinstance(i, float)
        if l_pt_prev is not None:
            assert l_pt == l_pt_prev
        l_pt_prev = l_pt
    assert isinstance(plane, list)
    l_pl = len(plane)
    assert l_pl == l_pt
    for i in plane:
        assert isinstance(i, float) or i is None
    
    return [pt_reflect(pt, plane) for pt in pts]

