import logging
import socket
from struct import unpack
from functools import reduce
from typing import List, Set, Any, Any

from definitions import general_vals, request_codes


class Pytestxrd_Base_Function:
    """
    Implement a basic class for the functions
    
    How to use??
    * init(): pass parameters
    * check(): find out if initialisation was successful
    * run(): run the function
    """

    @staticmethod
    def help_str() -> str:
        return "Help has not been defined for this function."

    def __init__(self, args: List[str], socket: socket.socket, **kwargs: Any) -> None:
        self.can_run = False
        self.socket = socket
        self.args = args
        self.largs = len(self.args)
        self.kwargs = kwargs

    def check(self) -> bool:
        return self.can_run 

    def run(self) -> bool:
        return True 

    def check_response_ok(self) -> bool:
        """
        Checking the response of a request

        For the simplest of requests, the response consists of only 3 components
        -> StreamID
        -> Response Code
        -> an kXR_int32

        this function requests the response, checks the values,
        logs debug/warnings and returns whether everything is_ok
        """
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
        (num,) = unpack("!l", data)
        if sid != general_vals.StreamID:
            logging.warning(f"StreamID {sid} != StreamID")
            is_ok = False
        if reqcode != request_codes.kXR_ok:
            logging.warning(f"Response Code {reqcode} != kXR_ok")
            is_ok = False
        if num != 0:
            logging.warning(f"Number {num} != 0")
            is_ok = False
        return is_ok

    def handle_error_response(self) -> None:
        """
        Handles the response if kXR_error is returned

        -> stream has been read up to kXR_error
        -> begin reading from dlen
        """
        data = self.socket.recv(8)
        (dlen, errnum) = unpack("!ll", data)
        logging.debug(f"Dlen={dlen}, Errnum={errnum}")
        data = self.socket.recv(dlen - 4)
        errmsg: bytes = unpack(f"!{dlen - 4}s", data)[0]
        print(errmsg.decode("UTF-8"))

    @staticmethod
    def err_number_of_arguments(num: int, wanted: int) -> None:
        print(f"Check number of arguments: {num}/{wanted} args given")

    @staticmethod
    def err_number_of_options(num: int, maxi: int) -> None:
        print(f"Check number of options: {num}/maximum of {maxi} options")

    @staticmethod
    def check_options_subset(
        list_opts_given: List[str], opts_allowed: Set[str]
    ) -> bool:
        opts_given = set(list_opts_given)
        extraneous_opts = opts_given.difference(opts_allowed)
        if extraneous_opts:
            print(f"The following options were not recognised: {list(extraneous_opts)}")
            return False
        logging.debug(f"All options (given {list_opts_given}) were recognised")
        return True

    def get_mode(self, mode_str: str, forbidden_flags: Set[int] = set()) -> int:
        try:
            mode_intlist = list(map(lambda x: int(x), list(mode_str)))
        except ValueError:
            logging.warning("Conversion from string to int array was not successful")
            return -1
        # throw error if it doesnt have length 3
        if len(mode_intlist) != 3:
            print(f"Check number of arguments in mode: {len(mode_intlist)} != 3")
            return -1
        flags_set: set[int] = set()

        for access_group, value in enumerate(mode_intlist):
            # print(f"~incremented, starting at {value}~")
            while value > 0:
                # print(f"Position={value}")
                if value - 4 >= 0:
                    value = value - 4
                    if access_group == 0:
                        flags_set.add(request_codes.kXR_ur)
                    elif access_group == 1:
                        flags_set.add(request_codes.kXR_gr)
                    elif access_group == 2:
                        flags_set.add(request_codes.kXR_or)
                    # print(4)
                if value - 2 >= 0:
                    value = value - 2
                    if access_group == 0:
                        flags_set.add(request_codes.kXR_uw)
                    elif access_group == 1:
                        flags_set.add(request_codes.kXR_gw)
                    elif access_group == 2:
                        flags_set.add(request_codes.kXR_ow)
                    # print(2)
                if value - 1 >= 0:
                    value = value - 1
                    if access_group == 0:
                        flags_set.add(request_codes.kXR_ux)
                    elif access_group == 1:
                        flags_set.add(request_codes.kXR_gx)
                    elif access_group == 2:
                        flags_set.add(request_codes.kXR_ox)
                    # print(1)
        logging.debug(f"Following flags were requested by user: {flags_set}")
        flags_removed = flags_set.intersection(forbidden_flags)
        if flags_removed:
            logging.warning(
                f"Following flags are forbidden and were removed: {flags_removed}"
            )
        else:
            logging.debug("No flags were removed.")
        flags_set.difference_update(forbidden_flags)
        logging.debug(f"Will set flags {flags_set}")

        if flags_set:
            val_to_send: int = reduce(lambda x, y: x | y, flags_set)
            logging.debug(f"Send value: {val_to_send}")
        else:
            val_to_send: int = 0
            logging.debug("No flags to send, will send 0")

        return val_to_send
