import os
from enum import Enum

import binascii
from cli import crypto
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

    def keygen(self, context, argv):
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

