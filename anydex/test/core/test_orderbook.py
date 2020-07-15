from anydex.core.product_amount import ProductAmount
from anydex.core.assetpair import AssetPair
from anydex.core.message import TraderId
from anydex.core.order import OrderId, OrderNumber
from anydex.core.orderbook import OrderBook
from anydex.core.price import Price
from anydex.core.tick import Ask, Bid
from anydex.core.timeout import Timeout
from anydex.core.timestamp import Timestamp
from anydex.core.trade import Trade
from anydex.test import util
from anydex.test.base import AbstractServer


class AbstractTestOrderBook(AbstractServer):
    """
    Base class for the order book tests.
    """

    async def setUp(self):
        super(AbstractTestOrderBook, self).setUp()
        # Object creation
        self.ask = Ask(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                       AssetPair(ProductAmount(100, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(100), Timestamp.now())
        self.invalid_ask = Ask(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                               AssetPair(ProductAmount(100, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(0), Timestamp(0))
        self.ask2 = Ask(OrderId(TraderId(b'1' * 20), OrderNumber(1)),
                        AssetPair(ProductAmount(400, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(100), Timestamp.now())
        self.bid = Bid(OrderId(TraderId(b'2' * 20), OrderNumber(1)),
                       AssetPair(ProductAmount(200, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(100), Timestamp.now())
        self.invalid_bid = Bid(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                               AssetPair(ProductAmount(100, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(0), Timestamp(0))
        self.bid2 = Bid(OrderId(TraderId(b'3' * 20), OrderNumber(1)),
                        AssetPair(ProductAmount(300, util.urn_btc), ProductAmount(30, util.urn_mb)), Timeout(100), Timestamp.now())
        self.trade = Trade.propose(TraderId(b'0' * 20),
                                   OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                                   OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                                   AssetPair(ProductAmount(100, util.urn_btc), ProductAmount(30, util.urn_mb)),
                                   Timestamp(1462224447117))
        self.order_book = OrderBook()

    async def tearDown(self):
        await self.order_book.shutdown_task_manager()
        await super(AbstractTestOrderBook, self).tearDown()


class TestOrderBook(AbstractTestOrderBook):
    """OrderBook test cases."""

    def test_timeouts(self):
        """
        Test the timeout functions of asks/bids
        """
        self.order_book.insert_ask(self.ask)
        self.assertEqual(self.order_book.timeout_ask(self.ask.order_id), self.ask)

        self.order_book.insert_bid(self.bid)
        self.assertEqual(self.order_book.timeout_bid(self.bid.order_id), self.bid)

        self.order_book.on_invalid_tick_insert()

    async def test_ask_insertion(self):
        # Test for ask insertion
        self.order_book.insert_ask(self.ask2)
        self.assertTrue(self.order_book.tick_exists(self.ask2.order_id))
        self.assertTrue(self.order_book.ask_exists(self.ask2.order_id))
        self.assertFalse(self.order_book.bid_exists(self.ask2.order_id))
        self.assertEqual(self.ask2, self.order_book.get_ask(self.ask2.order_id).tick)

    def test_get_tick(self):
        """
        Test the retrieval of a tick from the order book
        """
        self.order_book.insert_ask(self.ask)
        self.order_book.insert_bid(self.bid)
        self.assertTrue(self.order_book.get_tick(self.ask.order_id))
        self.assertTrue(self.order_book.get_tick(self.bid.order_id))

    def test_ask_removal(self):
        # Test for ask removal
        self.order_book.insert_ask(self.ask2)
        self.assertTrue(self.order_book.tick_exists(self.ask2.order_id))
        self.order_book.remove_ask(self.ask2.order_id)
        self.assertFalse(self.order_book.tick_exists(self.ask2.order_id))

    def test_bid_insertion(self):
        # Test for bid insertion
        self.order_book.insert_bid(self.bid2)
        self.assertTrue(self.order_book.tick_exists(self.bid2.order_id))
        self.assertTrue(self.order_book.bid_exists(self.bid2.order_id))
        self.assertFalse(self.order_book.ask_exists(self.bid2.order_id))
        self.assertEqual(self.bid2, self.order_book.get_bid(self.bid2.order_id).tick)

    def test_bid_removal(self):
        # Test for bid removal
        self.order_book.insert_bid(self.bid2)
        self.assertTrue(self.order_book.tick_exists(self.bid2.order_id))
        self.order_book.remove_bid(self.bid2.order_id)
        self.assertFalse(self.order_book.tick_exists(self.bid2.order_id))

    def test_properties(self):
        # Test for properties
        self.order_book.insert_ask(self.ask2)
        self.order_book.insert_bid(self.bid2)
        self.assertEqual(Price(-25, 1000, util.urn_mb, util.urn_btc), self.order_book.get_bid_ask_spread(util.urn_mb, util.urn_btc))

    def test_ask_price_level(self):
        self.order_book.insert_ask(self.ask)
        price_level = self.order_book.get_ask_price_level(util.urn_mb, util.urn_btc)
        self.assertEqual(price_level.depth, 100)

    def test_bid_price_level(self):
        # Test for tick price
        self.order_book.insert_bid(self.bid2)
        price_level = self.order_book.get_bid_price_level(util.urn_mb, util.urn_btc)
        self.assertEqual(price_level.depth, 300)

    def test_ask_side_depth(self):
        # Test for ask side depth
        self.order_book.insert_ask(self.ask)
        self.order_book.insert_ask(self.ask2)
        self.assertEqual(100, self.order_book.ask_side_depth(Price(3, 10, util.urn_mb, util.urn_btc)))
        self.assertEqual([(Price(75, 1000, util.urn_mb, util.urn_btc), 400), (Price(3, 10, util.urn_mb, util.urn_btc), 100)],
                         self.order_book.get_ask_side_depth_profile(util.urn_mb, util.urn_btc))

    def test_bid_side_depth(self):
        # Test for bid side depth
        self.order_book.insert_bid(self.bid)
        self.order_book.insert_bid(self.bid2)
        self.assertEqual(300, self.order_book.bid_side_depth(Price(1, 10, util.urn_mb, util.urn_btc)))
        self.assertEqual([(Price(1, 10, util.urn_mb, util.urn_btc), 300), (Price(15, 100, util.urn_mb, util.urn_btc), 200)],
                         self.order_book.get_bid_side_depth_profile(util.urn_mb, util.urn_btc))

    def test_remove_tick(self):
        # Test for tick removal
        self.order_book.insert_ask(self.ask2)
        self.order_book.insert_bid(self.bid2)
        self.order_book.remove_tick(self.ask2.order_id)
        self.assertFalse(self.order_book.tick_exists(self.ask2.order_id))
        self.order_book.remove_tick(self.bid2.order_id)
        self.assertFalse(self.order_book.tick_exists(self.bid2.order_id))

    def test_get_order_ids(self):
        """
        Test the get order IDs function in order book
        """
        self.assertFalse(self.order_book.get_order_ids())
        self.order_book.insert_ask(self.ask)
        self.order_book.insert_bid(self.bid)
        self.assertEqual(len(self.order_book.get_order_ids()), 2)

    def test_update_ticks(self):
        """
        Test updating ticks in an order book
        """
        self.order_book.insert_ask(self.ask)
        self.order_book.insert_bid(self.bid)

        ask_dict = {
            "trader_id": self.ask.order_id.trader_id.as_hex(),
            "order_number": int(self.ask.order_id.order_number),
            "assets": self.ask.assets.to_dictionary(),
            "traded": 100,
            "timeout": 3600,
            "timestamp": int(Timestamp.now())
        }
        bid_dict = {
            "trader_id": self.bid.order_id.trader_id.as_hex(),
            "order_number": int(self.bid.order_id.order_number),
            "assets": self.bid.assets.to_dictionary(),
            "traded": 100,
            "timeout": 3600,
            "timestamp": int(Timestamp.now())
        }

        ask_dict["traded"] = 50
        bid_dict["traded"] = 50
        self.order_book.completed_orders = []
        self.order_book.update_ticks(ask_dict, bid_dict, 100)
        self.assertEqual(len(self.order_book.asks), 1)
        self.assertEqual(len(self.order_book.bids), 1)

    def test_str(self):
        # Test for order book string representation
        self.order_book.insert_ask(self.ask)
        self.order_book.insert_bid(self.bid)

        self.assertEqual('------ Bids -------\n'
                          '200 %s\t@\t0.15 %s\n\n'
                          '------ Asks -------\n'
                          '100 %s\t@\t0.3 %s\n\n' % (util.urn_btc, util.urn_mb, util.urn_btc, util.urn_mb), str(self.order_book))
