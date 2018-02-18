import matplotlib.pyplot as plt
import hilbert

plt.figure(figsize=(10,10))
N = 2 # number of dimensions
p = 3 # number of iterations
hc = hilbert.HilbertCurve(p, N)
npts = 2**(N*p)
pts = []
for i in range(npts):
    pts.append(hc.coordinates_from_distance(i))

connectors = range(3, npts, 4)
for i in range(npts-1):
    if i in connectors:
        color='grey'
        linestyle='--'
    else:
        color='black'
        linestyle='-'
    plt.plot((pts[i][0], pts[i+1][0]), (pts[i][1], pts[i+1][1]),
             color=color, linewidth=3, linestyle=linestyle)

for i in range(npts):
    plt.scatter(pts[i][0], pts[i][1], 60, color='red')
    plt.text(pts[i][0] + 0.1, pts[i][1] + 0.1, str(i))

side = 2**p - 1
cmin = -0.5
cmax = side + 0.5
plt.grid()
plt.xlim(cmin, cmax)
plt.ylim(cmin, cmax)
plt.xlabel('x_0', fontsize=16)
plt.ylabel('x_1', fontsize=16)
plt.tight_layout()
plt.savefig('nD=2_p=3.png')
