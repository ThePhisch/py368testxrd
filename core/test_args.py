import unittest
from core.args import cli_args

class ArgsTester(unittest.TestCase):
    def setUp(self) -> None:
        return

    def test_only_host(self):
        """Test case in which only the hostname is given + default port selected"""
        user_input = ["hosterzz"]
        self.assertSequenceEqual(cli_args(user_input), ("hosterzz", 1094, 0))

    def test_both_given(self):
        """Test case in which both values are given"""
        user_input=["hoSSST", "2444"]
        self.assertSequenceEqual(cli_args(user_input), ("hoSSST", 2444, 0))

    def test_with_loglevel(self):
        """Test case with 3 values"""
        user_input=["bro", "789", "-d 1"]
        self.assertSequenceEqual(cli_args(user_input), ("bro", 789, 1))
