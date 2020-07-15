import unittest

from anydex.core.product_amount import ProductAmount
from anydex.test import util


class TestProductAmount(unittest.TestCase):
    """
    Test the product amount class
    """

    def setUp(self):
        # Object creation
        self.product_amount1 = ProductAmount(2, util.urn_btc)
        self.product_amount2 = ProductAmount(100, util.urn_btc)
        self.product_amount3 = ProductAmount(0, util.urn_mb)
        self.product_amount4 = ProductAmount(2, util.urn_mb)

    def test_init(self):
        """
        Test the initialization of a price
        """
        with self.assertRaises(ValueError):
            ProductAmount('1', util.urn_btc)
        with self.assertRaises(ValueError):
            ProductAmount(1, '2')

    def test_addition(self):
        # Test for addition
        self.assertEqual(ProductAmount(102, util.urn_btc), self.product_amount1 + self.product_amount2)
        self.assertFalse(self.product_amount1 is (self.product_amount1 + self.product_amount2))
        self.assertEqual(NotImplemented, self.product_amount1.__add__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__add__(self.product_amount4))

    def test_subtraction(self):
        # Test for subtraction
        self.assertEqual(ProductAmount(98, util.urn_btc), self.product_amount2 - self.product_amount1)
        self.assertEqual(NotImplemented, self.product_amount1.__sub__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__sub__(self.product_amount4))

    def test_comparison(self):
        # Test for comparison
        self.assertTrue(self.product_amount1 < self.product_amount2)
        self.assertTrue(self.product_amount2 > self.product_amount1)
        self.assertEqual(NotImplemented, self.product_amount1.__le__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__lt__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__ge__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__gt__(10))
        self.assertEqual(NotImplemented, self.product_amount1.__le__(self.product_amount4))
        self.assertEqual(NotImplemented, self.product_amount1.__lt__(self.product_amount4))
        self.assertEqual(NotImplemented, self.product_amount1.__ge__(self.product_amount4))
        self.assertEqual(NotImplemented, self.product_amount1.__gt__(self.product_amount4))

    def test_equality(self):
        # Test for equality
        self.assertTrue(self.product_amount1 == ProductAmount(2, util.urn_btc))
        self.assertTrue(self.product_amount1 != self.product_amount2)
        self.assertFalse(self.product_amount1 == 2)
        self.assertFalse(self.product_amount1 == self.product_amount4)

    def test_hash(self):
        # Test for hashes
        self.assertEqual(self.product_amount1.__hash__(), ProductAmount(2, util.urn_btc).__hash__())
        self.assertNotEqual(self.product_amount1.__hash__(), self.product_amount2.__hash__())

    def test_str(self):
        """
        Test the string representation of a ProductAmount object
        """
        self.assertEqual(str(self.product_amount1), "2 %s" % str(util.urn_btc))
