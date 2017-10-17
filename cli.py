#! /usr/bin/python

import sys
import readline
from cli import loader, completer, commands, network
from cli.exception import CliException
from cli.network import generateTransaction

BASE_NAME = "iroha-cli"


class ChiekuiCli:
    def __init__(self, commands, printInfo=False):
        try:
            res = loader.load(printInfo)
        except CliException as e:
            print(e.args[0])
            sys.exit(1)
        self.printInfo = False
        self.location = res["location"]
        self.name = res["name"]
        self.key_pair = {"publicKey": res["publicKey"], "privateKey": res["privateKey"]}
        self.source = res["source"]

        self.commands = commands.commands
        self.Type = commands.Type
        self.built_in = {
            "config": {
                "option": {},
                "function": self.config,
                "detail": " Print current state \n"
                          "   - name\n"
                          "   - publicKey\n"
                          "   - privateKey\n"
            }
        }

        commandNames = self.commands.keys()
        opt = {}
        for name in commandNames:
            opt[name] = list(map(lambda name: name, self.commands[name]["option"].keys())) + ["-h"]

        opt["quit"] = []
        opt["bye"] = []
        readline.set_completer(completer.ChiekuiCliBufferCompleter(opt).complete)
        readline.parse_and_bind('tab: complete')

    def config(self, argv):
        print(
            "\n"
            "  Config  \n"
            " =========\n"
        )
        print(" name      : {}".format(self.name))
        print(" publicKey : {}".format(self.key_pair["publicKey"]))
        print(" privateKey: {}".format(self.key_pair["privateKey"][:5] + "**...**" + self.key_pair["privateKey"][-5:]))
        print(" load from : {}".format(self.source))
        print(" targetPeer: {}".format(self.location))
        print("")
        return None

    def exec_command(self, cmd, argv):
        # Built in command is invoked in this
        if cmd in self.built_in:
            self.built_in[cmd]["function"]({})
            return

        # Command is invoked in this
        elif cmd in self.commands:
            if "-h" in argv or "--help" in argv:
                print(self.commands[cmd]["detail"])
                print("-----------")
                print("Arguments")
                for name, opt in self.commands[cmd]["option"].items():
                    print("- {:10s}: {:6}".format(name, opt["detail"]))

                return
            else:
                import getopt
                expected = list(map(lambda x: x + "=", self.commands[cmd]["option"]))

                try:
                    optlist, _ = getopt.getopt(argv, '', expected)
                except getopt.GetoptError:
                    print("Maybe option is wrong, I required {}".format(expected))
                    return

                new_argv = {}
                for opt in optlist:
                    for name in self.commands[cmd]["option"]:
                        if name == opt[0].split('--')[-1]:
                            new_argv[name] = opt[1]
                try:
                    command = self.commands[cmd]["function"](new_argv)
                    print("generated command: {}".format(command))
                    tx = generateTransaction(self.name, [command],self.key_pair)
                    if not network.sendTx(self.location, tx):
                        print(
                            "Transaction is not arrived...\n"
                            "Could you ckeck this => {}\n"
                                .format(self.location)
                        )
                except CliException as e:
                    print(e.message)
                    return
                return
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
        res = c.exec_command(argv[1], argv[2:])
        if res:
            print(res)
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
