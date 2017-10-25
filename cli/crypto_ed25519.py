
# coding=utf-8
import cli_ed25519
import sha3
import base64
import time

from collections import namedtuple
from cli.crypto import KeyPair

def generate_keypair_ed25519():
    # Mind the private/public key order!
    public_key, private_key = cli_ed25519.create_keypair()
    return KeyPair(raw_private_key=private_key, raw_public_key=public_key)

def sign_ed25519(key_pair, message):
    raw_signature = cli_ed25519.sign(message, key_pair.raw_public_key, key_pair.raw_private_key)
    return base64.b64encode(raw_signature)

def verify_ed25519(public_key, signature, message):
    public_key = base64.b64decode(public_key)
    signature = base64.b64decode(signature)
    return bool(cli_ed25519.verify(message,signature,public_key))
