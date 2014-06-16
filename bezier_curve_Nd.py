# Math functions for calculating bezier curves in N dimensions.

import math


def pt_between_pts(a=(0.0, 0.0), b=(0.0, 0.0), t=0.5):
    '''Return the point between two points on N dimensions.
    '''
    assert isinstance(a, tuple)
    assert isinstance(b, tuple)
    assert len(a) > 1
    assert len(a) == len(b)
    for i in a:
        assert isinstance(i, float)
    for i in b:
        assert isinstance(i, float)
    assert isinstance(t, float)
    assert 0 <= t <= 1
    
    L = len(a)
    return tuple([ ((b[i] - a[i]) * t) + a[i] for i in range(L) ])


def distance_between_pts(a=(0.0, 0.0), b=(0.0, 0.0)):
    '''Return the distance between two points on N dimensions (Euclidean distance).
    '''
    assert isinstance(a, tuple)
    assert isinstance(b, tuple)
    assert len(a) > 1
    assert len(a) == len(b)
    for i in a:
        assert isinstance(i, float)
    for i in b:
        assert isinstance(i, float)
    
    L = len(a)
    return math.sqrt(sum([(b[i] - a[i])**2 for i in range(L)]))


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

