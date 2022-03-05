from os import stat
import socket
from definitions import request_codes
from functions.baseclass import Pytestxrd_Base_Function
import logging
from core.connect import send
from struct import unpack
from definitions import general_vals
from typing import List, Set, Any


class Dir(Pytestxrd_Base_Function):
    @staticmethod
    def help_str() -> str:
        return "dir\t[c] [s] <path>\n\twhere: c->chksum s->return stat"
        # option "online" has been removed, not present in 5.0.0 spec

    def check(self) -> bool:
        if self.largs == 0:
            # at least one argument required
            self.err_number_of_arguments(self.largs, 1)
        elif self.largs > 2:
            # too many options given
            self.err_number_of_options(self.largs-1, 1)
        elif self.check_options_subset(self.args[:-1], {"c", "s"}):
            # All options recognised
            self.options = self.args[:-1]
            self.dirpath = self.args[-1]
            self.can_run = True
        else:
            print("Cancelling dir")
        return super().check()

    def run(self) -> None:
        """
        Send the dir request to the server

        also deals with option flags (but validation of user input
        is already complete)
        """

        plen = len(self.dirpath)

        parsed_options = 0
        if "s" in self.options:
            parsed_options = parsed_options | request_codes.kXR_dstat
        if "c" in self.options:
            parsed_options = parsed_options | request_codes.kXR_dcksm

        logging.debug(f"Value of parsed_options is {parsed_options}")

        args = (
            request_codes.kXR_dirlist,
            b"\0" * 15,
            parsed_options.to_bytes(1, "big"),
            plen,
            self.dirpath.encode("UTF-8"),
        )

        send(self.socket, f"!H15ssl{plen}s", args)

        if self.parse_dir_response():
            logging.info("dir succeeded.")

    def parse_dir_response(self) -> bool:
        """
        Parsing a normal response to a request WITHOUT options

        -> streamID and request_code are checked
        -> dlen gives the number of bytes to listen for next
        -> decode chars into UTF-8 and print with some decoration
        """

        logging.debug("Request sent, receiving an answer now...")
        logging.debug("Checking a normal response (no options)...")
        is_ok = True
        data = self.socket.recv(8)
        (sid, reqcode, dlen) = unpack("!HHl", data)
        logging.debug(f"Streamid={sid}, Response Code={reqcode}, num={dlen}")
        if sid != general_vals.StreamID:
            logging.warning(f"StreamID {sid} != StreamID")
            is_ok = False
        if reqcode is not request_codes.kXR_ok:
            logging.warning(f"Response Code {reqcode} != kXR_ok")
            is_ok = False

        data = self.socket.recv(dlen)
        dircontents: bytes = unpack(f"!{dlen}s", data)[0]
        print("==========Printing directory contents=========")
        print(dircontents.decode("UTF-8"))
        print("===========End of directory contents==========")

        return is_ok
