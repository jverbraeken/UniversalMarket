import unittest

from anydex.core.product_amount import ProductAmount
from anydex.core.assetpair import AssetPair
from anydex.core.message import TraderId
from anydex.core.order import Order, OrderId, OrderNumber
from anydex.core.order_repository import MemoryOrderRepository
from anydex.core.timeout import Timeout
from anydex.core.timestamp import Timestamp
from anydex.test import util


class MemoryOrderRepositoryTestSuite(unittest.TestCase):
    """Memory order repository test cases."""

    def setUp(self):
        # Object creation
        self.memory_order_repository = MemoryOrderRepository(b'0' * 20)
        self.order_id = OrderId(TraderId(b'0' * 20), OrderNumber(1))
        self.order = Order(self.order_id, AssetPair(ProductAmount(100, util.urn_btc), ProductAmount(30, util.urn_mb)),
                           Timeout(0), Timestamp(10), False)
        self.order2 = Order(self.order_id, AssetPair(ProductAmount(1000, util.urn_btc), ProductAmount(30, util.urn_mb)),
                            Timeout(0), Timestamp(10), False)

    def test_add(self):
        # Test for add
        self.assertEqual([], list(self.memory_order_repository.find_all()))
        self.memory_order_repository.add(self.order)
        self.assertEqual([self.order], list(self.memory_order_repository.find_all()))

    def test_delete_by_id(self):
        # Test for delete by id
        self.memory_order_repository.add(self.order)
        self.assertEqual([self.order], list(self.memory_order_repository.find_all()))
        self.memory_order_repository.delete_by_id(self.order_id)
        self.assertEqual([], list(self.memory_order_repository.find_all()))

    def test_find_by_id(self):
        # Test for find by id
        self.assertEqual(None, self.memory_order_repository.find_by_id(self.order_id))
        self.memory_order_repository.add(self.order)
        self.assertEqual(self.order, self.memory_order_repository.find_by_id(self.order_id))

    def test_find_all(self):
        # Test for find all
        self.assertEqual([], list(self.memory_order_repository.find_all()))
        self.memory_order_repository.add(self.order)
        self.assertEqual([self.order], list(self.memory_order_repository.find_all()))

    def test_next_identity(self):
        # Test for next identity
        self.assertEqual(OrderId(TraderId(b'0' * 20), OrderNumber(1)),
                          self.memory_order_repository.next_identity())

    def test_update(self):
        # Test for update
        self.memory_order_repository.add(self.order)
        self.memory_order_repository.update(self.order2)
        self.assertNotEqual(self.order, self.memory_order_repository.find_by_id(self.order_id))
        self.assertEqual(self.order2, self.memory_order_repository.find_by_id(self.order_id))
