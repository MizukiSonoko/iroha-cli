# coding=utf-8
import base64
import time

from collections import namedtuple
from ed25519_python import ed25519

from iroha_cli.crypto import KeyPair


def generate_keypair_ed25519():
    # Mind the private/public key order!
    public_key, private_key = ed25519.generate()
    return KeyPair(public_key, private_key)


def sign_ed25519(key_pair, message):
    m = bytearray.fromhex(message.decode('utf-8'))
    return ed25519.sign(m, key_pair.public_key, key_pair.private_key)


def verify_ed25519(public_key, signature, message):
    return bool(ed25519.verify(message, signature, public_key))


def ed25519_sha3_256(message):
    return ed25519.sha3_256(message)


def ed25519_sha3_512(message):
    return ed25519.sha3_512(message)
