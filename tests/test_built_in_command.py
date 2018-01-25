import unittest
import sys, os

sys.path.insert(0, os.path.abspath(__file__ + "/../../cli"))
sys.path.insert(0, os.path.abspath(__file__ + "/../../schema"))
from iroha_cli.built_in_commands import BuildInCommand
from iroha_cli.exception import CliException

class Sample:
    def __init__(self):
        self.sample_account_id_1 = "sample_account_id_1"
        self.sample_account_id_2 = "sample_account_id_2"
        self.sample_account_id_3 = "sample_account_id_3"

        self.sample_asset_id_1 = "sample_asset_id_1"
        self.sample_asset_id_2 = "sample_asset_id_2"
        self.sample_asset_id_3 = "sample_asset_id_3"

        self.sample_account_name = "sonoko_mizuki"

        self.sample_domain_id = "japan"
        self.sample_account_name = "mizuki"
        self.sample_keypair_path = "mizuki_key"


def deleteKeyIfExists(account_id):
    if os.path.exists("{}/.irohac/{}.pub".format(os.environ['HOME'], account_id)):
        os.remove("{}/.irohac/{}.pub".format(os.environ['HOME'], account_id))
    if os.path.exists("{}/.irohac/{}".format(os.environ['HOME'], account_id)):
        os.remove("{}/.irohac/{}".format(os.environ['HOME'], account_id))

class TestKeygen(unittest.TestCase):

    def setUp(self):
        self.commands = BuildInCommand().commands
        self.sample = Sample()

    def tearDown(self):
        base = self.sample.sample_account_name + "@" + self.sample.sample_domain_id
        base_key = self.sample.sample_keypair_path
        deleteKeyIfExists(base)
        deleteKeyIfExists(base_key)
        deleteKeyIfExists(self.sample.sample_account_name)

    def test_normal_with_account_name(self):
        self.commands["keygen"]["function"](
            {"account_id": self.sample.sample_account_name}
        )
        self.assertTrue(
            os.path.exists("{}/.irohac/{}.pub".format(os.environ['HOME'], self.sample.sample_account_name)) and \
            os.path.exists("{}/.irohac/{}".format(os.environ['HOME'], self.sample.sample_account_name))
        )

    def test_normal_with_keypair_name(self):
        self.commands["keygen"]["function"](
            {"account_id": self.sample.sample_account_name,
            "keypair_name": self.sample.sample_keypair_path}
        )
        self.assertTrue(
            os.path.exists("{}/.irohac/{}.pub".format(os.environ['HOME'], self.sample.sample_keypair_path)) and \
            os.path.exists("{}/.irohac/{}".format(os.environ['HOME'], self.sample.sample_keypair_path))
        )

    def test_error_no_account_name(self):
        try:
            self.commands["keygen"]["function"]({
                "keypair_name": self.sample.sample_keypair_path
            })
        except CliException:
            pass
        else:
            self.fail()
