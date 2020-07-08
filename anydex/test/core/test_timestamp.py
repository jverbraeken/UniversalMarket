import time
import unittest

from anydex.core.timestamp import Timestamp


class TimestampTestSuite(unittest.TestCase):
    """Timestamp test cases."""

    def setUp(self):
        # Object creation
        self.timestamp = Timestamp(1462224447000)
        self.timestamp2 = Timestamp(1462224447000)
        self.timestamp3 = Timestamp(1305743832000)

    def test_init(self):
        # Test for init validation
        with self.assertRaises(ValueError):
            Timestamp(-1.0)
        with self.assertRaises(ValueError):
            Timestamp("1")

    def test_now(self):
        # Test for Timestamp.now
        self.assertAlmostEqual(int(time.time() * 1000), int(Timestamp.now()), delta=1000)

    def test_conversion(self):
        # Test for conversions
        self.assertEqual(1462224447000, int(self.timestamp))

        # We cannot check the exact timestamp since this is specific to the configured time zone
        self.assertTrue(str(self.timestamp))

    def test_comparison(self):
        # Test for comparison
        self.assertTrue(self.timestamp3 < self.timestamp)
        self.assertTrue(self.timestamp > self.timestamp3)
        self.assertTrue(self.timestamp3 < 1405743832000)
        self.assertTrue(self.timestamp <= 1462224447000)
        self.assertTrue(self.timestamp > 1362224447000)
        self.assertTrue(self.timestamp3 >= 1305743832000)
        self.assertEqual(NotImplemented, self.timestamp.__lt__("10"))
        self.assertEqual(NotImplemented, self.timestamp.__le__("10"))
        self.assertEqual(NotImplemented, self.timestamp.__gt__("10"))
        self.assertEqual(NotImplemented, self.timestamp.__ge__("10"))

    def test_equality(self):
        # Test for equality
        self.assertTrue(self.timestamp == self.timestamp2)
        self.assertTrue(self.timestamp != self.timestamp3)
        self.assertFalse(self.timestamp == 6)

    def test_hash(self):
        # Test for hashes
        self.assertEqual(self.timestamp.__hash__(), self.timestamp2.__hash__())
        self.assertNotEqual(self.timestamp.__hash__(), self.timestamp3.__hash__())
