import base64

import sha3
import os

from collections import namedtuple


class KeyPair(namedtuple('KeyPair', ['raw_private_key', 'raw_public_key'])):
    def encode(value):
        return base64.b64encode(value)

    def __encode__(self, value):
        return base64.b64encode(value)

    def decode(value):
        return base64.b64decode(value)

    def __decode__(self,value):
        return base64.b64decode(value)

    @property
    def private_key(self):
        return self.__encode__(self.raw_private_key)

    @property
    def public_key(self):
        return self.__encode__(self.raw_public_key)


from cli.crypto_ed25519 import generate_keypair_ed25519, sign_ed25519, verify_ed25519


def generate_keypair():
    return generate_keypair_ed25519()


def sign(key_pair, message):
    return base64.b64decode(sign_ed25519(key_pair, message))


def verify(pub_key, sig, message):
    return verify_ed25519(pub_key, sig, message)


def sha3_256(message):
    return sha3.sha3_256(message).digest()
