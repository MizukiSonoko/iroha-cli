import base64

import sha3
import os

from collections import namedtuple


class KeyPair:
    def __init__(self, pub, pri):
        self.private_key = pri
        self.public_key = pub


from iroha_cli.crypto_ed25519 import generate_keypair_ed25519, sign_ed25519, verify_ed25519, ed25519_sha3_512, \
    ed25519_sha3_256


def generate_keypair():
    return generate_keypair_ed25519()


def sign(key_pair, message):
    return sign_ed25519(key_pair, message)


def verify(pub_key, sig, message):
    return verify_ed25519(pub_key, sig, message)


def sha3_256(message):
    return ed25519_sha3_256(message)


def sha3_512(message):
    return ed25519_sha3_512(message)
