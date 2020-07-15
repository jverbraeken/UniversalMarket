import unittest

from anydex.core.product_amount import ProductAmount
from anydex.core.assetpair import AssetPair
from anydex.test import util


class TestAssetPair(unittest.TestCase):
    """
    Test the asset pair class
    """

    def setUp(self):
        # Object creation
        self.assetpair1 = AssetPair(ProductAmount(2, util.urn_btc), ProductAmount(2, util.urn_mb))
        self.assetpair2 = AssetPair(ProductAmount(4, util.urn_btc), ProductAmount(8, util.urn_mb))
        self.assetpair3 = AssetPair(ProductAmount(2, util.urn_btc), ProductAmount(2, util.urn_mb))
        self.assetpair4 = AssetPair(ProductAmount(10, util.urn_dum1), ProductAmount(13, util.urn_dum2))

    def test_init(self):
        """
        Test initializing an AssetPair object
        """
        pass

    def test_equality(self):
        """
        Test the equality method of an AssetPair
        """
        self.assertFalse(self.assetpair1 == self.assetpair2)
        self.assertTrue(self.assetpair1 == self.assetpair3)

    def test_to_dictionary(self):
        """
        Test the method to convert an AssetPair object to a dictionary
        """
        self.assertDictEqual({
            "first": {
                "amount": 2,
                "type": str(util.urn_btc),
            },
            "second": {
                "amount": 2,
                "type": str(util.urn_mb)
            }
        }, self.assetpair1.to_dictionary())

    def test_from_dictionary(self):
        """
        Test the method to create an AssetPair object from a given dictionary
        """
        self.assertEqual(AssetPair.from_dictionary({
            "first": {
                "amount": 2,
                "type": str(util.urn_btc),
            },
            "second": {
                "amount": 2,
                "type": str(util.urn_mb)
            }
        }), self.assetpair1)

    def test_price(self):
        """
        Test creating a price from an asset pair
        """
        self.assertEqual(self.assetpair1.price.amount, 1)
        self.assertEqual(self.assetpair2.price.amount, 2)

    def test_proportional_downscale(self):
        """
        Test the method to proportionally scale down an asset pair
        """
        self.assertEqual(self.assetpair2.proportional_downscale(first=1).second.amount, 2)
        self.assertEqual(self.assetpair2.proportional_downscale(second=4).first.amount, 2)
        self.assertEqual(self.assetpair4.proportional_downscale(first=10).second.amount, 13)
        self.assertEqual(self.assetpair4.proportional_downscale(second=13).first.amount, 10)

    def test_to_str(self):
        """
        Test string conversion from an asset pair
        """
        self.assertEqual("2 %s 2 %s" % (str(util.urn_btc), str(util.urn_mb)), str(self.assetpair1))
