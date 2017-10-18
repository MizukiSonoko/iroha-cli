import datetime

import grpc

from cli import crypto
from endpoint_pb2_grpc import CommandServiceStub
from primitive_pb2 import Signature
from block_pb2 import Transaction


def generateTransaction(account_id, commands, key_pair):
    payload = Transaction.Payload(
        commands=commands,
        creator_account_id=account_id,
        tx_counter=0,
        created_time=int(datetime.datetime.now().timestamp() * 1000)
    )
    payload_hash = crypto.hash((payload.SerializeToString()))
    sign = crypto.sign(key_pair["privateKey"], payload_hash)
    return Transaction(
        payload=payload,
        signature=[Signature(pubkey=key_pair["publicKey"].encode(),signature=sign)]
    )


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
