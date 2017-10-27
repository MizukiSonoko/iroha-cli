import base64
import datetime

import binascii
import grpc

from cli import crypto
from endpoint_pb2_grpc import CommandServiceStub, QueryServiceStub
from primitive_pb2 import Signature
from block_pb2 import Transaction
from queries_pb2 import Query


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
            Signature(pubkey=key_pair.raw_public_key, signature=sign)
        ]
    )
    return tx


def generateQuery(account_id, qry, key_pair):
    payload = Query.Payload(
        **qry,
        creator_account_id=account_id,
        created_time=int(datetime.datetime.now().timestamp() * 1000),
        query_counter=1
    )
    payload_hash = crypto.sha3_256(payload.SerializeToString())
    sign = crypto.sign(key_pair, payload_hash)
    query = Query(
        payload=payload,
        signature=Signature(pubkey=key_pair.raw_public_key, signature=sign)
    )
    return query


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
              .format(e.is_active(), e.details())
        )
        return False


def sendQuery(location, query):
    try:
        channel = grpc.insecure_channel(location)
        stub = QueryServiceStub(channel)
        stub.Find(query, timeout=1)  # wait 1s
        return True
    except grpc.RpcError as e:
        print("== Grpc happens error ==\n"
              "- Server is active?: {} \n"
              "- What's happen?   : {} \n"
              .format(e.is_active(), e.details())
              )
        return False
