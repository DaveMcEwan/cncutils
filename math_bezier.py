# Math functions for calculating bezier curves in N dimensions.

from math_base import *


def pt_on_bezier_curve(P=[(0.0, 0.0)], t=0.5):
    '''Return point at t on bezier curve defined by control points P.
    '''
    assert isinstance(P, list)
    assert len(P) > 0
    for p in P:
        assert isinstance(p, tuple)
        for i in p:
            assert len(p) > 1
            assert isinstance(i, float)
    assert isinstance(t, float)
    assert 0 <= t <= 1
    
    O = len(P) - 1 # Order of curve

    # Recurse down the orders calculating the next set of control points until
    #   there is only one left, which is the point we want.
    Q = P
    while O > 0:
        Q = [pt_between_pts(Q[l], Q[l+1], t) for l in range(O)]
        O -= 1
    
    assert len(Q) == 1
    return Q[0]


def pts_on_bezier_curve(P=[(0.0, 0.0)], n_seg=0):
    '''Return list N+1 points representing N line segments on bezier curve
  defined by control points P.
    '''
    assert isinstance(P, list)
    assert len(P) > 0
    for p in P:
        assert isinstance(p, tuple)
        for i in p:
            assert len(p) > 1
            assert isinstance(i, float)
    assert isinstance(n_seg, int)
    assert n_seg >= 0
    
    return [pt_on_bezier_curve(P, float(i)/n_seg) for i in range(n_seg)] + [P[-1]]


def bezier_curve_approx_len(P=[(0.0, 0.0)]):
    '''Return approximate length of a bezier curve defined by control points P.
Segment curve into N lines where N is the order of the curve, and accumulate
  the length of the segments.
    '''
    assert isinstance(P, list)
    assert len(P) > 0
    for p in P:
        assert isinstance(p, tuple)
        for i in p:
            assert len(p) > 1
            assert isinstance(i, float)
    
    n_seg = len(P) - 1
    pts = pts_on_bezier_curve(P, n_seg)
    return sum([distance_between_pts(pts[i], pts[i+1]) for i in range(n_seg)])


def dir_on_bezier_curve(P=[(0.0, 0.0)], t=0.5):
    '''Return direction at t on bezier curve defined by control points P.
List of vectors per pair of dimensions are returned in radians.
E.g. Where X is "right", Y is "up", Z is "in" on a computer screen, and
  returned value is [pi/4, -pi/4], then the vector will be coming out the
  screen over the viewer's right shoulder.
    '''
    assert isinstance(P, list)
    assert len(P) > 0
    if not len(P) > 1:
        return None # Points have no gradient.
    for p in P:
        assert isinstance(p, tuple)
        for i in p:
            assert len(p) > 1
            assert isinstance(i, float)
    assert isinstance(t, float)
    assert 0 <= t <= 1
    
    O = len(P) - 1 # Order of curve
    
    # Recurse down the orders calculating the next set of control points until
    #   there are only two left, which is the points on the gradient we want.
    Q = P
    while O > 1:
        Q = [pt_between_pts(Q[l], Q[l+1], t) for l in range(O)]
        O -= 1
    
    assert len(Q) == 2
    # Now that we have the two points in N dimensions, we can reduce to the
    #   gradients on N-1 planes.
    q0 = Q[0]
    q1 = Q[1]
    
    return dir_between_pts(q0, q1)

