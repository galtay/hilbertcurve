import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve

N = 3
p = 3
hc = HilbertCurve(p, N)
npts = 2**(N*p)
pts = []
for i in range(npts):
    pts.append(hc.coordinates_from_distance(i))

x = [pt[0] for pt in pts]
y = [pt[1] for pt in pts]
z = [pt[2] for pt in pts]

fig = plt.figure(figsize=(10,10))
ax = fig.gca(projection='3d')
cmap = cm.nipy_spectral
s = 1
for i in range(0, npts-s, s):
    if (i+1) % 8 == 0:
        linestyle='--'
        linewidth=2
        alpha=0.4
    else:
        linestyle = '-'
        linewidth=2
        alpha=0.7
    ax.plot(x[i:i+s+1], y[i:i+s+1], z[i:i+s+1],
            linestyle=linestyle, linewidth=linewidth, alpha=alpha,
            color=cmap(i/(npts-s)))

ax.set_xlabel('x_0', fontsize=16)
ax.set_ylabel('x_1', fontsize=16)
ax.set_zlabel('x_2', fontsize=16)

plt.tight_layout()
plt.savefig('nD=3_p=3.png')
