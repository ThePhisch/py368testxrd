from pathlib import Path
from os import system, remove
import unittest
from core.connect import connect_xrootd, login
from functions.rm import Rm
from testing_setup import *
import socket


class RmTester(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.xrd_connect_args = [XROOTD_HOST, XROOTD_PORT, DEFAULT_LOG_LEVEL]
        self.testfile = Path(TESTING_FOLDER) / "pytestxrd_testfile_rm.txt"

    def test_too_many_arguments(self):
        op = Rm(["hello", "too many args!!"], self.dummy_socket)
        self.assertFalse(op.check())

    def test_no_arguments_given(self):
        op = Rm([], self.dummy_socket)
        self.assertFalse(op.check())

    def test_one_argument_given(self):
        op = Rm(["asdf"], self.dummy_socket)
        self.assertTrue(op.check())

    @unittest.skipUnless(
        CONNECT_TO_XROOTD_FOR_TEST,
        "Connecting to xrootd not permitted. Change the flag in 'testin_setup.py'",
    )
    def test_connect_run_full(self):
        self.assertFalse(
            self.testfile.exists(),
            f"Testfile already exists! Please remove {self.testfile}",
        )
        system(f"echo 'remove this lmao' >> {self.testfile}")
        self.assertTrue(self.testfile.exists(), "Something went wrong in testfile creation.")
        with connect_xrootd(*self.xrd_connect_args) as s:
            session_id = login(s)
            op = Rm([str(self.testfile)], s)
            if op.check():
                return_bool = op.run()
                self.assertTrue(return_bool, "run() returned False value")
        self.assertFalse(self.testfile.exists())
        if self.testfile.exists(): remove(self.testfile)