# -*- coding: utf-8 -*-

"""
Class that defines the abstract syntax tree
"""

__author__ = 'laura'


class Ast(object):
    """Class to represent an abstract syntax tree."""

    def __init__(self, formula):
        """Create an AST from formula.
        :param formula: the formula to create an AST for.
        :type formula: string
        :return: an AST representing formula.
        :rtype : Ast
        """
        print(formula)