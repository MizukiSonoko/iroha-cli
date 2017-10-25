import unittest
import sys, os
import cli
from io import StringIO
io = StringIO()


class TestBuildInCommands(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_normal(self):
        sys.stdout = io
        # $ iroha-ya-cli
        cli.main.main(['iroha-ya-cli'])
        sys.stdout = sys.__stdout__
        self.assertTrue('Iroha-mizuki-cli' in io.getvalue())

    def test_config(self):
        sys.stdout = io
        # $ iroha-ya-cli config
        cli.main.main(['iroha-ya-cli','config'])
        sys.stdout = sys.__stdout__
        self.assertTrue('Iroha-mizuki-cli' in io.getvalue())