import os
import socket

# import functions here
from core.connect import login

class UI:
    """
    Class to deal with all the input and output
    (except CLI args passed earlier).

    Also includes logic on which command to execute
    """

    def __init__(self, hostname: str, port: int, debuglevel: int, session_id: str, socket: socket.socket) -> None:
        self.hostname = hostname
        self.port = port
        self.socket = socket
        self.session_id = session_id
        print(f"Login PID: {os.getpid()} Session ID: {self.session_id}")
        return

    def prompt(self) -> None:
        """
        Standard prompt
        """
        command = input(f"{self.hostname}:{self.port}> ")
        # parse user input here
        return

    def exiting(self) -> None:
        """
        Exiting pytestxrd
        """
        print("\nExiting")
        return

    def get_help(self) -> None:
        """
        Print a helpscreen
        """
        for f in functions.funclist:
            print(f.help_str())

