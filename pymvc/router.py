#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

from flask import render_template

from . import wsgi, controller


def add_route(path: str, ctrl: typing.Union[controller.Controller, typing.Type]):
    """
    add router class to system
    :param path: url (see Flask reference)
    :param ctrl: control class or class instance
    """
    if not isinstance(ctrl, controller.Controller):
        ctrl = ctrl()

    def vf(func):
        def internal(**kwargs):
            res = func(**kwargs)

            if res is None or isinstance(res, controller.RenderParameter):
                view = ctrl.VIEW
                params = {}
                if res is not None:
                    params = res.params
                    if res.view is not None:
                        view = res.view

                res = render_template(view, **params)
            return res
        return internal

    endpoint = "{}:{}".format(path, ctrl.__class__.__name__)
    wsgi.app.add_url_rule(path, view_func=vf(ctrl.get), methods=["GET"], endpoint=endpoint+":GET")
    wsgi.app.add_url_rule(path, view_func=vf(ctrl.post), methods=["POST"], endpoint=endpoint+":POST")
    wsgi.app.add_url_rule(path, view_func=vf(ctrl.put), methods=["PUT"], endpoint=endpoint+":PUT")
    wsgi.app.add_url_rule(path, view_func=vf(ctrl.delete), methods=["DELETE"], endpoint=endpoint+":DELETE")


def route(path: str):
    """
    add router class to system as decorator
    :param path: url (see Flask reference)
    """
    def route_deco(cls):
        add_route(path, cls)
    return route_deco
