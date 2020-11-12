"""
This is a module to convert between one dimensional distance along a
`Hilbert curve`_, :math:`h`, and N-dimensional points,
:math:`(x_0, x_1, ... x_N)`.  The two important parameters are :math:`n`
(the number of dimensions, must be > 0) and :math:`p` (the number of
iterations used in constructing the Hilbert curve, must be > 0).

We consider an n-dimensional `hypercube`_ of side length :math:`2^p`.
This hypercube contains :math:`2^{n p}` unit hypercubes (:math:`2^p` along
each dimension).  The number of unit hypercubes determine the possible
discrete distances along the Hilbert curve (indexed from :math:`0` to
:math:`2^{n p} - 1`).
"""
from typing import Iterable, List, Union


def _binary_repr(num: int, width: int) -> str:
    """Return a binary string representation of `num` zero padded to `width`
    bits."""
    return format(num, 'b').zfill(width)


class HilbertCurve:

    def __init__(self, p: Union[int, float], n: Union[int, float]) -> None:
        """Initialize a hilbert curve with,

        Args:
            p (int or float): iterations to use in constructing the hilbert curve.
                if float, must satisfy p % 1 = 0
            n (int or float): number of dimensions.
                if float must satisfy n % 1 = 0
        """
        if (p % 1) != 0:
            raise TypeError("p is not an integer and can not be converted")
        if (n % 1) != 0:
            raise TypeError("n is not an integer and can not be converted")

        self.p = int(p)
        self.n = int(n)

        if self.p <= 0:
            raise ValueError('p must be > 0 (got p={} as input)'.format(p))
        if self.n <= 0:
            raise ValueError('n must be > 0 (got n={} as input)'.format(n))

        # minimum and maximum distance along curve
        self.min_h = 0
        self.max_h = 2**(self.p * self.n) - 1

        # minimum and maximum coordinate value in any dimension
        self.min_x = 0
        self.max_x = 2**self.p - 1

    def _hilbert_integer_to_transpose(self, h: int) -> List[int]:
        """Store a hilbert integer (`h`) as its transpose (`x`).

        Args:
            h (int): integer distance along hilbert curve

        Returns:
            x (list): transpose of h
                (n components with values between 0 and 2**p-1)
        """
        h_bit_str = _binary_repr(h, self.p*self.n)
        x = [int(h_bit_str[i::self.n], 2) for i in range(self.n)]
        return x

    def _transpose_to_hilbert_integer(self, x: Iterable[int]) -> int:
        """Restore a hilbert integer (`h`) from its transpose (`x`).

        Args:
            x (list): transpose of h
                (n components with values between 0 and 2**p-1)

        Returns:
            h (int): integer distance along hilbert curve
        """
        x_bit_str = [_binary_repr(x[i], self.p) for i in range(self.n)]
        h = int(''.join([y[i] for i in range(self.p) for y in x_bit_str]), 2)
        return h

    def points_from_distances(self, distances: Iterable[int]) -> Iterable[Iterable[int]]:
        """Return points in n-dimensional space given distances along a hilbert curve.

        Args:
            distances (iterable of int): iterable of integer distances along hilbert curve

        Returns:
            points (iterable of iterable of ints): an iterable of n-dimensional vectors
                where each vector has lengh n and component values between 0 and 2**p-1.
                the return type will match the type used for distances.
        """
        for ii, dist in enumerate(distances):
            if (dist % 1) != 0:
                raise TypeError(
                    "all values in distances must be int or floats that are convertible to "
                    "int but found distances[{}]={}".format(ii, dist))
            if dist > self.max_h:
                raise ValueError(
                    "all values in distances must be <= 2**(p*n)-1={} but found "
                    "distances[{}]={} ".format(self.max_h, ii, dist))
            if dist < self.min_h:
                raise ValueError(
                    "all values in distances must be >= {} but found distances[{}]={} "
                    "".format(self.min_h, ii, dist))

        points = []
        for dist in distances:

            x = self._hilbert_integer_to_transpose(int(dist))
            Z = 2 << (self.p-1)

            # Gray decode by H ^ (H/2)
            t = x[self.n-1] >> 1
            for i in range(self.n-1, 0, -1):
                x[i] ^= x[i-1]
            x[0] ^= t

            # Undo excess work
            Q = 2
            while Q != Z:
                P = Q - 1
                for i in range(self.n-1, -1, -1):
                    if x[i] & Q:
                        # invert
                        x[0] ^= P
                    else:
                        # exchange
                        t = (x[0] ^ x[i]) & P
                        x[0] ^= t
                        x[i] ^= t
                Q <<= 1

            points.append(x)

        # TODO: magic conversion to type(distances)
        return points


    def distances_from_points(self, points: Iterable[Iterable[int]]) -> Iterable[int]:
        """Return distance along the hilbert curve for a given set of points.

        Args:
            points (iterable of iterable of ints): an iterable of n-dimensional vectors
                where each vector has lengh n and component values between 0 and 2**p-1.

        Returns:
            distances (iterable of int): iterable of integer distances along hilbert curve
              the return type will match the type used for points.
        """
        for ii, point in enumerate(points):

            if len(point) != self.n:
                raise ValueError(
                    "all vectors in points must have length n={} "
                    "but found points[{}]={}".format(self.n, ii, point))

            if any(elx > self.max_x for elx in point):
                raise ValueError(
                    "all coordinate values in all vectors in points must be <= 2**p-1={} "
                    "but found points[{}]={}".format(self.max_x, ii, point))

            if any(elx < self.min_x for elx in point):
                raise ValueError(
                    "all coordinate values in all vectors in points must be > {} "
                    "but found points[{}]={}".format(self.min_x, ii, point))

            if any((elx % 1) != 0 for elx in point):
                raise TypeError(
                    "all coordinate values in all vectors in points must be int or floats "
                    "that are convertible to int but found points[{}]={}".format(ii, point))


        distances = []
        for point in points:

            point = [int(el) for el in point]

            M = 1 << (self.p - 1)

            # Inverse undo excess work
            Q = M
            while Q > 1:
                P = Q - 1
                for i in range(self.n):
                    if point[i] & Q:
                        point[0] ^= P
                    else:
                        t = (point[0] ^ point[i]) & P
                        point[0] ^= t
                        point[i] ^= t
                Q >>= 1

            # Gray encode
            for i in range(1, self.n):
                point[i] ^= point[i-1]
            t = 0
            Q = M
            while Q > 1:
                if point[self.n-1] & Q:
                    t ^= Q - 1
                Q >>= 1
            for i in range(self.n):
                point[i] ^= t

            distance = self._transpose_to_hilbert_integer(point)
            distances.append(distance)

        # TODO: magic conversion to type(points)
        return distances
