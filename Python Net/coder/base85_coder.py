import base64

from .coder import Coder


class Base85Coder(Coder):
    def encode(self, data: bytes) -> bytes:
        return base64.b85encode(data)

    def decode(self, data: bytes) -> bytes:
        return base64.b85decode(data)