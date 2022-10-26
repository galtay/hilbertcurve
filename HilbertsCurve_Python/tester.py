
from hilbertcurve import HilbertCurve, _binary_repr
p=2; n=2
a = [(0, 0), (0, 1), (1, 0), (1, 1)]
new_order_arr = []
hilbert_curve = HilbertCurve(p, n)

print(_binary_repr(10, 2*2))
print(hilbert_curve.distance_from_point([6, 9]))
#print(hilbert_curve.point_from_distance(6))
