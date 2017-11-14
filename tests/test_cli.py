import unittest
import sys, os

import cli

sys.path.insert(0, os.path.abspath(__file__ + "/../../cli"))
sys.path.insert(0, os.path.abspath(__file__ + "/../../schema"))
from iroha_cli import commands
from iroha_cli.exception import CliException

from io import StringIO

io = StringIO()
TARGET = "Iroha"


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


class TestBuildInCommands(unittest.TestCase):
    def setUp(self):
        self.commands = commands.CommandList().commands
        self.sample = Sample()
        self.skeleton_key = "skeleton"
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'keygen', '--make_conf','yes','--account_name', self.skeleton_key])
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

        os.remove(self.skeleton_key + ".pub")
        os.remove(self.skeleton_key + ".pri")
        if os.path.exists("config.yml"):
            os.remove("config.yml")

    def test_normal_without_argv(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli'])
        sys.stdout = sys.__stdout__
        self.assertTrue('{}-mizuki-cli'.format(TARGET) in io.getvalue())
        self.assertTrue('Current support commands' in io.getvalue())
        self.assertTrue('Sample keygen:' in io.getvalue())
        self.assertTrue('Sample Tx:' in io.getvalue())
        self.assertTrue('Sample Query:' in io.getvalue())

    def test_config_without_config_data(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'config'])
        sys.stdout = sys.__stdout__
        self.assertTrue('skeleton' in io.getvalue())

    def test_config(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'config', '--config','config.yml'])
        sys.stdout = sys.__stdout__
        self.assertTrue("name      : {}".format(self.skeleton_key) in io.getvalue())
        self.assertTrue("privateKey:" in io.getvalue())

    def test_key_gen(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'keygen', '--account_name', self.sample.sample_keypair_path])
        sys.stdout = sys.__stdout__
        self.assertTrue(os.path.exists(self.sample.sample_keypair_path + ".pub") and os.path.exists(
            self.sample.sample_keypair_path + ".pri"))

    # It's fake... I want make_conf option require config name....
    def test_key_gen_with_config(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'keygen', '--make_conf','yes','--account_name', self.sample.sample_keypair_path])
        sys.stdout = sys.__stdout__
        self.assertTrue(os.path.exists(self.sample.sample_keypair_path + ".pub") and os.path.exists(
            self.sample.sample_keypair_path + ".pri"))
        self.assertTrue(os.path.exists('config.yml'))

    def test_create_asset(self):
        sys.stdout = io
        cli.main.main(['iroha-ya-cli', 'tx', 'CreateAsset', '--config','config.yml', '--domain_id', self.sample.sample_domain_id, '--asset_name', self.sample.sample_asset_id_1])
        sys.stdout = sys.__stdout__

        # I want mock grpc server....
        self.assertTrue('== Grpc happens error ==' in io.getvalue())



