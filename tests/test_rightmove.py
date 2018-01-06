import unittest
from rightmove import extract_price


class TestRightmove(unittest.TestCase):

    def test_extract_price(self):
        test_data = ' price 799.00 pcm'
        result = extract_price(test_data)
        self.assertEquals(799, result)

        test_data = '799 pcm'
        result = extract_price(test_data)
        self.assertEquals(799, result)

        test_data = '1,799.00 pcm'
        result = extract_price(test_data)
        self.assertEquals(1799, result)

        test_data = '1,799 pcm'
        result = extract_price(test_data)
        self.assertEquals(1799, result)

        test_data = 'no price'
        result = extract_price(test_data)
        self.assertEqual(0, result)
