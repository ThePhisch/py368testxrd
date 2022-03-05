import os
import socket

# import functions here
from core.connect import login
from functions import class_dict

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
        And Parse and Execute Necessary Functions
        """
        command = input(f"{self.hostname}:{self.port}> ").split()
        # parse user input here
        if command[0] == "help":
            if len(command) == 1:
                self.get_help()
            else:
                print(f"Check number of arguments: {len(command)}/1 args given")
        elif command[0] in class_dict.keys():
            operator = class_dict[command[0]](command[1:], self.socket)
        else:
            print("Command not found.")
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
        for f in class_dict.values():
            print(f.help_str())

