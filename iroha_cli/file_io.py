import os
import sys
from iroha_cli.exception import CliException

BASE_NAME = "iroha-mizuki-cli"

def save_keypair(account_id, key_pair):
    base = '{}/.irohac'.format(os.environ['HOME'])
    os.makedirs('{}/.irohac'.format(os.environ['HOME']), exist_ok=True)
    try:
        if os.path.exists("{}/{}.pub".format(base, account_id)) or \
                os.path.exists("{}/{}".format(base, account_id)):
            raise CliException("Aleady key pair '{name}' exists!! ".format(name=account_id))

        with open("{}/{}.pub".format(base, account_id), "w") as pub:
            pub.write(key_pair.public_key.decode())
    except (OSError, IOError) as e:
        raise CliException("Cannot save : {name}".format(name="{}/{}.pub".format(base, account_id)))

    try:
        with open("{}/{}".format(base, account_id), "w") as pub:
            pub.write(key_pair.private_key.decode())
    except (OSError, IOError) as e:
        print(e)
        raise CliException("Cannot save : {name}".format(name="{}/{}".format(base, account_id)))
