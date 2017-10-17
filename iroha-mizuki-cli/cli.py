#! /Users/mizuki/.pyenv/versions/3.5.0/envs/sandbox/bin/python
import readline
import logging

import re
import grpc
from schema.endpoint_pb2_grpc import TerminalServiceStub, KusariTerminalServiceStub
from schema.endpoint_pb2 import Request, Command, Transaction, Block

from concurrent.futures import ThreadPoolExecutor, as_completed

import sys
import yaml
import datetime

BASE_NAME = "iroha-cli"

LOG_FILENAME = '/tmp/{}_cli.log'.format(BASE_NAME)
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)


class ChiekuiCliBufferCompleter(object):
    def __init__(self, commands):
        self.commands = commands
        self.current_candidates = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            if not words:
                self.current_candidates = sorted(self.commands.keys())
            else:
                try:
                    if begin == 0:
                        candidates = self.commands.keys()
                    else:
                        first = words[0]
                        candidates = self.commands[first]

                    if being_completed:
                        self.current_candidates = [
                            w for w in candidates if w.startswith(being_completed)
                        ]
                    else:
                        self.current_candidates = candidates

                    nw = []
                    for w in words:
                        try:
                            nw.append(w.split('=')[0] + '=')
                        except:
                            pass
                    self.current_candidates = list(filter(lambda c: not c in nw, self.current_candidates))

                except (KeyError, IndexError) as err:
                    logging.error('completion error: %s', err)
                    self.current_candidates = []

        try:
            response = self.current_candidates[state]
        except IndexError:
            response = None
        return response


def load():
    import yaml
    import os
    try:
        data = yaml.load(open("config.yml", "r"), yaml.SafeLoader)
        if not "account" in data:
            print("[{}] Require account dict".format(BASE_NAME))
            sys.exit(1)
        name = data["account"].get("name")
        publicKey = data["account"].get("publicKey")
        privateKey = data["account"].get("privateKey")
        logging.info("[{}] use config.yml data".format(BASE_NAME))
        if not name:
            print("[{}]  Require name in account".format(BASE_NAME))
            raise
        if not publicKey:
            print("[{}]  Require publicKey in account".format(BASE_NAME))
            raise
        if not privateKey:
            print("[{}]  Require publicKey in account".format(BASE_NAME))
            raise
    except yaml.YAMLError as exc:
        print("[{}] Error while parsing YAML file:".format(BASE_NAME))
        if hasattr(exc, 'problem_mark'):
            if exc.context is not None:
                print("""
                [{}] 
                  parser says
                  -----------
                  {}
                  {} {}
                  Could you correct it?
                """.format(
                    BASE_NAME,
                    exc.problem_mark,
                    exc.problem,
                    exc.context
                ))
            else:
                print("""
                [{}] 
                  parser says
                  -----------
                  {}
                  {}
                  Could you correct it?
                """.format(
                    BASE_NAME,
                    exc.problem_mark,
                    exc.problem
                ))
        else:
            print("[{}] Something went wrong while parsing yaml file".format(BASE_NAME))
        return
    except FileNotFoundError as e:
        pass
    except:
        print("[{}] config.yml is not enough. load environment".format(BASE_NAME))
    else:
        return {
            "name": name,
            "publicKey": publicKey,
            "privateKey": privateKey,
            "source": "config.yml"
        }

    name = os.getenv("CHIEKUI_CLI_NAME")
    publicKey = os.getenv("CHIEKUI_CLI_PUBLIC_KEY")
    privateKey = os.getenv("CHIEKUI_CLI_PRIVATE_KEY")

    if not name:
        print("[{}] Required name in environment 'CHIEKUI_CLI_NAME' ".format(BASE_NAME))
        sys.exit(1)

    if publicKey and privateKey:
        return {
            "name": name,
            "publicKey": publicKey,
            "privateKey": privateKey,
            "source": "environment"
        }

    pubKeyFile = os.getenv("CHIEKUI_CLI_PUBLIC_KEY_PATH")
    priKeyFile = os.getenv("CHIEKUI_CLI_PRIVATE_KEY_PATH")

    if not priKeyFile or not pubKeyFile:
        sys.exit(1)

    try:
        publicKey = open(pubKeyFile, 'r').read()
        privateKey = open(priKeyFile, 'r').read()
    except IOError:
        print(
            "[{}] Unfortunately, I can not load\n {} in CHIEKUI_CLI_PUBLIC_KEY or {} in CHIEKUI_CLI_PRIVATE_KEY_PATH".format(
                BASE_NAME, pubKeyFile, priKeyFile
            ))
        sys.exit(1)

    if not publicKey or not privateKey:
        print("[{}] Unfortunately, I can not load enough information.... so I can not boot".format(
            BASE_NAME
        ))
        sys.exit(1)
    return {
        "name": name,
        "publicKey": publicKey,
        "privateKey": privateKey,
        "source": "environment and file"
    }

class CommandList:

    def __init__(self):
        self.commands = {
            "config": {
                "option": [],
                "function": self.config,
                "detail": "\n Config \n"
                          "-----------\n"
                          " Print current state \n"
                          "   - name\n"
                          "   - publicKey\n"
                          "   - privateKey\n"
            },
            "add": {
                "option": ["account_id=", "asset_id=", "amount="],
                "function": self.add,
                "detail": "\n Add \n"
                          "-----------\n"
                          " Add asset's quantity \n"
                          "   - account_id (req): target's account id like mizuki\n"
                          "   - asset_id   (req): target's asset id like japan/yen \n"
                          "   - amount     (req):   added asset's quantity (int)\n"
            },
            "transfer": {
                "option": ["from_id=", "to_id=", "asset_id=", "amount="],
                "function": self.transfer,
                "detail": "\n Transfer \n"
                          "-----------\n"
                          " Transfer asset's quantity \n"
                          "   - from_id  (req): current asset owner account id like mizuki\n"
                          "   - to_id    (req):   next asset owner account id like iori\n"
                          "   - asset_id (req): target's asset id like japan/yen \n"
                          "   - amount   (req):   how much transfer asset's quantity (int)\n"
            },
            "createAccount": {
                "option": ["name=", "domain_id=", "keypair_path="],
                "function": self.createAccount,
                "detail": "\n createAccount \n"
                          "-----------\n"
                          " create Account\n"
                          "   - name         (req): account name like mizuki\n"
                          "   - domain_id    (req):  new account will be in this domain like iori\n"
                          "   - keypair_path (opt): if there is key pair, please path. but if not keypair, auto generated and will be stored in config.yml\n"
            },
        }

    def config(self, argv):
        print(
            "\n"
            "  Config  \n"
            " =========\n"
        )
        print(" name      : {}".format(self.name))
        print(" publicKey : {}".format(self.publicKey))
        print(" privateKey: {}".format(self.privateKey[:5] + "**...**" + self.privateKey[-5:]))
        print(" load from : {}".format(self.source))
        print("")
        return None

    def add(self, argv):
        return "No implement this command Add"

    def transfer(self, argv):
        return "No implement this command Transfer"

    def createAsset(self, argv):
        return "No implement this command createAsset"

    def createAccount(self, argv):
        return "No implement this command createAccount"

    def createDomain(self, argv):
        return "No implement this command createDomain"

class ChiekuiCli:
    def __init__(self, commands):
        res = load()
        self.name = res["name"]
        self.publicKey = res["publicKey"]
        self.privateKey = res["privateKey"]
        self.source = res["source"]

        self.commands = commands.commands
        self.built_in = {
            "push": {
                "option": [],
                "function": self.push,
                "detail": "\n Push (built in) \n"
                          "-----------\n"
                          " Enter stack shell \n"
                          " 1) Stack command. \n"
                          " 2) 'pop' whenever you want\n"
            },
            "pop": {
                "option": [],
                "function": self.pop,
                "detail": "\n Pop (built in) \n"
                          "-----------\n"
                          " Outer stack shell \n"
                          " 1) Stack command. \n"
                          " 2) 'pop' whenever you want\n"
            }

        }

        commandNames = self.commands.keys()
        opt = {}
        for name in commandNames:
            opt[name] = self.commands[name]["option"] + ["-h"]

        opt["quit"] = []
        opt["bye"] = []
        readline.set_completer(ChiekuiCliBufferCompleter(opt).complete)

        readline.parse_and_bind('tab: complete')

    def push(self):
        pass

    def pop(self):
        pass

    def exec_command(self, cmd, argv):
        if cmd in self.commands:
            if "-h" in argv or "--help" in argv:
                print(self.commands[cmd]["detail"])
            else:
                return self.commands[cmd]["function"](argv)

        if cmd.lower() in ["quit", "bye", "finish", "exit", "end"]:
            print("Thanks bye! (^o^) ")
            sys.exit(0)
        return "command not found: {}".format(cmd)

    def run(self):
        line = ''
        while line != 'stop':
            line = None
            try:
                line = input('{}@default [{}] >> '.format(self.name, BASE_NAME))
            except EOFError:
                print("\nThanks bye! (^o^) ")
                sys.exit(0)
            if line:
                argv = line.split()[1:]
                res = self.exec_command(line.split()[0], line.split()[1:])
                if res:
                    print(res)


def handler(signal, frame):
    print("\nThanks bye! (^o^) ")
    sys.exit(0)


if __name__ == "__main__":
    import signal

    argv = sys.argv
    cmdList = CommandList()
    c = ChiekuiCli(cmdList)
    if len(argv) == 2 and argv[-1] == "--interactive":
        signal.signal(signal.SIGINT, handler)
        c.run()
    elif len(argv) >= 2:
        res = c.exec_command(argv[1],argv[2:])
        if res:
            print(res)
    else:
        print("How to use")