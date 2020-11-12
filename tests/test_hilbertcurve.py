"""Test the functions in hilbert.py"""

import pytest
import unittest
from hilbertcurve.hilbertcurve import HilbertCurve

class TestHilbertIntegerToTranspose(unittest.TestCase):
    """Test hilbert_integer_to_transpose."""

    def test_10590(self):
        """Assert that a 15 bit hilber integer is correctly transposed into
        a 3-d vector ...

                      ABCDEFGHIJKLMNO
             10590 (0b010100101011110)

                      ADGJM
             X[0] = 0b01101 = 13

                      BEHKN
             X[1] = 0b10011 = 19

                      CFILO
             X[2] = 0b00110 = 6
        """
        p = 5
        n = 3
        hilbert_curve = HilbertCurve(p, n)
        h = 10590
        expected_x = [13, 19, 6]
        actual_x = hilbert_curve._hilbert_integer_to_transpose(h)
        self.assertEqual(actual_x, expected_x)

class TestTransposeToHilbertInteger(unittest.TestCase):
    """Test _transpose_to_hilbert_integer."""

    def test_13_19_6(self):
        """Assert that a 15 bit hilber integer is correctly recovered from its
        transposed 3-d vector ...

                      ABCDEFGHIJKLMNO
             10590 (0b010100101011110)

                      ADGJM
             X[0] = 0b01101 = 13

                      BEHKN
             X[1] = 0b10011 = 19

                      CFILO
             X[2] = 0b00110 = 6
        """
        p = 5
        n = 3
        hilbert_curve = HilbertCurve(p, n)
        x = [13, 19, 6]
        expected_h = 10590
        actual_h = hilbert_curve._transpose_to_hilbert_integer(x)
        self.assertEqual(actual_h, expected_h)

class TestReversibility(unittest.TestCase):
    """Test that transpose2axes and axes2transpose are consistent."""

    def test_reversibility(self):
        """Assert points_from_distances and distances_from_points
        are inverse operations."""
        n = 3
        p = 5
        hilbert_curve = HilbertCurve(p, n)
        n_h = 2**(n * p)
        distances = list(range(n_h))
        coordinates = hilbert_curve.points_from_distances(distances)
        distances_check = hilbert_curve.distances_from_points(coordinates)
        for dist, dist_check in zip(distances, distances_check):
            self.assertEqual(dist, dist_check)

class TestInitIntConversion(unittest.TestCase):
    """Test __init__ conversion of floating point to integers."""

    def test_pt_oh(self):
        """Assert x.0 goes to x"""
        n = 3.0
        n_int = 3
        p = 5
        hilbert_curve = HilbertCurve(p, n)
        self.assertTrue(isinstance(hilbert_curve.n, int))
        self.assertEqual(hilbert_curve.n, n_int)

        n = 3
        p_int = 5
        p = 5.0
        hilbert_curve = HilbertCurve(p, n)
        self.assertTrue(isinstance(hilbert_curve.p, int))
        self.assertEqual(hilbert_curve.p, p_int)

    def test_pt_one(self):
        """Assert x.1 raises an error"""
        n = 3
        p = 5.1
        with pytest.raises(TypeError):
            hilbert_curve = HilbertCurve(p, n)

        n = 3.1
        p = 5
        with pytest.raises(TypeError):
            hilbert_curve = HilbertCurve(p, n)

class TestInitBounds(unittest.TestCase):
    """Test __init__ bounds on n and p."""

    def test_pt_one(self):
        """Assert x=0 raises an error"""
        n = 0
        p = 5
        with pytest.raises(ValueError):
            hilbert_curve = HilbertCurve(p, n)

        n = 3
        p = 0
        with pytest.raises(ValueError):
            hilbert_curve = HilbertCurve(p, n)

class TestInitUnmodified(unittest.TestCase):
    """Test distances_from_points does not modify input."""

    def test_base(self):
        """Assert list is unmodified"""
        n = 2
        p = 3
        hilbert_curve = HilbertCurve(p, n)
        x = [[1, 1]]
        x_in = list(x)
        h = hilbert_curve.distances_from_points(x_in)
        self.assertEqual(x, x_in)


if __name__ == '__main__':
    unittest.main()
