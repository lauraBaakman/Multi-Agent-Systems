# -*- coding: utf-8 -*-

"""
This module can be used to build an abstract syntax tree.
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

class Knowledge(object):
    """Class to represent the knowledge operator."""

    def __init__(self, ast, agent):
        """Create an K node for an AST
        :param ast: the ast that hangs in the K node.
        :type ast: Ast
        :param agent: the number of the agent
        :type agent: int
        :return: a K node
        :rtype : node
        """