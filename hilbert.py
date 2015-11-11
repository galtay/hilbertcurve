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
:math:`2^{N p} - 1`).  The image below illustrates the situation for
:math:`N=2` and :math:`p=3`.

.. figure:: nD=2_p=3.png

   This is the third iteration (:math:`p=3`) of the Hilbert curve in two
   (:math:`N=2`) dimensions.  Distances, :math:`h`, along the curve are
   labeled from 0 to 63 (i.e. from 0 to :math:`2^{N p}-1`).  The provided
   functions translate between N-dimensional coordinates and the one
   dimensional distance.  For example, between (:math:`x_0=4, x_1=6`) and
   :math:`h=36`.

Reference
=========

This module is based on the C code provided in the 2004 article
"Programming the Hilbert Curve" by John Skilling,

  - http://adsabs.harvard.edu/abs/2004AIPC..707..381S

I was also helped by the discussion in the following stackoverflow post,

  - `mapping-n-dimensional-value-to-a-point-on-hilbert-curve`_

which points out a typo in the source code of the paper.  The Skilling code
provides two functions ``TransposetoAxes`` and ``AxestoTranspose``.  In this
case, Transpose refers to a specific packing of the integer that represents
distance along the Hilbert curve (see below for details) and
Axes refer to the N-dimensional coordinates.  Below is an excerpt of the docs
from that code that appears in the paper by Skilling, ::

//+++++++++++++++++++++++++++ PUBLIC-DOMAIN SOFTWARE ++++++++++++++++++++++++++
// Functions: TransposetoAxes  AxestoTranspose
// Purpose:   Transform in-place between Hilbert transpose and geometrical axes
// Example:   b=5 bits for each of n=3 coordinates.
//            15-bit Hilbert integer = A B C D E F G H I J K L M N O is stored
//            as its Transpose
//                   X[0] = A D G J M                X[2]|
//                   X[1] = B E H K N    <------->       | /X[1]
//                   X[2] = C F I L O               axes |/
//                          high  low                    0------ X[0]
//            Axes are stored conveniently as b-bit integers.
// Author:    John Skilling  20 Apr 2001 to 11 Oct 2003


.. _Hilbert curve: https://en.wikipedia.org/wiki/Hilbert_curve
.. _hypercube: https://en.wikipedia.org/wiki/Hypercube
.. _mapping-n-dimensional-value-to-a-point-on-hilbert-curve: http://stackoverflow.com/questions/499166/mapping-n-dimensional-value-to-a-point-on-hilbert-curve/10384110#10384110
"""

def _binary_repr(num, width):
    """Return a binary string representation of `num` zero padded to `width`
    bits."""
    return format(num, 'b').zfill(width)

def _hilbert_integer_to_transpose(h, p, N):
    """Store a hilbert integer (`h`) as its transpose (`x`).

    :param h: integer distance along hilbert curve
    :type h: ``int``
    :param p: number of iterations in Hilbert curve
    :type p: ``int``
    :param N: number of dimensions
    :type N: ``int``
    """
    h_bit_str = _binary_repr(h, p*N)
    x = [int(h_bit_str[i::N], 2) for i in range(N)]
    return x

def _transpose_to_hilbert_integer(x, p, N):
    """Restore a hilbert integer (`h`) from its transpose (`x`).

    :param x: the transpose of a hilbert integer (N components of length p)
    :type x: ``list`` of ``int``
    :param p: number of iterations in hilbert curve
    :type p: ``int``
    :param N: number of dimensions
    :type N: ``int``
    """
    x_bit_str = [_binary_repr(x[i], p) for i in range(N)]
    h = int(''.join([y[i] for i in range(p) for y in x_bit_str]), 2)
    return h

def coordinates_from_distance(h, p, N):
    """Return the coordinates for a given hilbert distance.

    :param h: integer distance along the curve
    :type h: ``int``
    :param p: side length of hypercube is 2^p
    :type p: ``int``
    :param N: number of dimensions
    :type N: ``int``
    """
    x = _hilbert_integer_to_transpose(h, p, N)
    Z = 2 << (p-1)

    # Gray decode by H ^ (H/2)
    t = x[N-1] >> 1
    for i in range(N-1, 0, -1):
        x[i] ^= x[i-1]
    x[0] ^= t

    # Undo excess work
    Q = 2
    while Q != Z:
        P = Q - 1
        for i in range(N-1, -1, -1):
            if x[i] & Q:
                # invert
                x[0] ^= P
            else:
                # excchange
                t = (x[0] ^ x[i]) & P
                x[0] ^= t
                x[i] ^= t
        Q <<= 1

    # done
    return x

def distance_from_coordinates(x, p, N):
    """Return the hilbert distance for a given set of coordinates.

    :param x: coordinates len(x) = N
    :type x: ``list`` of ``int``
    :param p: side length of hypercube is 2^p
    :type p: ``int``
    :param N: number of dimensions
    :type N: ``int``
    """
    M = 1 << (p - 1)

    # Inverse undo excess work
    Q = M
    while Q > 1:
        P = Q - 1
        for i in range(N):
            if x[i] & Q:
                x[0] ^= P
            else:
                t = (x[0] ^ x[i]) & P
                x[0] ^= t
                x[i] ^= t
        Q >>= 1

    # Gray encode
    for i in range(1, N):
        x[i] ^= x[i-1]
    t = 0
    Q = M
    while Q > 1:
        if x[N-1] & Q:
            t ^= Q - 1
        Q >>= 1
    for i in range(N):
        x[i] ^= t

    h = _transpose_to_hilbert_integer(x, p, N)
    return h
