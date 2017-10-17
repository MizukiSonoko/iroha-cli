import grpc

from cli import crypto
from schema.primitive_pb2 import Signature
from schema.block_pb2 import Transaction
from schema.endpoint_pb2_grpc import CommandServiceStub, QueryServiceStub

import datetime

"""
message Header {
  uint64 created_time = 1;
  repeated Signature signatures = 2;
}

message Signature {
   bytes pubkey    = 1;
   bytes signature = 2;
}


 message Transaction {
  message Payload {
     repeated Command commands = 1;
    string creator_account_id = 2;
    uint64 tx_counter  = 3;
    uint64 created_time = 4;
   }

  Payload payload = 1;
  repeated Signature signature = 2;
 }
 
        AddAssetQuantity add_asset_quantity = 1;
        AddPeer add_peer = 2;
        AddSignatory add_signatory = 3;
        CreateAsset create_asset = 4;
        CreateAccount create_account = 5;
        CreateDomain create_domain = 6;
        RemoveSignatory remove_sign = 7;
        SetAccountPermissions set_permission = 8;
        SetAccountQuorum set_quorum = 9;
        TransferAsset transfer_asset = 10;
        AppendRole append_role = 11;
        CreateRole create_role = 12;
        GrantPermission grant_permission = 13;
        RevokePermission revoke_permission = 14;
        ExternalGuardian external_guardian = 15;
"""

def generateTransaction(account_id, commands):
    return Transaction(
        payload=Transaction.Payload(
            commands=commands,
            creator_account_id=account_id,
            tx_counter=0,
            created_time=int(datetime.datetime.now().timestamp() * 1000)
        ),
        signature=[Signature()]
    )


def sendTx(location, tx):
    try:
        crypto.hash((tx.payload.SerializeToString()))
        channel = grpc.insecure_channel(location)
        stub = CommandServiceStub(channel)
        stub.Torii(tx, timeout=1)  # wait 1s
        return True
    except Exception as e:
        print(e)
        return False
