from ctypes import *
import base64

libed2559 = cdll.LoadLibrary('./lib/ed25519/lib/libed25519.so')


def generate():
    seed = POINTER(c_ubyte)((c_ubyte * 32)())
    public_key = POINTER(c_ubyte)((c_ubyte * 32)())
    private_key = POINTER(c_ubyte)((c_ubyte * 64)())

    libed2559.ed25519_create_seed.argtypes = [POINTER(c_ubyte)]
    libed2559.ed25519_create_seed(seed)
    libed2559.ed25519_create_keypair.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_create_keypair(public_key, private_key, seed)
    publist = []
    for i in range(32):
        publist.append(public_key[i])
    print(publist)
    publicKey64 = base64.b64encode(bytes(publist))

    prilist = []
    for i in range(64):
        prilist.append(private_key[i])
    print(prilist)
    privateKey64 = base64.b64encode(bytes(prilist))

    return (publicKey64, privateKey64)


def generate_int():
    seed = POINTER(c_ubyte)((c_ubyte * 32)())
    public_key = POINTER(c_ubyte)((c_ubyte * 32)())
    private_key = POINTER(c_ubyte)((c_ubyte * 64)())

    libed2559.ed25519_create_seed.argtypes = [POINTER(c_ubyte)]
    libed2559.ed25519_create_seed(seed)
    libed2559.ed25519_create_keypair.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_create_keypair(public_key, private_key, seed)
    publist = []
    for i in range(32):
        publist.append(public_key[i])

    prilist = []
    for i in range(64):
        prilist.append(private_key[i])

    return (publist, prilist)

"""
ed25519_sign(
  unsigned char *signature,
  const unsigned char *message,
  size_t message_len,
  const unsigned char *public_key,
  const unsigned char *private_key
);
"""


def sign(message, public, private):
    signature = POINTER(c_ubyte)((c_ubyte * 64)())
    libed2559.ed25519_sign.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_sign(
        signature,
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(public))).from_buffer_copy(base64.b64decode(public))),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(private))).from_buffer_copy(base64.b64decode(private)))
    )

    siglist = []
    for i in range(64):
        siglist.append(signature[i])
    print(len(siglist))
    return base64.b64encode(bytes(siglist))


def sign_int(message, public, private):
    signature = POINTER(c_ubyte)((c_ubyte * 64)())
    libed2559.ed25519_sign.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_sign(
        signature,
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(public)).from_buffer_copy(bytes(public))),
        POINTER(c_ubyte)((c_ubyte * len(private)).from_buffer_copy(bytes(private)))
    )
    siglist = []
    for i in range(64):
        siglist.append(signature[i])
    return siglist


def verify_int(message, signature, public):
    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    print('int sig:', signature)
    print('int siglen:', len(signature))
    print('int pub:', public)
    print('int publen:', len(public))
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * len(signature)).from_buffer_copy(bytes(signature))),
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(public)).from_buffer_copy(bytes(public))),
    )


"""
ed25519_verify(
  const unsigned char *signature,
  const unsigned char *message,
  size_t message_len,
  const unsigned char *public_key
);
"""


def verify(message, signature, public):
    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(signature))).from_buffer_copy(base64.b64decode(signature))),
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(public))).from_buffer_copy(base64.b64decode(public))),
    )


def hex2bin(message):
    b = []
    for i in range(len(message) - 1):
        b.append(int(
            '0b' + format(int(chr(message[i]), 16), 'b').zfill(4) + format(int(chr(message[i + 1]), 16), 'b').zfill(4),
            2))
    return b[::2]


def verify_with_hex(message, signature, public):
    print(hex2bin(public))

    pubhex = b''.join(list(map(lambda x: x.to_bytes(1, byteorder='big'), hex2bin(public))))
    sighex = b''.join(list(map(lambda x: x.to_bytes(1, byteorder='big'), hex2bin(signature))))

    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * 64).from_buffer_copy(sighex)),
        POINTER(c_ubyte)((c_ubyte * 64).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * 32).from_buffer_copy(pubhex)),
    )

if __name__ == "__main__":
    message = b"c0a5cca43b8aa79eb50e3464bc839dd6fd414fae0ddf928ca23dcebf8a8b8dd0"
    pubb, prib = generate()

    private_key = b"+BTZfRSPRgDdxmjZlK+QhJ3RQryMH23LIPqg5C/Eu2QcBoj3QM6ovTcmPok0iFYI1y9M683ZS4Ifp10jr9dQrQ=="
    public_key = b"b+etgin9x1S16omALSjr4HTVzv9IEXQzlvSTp7el0Js="

    signature = b"HlJIjuds2OaSeyOjWjpnpXis55NvH3TD1SNVEwedu7sAY+Ypkksg3ovHUGfBhwd8uVmIX+JgnjrhKgPdyeO7DA==";
    message = b"0f1a39c82593e8b48e69f000c765c8e8072269d3bd4010634fa51d4e685076e30db22a9fb75def7379be0e808392922cb8c43d5dd5d5039828ed7ade7e1c6c81";

    pub_go = b"ZipcethJh6X7GCeYSPsD/FQLo5gbqcDU1S+yG8JKVJ0="
    pri_go = b"lP7Z+eyg91OEyS1T0QvZHk95eaoW5inOIhNLz/jRlUFmKlx62EmHpfsYJ5hI+wP8VAujmBupwNTVL7IbwkpUnQ=="
    sig_go = b"d1B8kLk7i+aUMWJsvkrOvuHwTdvB0HtQPhQiB44QoXgGHaTPOL4+kagobPhWvF61hGezzLn6qukv2UYV5R1/CQ=="

    msg = sign(message, pub_go, pri_go)
    print("====")
    print(msg)
    print(len(msg))

    print(verify(
        message,
        msg,
        pub_go
    ))
    print(verify(
        b"charinko_locked_sate",
        sig_go,
        pub_go
    ))
    print("====")

    signatureb = sign(message, pubb, prib)

    print('b pygen sig: ', signatureb)
    print('b pygen sig: ', len(signatureb))

    print(generate_int())

    print(verify(
        message,
        signatureb,
        pubb
    ))

    print('android verify is ',verify(
        message,
        signature,
        public_key
    ))

    signature_android = sign(message, public_key, private_key)

    print('android\'s key sign and verify is ',verify(
        message,
        signature,
        public_key
    ))
