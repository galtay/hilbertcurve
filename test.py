#!/usr/bin/env python
"""Test the functions in hilbert.py"""

import unittest
import hilbert

class TestBitAt(unittest.TestCase):
    """Test the function _at_bit."""

    def test_143(self):
        """Assert the bits of 143 (from least to most significant) are
        11110001 followed by zeros."""
        self.assertEqual(hilbert._bit_at(143,0), '1')
        self.assertEqual(hilbert._bit_at(143,1), '1')
        self.assertEqual(hilbert._bit_at(143,2), '1')
        self.assertEqual(hilbert._bit_at(143,3), '1')
        self.assertEqual(hilbert._bit_at(143,4), '0')
        self.assertEqual(hilbert._bit_at(143,5), '0')
        self.assertEqual(hilbert._bit_at(143,6), '0')
        self.assertEqual(hilbert._bit_at(143,7), '1')
        for i in range(8, 40):
            self.assertEqual(hilbert._bit_at(13,i), '0')

class TestPackIhIntoX(unittest.TestCase):
    """Test function _pack_iH_into_x."""

    def test_10590(self):
        """Assert that a 15 bit integer is packed into a 3-d vector properly
             10590 (0b010100101011110)
                      ABCDEFGHIJKLMNO

             X[0] = 0b01101 = 13
             X[1] = 0b10011 = 19
             X[2] = 0b00110 = 6
        """
        pH = 5
        nD = 3
        iH = 10590
        expected_x = [13, 19, 6]
        actual_x = hilbert._pack_iH_into_x(iH, pH, nD)
        self.assertEqual(actual_x, expected_x)

class TestExtractIhFromX(unittest.TestCase):
    """Test function _extract_iH_from_x."""

    def test_13_19_6(self):
        """Assert that a 15 bit integer is extracted from a 3-d vector properly
             10590 (0b010100101011110)
                      ABCDEFGHIJKLMNO

             X[0] = 0b01101 = 13
             X[1] = 0b10011 = 19
             X[2] = 0b00110 = 6
        """
        pH = 5
        nD = 3
        x = [13, 19, 6]
        expected_iH = 10590
        actual_iH = hilbert._extract_iH_from_x(x, pH, nD)
        self.assertEqual(actual_iH, expected_iH)

class TestReversibility(unittest.TestCase):
    """Test that transpose2axes and axes2transpose are consistent."""

    def test_reversibility(self):
        """Assert that a 15 bit integer is extracted from a 3-d vector properly
             10590 (0b010100101011110)
                      ABCDEFGHIJKLMNO

             X[0] = 0b01101 = 13
             X[1] = 0b10011 = 19
             X[2] = 0b00110 = 6
        """
        nD = 3
        pH = 5
        n_iH = 2**(nD * pH)
        for iH in range(n_iH):
            x = hilbert.transpose2axes(iH, pH, nD)
            iH_test = hilbert.axes2transpose(x, pH, nD)
            self.assertEqual(iH, iH_test)


if __name__ == '__main__':
    unittest.main()
