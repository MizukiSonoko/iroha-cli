import unittest
import sys, os

sys.path.insert(0, os.path.abspath(__file__ + "/../../cli"))
sys.path.insert(0, os.path.abspath(__file__ + "/../../schema"))
from cli import commands
from cli.exception import CliException

from io import StringIO
io = StringIO()


class TestBuildInCommands(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_normal(self):
        sys.stdout = io
        ##
        sys.stdout = sys.__stdout__
        #self.assertTrue('Iroha-mizuki-cli' in io.getvalue())

    def test_config(self):
        sys.stdout = io
        ##
        sys.stdout = sys.__stdout__
        #self.assertTrue('Iroha-mizuki-cli' in io.getvalue())