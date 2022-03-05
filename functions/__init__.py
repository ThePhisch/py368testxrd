"""
This module contains all the functions corresponding to xrootd commands
"""

from typing import Type, Dict
from functions import ping, chmod, dir, mv, rm, rmdir, open, read, close
from functions.baseclass import Pytestxrd_Base_Function

__all__ = ["ping", "chmod", "dir", "mv", "rm", "rmdir", "open", "read", "close"]

class_dict: Dict[str, Type[Pytestxrd_Base_Function]] = {
    "ping": ping.Ping,
    "chmod": chmod.Chmod,
    "dir": dir.Dir,
    "mv": mv.Mv,
    "rm": rm.Rm,
    "rmdir": rmdir.Rmdir,
    "open": open.Open,
    "read": read.Read,
    "close": close.Close,
}
