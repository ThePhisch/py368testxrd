from pathlib import Path
from os import system, remove
import unittest
from core.connect import connect_xrootd, login
from functions.rmdir import Rmdir
from testing_setup import *
import socket


class RmTester(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.xrd_connect_args = [XROOTD_HOST, XROOTD_PORT, DEFAULT_LOG_LEVEL]
        self.testdir = Path(TESTING_FOLDER) / "pytestxrd_testfolder_rmdir"
        self.testfile = self.testdir / "pytestxrd_testfile_rmdir.txt"

    def test_too_many_arguments(self):
        op = Rmdir(["hello", "too many args!!"], self.dummy_socket)
        self.assertFalse(op.check())

    def test_no_arguments_given(self):
        op = Rmdir([], self.dummy_socket)
        self.assertFalse(op.check())

    def test_one_argument_given(self):
        op = Rmdir(["asdf"], self.dummy_socket)
        self.assertTrue(op.check())

    @unittest.skipUnless(
        CONNECT_TO_XROOTD_FOR_TEST,
        "Connecting to xrootd not permitted. Change the flag in 'testin_setup.py'",
    )
    def test_connect_run_full(self):
        """
        Testing a full rmdir run
        -> check whether connecting to xrootd for testing is allowed
        -> create folder with one file
        -> try to delete non-empty folder (expect fail)
        -> try to delete emptied folder (expect success)
        """
        self.assertFalse(
            self.testdir.exists(),
            f"Testdir already exists! Please remove {self.testdir}",
        )
        system(f"mkdir {self.testdir}")
        system(f"echo 'remove this too :)' >> {self.testfile}")
        self.assertTrue(
            self.testfile.exists(), "Something went wrong in testfile creation."
        )
        with connect_xrootd(*self.xrd_connect_args) as s:
            session_id = login(s)
            op = Rmdir(
                [str(self.testdir)], s
            )  # try to delete non-empty folder -> should fail
            if op.check():
                return_bool = op.run()
                self.assertFalse(
                    return_bool, "The folder was not empty, but it was deleted anyway!"
                )
            remove(self.testfile)
            op = Rmdir([str(self.testdir)], s)  # delete empty folder -> should pass
            if op.check():
                return_bool = op.run()
                self.assertTrue(
                    return_bool, "Folder was empty, should have been removed."
                )
        self.assertFalse(self.testfile.exists())
        if self.testfile.exists():
            remove(self.testfile)
        self.assertFalse(self.testdir.exists())
        if self.testdir.exists():
            remove(self.testdir)
