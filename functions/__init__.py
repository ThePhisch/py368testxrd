"""
This module contains all the functions corresponding to xrootd commands
"""

from typing import Type, Dict
from functions import ping
from functions.baseclass import Pytestxrd_Base_Function

__all__ = ["ping"]

class_dict : Dict[str, Type[Pytestxrd_Base_Function]]= {
    "ping" : ping.Ping
}