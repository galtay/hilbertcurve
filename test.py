#!/usr/bin/env python
"""Test the functions in hilbert.py"""

import unittest
import hilbert

class TestHilbertIntegerToTranspose(unittest.TestCase):
    """Test hilbert_integer_to_transpose."""

    def test_10590(self):
        """Assert that a 15 bit hilber integer is correctly transposed into
        a 3-d vector properly ...

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
        N = 3
        h = 10590
        expected_x = [13, 19, 6]
        actual_x = hilbert._hilbert_integer_to_transpose(h, p, N)
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
        N = 3
        x = [13, 19, 6]
        expected_h = 10590
        actual_h = hilbert._transpose_to_hilbert_integer(x, p, N)
        self.assertEqual(actual_h, expected_h)

class TestReversibility(unittest.TestCase):
    """Test that transpose2axes and axes2transpose are consistent."""

    def test_reversibility(self):
        """Assert coordinates_from_distance and distance_from_coordinates
        are inverse operations."""
        N = 3
        p = 5
        n_h = 2**(N * p)
        for h in range(n_h):
            x = hilbert.coordinates_from_distance(h, p, N)
            h_test = hilbert.distance_from_coordinates(x, p, N)
            self.assertEqual(h, h_test)


if __name__ == '__main__':
    unittest.main()
