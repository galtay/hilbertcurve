import matplotlib.pyplot as plt
import hilbert

nD = 2 # number of dimensions
pH = 3 # number of iterations
npts = 2**(nD*pH)
pts = []
for i in range(npts):
    pts.append(hilbert.transpose2axes(i, pH, nD))

plt.figure(figsize=(10,10))
connectors = range(3,npts,4)
for i in range(npts-1):
    if i in connectors:
        color='grey'
        linestyle='--'
    else:
        color='black'
        linestyle='-'
    plt.plot( (pts[i][0], pts[i+1][0]), (pts[i][1], pts[i+1][1]),
              color=color, linewidth=3, linestyle=linestyle)

for i in range(npts):
    plt.scatter(pts[i][0], pts[i][1], 60, color='red')
    plt.text(pts[i][0] + 0.1, pts[i][1] + 0.1, str(i))

side = 2**pH - 1
cmin = -0.5
cmax = side + 0.5
plt.grid()
plt.xlim(cmin, cmax)
plt.ylim(cmin, cmax)
plt.xlabel('x_0', fontsize=16)
plt.ylabel('x_1', fontsize=16)
plt.tight_layout()
plt.savefig('nD=2_p=3.png')


#    nD = 3
#    pH = 3
#    npts = 2**(nD*pH)
#    pts = []
#    for i in range(npts):
#        pts.append(transpose2axes(i, pH, nD))

#    import matplotlib as mpl
#    from mpl_toolkits.mplot3d import Axes3D

#    x = [p[0] for p in pts]
#    y = [p[1] for p in pts]
#    z = [p[2] for p in pts]

#    fig = plt.figure()
#    ax = fig.gca(projection='3d')
#    ax.plot(x, y, z, linewidth=2.0, alpha=0.6)

#    side = 2**pH - 1
#    cmin = -0.5
#    cmax = side + 0.5

#    plt.xlim(cmin, cmax)
#    plt.ylim(cmin, cmax)
#    plt.zlim(cmin, cmax)
