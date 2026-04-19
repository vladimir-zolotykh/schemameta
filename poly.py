#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, *args):
        super().__init__(*args)
        for n, field in enumerate(cls._fields):
            setattr(cls, field, itemgetter(n))


class Poly(tuple):
    def __new__(cls, *args):
        # turn super(Poly, cls).__new__(cls, args)
        return super().__new__(cls, args)

    def __repr__(self):
        return f"Poly{super().__repr__()}"


class Point(Poly, metaclass=TupleMeta):
    _fields = ["x", "y"]


poly = Poly(3, 5)
print(poly)
