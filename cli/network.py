import datetime

import binascii
import grpc

from cli import crypto
from endpoint_pb2_grpc import CommandServiceStub
from primitive_pb2 import Signature
from block_pb2 import Transaction


def generateTransaction(account_id, commands, key_pair):
    payload = Transaction.Payload(
        commands=commands,
        creator_account_id=account_id,
        tx_counter=1,
        created_time=int(datetime.datetime.now().timestamp() * 1000)
    )
    payload_hash = crypto.sha3_256(payload.SerializeToString())
    sign = crypto.sign(key_pair, payload_hash)
    tx = Transaction(
        payload=payload,
        signature=[
            Signature(pubkey=binascii.hexlify(key_pair.raw_public_key),signature=binascii.hexlify(sign))
        ]
    )
    print(tx)
    return tx


def sendTx(location, tx):
    try:
        channel = grpc.insecure_channel(location)
        stub = CommandServiceStub(channel)
        stub.Torii(tx, timeout=1)  # wait 1s
        return True
    except grpc.RpcError as e:
        print("== Grpc happens error ==\n"
              "- Server is active?: {} \n"
              "- What's happen?   : {} \n"
              .format(e.is_active(),e.details())
        )
        return False
