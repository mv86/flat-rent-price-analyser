"""Test module for scrapers.rightmove module"""
import unittest
from scrapers.rightmove import extract_price


class TestRightmove(unittest.TestCase):
    """Test class for the rightmove module"""
    def test_extract_price(self):
        """Test regular expression used in extract price function"""
        test_data = ' price 799.00 pcm'
        result = extract_price(test_data)
        self.assertEqual(799, result)

        test_data = '799 pcm'
        result = extract_price(test_data)
        self.assertEqual(799, result)

        test_data = '1,799.00 pcm'
        result = extract_price(test_data)
        self.assertEqual(1799, result)

        test_data = '1,799 pcm'
        result = extract_price(test_data)
        self.assertEqual(1799, result)

        test_data = 'no price'
        result = extract_price(test_data)
        self.assertEqual(0, result)
