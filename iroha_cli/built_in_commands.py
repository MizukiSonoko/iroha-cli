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
                        "type": str,
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
                if argv[item[0]] and type(argv[item[0]]) != item[1]["type"]:
                    raise CliException("{} is {}".format(
                        item[0],
                        str(item[1]["type"])
                    ))

    def config(self, argv, context):
        if not context.loaded:
            print("Config data is not loaded!")
            return
        print(
            "\n"
            "  Config  \n"
            " =========\n"
        )
        print(" name      : {}".format(context.name))
        print(" publicKey : {}".format(context.public_key))
        print(" privateKey: {}".format(
            context.private_key[:5] + "**...**" + context.private_key[-5:])
        )
        print(" targetPeer: {}\n".format(context.location))
        return True

    def keygen(self, argv,context = None):
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

