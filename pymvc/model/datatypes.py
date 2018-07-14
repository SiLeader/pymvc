#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
import abc
import uuid


class ModelTypeBase(abc.ABC):
    """
    Model data type.
    """

    def __init__(self, primary: bool=False, non_null: bool=False, unique: bool=False, default=None):
        """
        Initializer
        :param primary: is primary key
        :param non_null: not null value
        :param unique: unique value
        """
        self.__primary = primary
        self.__non_null = non_null
        self.__unique = unique
        if non_null and default is None:
            raise TypeError("type specified non null but default value is None or not specified")

        if primary:
            self.__unique = True
            self.__non_null = True

        if default is not None and not isinstance(default, self.type):
            raise TypeError(
                "default value type is not compatible with specified type.\n"
                "type(default)={}, specified type={}".format(type(default), self.type)
            )
        self.__default = default

    @property
    def primary(self) -> bool:
        """
        is primary key
        :return: is primary key
        """
        return self.__primary

    @property
    def non_null(self) -> bool:
        """
        is non null
        :return: is non null
        """
        return self.__non_null

    @property
    def unique(self) -> bool:
        """
        is unique value
        :return: is unique value
        """
        return self.__unique

    @property
    @abc.abstractmethod
    def type(self) -> typing.Type:
        """
        value type
        :return: value type
        """
        pass

    def create_instance(self, value):
        """
        create specified instance
        :param value: value
        :return: data instance
        """
        return value

    def to_model_data(self, value):
        """
        convert to model data
        :param value: original value
        :return: data
        """
        return value

    @property
    def default(self):
        return self.__default


class StringType(ModelTypeBase):
    """
    String type
    """
    @property
    def type(self) -> typing.Type:
        return str


class IntType(ModelTypeBase):
    """
    integer type
    """
    @property
    def type(self) -> typing.Type:
        return int


class FloatType(ModelTypeBase):
    """
    float type
    """
    @property
    def type(self) -> typing.Type:
        return float


class UniqueIdType(ModelTypeBase):
    """
    UUID data type
    """
    def __init__(self, primary: bool=False, non_null: bool=False, unique: bool=False, default: uuid.UUID=uuid.uuid4()):
        super(UniqueIdType, self).__init__(primary, non_null, unique, default)

    @property
    def type(self):
        return uuid.UUID

    def create_instance(self, value):
        return uuid.UUID(value)

    def to_model_data(self, value):
        return str(value)


class ListType(ModelTypeBase):
    """
    List type
    """
    @property
    def type(self) -> typing.Type:
        return list


class ForeignType(ModelTypeBase):
    """
    Foreign model value type
    """
    def __init__(self, model, model_primary_key=None,
                 primary: bool=False, non_null: bool=False, unique: bool=False, default=None):
        """
        constructor
        :param model: model name or model class
        :param model_primary_key: primary key (optional)
        :param primary: this item is primary
        :param non_null: non null value
        :param unique: unique value
        :param default: default value
        """
        super(ForeignType, self).__init__(primary, non_null, unique, default)

        from pymvc.model import model_base as mb

        if isinstance(model, str):
            model = mb.get_loaded_model(model)
        self.__model = model

        if model_primary_key is None:
            model_primary_key = self.__model.get_primary_key_name()
        self.__model_primary_key = model_primary_key

    def create_instance(self, value):
        return self.__model.load(**{self.__model_primary_key: value})

    def to_model_data(self, value):
        return getattr(value, self.__model_primary_key)

    @property
    def type(self):
        return self.__model
