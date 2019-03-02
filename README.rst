============
Introduction
============

This is a package to convert between one dimensional distance along a
`Hilbert curve`_, :math:`h`, and :math:`N`-dimensional coordinates,
:math:`(x_0, x_1, ... x_N-1)`.  There are two important parameters,

      * :math:`N` -- the number of dimensions (must be > 0)
      * :math:`p` -- the number of iterations used in constructing the Hilbert curve (must be > 0)

We consider an :math:`N`-dimensional `hypercube`_ of side length :math:`2^p`.
This hypercube contains :math:`2^{N p}` unit hypercubes (:math:`2^p` along
each dimension).  The number of unit hypercubes determine the possible
discrete distances along the Hilbert curve (indexed from 0 to
:math:`2^{N p} - 1`).


==========
Quickstart
==========

You can calculate coordinates given distances along a hilbert curve,

.. code-block:: python

  >>> from hilbertcurve.hilbertcurve import HilbertCurve
  >>> p=1; N=2
  >>> hilbert_curve = HilbertCurve(p, N)
  >>> for ii in range(4):
  >>>     coords = hilbert_curve.coordinates_from_distance(ii)
  >>>     print(f'coords(h={ii}) = {coords}')

  coords(h=0) = [0, 0]
  coords(h=1) = [0, 1]
  coords(h=2) = [1, 1]
  coords(h=3) = [1, 0]

You can also calculate distances along a hilbert curve given coordinates,

.. code-block:: python

  >>> for coords in [[0,0], [0,1], [1,1], [1,0]]:
  >>>     dist = hilbert_curve.distance_from_coordinates(coords)
  >>>     print(f'distance(x={coords}) = {dist}')

  distance(x=[0, 0]) = 0
  distance(x=[0, 1]) = 1
  distance(x=[1, 1]) = 2
  distance(x=[1, 0]) = 3


=========================
(Absurdly) Large Integers
=========================

Due to the magic of `arbitrarily large integers in Python`_,
these calculations can be done with ... well ... arbitrarily large integers!

.. code-block:: python

  >>> p = 512; N = 10
  >>> hilbert_curve = HilbertCurve(p, N)
  >>> ii = 123456789101112131415161718192021222324252627282930
  >>> coords = hilbert_curve.coordinates_from_distance(ii)
  >>> print(f'coords = {coords}')

  coords = [121075, 67332, 67326, 108879, 26637, 43346, 23848, 1551, 68130, 84004]

The calculations above represent the 512th iteration of the Hilbert curve in 10 dimensions.
The maximum value along any coordinate axis is an integer with 155 digits and the maximum
distance along the curve is an integer with 1542 digits.  For comparison,
`an estimate of the number of atoms in the observable universe`_
is :math:`10^{82}` (i.e. an integer with 83 digits).

=======
Visuals
=======


.. figure:: nD=2_p=3.png

   The figure above shows the first three iterations of the Hilbert
   curve in two (:math:`N=2`) dimensions.  The :math:`p=1` iteration is shown
   in red, :math:`p=2` in blue, and :math:`p=3` in black.
   For the :math:`p=3` iteration, distances, :math:`h`, along the curve are
   labeled from 0 to 63 (i.e. from 0 to :math:`2^{N p}-1`).  This package
   provides methods to translate between :math:`N`-dimensional coordinates and one
   dimensional distance.  For example, between (:math:`x_0=4, x_1=6`) and
   :math:`h=36`.  Note that the :math:`p=1` and :math:`p=2` iterations have been
   scaled and translated to the coordinate system of the :math:`p=3` iteration.


An animation of the same case in 3-D is available on YouTube.  To watch the video,
click the link below.  Once the YouTube video loads, you can right click on it and
turn "Loop" on to watch the curve rotate continuously.

.. figure:: https://img.youtube.com/vi/TfJEJidwkBQ/0.jpg

   3-D Hilbert Curve Animation https://www.youtube.com/watch?v=TfJEJidwkBQ

=========
Reference
=========

This module is based on the C code provided in the 2004 article
"Programming the Hilbert Curve" by John Skilling,

  * http://adsabs.harvard.edu/abs/2004AIPC..707..381S

I was also helped by the discussion in the following stackoverflow post,

  * `mapping-n-dimensional-value-to-a-point-on-hilbert-curve`_

which points out a typo in the source code of the paper.  The Skilling code
provides two functions ``TransposetoAxes`` and ``AxestoTranspose``.  In this
case, Transpose refers to a specific packing of the integer that represents
distance along the Hilbert curve (see below for details) and
Axes refer to the N-dimensional coordinates.  Below is an excerpt from the
documentation of Skilling's code,

::

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
.. _arbitrarily large integers in Python: https://docs.python.org/3.3/library/stdtypes.html#numeric-types-int-float-complex
.. _an estimate of the number of atoms in the observable universe: https://www.universetoday.com/36302/atoms-in-the-universe
.. _mapping-n-dimensional-value-to-a-point-on-hilbert-curve: http://stackoverflow.com/questions/499166/mapping-n-dimensional-value-to-a-point-on-hilbert-curve
