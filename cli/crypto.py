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


from cli.crypto_ed25519_sha3 import generate_keypair_ed25519_sha3, sign_ed25519_sha3


def generate_keypair():
    return generate_keypair_ed25519_sha3()


def sign(key_pair, message):
    return base64.b64decode(sign_ed25519_sha3(key_pair, message))


def verify_ed25519_sha3(pub_key, sig, message):
    return verify_ed25519_sha3(pub_key, sig, message)


def sha3_256(message):
    return sha3.sha3_256(message).hexdigest()
