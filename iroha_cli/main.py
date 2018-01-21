#! /usr/bin/python
import os
import sys
import argparse

from iroha_cli.built_in_commands import BuildInCommand
from iroha_cli.commands import CommandList
from iroha_cli.crypto import KeyPair
from iroha_cli.exception import CliException
from iroha_cli.network import generateTransaction, sendTx, generateQuery, sendQuery, waitTransaciton
from iroha_cli.query import QueryList

BASE_NAME = "iroha-cli"
TARGET = "iroha"


class ChiekuiCli:
    def __init__(self):
        self.tx_commands = CommandList().commands
        self.queries = QueryList().queries
        self.built_in_commands = BuildInCommand().commands

        self.account_id = None
        self.hostname = None

        # ================================
        #              Parser
        # ================================
        self.action_parser = argparse.ArgumentParser(description='Cli of {}'.format(TARGET))
        self.meta_parser = argparse.ArgumentParser(description='Cli of {}'.format(TARGET))

        self.meta_parser.add_argument("--hostname", type=str, required=True,
                                      help="Target hostname")
        self.meta_parser.add_argument("--account_id", type=str, required=True,
                                      help="My account_id")

        _sub_parser = self.action_parser.add_subparsers()

        # parse: transaction
        for cmd in self.tx_commands:
            _parser = _sub_parser.add_parser(cmd, help='{} help'.format(cmd))
            for name, val in self.tx_commands[cmd]['option'].items():
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],
                                     help=val["detail"])

        # parse: query
        for qry in self.queries:
            _parser = _sub_parser.add_parser(qry, help='{} help'.format(qry))
            for name, val in self.queries[qry]['option'].items():
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],
                                     help=val["detail"])

        # parse: built in command
        for cmd_name, cmd_val in self.built_in_commands.items():
            _parser = _sub_parser.add_parser(cmd_name, help='{} help'.format(cmd_name))
            for name, val in self.built_in_commands[cmd_name]['option'].items():
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],
                                     help=val["detail"])

    def print_introduction(self):
        print(
            "----------------\n"
            "Iroha-mizuki-cli\n"
            "----------------\n\n"
            "Current support commands"
        )
        for cmd in self.tx_commands.keys():
            print("  - {}".format(cmd))
        print(
            "\n"
            "Sample keygen:\n\n"
            "  > iroha-ya-cli keygen  --account_name mizuki --make_conf yes\n\n"
            "Sample Tx:\n\n"
            "  > iroha-ya-cli tx CreateAccount --account_name mizuki --domain_id japan --config config.yml\n"
            "Sample Query:\n\n"
            "  > iroha-ya-cli query GetAccount --account_id mizuki@japan --config my_config.yml\n"
        )

    def exec_tx(self, cmd, argv):
        command = self.tx_commands[cmd]["function"](vars(argv))
        if command:

            if not self.key_pair:
                print("Key pair is not loaded! to send tx require key pair")
                return -1

            tx, tx_hash = generateTransaction(self.account_id, [command], self.key_pair)
            if not sendTx(self.hostname, tx):
                print(
                    "Transaction is not arrived...\n"
                    "Could you ckeck this => {}\n".format(self.hostname)
                )
                return -1
            try:
                waitTransaciton(self.hostname, tx_hash)
            except Exception as e:
                print(e.args)
                print(
                    "failed to executed the transaction \n"
                    "error => {}\n".format(e)
                )
                return -1

        else:
            print("Err")
            return -1

    def exec_query(self, qry, argv):
        qry = self.queries[qry]["function"](vars(argv))
        if qry:
            query = generateQuery(self.account_id, qry, self.key_pair)
            try:
                res = sendQuery(self.hostname, query)
                print(res)
            except CliException as e:
                print(e)
                return -1
        else:
            print("Err")
            return -1

    def exec(self, argv):

        if len(argv) < 2:
            return self.print_introduction()

        meta_parsed_argv = self.meta_parser.parse_args(argv[1:3])
        parsed_argv = self.action_parser.parse_args(argv[3:])

        self.account_id = vars(meta_parsed_argv)["account_id"]
        self.hostname = vars(meta_parsed_argv)["hostname"]

        # ==========
        # Load key pair
        # ToDo: separate from this
        self.key_pair = None
        try:
            with open("{}/.irohac/{}.pub".format(os.environ['HOME'],self.account_id), "r") as pubKeyFile:
                publicKey = pubKeyFile.read()
            with open("{}/.irohac/{}".format(os.environ['HOME'],self.hostname), "r") as priKeyFile:
                privateKey = priKeyFile.read()
            self.key_pair = KeyPair(
                raw_private_key=KeyPair.decode(publicKey),
                raw_public_key=KeyPair.decode(privateKey)
            )
        except FileNotFoundError:
            raise CliException("File not found : {}/.irohac/{}".format(os.environ['HOME'],self.hostname))

        if argv[3] in self.tx_commands:
            return self.exec_tx(argv[3], parsed_argv)

        elif argv[3] in self.queries:
            return self.exec_query(argv[3], parsed_argv)

        if argv[1] in self.built_in_commands:
            return self.built_in_commands[argv[1]]["function"](vars(parsed_argv))


def main(argv=sys.argv):
    cli = ChiekuiCli()
    return cli.exec(argv)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code if not exit_code is None else 0)
