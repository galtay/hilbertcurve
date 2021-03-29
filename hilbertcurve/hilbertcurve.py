"""
This is a module to convert between one dimensional distance along a
`Hilbert curve`_, :math:`h`, and n-dimensional points,
:math:`(x_0, x_1, ... x_n)`.  The two important parameters are :math:`n`
(the number of dimensions, must be > 0) and :math:`p` (the number of
iterations used in constructing the Hilbert curve, must be > 0).

We consider an n-dimensional `hypercube`_ of side length :math:`2^p`.
This hypercube contains :math:`2^{n p}` unit hypercubes (:math:`2^p` along
each dimension).  The number of unit hypercubes determine the possible
discrete distances along the Hilbert curve (indexed from :math:`0` to
:math:`2^{n p} - 1`).
"""
from typing import Iterable, List, Union
import multiprocessing
from multiprocessing import Pool
import numpy as np



def _binary_repr(num: int, width: int) -> str:
    """Return a binary string representation of `num` zero padded to `width`
    bits."""
    return format(num, 'b').zfill(width)


class HilbertCurve:

    def __init__(
        self,
        p: Union[int, float],
        n: Union[int, float],
        n_procs: int=0,
    ) -> None:

        """Initialize a hilbert curve with,

        Args:
            p (int or float): iterations to use in constructing the hilbert curve.
                if float, must satisfy p % 1 = 0
            n (int or float): number of dimensions.
                if float must satisfy n % 1 = 0
            n_procs (int): number of processes to use
                0 = dont use multiprocessing
               -1 = use all available threads
                any other positive integer = number of processes to use

        """
        if (p % 1) != 0:
            raise TypeError("p is not an integer and can not be converted")
        if (n % 1) != 0:
            raise TypeError("n is not an integer and can not be converted")
        if (n_procs % 1) != 0:
            raise TypeError("n_procs is not an integer and can not be converted")

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

        # set n_procs
        n_procs = int(n_procs)
        if n_procs == -1:
            self.n_procs = multiprocessing.cpu_count()
        elif n_procs == 0:
            self.n_procs = 0
        elif n_procs > 0:
            self.n_procs = n_procs
        else:
            raise ValueError(
                'n_procs must be >= -1 (got n_procs={} as input)'.format(n_procs))


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


    def point_from_distance(self, distance: int) -> Iterable[int]:
        """Return a point in n-dimensional space given a distance along a hilbert curve.

        Args:
            distance (int): integer distance along hilbert curve

        Returns:
            point (iterable of ints): an n-dimensional vector of lengh n where
            each component value is between 0 and 2**p-1.
        """
        x = self._hilbert_integer_to_transpose(int(distance))
        z = 2 << (self.p-1)

        # Gray decode by H ^ (H/2)
        t = x[self.n-1] >> 1
        for i in range(self.n-1, 0, -1):
            x[i] ^= x[i-1]
        x[0] ^= t

        # Undo excess work
        q = 2
        while q != z:
            p = q - 1
            for i in range(self.n-1, -1, -1):
                if x[i] & q:
                    # invert
                    x[0] ^= p
                else:
                    # exchange
                    t = (x[0] ^ x[i]) & p
                    x[0] ^= t
                    x[i] ^= t
            q <<= 1

        return x


    def points_from_distances(
        self,
        distances: Iterable[int],
        match_type: bool=False,
    ) -> Iterable[Iterable[int]]:
        """Return points in n-dimensional space given distances along a hilbert curve.

        Args:
            distances (iterable of int): iterable of integer distances along hilbert curve
            match_type (bool): if True, make type(points) = type(distances)

        Returns:
            points (iterable of iterable of ints): an iterable of n-dimensional vectors
                where each vector has lengh n and component values between 0 and 2**p-1.
                if match_type=False will be list of lists else type(points) = type(distances)
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

        if self.n_procs == 0:
            points = []
            for distance in distances:
                x = self.point_from_distance(distance)
                points.append(x)
        else:
            with Pool(self.n_procs) as p:
                points = p.map(self.point_from_distance, distances)

        if match_type:
            if isinstance(distances, np.ndarray):
                points = np.array(points, dtype=distances.dtype)
            else:
                target_type = type(distances)
                points = target_type([target_type(vec) for vec in points])

        return points


    def distance_from_point(self, point: Iterable[int]) -> int:
        """Return distance along the hilbert curve for a given point.

        Args:
            point (iterable of ints): an n-dimensional vector where each component value
                is between 0 and 2**p-1.

        Returns:
            distance (int): integer distance along hilbert curve
        """
        point = [int(el) for el in point]

        m = 1 << (self.p - 1)

        # Inverse undo excess work
        q = m
        while q > 1:
            p = q - 1
            for i in range(self.n):
                if point[i] & q:
                    point[0] ^= p
                else:
                    t = (point[0] ^ point[i]) & p
                    point[0] ^= t
                    point[i] ^= t
            q >>= 1

        # Gray encode
        for i in range(1, self.n):
            point[i] ^= point[i-1]
        t = 0
        q = m
        while q > 1:
            if point[self.n-1] & q:
                t ^= q - 1
            q >>= 1
        for i in range(self.n):
            point[i] ^= t

        distance = self._transpose_to_hilbert_integer(point)
        return distance


    def distances_from_points(
        self,
        points: Iterable[Iterable[int]],
        match_type: bool=False,
    ) -> Iterable[int]:
        """Return distances along the hilbert curve for a given set of points.

        Args:
            points (iterable of iterable of ints): an iterable of n-dimensional vectors
                where each vector has lengh n and component values between 0 and 2**p-1.
            match_type (bool): if True, make type(distances) = type(points)

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

        if self.n_procs == 0:
            distances = []
            for point in points:
                distance = self.distance_from_point(point)
                distances.append(distance)
        else:
            with Pool(self.n_procs) as p:
                distances = p.map(self.distance_from_point, points)

        if match_type:
            if isinstance(points, np.ndarray):
                distances = np.array(distances, dtype=points.dtype)
            else:
                target_type = type(points)
                distances = target_type(distances)

        return distances


    def __str__(self):
        return f"HilbertCruve(p={self.p}, n={self.n}, n_procs={self.n_procs})"


    def __repr__(self):
        return self.__str__()
