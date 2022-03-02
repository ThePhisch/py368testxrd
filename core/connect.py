from contextlib import contextmanager
import socket
from struct import pack, unpack
from typing import Any, Generator, Tuple
from definitions import request_codes, general_vals
import os
from functools import reduce
import logging


@contextmanager
def connect_xrootd(host: str, port: int, debuglevel: int) -> Generator[socket.socket, None, None]:
    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))  # Connect
    logging.debug(f"Connected to {host}:{port}")

    # Initial Handshake
    s.send(pack("!LLLLL", 0, 0, 0, 4, 2012))
    data = s.recv(16)
    (sid, status, rlen, pval, flag) = unpack("!HHlll", data)

    logging.info(f"h/s response: si={sid} rq={status} ln={rlen} vn={pval} st={flag}")

    # yield the socket object, handle closing.
    try:
        yield s
    finally:
        s.shutdown(socket.SHUT_WR)
        s.close()


def login(s: socket.socket) -> str:
    # Login
    # Typed out for better understanding
    to_send: Tuple[bytes, ...] = (
        pack("!H", general_vals.reqID),
        pack("!H", request_codes.kXR_login),
        pack(
            "!L", os.getpid()
        ),  # Spec says this should be signed, but perl is unsigned
        pack("8s", os.getenv("USER").encode("UTF-8")),  # type: ignore
        pack("!H", request_codes.Ability),
        pack("B", request_codes.kXR_asyncap | 4),  # Unsigned Char
        pack("B", 0),
        pack("!L", 0),
    )

    s.send(reduce(lambda x, y: x + y, to_send))
    logging.debug("Sending login.")
    data = s.recv(8)
    (sid, reqcode, slenplus) = unpack("!HHl", data)
    logging.debug(f"Streamid={sid}, Response Code={reqcode}, slen+16={slenplus}")
    logging.debug("Receiving Session ID and Sec now")
    data = s.recv(16)
    return data.hex()


def send(s: socket.socket, format: str, args: Tuple[Any, ...]) -> None:
    packed_stream_ID: bytes = pack("!H", general_vals.StreamID)
    packed_args = pack(format, *args)
    s.sendall(packed_stream_ID + packed_args)
    return