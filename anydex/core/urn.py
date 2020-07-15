import re
import uuid

_urn_rex = re.compile("^urn:[a-z0-9][a-z0-9-]{0,31}:[a-z0-9()+,\-.:=@;$_!*'%/?#]+$")


class URN(object):
    def __init__(self, urn: str):
        super(URN, self).__init__()

        if not isinstance(urn, str):
            raise ValueError("URN must be a string")

        if not _urn_rex.fullmatch(urn):
            raise ValueError("URN is not a valid URN, as defined by RFC 2141")

        self._urn = urn

    def __str__(self):
        return self._urn

    def __eq__(self, other):
        if isinstance(other, URN):
            return self._urn == other._urn
        return NotImplemented

    def __hash__(self):
        return hash(self._urn)

    @classmethod
    def generate_test(cls):
        return URN("urn:uuid:" + str(uuid.uuid1()))
