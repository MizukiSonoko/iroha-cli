#! /usr/bin/python

import sys
import argparse

from cli.built_in_commands import BuildInCommand
from cli.commands import CommandList
from cli.crypto import KeyPair
from cli.network import generateTransaction, sendTx, generateQuery, sendQuery
import cli.file_io as file_io
from cli.query import QueryList

BASE_NAME = "iroha-cli"
TARGET = "iroha"


class ChiekuiCli:
    class Context:
        def __init__(self, filepath):
            conf = file_io.load_config(filepath)
            if not conf:
                return
            self.name, \
            self.public_key, \
            self.private_key, \
            address, port = conf

            self.location = "{}:{}".format(address, str(port))
            self.key_pair = KeyPair(
                raw_private_key=KeyPair.decode(self.private_key),
                raw_public_key=KeyPair.decode(self.public_key))

    def __init__(self):
        self.tx_commands = CommandList().commands
        self.queries = QueryList().queries
        self.built_in_commands = BuildInCommand().commands
        self.context = None

        # ================================
        #              Parser
        # ================================
        self.parser = argparse.ArgumentParser(description='Cli of {}'.format(TARGET))
        _sub_parser = self.parser.add_subparsers()

        # parse: transaction
        parse_tx = _sub_parser.add_parser("tx")
        sup_parser_tx = parse_tx.add_subparsers()
        for cmd in self.tx_commands:
            _parser = sup_parser_tx.add_parser(cmd, help='{} help'.format(cmd))
            for name, val in self.tx_commands[cmd]['option'].items():
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],
                                     help=val["detail"])
            _parser.add_argument("--config", type=str, required=False, help="config.yml's path")

        # parse: query
        parse_query = _sub_parser.add_parser("query")
        sup_parser_query = parse_query.add_subparsers()
        for qry in self.queries:
            _parser = sup_parser_query.add_parser(qry, help='{} help'.format(qry))
            for name, val in self.queries[qry]['option'].items():
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],
                                     help=val["detail"])
            _parser.add_argument("--config", type=str, required=False, help="config.yml's path")

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
            "Sample:\n\n"
            "  > python ./cli.py CreateAsset --domain_id japan --precision 0 --asset_name yen\n"
        )
        sys.exit(0)

    def exec_tx(self, cmd, argv):
        file_io.load(argv.config)
        command = self.tx_commands[cmd]["function"](vars(argv))
        if command:
            tx = generateTransaction(self.context.name, [command], self.context.key_pair)
            if not sendTx(self.context.location, tx):
                print(
                    "Transaction is not arrived...\n"
                    "Could you ckeck this => {}\n".format(self.context.location)
                )
                return False
        else:
            print("Err")

    def exec_query(self, qry, argv):
        file_io.load(argv.config)
        qry = self.queries[qry]["function"](vars(argv))
        if qry:
            query = generateQuery(self.context.name, qry, self.context.key_pair)
            if not sendQuery(self.context.location, query):
                print(
                    "Transaction is not arrived...\n"
                    "Could you ckeck this => {}\n".format(self.context.location)
                )
                return False
        else:
            print("Err")

    def exec(self, argv):
        parsed_argv = self.parser.parse_args(argv[1:])
        if len(argv) < 3:
            self.print_introduction()
        self.context = self.Context(vars(parsed_argv).get('config'))
        if argv[1] == 'tx':
            self.exec_tx(argv[2], parsed_argv)
        elif argv[1] == 'query':
            self.exec_query(argv[2], parsed_argv)

        if argv[2] in self.built_in_commands:
            self.built_in_commands[argv[2]]["functions"](argv)


def main():
    cli = ChiekuiCli()
    cli.exec(sys.argv)
    return


if __name__ == "__main__":
    main()
