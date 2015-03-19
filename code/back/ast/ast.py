# -*- coding: utf-8 -*-

"""
Class that defines the abstract syntax tree
"""

__author__ = 'laura'

from logicparser import Parser
from tokenize import tokenizer

class Ast(object):
    """Class to represent an abstract syntax tree."""

    def __init__(self, tokens):
        """Create an AST from a list of tokens.
        :param tokens: the lsit of tokens to create an AST for.
        :type tokens: [Tokens]
        :return: an AST representing formula.
        :rtype : Ast
        """
        parser = Parser()
        self.root = parser.parse(tokens)

    def __repr__(self):
        """
        Print friendly representation of the AST object
        :return: string
        """
        return "Tree: {obj.root}".format(obj = self)

    @classmethod
    def from_string(cls, string, logic):
        try:
            tokens = tokenizer.tokenize(logic, string)
            return Ast(tokens)
        except:
            raise

    def is_true(self, model, state):
        return self.root.is_true(model, state)


