# -*- coding: utf-8 -*-

__author__ = 'laura'


class ModelError(Exception):
    """ Exception raised for errors in the models."""
    pass

class ValuationError(Exception):
    """ Exception raised for erros in valuation."""
    pass


class TokenizeError(IOError):
    """
    Exception raised when the string cannot be tokenized.
    """

    def __init__(self, expr, msg):
        """
        Constructor for TokenizeError
        :param expr: input expression in which the error occurred
        :param msg: explanation of the error
        """
        self.expr = expr
        self.msg = msg


class ParserError(IOError):
    """
    Exception raised when the string cannot be parsed
    """

    def __init__(self, msg):
        """
        Constructor for TokenizeError
        :param msg: explanation of the error
        """
        self.msg = msg