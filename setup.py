#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from pymvc import pkg_info

with open("README.md") as fp:
    readme = fp.read()

with open("requirements.txt") as fp:
    requirements = [r.strip() for r in fp.readlines()]


package_name = "pymvc"

setup(
    name=package_name,
    packages=find_packages(),
    version=pkg_info.__version__,
    license=pkg_info.__license__,
    author=pkg_info.__author__,
    url="https://github.com/SiLeader/pymvc",

    description="MVC framework for Python",
    long_description=readme,
    long_description_content_type="text/markdown",

    install_requires=requirements,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware"
    ]
)
