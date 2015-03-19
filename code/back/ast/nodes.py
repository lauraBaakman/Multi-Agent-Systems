# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'

from tokenize import operators

class Node(object):
    """General node class"""

class Unary(Node):

    def __init__(self, token):
        """
        Constructor for unary nodes
        :param token: unary token
        :return: Unary Node
        """
        self.type = token.type
        self.lhs = None

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type} {obj.lhs})".format(obj=self)
        )

    def is_true(self, model, state):
        raise NotImplementedError

class Agent(Unary):

    def __init__(self, token):
        """
        Constructor for Agent nodes
        :param token: unary token
        :return:
        """
        super(Unary, self).__init__(token)
        self.agent = token.agent
    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type}_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, model, state):
        raise NotImplementedError


class Binary(Node):

    def __init__(self, token):
        """
        Constructor for binary nodes
        :param token: binary token
        :return: Binary Node
        """
        self.type = token.type
        self.rhs = None
        self.lhs = None

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} {obj.type} {obj.rhs})".format(obj=self)
        )

    def is_true(self, model, state):
        def conjunction(lhs, rhs):
            return lhs.is_true() and rhs.is_true()

        def disjunction(lhs, rhs):
            return lhs.is_true() or rhs.is_true()

        def implication(lhs, rhs):
            return (not lhs.is_true()) or rhs.is_true()

        def biimplication(lsh, rhs):
            return conjunction(
                implication(lsh, rhs), implication(rhs, lsh)
            )

        operator_to_function = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs)


class Proposition(Node):

    def __init__(self, token):
        self.name = token.name

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.name}".format(obj=self)
        )

    def is_true(self, model, state):
        return model.get_state_by_name(state).is_true(self.name)