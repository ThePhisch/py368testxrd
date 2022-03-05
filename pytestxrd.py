"""
Anton Schwarz
Main file of pytestxrd: testing utility for xrootd (rewritten from perl)
For Python 3.6.8
"""

from core import args, logger
from core.persist import Persist
from core.ui import UI
from core.connect import connect_xrootd, login
from sys import argv

args_passed = args.cli_args(argv[1:])
logger.setup_logging(args_passed[2])
persistor = Persist()

with connect_xrootd(*args_passed) as s:
    session_id = login(s)
    ui = UI(*args_passed, session_id, s, persistor)
    while True:
        try: 
            ui.prompt()
        except KeyboardInterrupt:
            ui.exiting()
            break