import os
from enum import Enum

import binascii
from cli import crypto, file_io
from cli.libs.amount import int_to_amount
from cli.exception import CliException
from primitive_pb2 import Amount, uint256
from commands_pb2 import Command, CreateAsset, AddAssetQuantity, CreateAccount, CreateDomain, TransferAsset

BASE_NAME = "iroha-mizuki-cli"


class CommandList:
    """
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
    """

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
                        "required": True
                    },
                },
                "function": self.AddAssetQuantity,
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
                    "keypair_name": {
                        "type": str,
                        "detail": "save to this keypair_name like mizukey, if no set, generates ${"
                                  "account_name}.pub/${account_name} ",
                        "required": False
                    }
                },
                "function": self.CreateAccount,
                "detail": "CreateAccount asset's quantity"
            },
            "CreateDomain": {
                "option": {
                    "domain_name": {
                        "type": str,
                        "detail": "new domain name like japan",
                        "required": True
                    }
                },
                "function": self.CreateDomain,
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
                        "required": False
                    }
                },
                "function": self.CreateAsset,
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
                        "required": True
                    }
                },
                "function": self.TransferAsset,
                "detail": "transfer asset"
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

    def printTransaction(self, name, expected, argv):
        if self.printInfo:
            print("[{}] run {} ".format(BASE_NAME, name))
            for n in expected.keys():
                print("- {}: {}".format(n, argv[n]))

    def AddAssetQuantity(self, argv):
        name = "AddAssetQuantity"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)

        # ToDo In now precision = 0, but when I enter 1.03, set precision = 2 automatically
        # ToDo Correct to set Amount.value
        return Command(add_asset_quantity=AddAssetQuantity(
            account_id=argv["account_id"],
            asset_id=argv["asset_id"],
            amount=int_to_amount(argv["amount"], precision=0)
        ))

    def CreateAccount(self, argv):
        name = "CreateAccount"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)

        # ToDo validate and print check
        # I want to auto generate
        key_pair = crypto.generate_keypair()
        if "keypair_name" in argv and argv["keypair_name"]:
            filename_base = argv["keypair_name"]
        else:
            filename_base = argv["account_name"] + "@" + argv["domain_id"]

        file_io.save_keypair(filename_base, key_pair)
        return Command(create_account=CreateAccount(
            account_name=argv["account_name"],
            domain_id=argv["domain_id"],
            main_pubkey=key_pair.raw_public_key
        ))

    def CreateAsset(self, argv):
        name = "CreateAsset"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)
        precision = argv.get("precision") if argv.get("precision") else 0
        return Command(create_asset=CreateAsset(
            asset_name=argv["asset_name"],
            domain_id=argv["domain_id"],
            precision= precision
        ))

    def CreateDomain(self, argv):
        name = "CreateDomain"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)
        return Command(create_domain=CreateDomain(
            domain_name=argv["domain_name"]
        ))

    def TransferAsset(self, argv):
        name = "CreateDomain"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)

        # ToDo validate and print check
        return Command(transfer_asset=TransferAsset(
            src_account_id=argv["src_account_id"],
            dest_account_id=argv["dest_account_id"],
            asset_id=argv["asset_id"],
            description=argv.get("description", ""),
            amount=int_to_amount(argv["amount"], precision=0)
        ))
