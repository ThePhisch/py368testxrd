import logging
import socket
from core.connect import send
from definitions import request_codes
from functions.baseclass import Pytestxrd_Base_Function
from typing import List, Set

class Rm(Pytestxrd_Base_Function):
    """
    Implements Rm
    """

    @staticmethod
    def help_str() -> str:
        return "rm\t<path>"

    def __init__(self, args: List[str], socket: socket.socket) -> None:
        super().__init__(args, socket)
        if len(args) == 1:
            self.path = args[0]
            logging.debug(f"rm will be operated on {self.path}")
            self.run()
        else:
            self.err_number_of_arguments(len(args), 1)

    def run(self) -> None:
        """
        Send the rm request to the server

        As of right now, the following behaviour has been emulated
        from the perl original
        -> rm may delete folders
        -> rmdir may not delete files
        -> empty folders may not be deleted

        also includes validation using check_response_ok
        """
        plen = len(self.path)
        args = (
            request_codes.kXR_rm,
            b"\0" * 16,
            plen,
            self.path.encode("UTF-8"),
        )
        send(self.socket, f"!H16sl{plen}s", args)

        if self.check_response_ok():
            logging.info("rm succeeded.")
