import os
from enum import Enum

import binascii
from iroha_cli import crypto, file_io
from iroha_cli.libs.amount import int_to_amount
from iroha_cli.exception import CliException
from primitive_pb2 import Amount, uint256
from commands_pb2 import *

BASE_NAME = "iroha-mizuki-cli"


class CommandList:
    def __init__(self, printInfo=False):
        self.printInfo = printInfo
        self.commands = {
            "AddAssetQuantity": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    },
                    "asset_id": {
                        "type": str,
                        "detail": "target's asset id like japan/yen",
                        "required": True
                    },
                    "amount": {
                        "type": int,
                        "detail": "target's asset id like japan/yen",
                        "required": True,
                        "converter": lambda amount: int_to_amount(amount, precision=0)
                    },
                },
                "function": self.generate("add_asset_quantity","AddAssetQuantity"),
                "detail": "Add asset's quantity"
            },
            "CreateAccount": {
                "option": {
                    "account_name": {
                        "type": str,
                        "detail": "account name like mizuki",
                        "required": True
                    },
                    "domain_id": {
                        "type": str,
                        "detail": "new account will be in this domain like japan",
                        "required": True
                    },
                    "main_pubkey": {
                        "type": str,
                        "detail": "save to this keypair_name like mizukey, if no set, generates ${"
                                  "account_name}.pub/${account_name} ",
                        "required": False,
                        "command_arguments": False
                    }
                },
                "function": self.generate("create_account","CreateAccount",self.prev_CreateAccount),
                "detail": "CreateAccount asset's quantity"
            },
            "CreateDomain": {
                "option": {
                    "domain_id": {
                        "type": str,
                        "detail": "new domain name like japan",
                        "required": True
                    },
                    "default_role": {
                        "type": str,
                        "detail": "new domain name like japan",
                        "required": True
                    }
                },
                "function": self.generate("create_domain","CreateDomain"),
                "detail": "Create domain in domain"
            },
            "CreateAsset": {
                "option": {
                    "asset_name": {
                        "type": str,
                        "detail": "asset name like mizuki",
                        "required": True
                    },
                    "domain_id": {
                        "type": str,
                        "detail": "new account will be in this domain like japan",
                        "required": True
                    },
                    "precision": {
                        "type": int,
                        "detail": "how much support .000, default 0",
                        "required": False,
                        "converter": lambda precision: precision if precision else 0
                    }
                },
                "function": self.generate("create_asset","CreateAsset"),
                "detail": "Create new asset in domain"
            },
            "TransferAsset": {
                "option": {
                    "src_account_id": {
                        "type": str,
                        "detail": "current owner's account name like mizuki@japan",
                        "required": True
                    },
                    "dest_account_id": {
                        "type": str,
                        "detail": "next owner's account name like iori@japan",
                        "required": True
                    },
                    "asset_id": {
                        "type": str,
                        "detail": "managed asset's name like yen",
                        "required": True
                    },
                    "description": {
                        "type": str,
                        "detail": "attach some text",
                        "required": False
                    },
                    "amount": {
                        "type": int,
                        "detail": "how much transfer",
                        "required": True,
                        "converter": lambda amount: int_to_amount( amount, precision=0)
                    }
                },
                "function":self.generate("transfer_asset","TransferAsset"),
                "detail": "transfer asset"
            }
        }

    def generate(self, value_name, class_name, previous_execute = lambda argv: argv):
        def __generate__(argv):
            self.validate(self.commands[class_name]["option"],argv)
            previous_execute(argv)
            # Remove config option from constructor arguments
            if "config" in argv:
                argv.pop("config")

            for name, value in self.commands[class_name]["option"].items():
                # Convert value like int -> Amount
                if "converter" in value:
                    argv[name] = value["converter"](argv[name])
                # 'command_arguments' is used only cli, so remove before construct command
                if "command_arguments" in value and name in argv:
                    argv.pop(name)

            return Command(**{value_name: eval(class_name)(**argv)})
        return __generate__

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

    def prev_CreateAccount(self, argv):
        # ToDo validate and print check
        # I want to auto generate
        key_pair = crypto.generate_keypair()
        if "keypair_name" in argv and argv["keypair_name"]:
            filename_base = argv["keypair_name"]
        else:
            filename_base = argv["account_name"] + "@" + argv["domain_id"]

        file_io.save_keypair(filename_base, key_pair)
