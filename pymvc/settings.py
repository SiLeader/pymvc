#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import wsgi
import typing
import pathlib


class _DatabaseSetting:
    """
    database setting class
    """
    def __init__(self):
        self.__host = None
        self.__port = None
        self.__database = None

    @property
    def host(self) -> typing.Optional[str]:
        """
        get host name
        :return: host name
        """
        return self.__host

    @host.setter
    def host(self, value: typing.Optional[str]):
        """
        set host name
        :param value: host name
        """
        self.__host = value

    @property
    def port(self) -> typing.Optional[int]:
        """
        get port number
        :return: port number
        """
        return self.__port

    @port.setter
    def port(self, value: typing.Optional[int]):
        """
        set port number
        :param value: port number
        """
        self.__port = value

    @property
    def database(self) -> typing.Optional[str]:
        """
        get database name
        :return: database name
        """
        return self.__database

    @database.setter
    def database(self, value: str):
        """
        set database name
        :param value: database name
        """
        self.__database = value


class _FlaskSetting:
    """
    Flask settings
    """
    def __init__(self):
        cwd = str(pathlib.Path.cwd().absolute())
        self.root_directory = cwd

    @property
    def static_directory(self) -> str:
        """
        get static files directory
        :return: static files directory
        """
        return wsgi.app.static_folder

    @static_directory.setter
    def static_directory(self, value: str):
        """
        set static files directory
        :param value: static files directory
        """
        wsgi.app.static_folder = value

    @property
    def static_url(self) -> str:
        """
        get static files url
        :return: static files url
        """
        return wsgi.app.static_url_path

    @static_url.setter
    def static_url(self, value: str):
        """
        set static files url
        :param value: static files url
        """
        wsgi.app.static_url_path = value

    @property
    def templates_directory(self) -> str:
        """
        get templates directory
        :return: templates directory
        """
        return wsgi.app.template_folder

    @templates_directory.setter
    def templates_directory(self, value: str):
        """
        set templates directory
        :param value: templates directory
        """
        wsgi.app.template_folder = value

    @property
    def root_directory(self) -> str:
        return wsgi.app.root_path

    @root_directory.setter
    def root_directory(self, value: str):
        wsgi.app.root_path = value


database = _DatabaseSetting()
flask = _FlaskSetting()
