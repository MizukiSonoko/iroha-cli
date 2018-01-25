import os
from enum import Enum

import binascii
from iroha_cli import crypto, file_io
from iroha_cli.exception import CliException
from primitive_pb2 import Amount, uint256
from commands_pb2 import Command, CreateAsset, AddAssetQuantity, CreateAccount, CreateDomain, TransferAsset

BASE_NAME = "iroha-mizuki-cli"


class BuildInCommand:

    def __init__(self):
        self.commands = {
            "keygen": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id",
                        "required": True
                    }
                },
                "function": self.keygen,
                "detail": " Generate keypair\n"
            }
        }

    def validate(self, expected, argv):
        for item in expected.items():
            if item[1]["required"] and not item[0] in argv:
                raise CliException("{} is required".format(item[0]))
            if item[0] in argv:
                if argv[item[0]] and type(argv[item[0]]) != item[1]["type"]:
                    raise CliException("{} is {}".format(
                        item[0],
                        str(item[1]["type"])
                    ))

    def keygen(self, argv):
        name = "keygen"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)

        key_pair = crypto.generate_keypair()
        account_id = argv["account_id"]
        file_io.save_keypair(account_id, key_pair)

