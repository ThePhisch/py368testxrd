import argparse
from typing import Tuple, List


def cli_args(user_input: List[str]) -> Tuple[str, int, int]:
    """
    Setup the parsing of arguments
    : Hostname
    : Port (optional) (positional) default 1094
    : debug levels (optional) options 0,1,2
    -> passes hostname and port as tuple
    -> calls the setup_logging() function with the logging level
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="the host")
    parser.add_argument(
        "port", type=int, nargs="?", default=1094, help="port number, default"
    )
    parser.add_argument(
        "--debug",
        "-d",
        help="toggle debug mode (increased verbosity)",
        type=int,
        choices=[0, 1, 2],
        default=0,
    )
    args = parser.parse_args(user_input)
    # setup_logging(args.debug)
    return (args.hostname, args.port, args.debug)
