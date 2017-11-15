import unittest
import sys, os

from iroha_cli.exception import CliException


class TestException(unittest.TestCase):

    def test_normal(self):
        try:
            raise CliException("Error!")
        except CliException as e:
            self.assertTrue(e.message == "Error!")
        else:
            self.fail()


    def test_CliException_catched(self):
        try:
            raise CliException("Error")
        except Exception as e:
            pass
        else:
            self.fail()

