from hilbertcurve.hilbertcurve import HilbertCurve

# we can go from distance along a curve to coordinates
# in 2 dimensions with p=1 there are only 4 locations on the curve
# [0, 0], [0, 1], [1, 1], [1, 0]
p = 1
N = 2
hilbert_curve = HilbertCurve(p, N)
for ii in range(4):
    print('coords(h={},p={},N={}) = {}'.format(
        ii, p, N, hilbert_curve.coordinates_from_distance(ii)))


# due to the magic of arbitrarily large integers in
# Python (https://www.python.org/dev/peps/pep-0237/)
# these calculations can be done with absurd numbers
p = 512
N = 10
hilbert_curve = HilbertCurve(p, N)
ii = 123456789101112131415161718192021222324252627282930
coords = hilbert_curve.coordinates_from_distance(ii)
print('coords(h={},p={},N={}) = {}'.format(ii, p, N, coords))
