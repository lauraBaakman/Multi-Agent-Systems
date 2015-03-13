# -*- coding: utf-8 -*-

"""
Class that defines the abstract syntax tree
"""

__author__ = 'laura'

import tokenize.operators as operators

class Ast(object):
    """Class to represent an abstract syntax tree."""

    _precedence = {
        operators.Unary.common : 1,
        operators.Modal.knowledge : 1,
        operators.Modal.possible : 1,

        operators.Unary.negation : 2,

        operators.Binary.conjunction : 3,

        operators.Binary.disjunction : 4,

        operators.Binary.implication : 5,

        operators.Binary.biimplication : 6
    }

    def __init__(self, formula):
        """Create an AST from formula.
        :param formula: the formula to create an AST for.
        :type formula: string
        :return: an AST representing formula.
        :rtype : Ast
        """
        print(formula)