import base64
import datetime

import binascii
import grpc

from iroha_cli import crypto
from iroha_cli.exception import CliException
from endpoint_pb2_grpc import CommandServiceStub, QueryServiceStub
from endpoint_pb2 import TxStatusRequest, TxStatus
from primitive_pb2 import Signature
from block_pb2 import Transaction
from queries_pb2 import Query
from responses_pb2 import ErrorResponse

from google.protobuf.json_format import MessageToJson

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
    #print(tx)
    return tx, payload_hash

def waitTransaciton(location, tx_hash):
    payload = TxStatusRequest(tx_hash=tx_hash)
    not_received_cnt = 0
    while True:
        result = sendTxStatus(location, payload)

        if result.tx_status == TxStatus.Value('STATELESS_VALIDATION_FAILED'):
            raise Exception('stateless validation failed')

        elif result.tx_status == TxStatus.Value('STATEFUL_VALIDATION_FAILED'):
            raise Exception('stateful validation failed')

        elif result.tx_status == TxStatus.Value('NOT_RECEIVED'):
            if not_received_cnt > MAX_POLLING_TIME:
                raise TimeoutError
            else:
                not_received_cnt += 1

        elif result.tx_status == TxStatus.Value('COMMITTED'):
            return True


def generateQuery(account_id, qry, key_pair):
    payload = Query.Payload(
        **qry,
        creator_account_id=account_id,
        created_time=int(datetime.datetime.now().timestamp() * 1000),
    )
    # This is a trap. ('A`) I guess hyperledger/iroha has bug in serialize or deserialize?
    # query_counter is removed before hash, so verify shouldn't be valid!!
    # payload.query_counter = 1
    #
    payload_hash = crypto.sha3_256(payload.SerializeToString())
    sign = crypto.sign(key_pair, payload_hash)
    query = Query(
        payload=payload,
        signature=Signature(pubkey=key_pair.raw_public_key, signature=sign)
    )
    return query

def sendTxStatus(location, tx_status):
    try:
        channel = grpc.insecure_channel(location)
        stub = CommandServiceStub(channel)
        return stub.Status(tx_status, timeout=1)  # wait 1s
    except grpc.RpcError as e:
        print("== Grpc happens error ==\n"
              "- Server is active?: {} \n"
              "- What's happen?   : {} \n"
              .format(e.is_active(), e.details())
        )
        return False


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
        res = stub.Find(query, timeout=1)  # wait 1s
        if res.HasField('error_response'):
            reason = res.error_response.reason
            if reason == ErrorResponse.STATELESS_INVALID:
                raise CliException("[Iroha] stateless invalied")
            elif reason == ErrorResponse.STATEFUL_INVALID:
                raise CliException("[Iroha] statefull invalied")
            elif reason == ErrorResponse.NO_ACCOUNT:
                raise CliException("[Iroha] account does not exist")
            elif reason == ErrorResponse.NO_ACCOUNT_ASSETS:
                raise CliException("[Iroha] account don't have asset")
            elif reason == ErrorResponse.NOT_SUPPORTED:
                raise CliException("[Iroha] signatories does not exist")
            elif reason == ErrorResponse.WRONG_FORMAT:
                raise CliException("[Iroha] json format wrong No happen")
            elif reason == ErrorResponse.NO_ASSET:
                raise CliException("[Iroha] asset does not exist")
            elif reason == ErrorResponse.NO_ROLES:
                raise CliException("[Iroha] there are no roles defined in the system")

        if res.HasField('account_response'):
            result = res.account_response
        elif res.HasField('asset_response'):
            result = res.asset_response
        elif res.HasField('signatories_response'):
            result = res.signatories_response
        elif res.HasField('transactions_response'):
            result = res.transactions_response
        elif res.HasField('account_assets_response'):
            result = res.account_assets_response
        else:
            raise CliException("Sorry! not implements...")

        return MessageToJson(result)
    except grpc.RpcError as e:
        raise CliException("[Grpc] Server({location}) is {status}, {detail}".format(
            location=location,status=e.is_active(),detail=e.details()))
