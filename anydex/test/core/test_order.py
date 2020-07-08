import time
import unittest

from anydex.core.assetamount import AssetAmount
from anydex.core.assetpair import AssetPair
from anydex.core.message import TraderId
from anydex.core.order import Order, OrderId, OrderNumber, TickWasNotReserved
from anydex.core.tick import Tick
from anydex.core.timeout import Timeout
from anydex.core.timestamp import Timestamp
from anydex.core.trade import Trade
from anydex.core.transaction import Transaction, TransactionId


class OrderTestSuite(unittest.TestCase):
    """Order test cases."""

    def setUp(self):
        # Object creation
        self.transaction_id = TransactionId(b'a' * 32)
        self.transaction = Transaction(self.transaction_id, AssetPair(AssetAmount(100, 'BTC'), AssetAmount(30, 'MC')),
                                       OrderId(TraderId(b'0' * 20), OrderNumber(2)),
                                       OrderId(TraderId(b'1' * 20), OrderNumber(1)), Timestamp(0))
        self.proposed_trade = Trade.propose(TraderId(b'0' * 20),
                                            OrderId(TraderId(b'0' * 20), OrderNumber(2)),
                                            OrderId(TraderId(b'1' * 20), OrderNumber(3)),
                                            AssetPair(AssetAmount(100, 'BTC'), AssetAmount(30, 'MC')), Timestamp(0))

        self.tick = Tick(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                         AssetPair(AssetAmount(5, 'BTC'), AssetAmount(5, 'MC')),
                         Timeout(0), Timestamp(00), True)
        self.tick2 = Tick(OrderId(TraderId(b'0' * 20), OrderNumber(2)),
                          AssetPair(AssetAmount(500, 'BTC'), AssetAmount(5, 'MC')),
                          Timeout(0), Timestamp(0), True)

        self.order_timestamp = Timestamp.now()
        self.order = Order(OrderId(TraderId(b'0' * 20), OrderNumber(3)),
                           AssetPair(AssetAmount(50, 'BTC'), AssetAmount(40, 'MC')),
                           Timeout(5000), self.order_timestamp, False)
        self.order.set_verified()
        self.order2 = Order(OrderId(TraderId(b'0' * 20), OrderNumber(4)),
                            AssetPair(AssetAmount(50, 'BTC'), AssetAmount(10, 'MC')),
                            Timeout(5), Timestamp(int(time.time() * 1000) - 1000 * 1000), True)
        self.order2.set_verified()

    def test_add_trade(self):
        """
        Test the add trade method of an order
        """
        self.order.reserve_quantity_for_tick(OrderId(TraderId(b'5' * 20), OrderNumber(1)), 10)
        self.assertEqual(self.order.traded_quantity, 0)
        self.order.add_trade(OrderId(TraderId(b'5' * 20), OrderNumber(1)), AssetAmount(10, 'BTC'))
        self.assertEqual(self.order.traded_quantity, 10)

        self.order.reserve_quantity_for_tick(OrderId(TraderId(b'6' * 20), OrderNumber(1)), 40)
        self.order.add_trade(OrderId(TraderId(b'6' * 20), OrderNumber(1)), AssetAmount(40, 'MC'))
        self.order.add_trade(OrderId(TraderId(b'6' * 20), OrderNumber(1)), AssetAmount(40, 'BTC'))
        self.assertTrue(self.order.is_complete())
        self.assertFalse(self.order.cancelled)

    def test_has_acceptable_price(self):
        """
        Test the acceptable price method
        """
        order = Order(OrderId(TraderId(b'0' * 20), OrderNumber(3)),
                      AssetPair(AssetAmount(60, 'BTC'), AssetAmount(30, 'MB')),
                      Timeout(5000), self.order_timestamp, True)

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(30, 'MB'))
        self.assertTrue(order.has_acceptable_price(pair))

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(15, 'MB'))
        self.assertFalse(order.has_acceptable_price(pair))

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(60, 'MB'))
        self.assertTrue(order.has_acceptable_price(pair))

        order._is_ask = False

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(30, 'MB'))
        self.assertTrue(order.has_acceptable_price(pair))

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(15, 'MB'))
        self.assertTrue(order.has_acceptable_price(pair))

        pair = AssetPair(AssetAmount(60, 'BTC'), AssetAmount(60, 'MB'))
        self.assertFalse(order.has_acceptable_price(pair))

    def test_is_ask(self):
        # Test for is ask
        self.assertTrue(self.order2.is_ask())
        self.assertFalse(self.order.is_ask())

    def test_reserve_quantity_insufficient(self):
        # Test for reserve insufficient quantity
        self.assertRaises(ValueError, self.order.reserve_quantity_for_tick, self.tick2.order_id,
                          self.tick2.assets.first.amount)

    def test_reserve_quantity(self):
        # Test for reserve quantity
        self.assertEqual(0, self.order.reserved_quantity)
        self.order.reserve_quantity_for_tick(self.tick.order_id, 5)
        self.assertEqual(5, self.order.reserved_quantity)
        self.order.reserve_quantity_for_tick(self.tick.order_id, 5)
        self.assertEqual(10, self.order.reserved_quantity)

    def test_release_quantity(self):
        # Test for release quantity
        self.order.reserve_quantity_for_tick(self.tick.order_id, 5)
        self.assertEqual(5, self.order.reserved_quantity)
        self.order.release_quantity_for_tick(self.tick.order_id, 5)
        self.assertEqual(0, self.order.reserved_quantity)

        self.order.reserve_quantity_for_tick(self.tick.order_id, self.tick.assets.first.amount)
        quantity = self.tick.assets.first.amount + 1
        self.assertRaises(ValueError, self.order.release_quantity_for_tick, self.tick.order_id, quantity)

    def test_release_unreserved_quantity(self):
        # Test for release unreserved quantity
        with self.assertRaises(TickWasNotReserved):
            self.order.release_quantity_for_tick(self.tick.order_id, AssetAmount(5, 'BTC'))

    def test_is_valid(self):
        self.assertTrue(self.order.is_valid())
        self.assertFalse(self.order2.is_valid())

    def test_status(self):
        """
        Test the status of an order
        """
        self.order._verified = False
        self.assertEqual(self.order.status, "unverified")
        self.order.set_verified()
        self.assertEqual(self.order.status, "open")
        self.order._timeout = Timeout(0)
        self.assertEqual(self.order.status, "expired")
        self.order._timeout = Timeout(3600)
        self.order._traded_quantity = self.order.assets.first.amount
        self.order._received_quantity = self.order.assets.second.amount
        self.assertEqual(self.order.status, "completed")
        self.order._cancelled = True
        self.assertEqual(self.order.status, "cancelled")

    def test_to_dict(self):
        """
        Test the conversion of an order to a dictionary
        """
        self.assertEqual(self.order.to_dictionary(), {
            "trader_id": "30" * 20,
            "cancelled": False,
            "completed_timestamp": None,
            "is_ask": False,
            "order_number": 3,
            "assets": {
                "first": {
                    "amount": 50,
                    "type": "BTC",
                },
                "second": {
                    "amount": 40,
                    "type": "MC"
                }
            },
            "reserved_quantity": 0,
            "traded": 0,
            "status": "open",
            "timeout": 5000,
            "timestamp": int(self.order_timestamp)
        })


class OrderIDTestSuite(unittest.TestCase):
    """Order ID test cases."""

    def setUp(self):
        # Object creation
        self.order_id = OrderId(TraderId(b'0' * 20), OrderNumber(1))
        self.order_id2 = OrderId(TraderId(b'0' * 20), OrderNumber(1))
        self.order_id3 = OrderId(TraderId(b'0' * 20), OrderNumber(2))

    def test_equality(self):
        # Test for equality
        self.assertEqual(self.order_id, self.order_id)
        self.assertEqual(self.order_id, self.order_id2)
        self.assertFalse(self.order_id == self.order_id3)

    def test_non_equality(self):
        # Test for non equality
        self.assertNotEqual(self.order_id, self.order_id3)

    def test_hashes(self):
        # Test for hashes
        self.assertEqual(self.order_id.__hash__(), self.order_id2.__hash__())
        self.assertNotEqual(self.order_id.__hash__(), self.order_id3.__hash__())

    def test_str(self):
        # Test for string representation
        self.assertEqual('%s.1' % ('30' * 20), str(self.order_id))


class OrderNumberTestSuite(unittest.TestCase):
    """Order number test cases."""

    def setUp(self):
        # Object creation
        self.order_number = OrderNumber(1)
        self.order_number2 = OrderNumber(1)
        self.order_number3 = OrderNumber(3)

    def test_init(self):
        # Test for init validation
        with self.assertRaises(ValueError):
            OrderNumber(1.0)

    def test_equality(self):
        # Test for equality
        self.assertEqual(self.order_number, self.order_number)
        self.assertEqual(self.order_number, self.order_number2)
        self.assertFalse(self.order_number == self.order_number3)

    def test_non_equality(self):
        # Test for non equality
        self.assertNotEqual(self.order_number, self.order_number3)

    def test_hashes(self):
        # Test for hashes
        self.assertEqual(self.order_number.__hash__(), self.order_number2.__hash__())
        self.assertNotEqual(self.order_number.__hash__(), self.order_number3.__hash__())

    def test_str(self):
        # Test for string representation
        self.assertEqual('1', str(self.order_number))

    def test_int(self):
        # Test for integer representation
        self.assertEqual(1, int(self.order_number))
