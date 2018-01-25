
from iroha_cli.exception import CliException
from queries_pb2 import Query, GetAccount, GetSignatories, GetAccountTransactions, GetAccountAssetTransactions, \
    GetAccountAssets, GetAssetInfo


BASE_NAME = "iroha-mizuki-cli"


class QueryList:
    """
       GetAccount get_account = 3;
       GetSignatories get_account_signatories = 4;
       GetAccountTransactions get_account_transactions = 5;
       GetAccountAssetTransactions get_account_asset_transactions = 6;
       GetAccountAssets get_account_assets = 7;
       GetRoles get_roles = 8;
       GetAssetInfo get_asset_info = 9;
       GetRolePermissions get_role_permissions = 10;
    """

    def __init__(self, printInfo=False):
        self.printInfo = printInfo
        self.queries = {
            "GetAccount": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    }
                },
                "function": self.GetAccount,
                "detail": "get account information"
            },
            "GetSignatories": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    }
                },
                "function": self.GetSignatories,
                "detail": "get signatories of account"
            },
            "GetAccountTransactions": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    }
                },
                "function": self.GetAccountTransactions,
                "detail": "get transactions of account"
            },
            "GetAssetInfo": {
                "option": {
                    "asset_id": {
                        "type": str,
                        "detail": "target's asset id like mizuki@domain",
                        "required": True
                    }
                },
                "function": self.GetAssetInfo,
                "detail": "get information of asset"
            },
            "GetAccountAssetTransactions": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    },
                    "asset_id": {
                        "type": str,
                        "detail": "target's asset id like yen",
                        "required": True
                    }
                },
                "function": self.GetAccountAssetTransactions,
                "detail": "Get transction list of account managed asset"
            },
            "GetAccountAssets": {
                "option": {
                    "account_id": {
                        "type": str,
                        "detail": "target's account id like mizuki@domain",
                        "required": True
                    },
                    "asset_id": {
                        "type": str,
                        "detail": "target's asset id like yen",
                        "required": True
                    }
                },
                "function": self.GetAccountAssets,
                "detail": "get assets account has"
            }
        }


    def validate(self, expected, argv):
        for item in expected.items():
            if item[1]["required"] and not item[0] in argv:
                raise CliException("{} is required".format(item[0]))
            if item[0] in argv:
                if type(argv[item[0]]) != item[1]["type"]:
                    raise CliException("{} is {}".format(item[0],str(item[1]["type"])))

    def GetAccount(self, argv):
        name = "GetAccount"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_account=GetAccount(account_id=argv["account_id"]))

    def GetSignatories(self, argv):
        name = "GetSignatories"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_account_signatories=GetSignatories(account_id=argv["account_id"]))

    def GetAccountAssets(self, argv):
        name = "GetAccountAssets"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_account_assets=GetAccountAssets(
            account_id=argv["account_id"],
            asset_id=argv["asset_id"]))

    def GetAccountTransactions(self, argv):
        name = "GetAccountTransactions"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_account_transactions=GetAccountTransactions(account_id=argv["account_id"]))

    def GetAccountAssetTransactions(self, argv):
        name = "GetAccountAssetTransactions"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_account_asset_transactions=GetAccountAssetTransactions(
            account_id=argv["account_id"],
            asset_id=argv["asset_id"]))

    def GetAssetInfo(self, argv):
        name = "GetAssetInfo"
        argv_info = self.queries[name]["option"]
        self.validate(argv_info, argv)
        return dict(get_asset_info=GetAssetInfo(
            asset_id=argv["asset_id"]))

