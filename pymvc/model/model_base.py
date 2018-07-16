#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import re
import inspect

import pymongo

from . import datatypes
from ..settings import database


def _to_snake(name: str) -> str:
    name = re.sub("([A-Z])", r"_\1", name)
    return name.lower().strip("_")


class Model(abc.ABC):
    HOST = None
    PORT = None
    DATABASE = None
    COLLECTION = None

    def __init__(self, **key_value):
        cls = self.__class__

        if "__data" not in dir(cls):
            cls.__data = []
            cls.__primary_key = None

            for name in dir(self):
                ty = getattr(self, name)
                if isinstance(ty, datatypes.ModelTypeBase):
                    cls.__data.append((name, ty))
                    if ty.primary:
                        cls.__primary_key = (name, ty)

        for name, ty in cls.__data:
            value = ty.default
            if name in key_value:
                value = ty.create_instance(key_value[name])
            setattr(self, name, value)

    @classmethod
    def _setup(cls):
        if "__data" not in dir(cls):
            cls.__data = []
            cls.__primary_key = None

            for name in dir(cls):
                ty = getattr(cls, name)
                if isinstance(ty, datatypes.ModelTypeBase):
                    cls.__data.append((name, ty))
                    if ty.primary:
                        cls.__primary_key = (name, ty)

    @classmethod
    def __collection(cls):
        if "__collection_name" not in dir(cls):
            if cls.COLLECTION is None:
                cls.__collection_name = _to_snake(cls.__name__)
            else:
                cls.__collection_name = cls.COLLECTION
        if cls.HOST is None:
            cls.HOST = database.host
        if cls.PORT is None:
            cls.PORT = database.port

        if cls.DATABASE is None:
            cls.DATABASE = database.database

        client = pymongo.MongoClient(host=cls.HOST, port=cls.PORT, tz_aware=True)
        db = client[cls.DATABASE]
        return db[cls.__collection_name]

    @classmethod
    def load(cls, multi=False, primary=None, **key_value):
        cls._setup()
        query = key_value
        if primary is not None:
            name, _ = cls.__primary_key
            query = {name: primary}

        if not multi:
            data = cls.__collection().find_one(query)
            if data is None:
                return None
            return cls(**data)

        return [cls(**data) for data in cls.__collection().find(query)]

    def save(self):
        cls = self.__class__
        primary_name, _ = cls.__primary_key
        data = {}
        for name, ty in cls.__data:
            data[name] = ty.to_model_data(getattr(self, name))
        self.__collection().update_one({primary_name: data[primary_name]}, {"$set": data}, upsert=True)

    @classmethod
    def get_primary_key_name(cls):
        cls._setup()
        name, _ = cls.__primary_key
        return name


__imported_by = []


def load_loaded_models():
    classes = []
    for imported_by in __imported_by:
        classes.extend(inspect.getmembers(imported_by, inspect.isclass))  # lambda obj: issubclass(type(obj), Model)))
    return [cls for _, cls in classes if cls != Model if issubclass(cls, Model)]


__loaded_models = None


def get_loaded_models():
    global __loaded_models
    if __loaded_models is None:
        models = load_loaded_models()
        __loaded_models = {cls.__name__: cls for cls in models}
        __loaded_models.update({_to_snake(name): cls for name, cls in __loaded_models.items()})
    return __loaded_models


def get_loaded_model(name):
    return get_loaded_models()[name]


class TestData(Model):
    name = datatypes.StringType(default="cerussite")
    age = datatypes.IntType()


if __name__ == '__main__':
    test = TestData()
    print(test.name)
    get_loaded_models()
else:
    __imported_by.extend([inspect.getmodule(stack[0]) for stack in inspect.stack()])
