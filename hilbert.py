"""
This is a module to convert between one dimensional distance along a
`Hilbert curve`_ and N-dimensional coordinates.  The two important parameters
are ``N`` (the number of dimensions, must be > 0) and ``p`` (the number of
iterations used in constructing the Hilbert curve, must be > 0).

We consider an ``N``-dimensional `hypercube`_ of side length 2**``p``.  This
hypercube contains 2**(N * p) unit hypercubes (2**p along each dimension).
The number of unit hypercubes determine the possible discrete distances along
the Hilber curve (indexed from 0 to 2**(N * p) - 1).  The image below
illustrates the situation for N=2 and p=3.

.. figure:: nD=2_p=3.png

   This is the third iteration (p=3) of the Hilbert curve in two (N=2)
   dimensions.  Distances, d, along the curve are labeled from 0 to 63 (i.e.
   from 0 to 2**(N*p)).  The provided functions translate between the
   two dimensional coordinates and the one dimensional distance.  For example
   between (x_0=4, x_1=6) and d=36.


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


def _bit_at(integer, offset):
    """Returns a string representation of the bit `offset` places from the least
    significant bit in `integer`.

    :param integer: integer to inspect the bits of
    :type integer: ``int``
    :param offset: offset from the least significant bit
    :type offset: ``int``
    """
    mask = 1 << offset
    bitwise_and = integer & (1<<offset)
    if bitwise_and > 0:
        return '1'
    else:
        return '0'

def _return_transpose(integer, pH, nD):
    """Construct the variable ``X`` refered to in the module level docs.

    :param integer: integer to pack into `nD` pieces.
    :type integer: ``int``
    :param pH: number of iterations in Hilbert curve
    :type pH: ``int``
    :param nD: number of dimensions
    :type nD: ``int``
    """
    x = [0] * nD
    for ix in range(nD):
        first_offset = nD - 1 - ix
        offsets = range(first_offset, nD*pH, nD)
        bit_str = ''.join([_bit_at(integer, offset) for offset in offsets])
        bit_str = bit_str[::-1]
        x[ix] = int('0b' + bit_str, 2)
    return x

def transpose2axes(iH, pH, nD):
    """
    :param ih: integer length along the hilbert curve, 0 -> 2^(p*n)-1
    :type ih: ``int``
    :param pH: side length of hypercube is 2^p
    :type pH: ``int``
    :param nD: number of dimensions
    :type nD: ``int``
    """
    x = _return_transpose(iH, pH, nD)
    N = 2 << (pH-1)

    # Gray decode by H ^ (H/2)
    t = x[nD-1] >> 1
    for i in range(nD-1, 0, -1):
        x[i] ^= x[i-1]
    x[0] ^= t

    # Undo excess work
    Q = 2
    while Q != N:
        P = Q - 1
        for i in range(nD-1, -1, -1):
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
