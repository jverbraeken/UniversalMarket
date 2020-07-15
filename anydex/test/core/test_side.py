import unittest

from anydex.core.product_amount import ProductAmount
from anydex.core.assetpair import AssetPair
from anydex.core.message import TraderId
from anydex.core.order import OrderId, OrderNumber
from anydex.core.price import Price
from anydex.core.side import Side
from anydex.core.tick import Tick
from anydex.core.timeout import Timeout
from anydex.core.timestamp import Timestamp
from anydex.test import util


class SideTestSuite(unittest.TestCase):
    """Side test cases."""

    def setUp(self):
        # Object creation

        self.tick = Tick(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                         AssetPair(ProductAmount(60, util.urn_btc), ProductAmount(30, util.urn_mb)),
                         Timeout(100), Timestamp.now(), True)
        self.tick2 = Tick(OrderId(TraderId(b'1' * 20), OrderNumber(2)),
                          AssetPair(ProductAmount(120, util.urn_btc), ProductAmount(30, util.urn_mb)),
                          Timeout(100), Timestamp.now(), True)
        self.side = Side()

    def test_max_price(self):
        # Test max price (list)
        self.assertEqual(None, self.side.get_max_price(util.urn_mb, util.urn_btc))
        self.assertEqual(None, self.side.get_max_price_list(util.urn_mb, util.urn_btc))

        self.side.insert_tick(self.tick)
        self.side.insert_tick(self.tick2)

        self.assertEqual(Price(1, 2, util.urn_mb, util.urn_btc), self.side.get_max_price(util.urn_mb, util.urn_btc))

    def test_min_price(self):
        # Test min price (list)
        self.assertEqual(None, self.side.get_min_price_list(util.urn_mb, util.urn_btc))
        self.assertEqual(None, self.side.get_min_price(util.urn_mb, util.urn_btc))

        self.side.insert_tick(self.tick)
        self.side.insert_tick(self.tick2)

        self.assertEqual(Price(1, 4, util.urn_mb, util.urn_btc), self.side.get_min_price(util.urn_mb, util.urn_btc))

    def test_insert_tick(self):
        # Test insert tick
        self.assertEqual(0, len(self.side))
        self.assertFalse(self.side.tick_exists(OrderId(TraderId(b'0' * 20), OrderNumber(1))))

        self.side.insert_tick(self.tick)
        self.side.insert_tick(self.tick2)

        self.assertEqual(2, len(self.side))
        self.assertTrue(self.side.tick_exists(OrderId(TraderId(b'0' * 20), OrderNumber(1))))

    def test_remove_tick(self):
        # Test remove tick
        self.side.insert_tick(self.tick)
        self.side.insert_tick(self.tick2)

        self.side.remove_tick(OrderId(TraderId(b'0' * 20), OrderNumber(1)))
        self.assertEqual(1, len(self.side))
        self.side.remove_tick(OrderId(TraderId(b'1' * 20), OrderNumber(2)))
        self.assertEqual(0, len(self.side))

    def test_get_price_level_list_wallets(self):
        """
        Test the price level lists of wallets of a side
        """
        self.assertFalse(self.side.get_price_level_list_wallets())
        self.side.insert_tick(self.tick)
        self.assertTrue(self.side.get_price_level_list_wallets())

    def test_get_list_representation(self):
        """
        Testing the list representation of a side
        """
        self.assertFalse(self.side.get_list_representation())
        self.side.insert_tick(self.tick)

        list_rep = self.side.get_list_representation()
        self.assertTrue(list_rep)
