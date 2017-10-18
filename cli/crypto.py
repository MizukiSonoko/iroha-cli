import ed25519
import sha3
import os

def generate_keypair_hex():
    h = sha3.sha3_256()
    h.update(os.urandom(87))
    signing_key, verifying_key = ed25519.create_keypair()
    return (
        signing_key.to_ascii(encoding="hex"),
        verifying_key.to_ascii(encoding="hex")
    )

def sign(priKey, message):
    return ed25519.SigningKey(priKey.encode('utf-8')).sign( message, encoding="hex")


def hash(msg):
    h = sha3.sha3_256()
    h.update(msg)
    return h.hexdigest()
