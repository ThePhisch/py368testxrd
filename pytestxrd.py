"""
Anton Schwarz
Main file of pytestxrd: testing utility for xrootd (rewritten from perl)
For Python 3.6.8
"""

from core import args
from sys import argv

args_passed = args.cli_args(argv[1:])

print(args_passed)