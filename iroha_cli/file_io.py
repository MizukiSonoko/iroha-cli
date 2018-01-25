import os
import sys
from iroha_cli.exception import CliException

BASE_NAME = "iroha-mizuki-cli"

def save_keypair(filename_base, key_pair):
    try:
        if os.path.exists("{}/.irohac/{}.pub".format(os.environ['HOME'], filename_base)) or \
                os.path.exists("{}/.irohac/{}".format(os.environ['HOME'], filename_base)):
            raise CliException("Aleady key pair '{name}' exists!! ".format(name=filename_base))
        with open("{}/.irohac/{}.pub".format(os.environ['HOME'], filename_base), "w") as pub:
            pub.write(key_pair.public_key.decode())
        with open("{}/.irohac/{}".format(os.environ['HOME'], filename_base), "w") as pri:
            pri.write(key_pair.private_key.decode())
    except (OSError, IOError) as e:
        raise CliException("Cannot save : {name}".format(name=filename_base + ".pub"))
