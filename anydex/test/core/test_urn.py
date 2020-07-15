import unittest

from anydex.core.product_amount import ProductAmount
from anydex.core.urn import URN


class TestURN(unittest.TestCase):
    """
    Test the asset amount class
    """

    def setUp(self):
        pass

    def test_init(self):
        """
        Test the initialization of a price
        """
        with self.assertRaises(ValueError):
            URN(1)
        with self.assertRaises(ValueError):
            URN('urn:feeds.archive.org:validator:1')

    def test_equality(self):
        # Test for equality
        self.assertTrue(URN("urn:feeds-archive-org:validator:1") == URN("urn:feeds-archive-org:validator:1"))

    def test_hash(self):
        # Test for hashes
        self.assertEqual(URN("urn:feeds-archive-org:validator:1").__hash__(), URN("urn:feeds-archive-org:validator:1").__hash__())

    def test_str(self):
        """
        Test the string representation of a URN object
        """
        self.assertEqual(str(URN("urn:feeds-archive-org:validator:1")), "urn:feeds-archive-org:validator:1")

    def test_generate_test(self):
        self.assertIsNotNone(URN.generate_test())
