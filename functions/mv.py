import logging
import socket
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from typing import List, Set, Any

class Mv(Pytestxrd_Base_Function):
    """
    Implements the mv function
    """

    @staticmethod
    def help_str() -> str:
        return "mv\t<old_path> <new_path>"

    def check(self) -> bool:
        if self.largs == 2:
            self.oldp = self.args[0] 
            self.newp = self.args[1] + "X" # to counteract truncation
            self.can_run = True
        else:
            print(f"Check number of arguments: {self.largs}/2 args given")
        return super().check()



    def run(self) -> bool:
        """
        Send the mv request to the server

        also includes validation using check_response_ok
        """
        plen = len(self.oldp + self.newp)
        send_args = (
            request_codes.kXR_mv,
            b"\0"*14,
            len(self.oldp),
            plen,
            f"{self.oldp} {self.newp}".encode("UTF-8"),
        )
        send(
            self.socket,
            f"!H14sHl{plen}s",
            send_args
        )

        if self.check_response_ok():
            logging.info("mv succeeded.")
            return True
        return False