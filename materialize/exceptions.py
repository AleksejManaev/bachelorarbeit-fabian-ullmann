# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MaterializeException(Exception):
    """
    Any exception from this package
    """
    pass


class MaterializeError(MaterializeException):
    """
    Any exception that is an error
    """
    pass
