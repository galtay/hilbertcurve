#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import hilbert

N = 3
p = 4
npts = 2**(N*p)
pts = []
for i in range(npts):
    pts.append(hilbert.coordinates_from_distance(i, p, N))

x = [pt[0] for pt in pts]
y = [pt[1] for pt in pts]
z = [pt[2] for pt in pts]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z, linewidth=2.0, alpha=0.6)

side = 2**p - 1
cmin = -0.5
cmax = side + 0.5

ax.set_xlim(cmin, cmax)
ax.set_ylim(cmin, cmax)
ax.set_zlim(cmin, cmax)

ax.set_xlabel('x_0', fontsize=16)
ax.set_ylabel('x_1', fontsize=16)
ax.set_zlabel('x_2', fontsize=16)

plt.show()
