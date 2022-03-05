import logging
import socket
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from functools import reduce
from typing import List, Set

class Ping(Pytestxrd_Base_Function):
    """
    Implements the ping function
    """

    @staticmethod
    def help_str() -> str:
        return "ping\t"

    def __init__(self, args: List[str], socket: socket.socket) -> None:
        super().__init__(args, socket)
        if len(args) != 0:
            extra_args = ", ".join(args) 
            print(f"Extraneous ping arguments - {extra_args}")
            return
        else:
            self.run()

    def run(self) -> None:
        """
        Ping the server
        """
        args = (
            request_codes.kXR_ping,
            b"\0"*16,
            0,
        )
        send(
            self.socket,
            f"!H16sl",
            args
        )

        if self.check_response_ok():
            logging.info("ping succeeded.")