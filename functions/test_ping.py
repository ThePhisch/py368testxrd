import unittest
from core.connect import connect_xrootd, login
from functions.ping import Ping
from testing_setup import *
import socket


class PingTester(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.xrd_connect_args = [XROOTD_HOST, XROOTD_PORT, DEFAULT_LOG_LEVEL]

    def test_too_many_arguments(self):
        op = Ping(["hello", "too many args!!"], self.dummy_socket)
        self.assertFalse(op.check())

    def test_no_arguments_given(self):
        op = Ping([], self.dummy_socket)
        self.assertTrue(op.check())

    @unittest.skipUnless(CONNECT_TO_XROOTD_FOR_TEST,
    "Connecting to xrootd not permitted. Change the flag in 'testin_setup.py'")
    def test_connect_run_full(self):
        with connect_xrootd(*self.xrd_connect_args) as s:
            session_id = login(s)
            op = Ping([], s)
            if op.check():
                return_bool = op.run()
                self.assertTrue(return_bool)
                return
        self.fail()