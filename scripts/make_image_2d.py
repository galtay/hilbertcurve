import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve

plt.figure(figsize=(10,10))
N = 2 # number of dimensions


pmax = 3
side = 2**pmax
min_coord = 0
max_coord = side - 1
cmin = min_coord - 0.5
cmax = max_coord + 0.5

colors = ['red', 'blue', 'black']
linewidths = [4, 2, 1]
offset = 0
dx = 0.5

for p in range(pmax, 0, -1):
    hc = HilbertCurve(p, N)
    sidep = 2**p

    npts = 2**(N*p)
    pts = []
    for i in range(npts):
        pts.append(hc.coordinates_from_distance(i))
    pts = [
        [(pt[0]*side/sidep) + offset,
         (pt[1]*side/sidep) + offset]
        for pt in pts]

    connectors = range(3, npts, 4)
    color = colors[p-1]
    linewidth = linewidths[p-1]
    for i in range(npts-1):
        if i in connectors:
            linestyle='--'
            alpha=0.5
        else:
            linestyle='-'
            alpha=1.0
        plt.plot((pts[i][0], pts[i+1][0]), (pts[i][1], pts[i+1][1]),
                 color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha)

    for i in range(npts):
        plt.scatter(pts[i][0], pts[i][1], 60, color=color)
        plt.text(pts[i][0] + 0.1, pts[i][1] + 0.1, str(i), color=color)

    offset += dx
    dx *= 2


plt.grid(alpha=0.3)
plt.xlim(cmin, cmax)
plt.ylim(cmin, cmax)
plt.xlabel('x_0', fontsize=16)
plt.ylabel('x_1', fontsize=16)
plt.tight_layout()
plt.savefig('nD=2_p=3.png')
