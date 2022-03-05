import logging
import socket
from core.persist import Persist
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from struct import unpack
from typing import List, Set, Any, Any


class Close(Pytestxrd_Base_Function):
    """
    Implements the close function

    -> when run with no arguments, closes all files
    -> otherwise closes the file with given path
    """

    @staticmethod
    def help_str() -> str:
        return "close\t[<path>]"

    def check(self) -> bool:
        self.persist: Persist = self.kwargs["persist"]
        self.to_close: dict[str, int]
        if self.largs == 0:
            self.to_close = self.persist.ft_prepare_deletion_dict()
            logging.debug("Proceed to close all files")
        else:
            self.to_close = self.persist.ft_prepare_deletion_dict(self.args)
            logging.debug(
                f"Proceed to close {self.largs} file{'s' if self.largs > 1 else ''}"
            )
        self.can_run = True # This function can always be run, regardless of arguments.
        # But you might send a command to close an empty dictionary. lol
        return super().check()

    def run(self) -> bool:
        """
        Send the close request to the server

        also includes extended validation using check_response_ok
        """
        for path_name, fhandle in self.to_close.items():
            logging.info(f"Closing {path_name} with fhandle {fhandle}...")
            args = (
                request_codes.kXR_close,
                fhandle.to_bytes(4, "little"),
                b"\0" * 12,
                0,
            )
            send(self.socket, f"!H4s12sl", args)

            logging.debug("Request sent, receiving an answer now...")
            data = self.socket.recv(4)
            (sid, reqcode) = unpack("!HH", data)

            logging.debug(f"Streamid={sid}, Response Code={reqcode}")

            # Handle response in case of error
            if reqcode == request_codes.kXR_error:
                logging.warning(f"Response Code {reqcode} indicates an error")
                self.handle_error_response()
                return False
            # Handle normal response
            (must_be_zero,) = unpack("!l", self.socket.recv(4))
            if must_be_zero != 0:
                logging.warning(
                    f"Response should be terminated by a zero, given {must_be_zero} instead."
                )

            # Remove from filetable
            self.persist.ft_remove_entry(path_name)

        logging.debug("Closing was successful.")
        return True
        # TODO maybe a tool that tells you which files are open??
