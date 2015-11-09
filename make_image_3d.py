import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import hilbert

nD = 3
pH = 4
npts = 2**(nD*pH)
pts = []
for i in range(npts):
    pts.append(hilbert.transpose2axes(i, pH, nD))

x = [p[0] for p in pts]
y = [p[1] for p in pts]
z = [p[2] for p in pts]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z, linewidth=2.0, alpha=0.6)

side = 2**pH - 1
cmin = -0.5
cmax = side + 0.5

ax.set_xlim(cmin, cmax)
ax.set_ylim(cmin, cmax)
ax.set_zlim(cmin, cmax)

ax.set_xlabel('x_0', fontsize=16)
ax.set_ylabel('x_1', fontsize=16)
ax.set_zlabel('x_2', fontsize=16)
