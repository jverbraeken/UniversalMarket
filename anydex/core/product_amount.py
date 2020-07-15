# pylint: disable=long-builtin,redefined-builtin
from anydex.core.urn import URN

try:
    long
except NameError:
    long = int


class ProductAmount(object):
    """
    This class represents a specific number of products (can be infinity: math.inf). It contains various utility methods to add/substract product
    amounts.
    """

    def __init__(self, amount: long, urn: URN):
        """
        :param amount: Integer representation of the product amount
        :param urn: URN identifier of the product
        """
        super(ProductAmount, self).__init__()

        if isinstance(amount, int):
            amount = long(amount)

        if not isinstance(amount, long):
            raise ValueError("Price must be a long")

        if not isinstance(urn, URN):
            raise ValueError("URN must be an urn")

        self._amount = amount
        self._urn = urn

    @property
    def urn(self):
        """
        :rtype: str
        """
        return self._urn

    @property
    def amount(self):
        """
        :rtype long
        """
        return self._amount

    def __str__(self):
        return "%d %s" % (self.amount, self.urn)

    def __add__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.__class__(self.amount + other.amount, self.urn)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.__class__(self.amount - other.amount, self.urn)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.amount < other.amount
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.amount <= other.amount
        else:
            return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, ProductAmount) or self.urn != other.urn:
            return NotImplemented
        else:
            return self.amount == other.amount

    def __gt__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.amount > other.amount
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ProductAmount) and self.urn == other.urn:
            return self.amount >= other.amount
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.amount, self.urn))

    def to_dictionary(self):
        return {
            "amount": self.amount,
            "type": str(self.urn)
        }
