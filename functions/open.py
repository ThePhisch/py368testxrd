from functools import reduce
import logging
import socket
from core.persist import Persist
from definitions import general_vals, request_codes
from functions.baseclass import Pytestxrd_Base_Function
from core.connect import send
from struct import unpack
from typing import List, Set, Any, Dict, Tuple, Any


class Open(Pytestxrd_Base_Function):
    """
    Implements the open function
    """

    @staticmethod
    def help_str() -> str:
        ret: str = (
            "open\t<path> [a] [c] [d] [f] [m] [n] [p] [r] [R] [s] [t] [u] [<mode>]"
        )
        ret += "\n\ta -> async c -> cmprs d -> dlete f -> force"
        ret += "\n\tm -> mkpth n -> new   p -> posc  r -> read "
        ret += "\n\tR -> rplca s -> rfrsh t -> stats u -> updte"
        return ret

    def check(self) -> bool:
        self.persist = self.kwargs["persist"]
        largs = len(self.args)
        if largs == 1:
            self.path = self.args[0]
            self.mode = "644"
            self.options, self.options_int = set(), 0
            self.can_run = True
        elif largs > 1:
            path, options, mode = self.args[0], self.args[1:-1], self.args[-1]
            if len(mode) != 3:
                logging.warning("Bad mode integer")
            else:
                self.path = path
                self.options, self.options_int = self.parse_options(set(options))
                self.mode = mode
                self.can_run = True
        else:
            self.err_number_of_arguments(largs, 1)
        return super().check()

    @staticmethod
    def parse_options(options_given: Set[str]) -> Tuple[Set[str], int]:
        """
        Parses the options given

        returns set of given options (cleaned)
        and the or'd int that is returned to the server
        """

        def calculate_options_int(options_given: Set[str]) -> int:
            """
            Static method to calculate the or'd option integer
            """
            options_set: set[int] = {0}
            for o in options_given:
                if o == "a":
                    options_set.add(request_codes.kXR_async)
                elif o == "c":
                    options_set.add(request_codes.kXR_compress)
                elif o == "d":
                    options_set.add(request_codes.kXR_delete)
                elif o == "f":
                    options_set.add(request_codes.kXR_force)
                elif o == "m":
                    options_set.add(request_codes.kXR_mkpath)
                elif o == "n":
                    options_set.add(request_codes.kXR_new)
                elif o == "p":
                    options_set.add(request_codes.kXR_posc)
                elif o == "r":
                    options_set.add(request_codes.kXR_open_read)
                elif o == "R":
                    options_set.add(request_codes.kXR_replica)
                elif o == "s":
                    options_set.add(request_codes.kXR_refresh)
                elif o == "t":
                    options_set.add(request_codes.kXR_retstat)
                elif o == "u":
                    options_set.add(request_codes.kXR_open_updt)
                else:
                    logging.warning("This should never happen: option not recognised")
                    pass

            ret = reduce(lambda x, y: x | y, options_set)
            logging.debug(f"Option (already or'd) is {ret}")

            return ret

        allowed = {"a", "c", "d", "f", "m", "n", "p", "r", "R", "s", "t", "u"}
        logging.debug(f"Options given: {options_given}")
        not_recognised = options_given.difference(allowed)
        if not_recognised:
            logging.warning(f"Options not recognised: {not_recognised}")
            # TODO actually implement some sort of raised error here
        options_allowed = options_given.intersection(allowed)
        logging.debug(f"Options allowed: {options_allowed}")
        return options_allowed, calculate_options_int(options_allowed)

    def run(self) -> bool:
        """
        Send the open request to the server

        also includes extended validation using check_response_ok
        """

        if self.persist.ft_entry_exists(self.path):
            # Checking if it is already open
            logging.warning("Aborting open process.")
            return False

        plen = len(self.path)
        mode = self.get_mode(
            self.mode, {request_codes.kXR_ow}
        )  # TODO add mode to read from input
        send_args = (
            request_codes.kXR_open,
            mode,
            self.options_int,
            b"\0" * 12,
            plen,
            self.path.encode("UTF-8"),
        )

        send(self.socket, f"!HHH12sl{plen}s", send_args)

        # Receive response
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
        (rlen, fhandle_bytes) = unpack("!l4s", self.socket.recv(8))
        fhandle = int.from_bytes(fhandle_bytes, "little")
        logging.debug(f"Rlen={rlen}, Fhandle={fhandle}")

        # TODO be able to handle compression optional addition to response
        # TODO handle retstat response

        if self.options.intersection({"c", "t"}):
            # if compress or retstat are set
            (cpsize, cptype_bytes) = unpack("!l4s", self.socket.recv(8))
            cptype = cptype_bytes.decode("UTF-8")
            logging.debug(f"cpsize={cpsize}, cptype bytes={cptype}")

            # TODO continue here

        # Add to filetable
        self.persist.ft_add_entry(self.path, fhandle)
        # TODO log success
        return True