# pylint: disable=long-builtin,redefined-builtin

from anydex.core.product_amount import ProductAmount
from anydex.core.price import Price
from anydex.core.urn import URN

try:
    long
except NameError:
    long = int


class AssetPair(object):
    """
    An asset pair represents a pair of specific amounts of assets, i.e. 10 BTC - 20 MB.
    It is used when dealing with orders in the market.
    """

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __eq__(self, other):
        if not isinstance(other, AssetPair):
            return NotImplemented
        else:
            return self.first == other.first and self.second == other.second

    def to_dictionary(self):
        return {
            "first": self.first.to_dictionary(),
            "second": self.second.to_dictionary()
        }

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(ProductAmount(dictionary["first"]["amount"], URN(dictionary["first"]["type"])),
                   ProductAmount(dictionary["second"]["amount"], URN(dictionary["second"]["type"])))

    @property
    def price(self):
        """
        Return a Price object of this asset pair, which expresses the second asset into the first asset.
        """
        return Price(self.second.amount, self.first.amount, self.second.urn, self.first.urn)

    def proportional_downscale(self, first=None, second=None):
        """
        This method constructs a new AssetPair where the ratio between the first/second asset is preserved.
        One should specify a new amount for the first asset.
        For instance, if we have an asset pair (4 BTC, 8 MB), the price is 8/4 = 2 MB/BTC.
        If we now change the amount of the first asset from 4 BTC to 1 BTC, the new AssetPair becomes (1 BTC, 2 MB).
        Likewise, if the second asset is changed to 4, the new AssetPair becomes (2 BTC, 4 MB)
        """
        if first:
            return AssetPair(ProductAmount(first, self.first.urn),
                             ProductAmount(long(self.price.amount * first), self.second.urn))
        elif second:
            return AssetPair(ProductAmount(long(second / self.price.amount), self.first.urn),
                             ProductAmount(second, self.second.urn))
        else:
            raise ValueError("No first/second provided in proportional downscale!")

    def __str__(self):
        return "%s %s" % (self.first, self.second)
