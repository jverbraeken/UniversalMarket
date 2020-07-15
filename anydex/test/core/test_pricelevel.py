import unittest

from anydex.core.product_amount import ProductAmount
from anydex.core.assetpair import AssetPair
from anydex.core.message import TraderId
from anydex.core.order import OrderId, OrderNumber
from anydex.core.price import Price
from anydex.core.pricelevel import PriceLevel
from anydex.core.tick import Tick
from anydex.core.tickentry import TickEntry
from anydex.core.timeout import Timeout
from anydex.core.timestamp import Timestamp
from anydex.test import util


class PriceLevelTestSuite(unittest.TestCase):
    """PriceLevel test cases."""

    def setUp(self):
        # Object creation
        tick = Tick(OrderId(TraderId(b'0' * 20), OrderNumber(1)), AssetPair(ProductAmount(60, util.urn_btc),
                                                                            ProductAmount(30, util.urn_mb)),
                    Timeout(100), Timestamp.now(), True)
        tick2 = Tick(OrderId(TraderId(b'0' * 20), OrderNumber(2)), AssetPair(ProductAmount(30, util.urn_btc),
                                                                             ProductAmount(30, util.urn_mb)),
                     Timeout(100), Timestamp.now(), True)

        self.price_level = PriceLevel(Price(50, 5, util.urn_mb, util.urn_btc))
        self.tick_entry1 = TickEntry(tick, self.price_level)
        self.tick_entry2 = TickEntry(tick, self.price_level)
        self.tick_entry3 = TickEntry(tick, self.price_level)
        self.tick_entry4 = TickEntry(tick, self.price_level)
        self.tick_entry5 = TickEntry(tick2, self.price_level)

    def test_appending_length(self):
        # Test for tick appending and length
        self.assertEqual(0, self.price_level.length)
        self.assertEqual(0, len(self.price_level))

        self.price_level.append_tick(self.tick_entry1)
        self.price_level.append_tick(self.tick_entry2)
        self.price_level.append_tick(self.tick_entry3)
        self.price_level.append_tick(self.tick_entry4)

        self.assertEqual(4, self.price_level.length)
        self.assertEqual(4, len(self.price_level))

    def test_tick_removal(self):
        # Test for tick removal
        self.price_level.append_tick(self.tick_entry1)
        self.price_level.append_tick(self.tick_entry2)
        self.price_level.append_tick(self.tick_entry3)
        self.price_level.append_tick(self.tick_entry4)

        self.price_level.remove_tick(self.tick_entry2)
        self.price_level.remove_tick(self.tick_entry1)
        self.price_level.remove_tick(self.tick_entry4)
        self.price_level.remove_tick(self.tick_entry3)
        self.assertEqual(0, self.price_level.length)

    def test_str(self):
        # Test for price level string representation
        self.price_level.append_tick(self.tick_entry1)
        self.price_level.append_tick(self.tick_entry2)
        self.assertEqual('60 %s\t@\t0.5 %s\n'
                          '60 %s\t@\t0.5 %s\n' % (str(util.urn_btc), str(util.urn_mb), str(util.urn_btc), str(util.urn_mb)), str(self.price_level))
