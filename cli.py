#! /Users/mizuki/.pyenv/versions/3.5.0/envs/sandbox/bin/python

import sys
import readline
from cli import loader, completer, commands, network
BASE_NAME = "iroha-cli"

class ChiekuiCli:

    def __init__(self, commands):
        res = loader.load()

        self.location = res["location"]
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
            opt[name] = list(map(lambda name: name, self.commands[name]["option"].keys())) + ["-h"]


        opt["quit"] = []
        opt["bye"] = []
        readline.set_completer(completer.ChiekuiCliBufferCompleter(opt).complete)
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
                tx = self.commands[cmd]["function"](argv)
                network.sendTx(self.location, tx)

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
    import signal
    argv = sys.argv
    cmdList = commands.CommandList()
    print(
        "----------------\n"
        "Iroha-mizuki-cli\n"
        "----------------\n\n"
        "Current support commands"
    )
    for cmd in cmdList.commands.keys():
        print("  - {}".format(cmd))
    print("\n")

    c = ChiekuiCli(cmdList)
    if len(argv) == 2 and argv[-1] == "--interactive":
        signal.signal(signal.SIGINT, handler)
        c.run()
    elif len(argv) >= 2 and argv[-1] != "--interactive":
        res = c.exec_command(argv[1], argv[2:])
        if res:
            print(res)
    else:
        print("How to use")

if __name__ == "__main__":
    import logging

    LOG_FILENAME = '/tmp/{}_cli.log'.format(BASE_NAME)
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.DEBUG,
    )
    main()