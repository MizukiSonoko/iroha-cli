import sys
from cli.exception import CliException

BASE_NAME = "iroha-mizuki-cli"

def load(printInfo = False):
    import yaml
    try:
        data = yaml.load(open("config.yml", "r"), yaml.SafeLoader)
        if not "account" in data:
            raise CliException("Require account dict in confid.yml")

        if not "peer" in data:
            raise CliException("Require peer dict in confid.yml")

        name = data["account"].get("name")
        publicKeyPath = data["account"].get("publicKeyPath")
        privateKeyPath = data["account"].get("privateKeyPath")
        if not name:
            raise CliException("Require name in account in confid.yml")
        if not publicKeyPath:
            raise CliException("Require publicKey in account in confid.yml")

        try:
            publicKey = open( publicKeyPath, "r").read()
            privateKey = open( privateKeyPath, "r").read()
        except FileNotFoundError:
            raise CliException("File not found : {} or {} ".format(publicKeyPath ,privateKeyPath))

        if not privateKeyPath:
            raise CliException("Require privateKey in account in confid.yml")

        address = data["peer"].get("address")
        port = data["peer"].get("port")
        if not address:
            raise CliException("Require address in peer in confid.yml")
        if not port:
            raise CliException("Require port(int) in peer in confid.yml")

        if printInfo:
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
            sys.exit(1)
        else:
            print("[{}] Something went wrong while parsing yaml file".format(BASE_NAME))
            sys.exit(1)
    except FileNotFoundError as e:
        print("[{}] Could you make config.yml in current directory".format(BASE_NAME))
        sys.exit(1)
    else:
        return {
            "name": name,
            "publicKey": publicKey,
            "privateKey": privateKey,
            "location": address +":" + str(port)
        }
