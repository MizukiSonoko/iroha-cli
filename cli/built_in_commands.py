import os
from enum import Enum

import binascii
from cli import crypto, file_io
from cli.exception import CliException
from primitive_pb2 import Amount, uint256
from commands_pb2 import Command, CreateAsset, AddAssetQuantity, CreateAccount, CreateDomain, TransferAsset

BASE_NAME = "iroha-mizuki-cli"


class BuildInCommand:

    def __init__(self):
        self.commands = {
            "config": {
                "option": {},
                "function": self.config,
                "detail": " Print current state \n"
                          "   - name\n"
                          "   - publicKey\n"
                          "   - privateKey\n"
            },
            "keygen": {
                "option": {
                    "account_name": {
                        "type": str,
                        "detail": "target's account name",
                        "required": True
                    },
                    "make_conf": {
                        "type": None,
                        "detail": "generate conf.yml",
                        "required": False
                    }
                },
                "function": self.keygen,
                "detail": " Print current state \n"
                          "   - name\n"
                          "   - publicKey\n"
                          "   - privateKey\n"
            }
        }

    def validate(self, expected, argv):
        for item in expected.items():
            if item[1]["required"] and not item[0] in argv:
                raise CliException("{} is required".format(item[0]))
            if item[0] in argv:
                if item[1]["type"] == int and not argv[item[0]].replace("-", "").isdigit():
                    raise CliException("{} is integer".format(item[0]))
                if item[1]["type"] == float and not argv[item[0]].isdigit():
                    raise CliException("{} is unsigned integer".format(item[0]))
                if item[1]["type"] == float and not argv[item[0]].replace("-", "").replace(".",                                                                                                         "").isdigit():
                    raise CliException("{} is float".format(item[0]))

    def config(self, context, argv):
        print(
            "\n"
            "  Config  \n"
            " =========\n"
        )
        print(" name      : {}".format(argv["name"]))
        print(" publicKey : {}".format(argv["publicKey"]))
        print(" privateKey: {}".format(
            argv["privateKey"][:5] + "**...**" + argv["privateKey"][-5:])
        )
        print(" targetPeer: {}".format(argv["location"]))
        print("")
        return None

    def keygen(self, argv):
        name = "keygen"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)

        key_pair = crypto.generate_keypair()
        if "keypair_name" in argv:
            filename_base = argv["keypair_name"]
        else:
            filename_base = argv["account_name"]
        file_io.save_keypair(filename_base, key_pair)

        if "make_conf" in argv:
            file_io.save_config(filename_base,{
                "peer": {
                    "address": "localhost",
                    "port": 50051
                },
                "account": {
                    "publicKeyPath": filename_base + ".pub",
                    "privateKeyPath": filename_base + ".pri",
                    "name": filename_base
                }
            })

