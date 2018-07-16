#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from flask import abort


class RenderParameter:
    """
    parameter for render_template
    """
    def __init__(self, view: str, **params):
        """
        constructor
        :param view: view file name
        :param params: parameters
        """
        self.__view = view
        self.__params = params

    @property
    def view(self):
        """
        get view file name
        :return: view file name
        """
        return self.__view

    @property
    def params(self):
        """
        get render parameters
        :return: render parameters
        """
        return self.__params


def render(view=None, **params):
    """
    get parameter class
    :param view: view file name (optional)
    :param params: template parameters (optional)
    :return: parameter instance
    """
    return RenderParameter(view, **params)


class Controller(abc.ABC):
    """
    Controller base class
    """
    VIEW = None

    def get(self, **kwargs):
        """
        http GET function
        :param kwargs: url parameter
        :return: response
        """
        return abort(405)

    def post(self, **kwargs):
        """
        http POST function
        :param kwargs: url parameter
        :return: response
        """
        return abort(405)

    def put(self, **kwargs):
        """
        http PUT function
        :param kwargs: url parameter
        :return: response
        """
        return abort(405)

    def delete(self, **kwargs):
        """
        http DELETE function
        :param kwargs: url parameter
        :return: response
        """
        return abort(405)

    def __hash__(self):
        return hash(self.__class__.__name__)
