"""
This is a module to convert between one dimensional distance along a
`Hilbert curve`_, :math:`h`, and N-dimensional coordinates,
:math:`(x_0, x_1, ... x_N)`.  The two important parameters are :math:`N`
(the number of dimensions, must be > 0) and :math:`p` (the number of
iterations used in constructing the Hilbert curve, must be > 0).

We consider an N-dimensional `hypercube`_ of side length :math:`2^p`.
This hypercube contains :math:`2^{N p}` unit hypercubes (:math:`2^p` along
each dimension).  The number of unit hypercubes determine the possible
discrete distances along the Hilbert curve (indexed from :math:`0` to
:math:`2^{N p} - 1`).
"""
from typing import Iterable, List, Union


def _binary_repr(num: int, width:int) -> str:
    """Return a binary string representation of `num` zero padded to `width`
    bits."""
    return format(num, 'b').zfill(width)


class HilbertCurve:

    def __init__(self, p: int, n: int) -> None:
        """Initialize a hilbert curve with,

        Args:
            p (int): iterations to use in constructing the hilbert curve
            n (int): number of dimensions
        """
        if p <= 0:
            raise ValueError('p must be > 0')
        if n <= 0:
            raise ValueError('n must be > 0')
        self.p = p
        self.n = n

        # maximum distance along curve
        self.max_h = 2**(self.p * self.n) - 1

        # maximum coordinate value in any dimension
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

    def _transpose_to_hilbert_integer(self, x: List[int]) -> int:
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

    def coordinates_from_distance(self, h: int) -> List[int]:
        """Return the coordinates for a given hilbert distance.

        Args:
            h (int): integer distance along hilbert curve

        Returns:
            x (list): transpose of h
                      (n components with values between 0 and 2**p-1)
        """
        if h > self.max_h:
            raise ValueError('h={} is greater than 2**(p*N)-1={}'.format(h, self.max_h))
        if h < 0:
            raise ValueError('h={} but must be > 0'.format(h))

        x = self._hilbert_integer_to_transpose(h)
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

        # done
        return x

    def distance_from_coordinates(self, *cords: Union[Iterable[int], int]) -> int:
        """Return the hilbert distance for a given set of coordinates.

        Args:
            *cords : transpose of h
                         (n components with values between 0 and 2**p-1)
            A single list or tuple is accepted or a set of n individual coordinates, but not both:
                distance_from_coordinates([x,y,z,...,etc])
                distance_from_coordinates((x,y,z,...,etc))
                distance_from_coordinates(x,y,z,...,etc)

        Returns:
            h (int): integer distance along hilbert curve
        """

        if len(cords) is 0:
            raise TypeError(
                'No arguments were given. '
                'A list, a tuple, or individual coordinates is expected')
        try:
            #this is the only reliable way to check if an object is iterable
            iter(cords[0])
        except:
            #when the first object is not iterable we assume that it is a set of individual coordinates
            x = list(cords)
        else:
            #now we check that they haven't passed an iterable and anything else
            if len(cords) > 1:
                raise TypeError(
                    'Only one argument accepted when using a list or tuple')
            x = list(cords[0])

        if len(x) != self.n:
            raise ValueError('x={} must have N={} dimensions'.format(x, self.n))

        if any(elx > self.max_x for elx in x):
            raise ValueError(
                'invalid coordinate input x={}.  one or more dimensions have a '
                'value greater than 2**p-1={}'.format(x, self.max_x))

        if any(elx < 0 for elx in x):
            raise ValueError(
                'invalid coordinate input x={}.  one or more dimensions have a '
                'value less than 0'.format(x))

        M = 1 << (self.p - 1)

        # Inverse undo excess work
        Q = M
        while Q > 1:
            P = Q - 1
            for i in range(self.n):
                if x[i] & Q:
                    x[0] ^= P
                else:
                    t = (x[0] ^ x[i]) & P
                    x[0] ^= t
                    x[i] ^= t
            Q >>= 1

        # Gray encode
        for i in range(1, self.n):
            x[i] ^= x[i-1]
        t = 0
        Q = M
        while Q > 1:
            if x[self.n-1] & Q:
                t ^= Q - 1
            Q >>= 1
        for i in range(self.n):
            x[i] ^= t

        h = self._transpose_to_hilbert_integer(x)
        return h
