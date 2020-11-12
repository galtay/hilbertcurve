import numpy as np
import time
from hilbertcurve.hilbertcurve import HilbertCurve


do_multiprocessing_test = True


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
print("="*80)
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
print("="*80)
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
print("arbitrarily large integer points from distances")
print("="*80)
for point, dist in zip(points, dists):
    print(f'point(h={ii}, p={p}, n={n}) = {point}')
print()


points = [
    [121075, 67332, 67326, 108879, 26637, 43346, 23848, 1551, 68130, 84004]
]
points_check = list(points)
dists = hilbert_curve.distances_from_points(points)
print("arbitrarily large integer distances from points")
print("="*80)
for point, dist in zip(points, dists):
    print(f'distance(x={point}, p={p}, n={n}) = {dist}')
print()
assert(points == points_check)



if do_multiprocessing_test:

    p = 8
    n = 7

    print("speed test single core")
    print("="*80)
    hilbert_curve = HilbertCurve(p, n)
    for num_points in [1_000, 10_000, 100_000, 1_000_000]:
        t1 = time.time()
        points = np.random.randint(
            low=0,
            high=hilbert_curve.max_x,
            size=(num_points, hilbert_curve.n)
        )
        t2 = time.time()
        print("created {} points in {:.3f}".format(num_points, t2-t1))

        t1 = time.time()
        distances = hilbert_curve.distances_from_points(points)
        t2 = time.time()
        print("calculated {} distances in {:.3f}".format(num_points, t2-t1))
        print()

    print("speed test multi core")
    print("="*80)
    hilbert_curve = HilbertCurve(p, n, n_procs=-1)
    for num_points in [1_000, 10_000, 100_000, 1_000_000]:
        t1 = time.time()
        points = np.random.randint(
            low=0,
            high=hilbert_curve.max_x,
            size=(num_points, hilbert_curve.n)
        )
        t2 = time.time()
        print("created {} points in {:.3f}".format(num_points, t2-t1))

        t1 = time.time()
        distances = hilbert_curve.distances_from_points(points)
        t2 = time.time()
        print("calculated {} distances in {:.3f}".format(num_points, t2-t1))
        print()
