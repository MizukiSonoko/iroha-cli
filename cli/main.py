#! /usr/bin/python

import sys
import argparse

from cli.built_in_commands import BuildInCommand
from cli.commands import CommandList
from cli.crypto import KeyPair
from cli.exception import CliException
from cli.network import generateTransaction, sendTx, generateQuery, sendQuery
import cli.file_io as file_io
from cli.query import QueryList

BASE_NAME = "iroha-cli"
TARGET = "iroha"


class Context:
    name = None
    public_key = None
    private_key = None
    location = None
    key_pair = None

    def __init__(self, filepath):
        try:
            conf = file_io.load_config(filepath)
        except:
            self.loaded = False
            return
        self.loaded = True
        self.name = conf.get('name')
        self.public_key = conf.get('publicKey')
        self.private_key = conf.get('privateKey')
        address = conf.get('address')
        port = conf.get('port')

        self.location = "{}:{}".format(address, str(port))
        self.key_pair = KeyPair(
            raw_private_key=KeyPair.decode(self.private_key),
            raw_public_key=KeyPair.decode(self.public_key))


class ChiekuiCli:
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
                _parser.add_argument("--{}".format(name), type=val["type"], required=val["required"],help=val["detail"])
            _parser.add_argument("--config", type=str, required=False,help="config.yml's path")

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
            if not self.context.loaded:
                print("Config data is not loaded! to send tx require config")
                return False
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
        qry = self.queries[qry]["function"](vars(argv))
        if qry:
            if not self.context.loaded:
                print("Config data is not loaded! to send tx require config")
                return False
            query = generateQuery(self.context.name, qry, self.context.key_pair)

            try:
                res = sendQuery(self.context.location, query)
                print(res)
            except CliException as e:
                print(e.message)
        else:
            print("Err")

    def exec(self, argv):
        parsed_argv = self.parser.parse_args(argv[1:])
        if len(argv) < 2:
            self.print_introduction()
            return

        self.context = Context(vars(parsed_argv).get('config'))
        #
        # if not set --config. load current directory's config.yml
        #
        if not self.context.loaded:
            self.context = Context('config.yml')

        if argv[1] == 'tx':
            self.exec_tx(argv[2], parsed_argv)
        elif argv[1] == 'query':
            self.exec_query(argv[2], parsed_argv)

        if argv[1] in self.built_in_commands:
            self.built_in_commands[argv[1]]["function"]( vars(parsed_argv), self.context)
        

def main(argv=sys.argv):
    cli = ChiekuiCli()
    cli.exec(argv)
    return

if __name__ == "__main__":
    main()
