import logging
import socket
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from functools import reduce
from typing import List, Set, Any
from struct import unpack


class Protocol(Pytestxrd_Base_Function):
    """
    Implements the protocol function
    """

    @staticmethod
    def help_str() -> str:
        return "protocol\t"

    def check(self) -> bool:
        if self.largs != 0:
            extra_args = ", ".join(self.args)
            print(f"Extraneous ping arguments - {extra_args}")
        else:
            self.can_run = True
        return super().check()

    def run(self) -> bool:
        """
        Ping the server
        """
        send_args = (
            request_codes.kXR_protocol,
            0x00000310, # clientpv as in perlscript
            bytes(request_codes.KXR_secreqs), # options: expect security signing reqs (TODO add more options)
            b"\0", # expect: no intentions (kXR_ExpNone -> TODO implement these codes too and more options)
            b"\0" * 10,
            0,
        )
        send(self.socket, f"!Hlcc10sl", send_args)

        # response
        logging.debug("Request sent, receiving an answer now...")
        is_ok = True
        data = self.socket.recv(4)
        (sid, reqcode) = unpack("!HH", data)
        logging.debug(f"Streamid={sid}, Response Code={reqcode}")
        if reqcode == request_codes.kXR_error:
            logging.warning(f"Response Code {reqcode} indicates an error")
            self.handle_error_response()
            return False
        data = self.socket.recv(4)
        (dlen,) = unpack("!l", data)
        # right now dlen must be 8 -> TODO implement further options later
        if dlen != 8:
            logging.warning(f"dlen {dlen} != 8 (must be 8 for now)")
            return False
        data = self.socket.recv(dlen)
        (pval, flags) = unpack("!ll", data)
        print(f"pval = {pval:x} and flags = {flags:x}") # "x" converts into unsigned hex
        logging.info("protocol was a success")
        return True

