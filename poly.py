#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        for n, field in enumerate(cls._fields):
            setattr(cls, field, itemgetter(n))


class _Tuple(tuple):
    def __new__(cls, *args):
        assert len(args) == len(cls._fields)
        print(f"{cls = }")
        return super().__new__(cls, args)

    def __repr__(self):
        return f"{self.__class__.__name__}{super().__repr__()}"


class Point(_Tuple, metaclass=TupleMeta):
    _fields = ["x", "y"]


p = Point(3, 5)
print(p)
