

import yaml
import sys
BASE_NAME = "iroha-mizuki-cli"

def load():
    import yaml
    import os
    try:
        data = yaml.load(open("config.yml", "r"), yaml.SafeLoader)
        if not "account" in data:
            print("[{}] Require account dict".format(BASE_NAME))
            sys.exit(1)

        if not "peer" in data:
            print("[{}] Require peer dict".format(BASE_NAME))
            sys.exit(1)

        name = data["account"].get("name")
        publicKey = data["account"].get("publicKey")
        privateKey = data["account"].get("privateKey")
        if not name:
            print("[{}]  Require name in account".format(BASE_NAME))
            raise
        if not publicKey:
            print("[{}]  Require publicKey in account".format(BASE_NAME))
            raise
        if not privateKey:
            print("[{}]  Require publicKey in account".format(BASE_NAME))
            raise

        address = data["peer"].get("address")
        port = data["peer"].get("port")
        if not address:
            print("[{}]  Require address in peer".format(BASE_NAME))
            raise
        if not port:
            print("[{}]  Require port in peer".format(BASE_NAME))
            raise

        print("[{}] use config.yml data".format(BASE_NAME))
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
    except FileNotFoundError as e:
        print("[{}] I recommend to make config.yml in current directory".format(BASE_NAME))
        return
    else:
        return {
            "name": name,
            "publicKey": publicKey,
            "privateKey": privateKey,
            "source": "config.yml",
            "location": address + str(port)
        }

    #------
    # This code will be deleted...
    #------
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


    try:
        pubKeyFile = os.getenv("CHIEKUI_CLI_PUBLIC_KEY_PATH")
        priKeyFile = os.getenv("CHIEKUI_CLI_PRIVATE_KEY_PATH")

        publicKey = open(pubKeyFile, 'r').read()
        privateKey = open(priKeyFile, 'r').read()
    except IOError:
        print(
            "[{}] Unfortunately, I can not load\n {} in CHIEKUI_CLI_PUBLIC_KEY or {} in CHIEKUI_CLI_PRIVATE_KEY_PATH".format(
                BASE_NAME, pubKeyFile, priKeyFile
            ))
        sys.exit(1)
    except TypeError:
        print(
            "[{}] Unfortunately, Not set CHIEKUI_CLI_PUBLIC_KEY or CHIEKUI_CLI_PRIVATE_KEY_PATH".format(
                BASE_NAME
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
