import logging
import socket
from core.persist import Persist
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from struct import unpack
from typing import List, Tuple, Set, Dict, Any


class Read(Pytestxrd_Base_Function):
    """
    Implements the read function
    """

    @staticmethod
    def help_str() -> str:
        return "read\t<path> <offset> [*|<length>]"

    def check(self) -> bool:
        self.persist: Persist = self.kwargs["persist"]

        if self.largs == 2:
            path, offset = self.args
            self.path = path
            self.offset = min(int(offset), general_vals.maxValidOffset)
            self.length = general_vals.pageSize
            self.can_run = True
        elif self.largs == 3:
            path, offset, length = self.args
            if self.args[-1] == "*":
                self.path = path
                self.offset = min(int(offset), general_vals.maxValidOffset)
                self.length = general_vals.maxValidLength
            else:
                # TODO this should be try/except or something
                self.path = path
                self.offset = min(int(offset), general_vals.maxValidOffset)
                self.length = min(int(length), general_vals.maxValidLength)
            self.can_run = True
        else:
            self.err_number_of_arguments(self.largs, 2)

        return super().check()

    def run(self) -> None:
        """
        Send the read request to the server

        -> read file
        -> beginning at offset
        -> for a length of length bytes
        -> data is requested while the response is kXR_oksofar, ends
        as soon as any other response is received

        o also includes extended validation using check_response_ok
        o also check whether the file is in the filetable
        """
        logging.debug(f"Beginning read with offset={self.offset} length={self.length}")

        if not self.persist.ft_entry_exists(self.path):
            # Checking if it is not yet open
            logging.warning("File not open. Aborting read process.")
            return

        send_args = (
            request_codes.kXR_read,
            self.persist.filetable[self.path].to_bytes(4, "big"),
            self.offset,
            self.length,
            0,  # no arguments -> alen = 0 TODO fix this
        )
        send(
            self.socket,
            f"!H4sqll",
            send_args,
        )

        # prepare loop
        reqcode = request_codes.kXR_oksofar
        with open(general_vals.defaultOutFileName, "wb") as out_file:
            out_file.write(b"")

        # loop while data is not complete
        while reqcode == request_codes.kXR_oksofar:
            # Receive response
            logging.debug("Request sent, receiving an answer now...")
            data = self.socket.recv(4)
            (sid, reqcode) = unpack("!HH", data)

            logging.debug(f"Streamid={sid}, Response Code={reqcode}")

            # Handle response in case of error
            if reqcode == request_codes.kXR_error:
                logging.warning(f"Response Code {reqcode} indicates an error")
                self.handle_error_response()
                return

            # Handle normal response
            dlen = unpack("!l", self.socket.recv(4))[0]
            data = unpack(f"!{dlen}s", self.socket.recv(dlen))[0]
            logging.debug(f"dlen={dlen}")
            # print(data)
            # write to file
            with open(general_vals.defaultOutFileName, "ab") as out_file:
                logging.debug(f"Writing to file {general_vals.defaultOutFileName}")
                out_file.write(data)

        logging.info("Read completed.")
        return
