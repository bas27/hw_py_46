import unittest
from for_test import calc_exp, calc_sum, calc_mult


class MyFirstTest(unittest.TestCase):

    def test_calc_sum(self):
        self.assertEqual(calc_sum(4, 2), 6)

    def test_calc_exp(self):
        self.assertEqual(calc_exp(2, 3), 8)

    def test_calc_mult(self):
        self.assertEqual(calc_mult(8, 2), 16)


if __name__ == '__main__':
    unittest.main()
