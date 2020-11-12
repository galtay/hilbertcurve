from hilbertcurve.hilbertcurve import HilbertCurve

# When using a single iteration (p=1) in 2 dimensions (N=2) there are only 4
# locations on the curve
# distance | coordinates
# 0        | [0, 0]
# 1        | [0, 1]
# 2        | [1, 1]
# 3        | [1, 0]


# calculate distances along a hilbert curve given points
p = 1
n = 2
hilbert_curve = HilbertCurve(p, n)
points = [[0,0], [0,1], [1,1], [1,0]]
dists = hilbert_curve.distances_from_points(points)
print("simple distances from points")
for point, dist in zip(points, dists):
    print(f'distance(x={point}, p={p}, n={n}) = {dist}')
print()

# calculate coordinates given distances along a hilbert curve
p = 1
n = 2
hilbert_curve = HilbertCurve(p, n)
dists = list(range(4))
points = hilbert_curve.points_from_distances(dists)
print("simple points from distances")
for point, dist in zip(points, dists):
    print(f'point(h={dist}, p={p}, n={n}) = {point}')
print()


# due to the magic of arbitrarily large integers in
# Python (https://www.python.org/dev/peps/pep-0237/)
# these calculations can be done with absurd numbers
p = 512
n = 10
hilbert_curve = HilbertCurve(p, n)
ii = 123456789101112131415161718192021222324252627282930
points = hilbert_curve.points_from_distances([ii])
print("arbitrarily large intger points from distances")
for point, dist in zip(points, dists):
    print(f'point(h={ii}, p={p}, n={n}) = {point}')
print()


point = [121075, 67332, 67326, 108879, 26637, 43346, 23848, 1551, 68130, 84004]
dist = hilbert_curve.distances_from_points([point])[0]
print("arbitrarily large intger distances from points")
print(f'distance(x={point}, p={p}, n={n}) = {dist}')
