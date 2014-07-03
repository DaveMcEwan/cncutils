#!/usr/bin/env python
# Generate gcode for milling a mcdox keyboard.
# All parts specified for LHS.
# RHS should just be a reflection around X=0.

from math import *
import sys

sys.path.insert(0, '../cncutils')
from math_base import *

# Spacing between centers of cherrymx switches.
spc = 19.0


# Ergonomic column offsets for finger cluster.
c0_Y = 0.0 # 1.5x outer.
c1_Y = 0.0 # Pinky finger.
c2_Y = 3.0 # Ring finger.
c3_Y = 4.5 # Middle finger.
c4_Y = 3.0 # Index finger.
c5_Y = 1.5 # Other index finger.
c6_Y = 1.5 # 1.5x inner.

# Non-ergonomic positions from origin
c0_X = 0.0              # 1.5x outer.
c1_X = c0_X + 1.25*spc  # Pinky finger.
c2_X = c1_X + spc       # Ring finger.
c3_X = c2_X + spc       # Middle finger.
c4_X = c3_X + spc       # Index finger.
c5_X = c4_X + spc       # Other index finger.
c6_X = c5_X + spc       # 1.5x inner.

c0 = [
      (c0_X,             4*spc+c0_Y, 0),
      (c0_X,             3*spc+c0_Y, 0),
      (c0_X,             2*spc+c0_Y, 0),
      (c0_X,             1*spc+c0_Y, 0),
      (c0_X + 0.25*spc,  0*spc+c0_Y, 0),
     ]
top_left = c0[0]
c0.reverse()

c1 = [
      (c1_X,  4*spc+c1_Y, 0),
      (c1_X,  3*spc+c1_Y, 0),
      (c1_X,  2*spc+c1_Y, 0),
      (c1_X,  1*spc+c1_Y, 0),
      (c1_X,  0*spc+c1_Y, 0),
     ]

c2 = [
      (c2_X,  4*spc+c2_Y, 0),
      (c2_X,  3*spc+c2_Y, 0),
      (c2_X,  2*spc+c2_Y, 0),
      (c2_X,  1*spc+c2_Y, 0),
      (c2_X,  0*spc+c2_Y, 0),
     ]
c2.reverse()

c3 = [
      (c3_X,  4*spc+c3_Y, 0),
      (c3_X,  3*spc+c3_Y, 0),
      (c3_X,  2*spc+c3_Y, 0),
      (c3_X,  1*spc+c3_Y, 0),
      (c3_X,  0*spc+c3_Y, 0),
     ]

c4 = [
      (c4_X,  4*spc+c4_Y, 0),
      (c4_X,  3*spc+c4_Y, 0),
      (c4_X,  2*spc+c4_Y, 0),
      (c4_X,  1*spc+c4_Y, 0),
      (c4_X,  0*spc+c4_Y, 0),
     ]
c4.reverse()

c5 = [
      (c5_X,  4*spc+c5_Y, 0),
      (c5_X,  3*spc+c5_Y, 0),
      (c5_X,  2*spc+c5_Y, 0),
      (c5_X,  1*spc+c5_Y, 0),
     ]

c6 = [
      (c6_X,  4*spc+c6_Y,    0),
      (c6_X,  2.75*spc+c6_Y, 1),
      (c6_X,  1.25*spc+c6_Y, 1),
     ]
c6.reverse()

finger_mx_holes = c6 + c5 + c4 + c3 + c2 + c1 + c0
finger_mx_holes = [(p[0], p[1], p[2]*pi/2) for p in finger_mx_holes]


# Ergonomic angle of rotation for thumb cluster.
thumb_rotate = radians(-25)

# Lower left of thumb cluster is taken as the origin.
thumb_pos = [c5_X +0.5*spc, -0.5*spc]

# Centers of switch holes in thumb cluster.
thumb_mx_holes = [
                  (0*spc, 0*spc),
                  (1*spc, 0*spc),
                  (2*spc, -0.5*spc),
                  (2*spc, +0.5*spc),
                  (2*spc, +1.5*spc),
                  (1*spc, +1.5*spc),
                 ]
thumb_mx_holes = pts_rotate(thumb_mx_holes, [thumb_rotate])
thumb_mx_holes = pts_shift(thumb_mx_holes, thumb_pos)
thumb_mx_holes = [list(p) + [thumb_rotate] for p in thumb_mx_holes]
thumb_mx_holes[0][2] += pi/2
thumb_mx_holes[1][2] += pi/2
thumb_mx_holes = [tuple(p) for p in thumb_mx_holes]
bottom_right = thumb_mx_holes[2]


mx_holes = thumb_mx_holes + finger_mx_holes
center = pt_between_pts(top_left[:2], bottom_right[:2])
radius = distance_between_pts(top_left[:2], center) + spc

# mx_holes is now a list of tuples containing the coordinates and rotations of all switches on LHS.
out = []
out += ['Operations:']
out += ['\tCherryMX holes:']
for h in mx_holes:
    out += ['\t\t(%0.2f, %0.2f) rotate=%d' % (h[0], h[1], degrees(h[2]))]
out += ['\tFixing holes: TODO']
out += ['\tLED holes: TODO']
out += ['\tOuter:']
out += ['\t\tcenter=(%0.2f, %0.2f)' % center]
out += ['\t\tradius=%0.2f' % radius]
print('\n'.join(out))

# TODO: Calculate fixing holes.
# TODO: Plot fixing holes.
# TODO: Calculate LED holes.
# TODO: Plot LED holes.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ax = plt.subplot(111, aspect=1)
# Plot path between centers of switch holes.
x = [p[0] for p in mx_holes]
y = [p[1] for p in mx_holes]
ax.plot(x, y, marker='x', color='r')

# Draw circle for outer
ax.scatter(center[0], center[1])
c = mpatches.Circle(center, radius, fill=False)
ax.add_patch(c)

# Plot paths for each switch
from cherrymx_hole import *
for h in mx_holes:
    pts = pts_shift(cherrymx_points(rotate=h[2]), [h[0], h[1]])
    x = [p[0] for p in pts] + [pts[0][0]]
    y = [p[1] for p in pts] + [pts[0][1]]
    ax.plot(x, y, color='b')
plt.show()

