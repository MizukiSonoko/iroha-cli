import os
import sys
from cli.exception import CliException

BASE_NAME = "iroha-mizuki-cli"

def load_config(file_path):
    if not file_path:
        return None

    import yaml
    try:
        with open(file_path, "r") as conf_file:
            data = yaml.load(conf_file, yaml.SafeLoader)

        account = data["account"]
        peer = data["peer"]

        try:
            with open(data["account"].get("publicKeyPath"), "r") as pubKeyFile:
                publicKey = pubKeyFile.read()
            with open(data["account"].get("privateKeyPath"), "r") as priKeyFile:
                privateKey = priKeyFile.read()
        except FileNotFoundError:
            raise CliException("File not found : {} or {} ".format(
                data["account"].get("publicKeyPath"), data["account"].get("privateKeyPath")))

        return {
            "name": account.get("name"),
            "publicKey": publicKey,
            "privateKey": privateKey,
            "address": peer.get("address"),
            "port": peer.get("port")
        }
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
            sys.exit(1)
        else:
            print("[{}] Something went wrong while parsing yaml file".format(BASE_NAME))
            sys.exit(1)
    except FileNotFoundError as e:
        print("[{}] Not found config.yml in {}".format(BASE_NAME, file_path))
        sys.exit(1)


def save_config(filename_base, data):
    import yaml
    conf_path = "config.yml"
    dumped_conf = yaml.dump(data, default_flow_style=False)

    try:
        with open(conf_path, "w") as conf_file:
            conf_file.write(dumped_conf)
    except (OSError, IOError) as e:
        print(e)
        raise CliException("Cannot open : {name}".format(name=conf_path))


def save_keypair(filename_base, key_pair):
    try:
        if os.path.exists(filename_base + ".pub") or os.path.exists(filename_base + ".pri") :
            raise CliException("Aleady key pair '{name}' exists!! ".format(name=filename_base))
        with open(filename_base + ".pub", "w") as pub:
            pub.write(key_pair.public_key.decode())
    except (OSError, IOError) as e:
        print(e)
        raise CliException("Cannot open : {name}".format(name=filename_base + ".pub"))

    try:
        with open(filename_base + ".pri", "w") as pub:
            pub.write(key_pair.private_key.decode())
    except (OSError, IOError) as e:
        print(e)
        raise CliException("Cannot open : {name}".format(name=filename_base + ".pri"))
