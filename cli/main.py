#! /usr/bin/python

import sys
import readline

from cli.exception import CliException
from cli.network import generateTransaction, sendTx
import cli.commands as commands
import cli.loader as loader
import cli.completer as completer

BASE_NAME = "iroha-cli"


class ChiekuiCli:
    def __init__(self, commands, printInfo=False):

        self.printInfo = False

        self.commands = commands.commands
        self.Type = commands.Type
        commandNames = self.commands.keys()
        opt = {}
        for name in commandNames:
            opt[name] = list(map(lambda name: name, self.commands[name]["option"].keys())) + ["-h"]

        opt["quit"] = []
        opt["bye"] = []
        readline.set_completer(completer.ChiekuiCliBufferCompleter(opt).complete)
        readline.parse_and_bind('tab: complete')


    def exec_command(self, cmd, argv):
        if cmd in self.commands:
            if "-h" in argv or "--help" in argv:
                print(self.commands[cmd]["detail"])
                print("-----------")
                print("Arguments")
                for name, opt in self.commands[cmd]["option"].items():
                    print("- {:10s}: {:6}".format(name, opt["detail"]))
                return True
            else:
                import getopt
                # I want to make it more simple....
                expected = list(map(lambda x: x[0] + "=",
                                list(filter(lambda o: o[1]['type'] != self.Type.NONE,self.commands[cmd]["option"].items()))
                            ))
                expected.extend(list(map(lambda x: x[0],
                                list(filter(lambda o: o[1]['type'] == self.Type.NONE,self.commands[cmd]["option"].items()))
                )))
                expected.append('config=')
                try:
                    optlist, _ = getopt.getopt(argv, '', expected)
                except getopt.GetoptError as e:
                    print("Maybe option is wrong, I required {}".format(expected))
                    return False

                new_argv = {}
                file_path = None
                for opt in optlist:
                    for name in self.commands[cmd]["option"]:
                        if name == opt[0].split('--')[-1]:
                            new_argv[name] = opt[1]
                    if opt[0] == "--config":
                        file_path = opt[1]
                try:
                    res = loader.load(file_path, self.printInfo)
                    self.withoutConf = False
                    self.location = res["location"]
                    self.name = res["name"]
                    self.key_pair = {"publicKey": res["publicKey"], "privateKey": res["privateKey"]}
                except CliException as e:
                    print(e.args[0])
                    print("Without config mode")
                    self.withoutConf = True

                try:
                    if cmd == "config":
                        if self.withoutConf:
                            print("you can show config under loading config, but not loaded config.yml...".format(cmd))
                            return False
                        self.commands[cmd]["function"](
                            {"name":self.name,
                             "publicKey":self.key_pair["publicKey"],
                             "privateKey":self.key_pair["privateKey"],
                             "location":self.location
                            }
                        )
                        return True

                    command = self.commands[cmd]["function"](new_argv)
                    if command:
                        print("generated command: {}".format(command))
                        if self.withoutConf:
                            print("{} is successful, but not loaded config.yml...".format(cmd))
                            return 0
                        tx = generateTransaction(self.name, [command],self.key_pair)
                        if not sendTx(self.location, tx):
                            print(
                                "Transaction is not arrived...\n"
                                "Could you ckeck this => {}\n"
                                    .format(self.location)
                            )
                            return False
                except CliException as e:
                    print(e.message)
                    return False
                return True

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


def main():
    printInfo = False
    import signal
    argv = sys.argv
    cmdList = commands.CommandList()
    c = ChiekuiCli(cmdList, printInfo)
    if len(argv) == 2 and argv[-1] == "--interactive":
        signal.signal(signal.SIGINT, handler)
        c.run()
    elif len(argv) >= 2 and argv[-1] != "--interactive":
        if c.exec_command(argv[1], argv[2:]):
            print("success full")
            sys.exit(0)
        else:
            print("failed")
            sys.exit(1)
    else:
        print(
            "----------------\n"
            "Iroha-mizuki-cli\n"
            "----------------\n\n"
            "Current support commands"
        )
        for cmd in cmdList.commands.keys():
            print("  - {}".format(cmd))

        print(
            "\n"
            "Sample:\n\n"
            "  > python ./cli.py CreateAsset --domain_id japan --precision 0 --asset_name yen"
        )
        print("\n")


if __name__ == "__main__":
    import logging

    LOG_FILENAME = '/tmp/{}_cli.log'.format(BASE_NAME)
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.DEBUG,
    )
    main()
