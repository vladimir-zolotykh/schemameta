#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Poly(tuple):
    def __new__(cls, *args):
        # turn super(Poly, cls).__new__(cls, args)
        return super().__new__(cls, args)

    def __repr__(self):
        return f"Poly{super().__repr__()}"


poly = Poly(1, 2, 3)
print(poly)
