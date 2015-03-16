# -*- coding: utf-8 -*-

"""
Class that defines the abstract syntax tree
"""

__author__ = 'laura'

from parser import  Parser
import nodes

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
        return "Tree: {tree}".format(tree = self._tree_repr())

    def _tree_repr(self):
        """
        Print friendly representation of the AST
        :return: string
        """
        if isinstance(self.root, nodes.Binary):
            return "({obj.type} [{obj.lhs}], [{obj.rhs}])".format(obj=self.root)
        else:
            return "({obj.type} [{obj.lhs}])".format(obj=self.root)



