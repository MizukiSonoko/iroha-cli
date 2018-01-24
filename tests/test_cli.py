import unittest
import sys, os

import iroha_cli

sys.path.insert(0, os.path.abspath(__file__ + "/../../cli"))
sys.path.insert(0, os.path.abspath(__file__ + "/../../schema"))
from iroha_cli import commands
from iroha_cli.exception import CliException
from io import StringIO

io = StringIO()
TARGET = "Iroha"

class Sample:
    def __init__(self):
        self.hostname = "localhost"

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


class TestBuildInCommands(unittest.TestCase):
    def setUp(self):
        self.commands = commands.CommandList().commands
        self.sample = Sample()
        self.skeleton_key = "skeleton"
        sys.stdout = io
        sys.stdout = sys.__stdout__

    def tearDown(self):
        base = self.sample.sample_account_name
        base_key = self.sample.sample_keypair_path
        if os.path.exists(base + ".pub"):
            os.remove(base + ".pub")
            os.remove(base + ".pri")
        if os.path.exists(base_key + ".pub"):
            os.remove(base_key + ".pub")
            os.remove(base_key + ".pri")

    def test_normal_without_argv(self):
        sys.stdout = io
        iroha_cli.main.main(['irohac'])
        sys.stdout = sys.__stdout__
        self.assertTrue('{}-mizuki-cli'.format(TARGET) in io.getvalue())
        self.assertTrue('Current support commands' in io.getvalue())
        self.assertTrue('Sample keygen:' in io.getvalue())
        self.assertTrue('Sample Tx:' in io.getvalue())
        self.assertTrue('Sample Query:' in io.getvalue())
