from hilbertcurve.hilbertcurve import HilbertCurve

# When using a single iteration (p=1) in 2 dimensions (N=2) there are only 4
# locations on the curve
# distance | coordinates
# 0        | [0, 0]
# 1        | [0, 1]
# 2        | [1, 1]
# 3        | [1, 0]


# calculate distances along a hilbert curve given coordinates
p = 1
n = 2
hilbert_curve = HilbertCurve(p, n)
for coords in [[0,0], [0,1], [1,1], [1,0]]:
    dist = hilbert_curve.distance_from_coordinates(coords)
    print(f'distance(x={coords}) = {dist}')

# calculate coordinates given distances along a hilbert curve
p = 1
n = 2
hilbert_curve = HilbertCurve(p, n)
for ii in range(4):
    print('coords(h={},p={},n={}) = {}'.format(
        ii, p, n, hilbert_curve.coordinates_from_distance(ii)))


# due to the magic of arbitrarily large integers in
# Python (https://www.python.org/dev/peps/pep-0237/)
# these calculations can be done with absurd numbers
p = 512
n = 10
hilbert_curve = HilbertCurve(p, n)
ii = 123456789101112131415161718192021222324252627282930
coords = hilbert_curve.coordinates_from_distance(ii)
print('coords(h={},p={},n={}) = {}'.format(ii, p, n, coords))


coords = [121075, 67332, 67326, 108879, 26637, 43346, 23848, 1551, 68130, 84004]
dist = hilbert_curve.distance_from_coordinates(coords)
print(f'distance(x={coords}) = {dist}')
