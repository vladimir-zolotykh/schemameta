#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        fields = getattr(cls, "_fields", [])
        for n, field in enumerate(fields):
            setattr(cls, field, itemgetter(n))


class _Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        assert len(args) == len(cls._fields)
        return super().__new__(cls, args)

    def __repr__(self):
        return f"{self.__class__.__name__}{super().__repr__()}"


class Point(_Tuple):
    _fields = ["x", "y"]


p = Point(3, 5)
print(p)
