import logging
import socket
from core.connect import send
from definitions import request_codes
from functions.baseclass import Pytestxrd_Base_Function
from typing import List, Set, Any


class Rmdir(Pytestxrd_Base_Function):
    """
    Implements Rmdir
    """

    @staticmethod
    def help_str() -> str:
        return "rmdir\t<path>"

    def check(self) -> bool:
        if self.largs == 1:
            self.path = self.args[0]
            self.can_run = True
        else:
            self.err_number_of_arguments(self.largs, 1)
        return super().check()

    def run(self) -> None:
        """
        Send the rmdir request to the server

        -> except for the different request code, this
        is functionally the same as rm

        As of right now, the following behaviour has been emulated
        from the perl original
        -> rm may delete folders
        -> rmdir may not delete files
        -> empty folders may not be deleted

        also includes validation using check_response_ok
        """
        plen = len(self.path)
        send_args = (
            request_codes.kXR_rmdir,
            b"\0" * 16,
            plen,
            self.path.encode("UTF-8"),
        )
        send(self.socket, f"!H16sl{plen}s", send_args)

        if self.check_response_ok():
            logging.info("rmdir succeeded.")
