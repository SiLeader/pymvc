#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base64
import re
import typing


__V1_STRETCH_COUNT = 10000


def __version0(target: str) -> str:
    bytes_ = target.encode(encoding="utf-8")
    salt = [
        base64.b16encode(bytes_).decode(encoding="utf-8"),
        base64.b32encode(bytes_).decode(encoding="utf-8"),
        base64.b64encode(bytes_).decode(encoding="utf-8"),
        base64.b85encode(bytes_).decode(encoding="utf-8")
    ]

    def to_salt(d, s):
        return (d + s + d + s + d + s).encode(encoding="utf-8")

    for i in range(__V1_STRETCH_COUNT):
        s512 = hashlib.sha512()
        s512.update(to_salt(target, salt[i % 4]))
        target = s512.hexdigest()

    return "$0$" + target


__HASH_FUNCTIONS = [
    __version0
]


def compute_hash(target: str, ver=None) -> str:
    if ver is None:
        ver = -1
    return __HASH_FUNCTIONS[ver](target)


def latest_version() -> int:
    return len(__HASH_FUNCTIONS) - 1


def check(hashed: str, non_hashed: str) -> typing.Tuple[bool, typing.Optional[str]]:
    ver = version(hashed)
    non_ver = version(non_hashed)
    new_value = None

    if ver is None:
        if non_ver is None:
            hashed = compute_hash(hashed)
            non_hashed = compute_hash(non_hashed)
            new_value = hashed
        elif non_ver != latest_version():
            new_value = compute_hash(hashed)
        hashed = compute_hash(hashed, non_ver)
    else:
        if non_ver is None:
            if ver != latest_version():
                new_value = compute_hash(non_hashed)
            non_hashed = compute_hash(non_hashed, ver)
        else:
            if non_ver == ver:
                return hashed == non_hashed, None
            raise RuntimeError("check function cannot do check hashed value and hashed value")

    if hashed != non_hashed:
        return False, None

    return True, new_value


def version(target: str) -> typing.Optional[int]:
    if target is None:
        return None
    match = re.match("\$(\d+)\$.+", target)
    if not match:
        return None
    return int(match.group(1))


class Hashed:
    def __init__(self, data=None, ver=None):
        if data is None:
            data = ""
        elif version(data) is None:
            data = compute_hash(data, ver)
        self.__data = data

    def __str__(self):
        return self.__data

    def __eq__(self, other):
        if isinstance(other, Hashed):
            other = str(other)
        ok, new = check(self.__data, other)

        if new is not None:
            self.__data = new
        return ok
