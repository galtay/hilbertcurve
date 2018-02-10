import hilbert

# we can go from distance along a curve to coordinates
# in 2 dimensions with p=1 there are only 4 locations on the curve
# [0, 0], [0, 1], [1, 1], [1, 0]
p = 1
N = 2
for ii in range(4):
    print(hilbert.coordinates_from_distance(ii, p, N))


# due to the magic of arbitrarily large integers in
# Python (https://www.python.org/dev/peps/pep-0237/)
# these calculations can be done with absurd numbers
p = 512
N = 10
ii = 1234567891011121314151617181920
coords = hilbert.coordinates_from_distance(ii, p, N)
