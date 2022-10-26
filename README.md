# Hilbert's Curve in C# and Python

============
Notes
============
This README file is made for the Python version.
All code is similar to the C# version however the folowing are different:
* ``dimention`` -- the number of dimensions (must be > 0) in C#
* ``iterator`` -- the number of iterations used in constructing the Hilbert curve (must be > 0) in C#
* Also, since this project was made before Python 3.11.0, no ``Iterable`` library and/or datatypes are not used in the script.
* They are here to help just to understand the code. In C#, ``Iterable`` are replaced with ``List`` as you have to select datatypes upfront.

============
Introduction
============
This is a package to convert between one dimensional distance along a
`Hilbert curve`_, ``h``, and ``n``-dimensional points,
``(x_0, x_1, ... x_n-1)``.  There are two important parameters,

* ``n`` -- the number of dimensions (must be > 0)
* ``p`` -- the number of iterations used in constructing the Hilbert curve (must be > 0)
*See notes for C# version

We consider an ``n``-dimensional `hypercube`_ of side length ``2^p``.
This hypercube contains ``2^{n p}`` unit hypercubes (``2^p`` along
each dimension).  The number of unit hypercubes determine the possible
discrete distances along the Hilbert curve (indexed from 0 to
``2^{n p} - 1``).


==========
Quickstart
==========

Install the package with pip (this partis irrelevent for C#, but the way to use the library is similar),

  pip install hilbertcurve

You can calculate points given distances along a hilbert curve,

.. code-block:: python

  >>> from hilbertcurve.hilbertcurve import HilbertCurve
  >>> p=1; n=2
  >>> hilbert_curve = HilbertCurve(p, n)
  >>> distances = list(range(4))
  >>> points = hilbert_curve.points_from_distances(distances)
  >>> for point, dist in zip(points, distances):
  >>>     print(f'point(h={dist}) = {point}')

  point(h=0) = [0, 0]
  point(h=1) = [0, 1]
  point(h=2) = [1, 1]
  point(h=3) = [1, 0]

You can also calculate distances along a hilbert curve given points,

.. code-block:: python

  >>> points = [[0,0], [0,1], [1,1], [1,0]]
  >>> distances = hilbert_curve.distances_from_points(points)
  >>> for point, dist in zip(points, distances):
  >>>     print(f'distance(x={point}) = {dist}')

  distance(x=[0, 0]) = 0
  distance(x=[0, 1]) = 1
  distance(x=[1, 1]) = 2
  distance(x=[1, 0]) = 3

=========================
Inputs and Outputs
=========================

The ``HilbertCurve`` class has four main public methods.
*
* ``point_from_distance(distance: int) -> Iterable[int]``
* ``points_from_distances(distances: Iterable[int], match_type: bool=False) -> Iterable[Iterable[int]]``
* ``distance_from_point(point: Iterable[int]) -> int``
* ``distances_from_points(points: Iterable[Iterable[int]], match_type: bool=False) -> Iterable[int]``

Arguments that are type hinted with ``Iterable[int]`` have been tested with lists, tuples, and 1-d numpy arrays.
Arguments that are type hinted with ``Iterable[Iterable[int]]`` have been tested with list of lists, tuples of tuples, and 2-d numpy arrays with shape (num_points, num_dimensions). The ``match_type`` key word argument forces the output iterable to match the type of the input iterable. 

The ``HilbertCurve`` class also contains some useful metadata derived from the inputs ``p`` and ``n``. For instance, you can construct a numpy array of random points on the hilbert curve and calculate their distances in the following way,

.. code-block:: python

  >>> from hilbertcurve.hilbertcurve import HilbertCurve
  >>> p=1; n=2
  >>> hilbert_curve = HilbertCurve(p, n)
  >>> num_points = 10_000                                                                                              
  >>> points = np.random.randint(                                                                                   
          low=0,                                                                                                    
          high=hilbert_curve.max_x + 1,                                                                                 
          size=(num_points, hilbert_curve.n)                                                                        
      )
  >>> distances = hilbert_curve.distances_from_points(points)
  >>> type(distances)
  
  list

  >>> distances = hilbert_curve.distances_from_points(points, match_type=True)
  >>> type(distances)


=======
Visuals
=======

.. figure:: n2_p3.png

   The figure above shows the first three iterations of the Hilbert
   curve in two (``n=2``) dimensions.  The ``p=1`` iteration is shown
   in red, ``p=2`` in blue, and ``p=3`` in black.
   For the ``p=3`` iteration, distances, ``h``, along the curve are
   labeled from 0 to 63 (i.e. from 0 to ``2^{n p}-1``).  This package
   provides methods to translate between ``n``-dimensional points and one
   dimensional distance.  For example, between (``x_0=4, x_1=6``) and
   ``h=36``.  Note that the ``p=1`` and ``p=2`` iterations have been
   scaled and translated to the coordinate system of the ``p=3`` iteration.
