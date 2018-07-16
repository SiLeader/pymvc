#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

from flask import render_template
from flask import url_for as flask_url_for

from . import wsgi, controller


__routes = {}


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
    __routes[ctrl.__class__.__name__] = endpoint+":GET"

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


def url_for(ctrl: typing.Union[controller.Controller, str, typing.Type], **kwargs):
    if not isinstance(ctrl, str):
        if isinstance(ctrl, controller.Controller):
            ctrl = ctrl.__class__.__name__
        else:
            ctrl = ctrl.__name__
    return flask_url_for(__routes[ctrl], **kwargs)


@wsgi.app.context_processor
def url_for_function():
    return {"url_for": url_for}
    pass
