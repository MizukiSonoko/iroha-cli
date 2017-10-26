import os
from enum import Enum

import binascii
from cli import crypto, file_io
from cli.exception import CliException
from primitive_pb2 import Amount, uint256
from commands_pb2 import Command, CreateAsset, AddAssetQuantity, CreateAccount, CreateDomain, TransferAsset

BASE_NAME = "iroha-mizuki-cli"


class QueryList:
    """
       GetAccount get_account = 3;
       GetSignatories get_account_signatories = 4;
       GetAccountTransactions get_account_transactions = 5;
       GetAccountAssetTransactions get_account_asset_transactions = 6;
       GetAccountAssets get_account_assets = 7;
       GetRoles get_roles = 8;
       GetAssetInfo get_asset_info = 9;
       GetRolePermissions get_role_permissions = 10;
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
                        "type": float,
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
                        "type": str,
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
                if type(argv[item[0]]) != item[1]["type"]:
                    raise CliException("{} is {}".format(item[0],str(item[1]["type"])))

    def printTransaction(self, name, expected, argv):
        if self.printInfo:
            print("[{}] run {} ".format(BASE_NAME, name))
            for n in expected.keys():
                print("- {}: {}".format(n, argv[n]))


    def config(self, argv):
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
        self.printTransaction(name, argv_info, argv)

        key_pair = crypto.generate_keypair()
        try:
            if "keypair_name" in argv:
                filename_base = argv["keypair_name"]
            else:
                filename_base = argv["account_name"]

            try:
                with open(filename_base + ".pub", "w") as pub:
                    pub.write(key_pair.public_key.decode())
            except (OSError, IOError) as e:
                print(e)
                raise CliException("Cannot open : {name}".format(name=filename_base + ".pub"))

            try:
                with open(filename_base + ".pri", "w") as pri:
                    pri.write(key_pair.private_key.decode())
            except (OSError, IOError) as e:
                print(e)
                raise CliException("Cannot open : {name}".format(name=filename_base + ".pri"))

            os.chmod(filename_base + ".pub", 0o400)
            os.chmod(filename_base + ".pri", 0o400)

            if "make_conf" in argv:
                import yaml
                conf_path = "config.yaml"
                dumped_conf = yaml.dump({
                    "peer": {
                        "address": "localhost",
                        "port": 50051
                    },
                    "account": {
                        "publicKeyPath": filename_base + ".pub",
                        "privateKeyPath": filename_base + ".pri",
                        "name": filename_base
                    }
                }, default_flow_style=False)

                try:
                    with open(conf_path, "w") as conf_file:
                        conf_file.write(dumped_conf)
                except (OSError, IOError) as e:
                    print(e)
                    raise CliException("Cannot open : {name}".format(name=conf_path))

                print("Generate {name}!".format(name=conf_path))
        except CliException as e:
            print(e)
            print("file error")
            return None
        else:
            if self.printInfo:
                print(
                    "key save publicKey -> {} privateKey -> {}".format(filename_base + ".pub", filename_base))
                print("key save publicKey:{} privateKey:{}".format(
                    key_pair.public_key[:5] + "..." + key_pair.public_key[-5:],
                    key_pair.private_key[:5] + "**...**" + key_pair.private_key[-5:],
                ))
            return None

    # =============================================

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
            amount=Amount(value=uint256(
                first=int(float(argv["amount"])),
                second=0,
                third=0,
                fourth=0,
            ), precision=0)
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
            main_pubkey=binascii.hexlify(key_pair.raw_public_key)
        ))

    def CreateAsset(self, argv):
        name = "CreateAsset"
        argv_info = self.commands[name]["option"]
        self.validate(argv_info, argv)
        self.printTransaction(name, argv_info, argv)
        return Command(create_asset=CreateAsset(
            asset_name=argv["asset_name"],
            domain_id=argv["domain_id"],
            precision=int(argv.get("precision", 0))
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
            amount=Amount(value=uint256(
                first=int(float(argv["amount"])),
                second=0,
                third=0,
                fourth=0,
            ), precision=0)
        ))
