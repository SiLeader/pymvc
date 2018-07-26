#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base64
import re
import typing


__V1_STRETCH_COUNT = 10000


def __version0(target: str) -> str:
    """
    hash function version 0
    :param target: input data
    :return: hashed data
    """
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
    """
    compute hash value
    :param target: input data
    :param ver: hash function version. None is latest version
    :return: hashed data
    """
    if ver is None:
        ver = -1
    return __HASH_FUNCTIONS[ver](target)


def latest_version() -> int:
    """
    latest hash function version
    :return: latest version number
    """
    return len(__HASH_FUNCTIONS) - 1


def check(hashed: str, non_hashed: str) -> typing.Tuple[bool, typing.Optional[str]]:
    """
    check correct value and get updated hashed value
    :param hashed: value 1
    :param non_hashed: value 2
    :return: (is corrected, updated value)
    """
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
    """
    get hashed data version
    :param target: hashed data
    :return: hashed data version
    """
    if target is None:
        return None
    match = re.match("\$(\d+)\$.+", target)
    if not match:
        return None
    return int(match.group(1))


class Hashed:
    """
    Hashed data type
    """
    def __init__(self, data=None, ver=None):
        """
        constructor
        :param data: data
        :param ver: version
        """
        if data is None:
            data = ""
        elif version(data) is None:
            data = compute_hash(data, ver)
        self.__data = data

    def __str__(self):
        """
        str operator
        hashed data
        :return: hashed data
        """
        return self.__data

    def __eq__(self, other):
        """
        equal operator
        :param other: opponent value
        :return: is same
        """
        if isinstance(other, Hashed):
            other = str(other)
        ok, new = check(self.__data, other)

        if new is not None:
            self.__data = new
        return ok
