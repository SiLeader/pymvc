#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import wsgi
from .model_base import get_loaded_model


@wsgi.app.context_processor
def model_loader():
    """
    Flask (Jinja2) function for loading model data
    :return: Flask (Jinja2) functions
    """
    def load_one(model, primary=None, **query):
        """
        load one model's data
        :param model: model class name or snake case class name
        :param primary: primary key (optional)
        :param query: query (optional)
        :return: data or None
        """
        model = get_loaded_model(model)
        model = model.load(primary=primary, **query)
        return model

    def load_many(model, primary=None, **query):
        """
        load model's data
        :param model: model class name or snake case class name
        :param primary: primary key (optional)
        :param query: query (optional)
        :return: data list
        """
        model = get_loaded_model(model)
        model = model.load(multi=True, primary=primary, **query)
        return model

    return {"load_one": load_one, "load_many": load_many}
