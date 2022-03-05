import logging
import socket
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from functools import reduce
from typing import List, Set, Any

class Ping(Pytestxrd_Base_Function):
    """
    Implements the ping function
    """

    @staticmethod
    def help_str() -> str:
        return "ping\t"

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
            request_codes.kXR_ping,
            b"\0"*16,
            0,
        )
        send(
            self.socket,
            f"!H16sl",
            send_args
        )

        if self.check_response_ok():
            logging.info("ping succeeded.")
            return True
        else:
            return False