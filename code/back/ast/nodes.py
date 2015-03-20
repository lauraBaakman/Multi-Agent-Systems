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

    def is_true(self, state):
        def conjunction(lhs, rhs,  state):
            return lhs.is_true(state) and rhs.is_true(state)

        def disjunction(lhs, rhs, state):
            return lhs.is_true(state) or rhs.is_true(state)

        def implication(lhs, rhs, state):
            return (not lhs.is_true(state)) or rhs.is_true(state)

        def biimplication(lsh, rhs, state):
            return implication(lsh, rhs, state) and implication(rhs, lsh, state)

        operator_to_function = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)


class Proposition(Node):

    def __init__(self, token):
        self.name = token.name

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.name}".format(obj=self)
        )

    def is_true(self, state):
        """
        Return true if this proposition is true in the passed state in the passed model.
        :param model: A model
        :param state: A state object
        :return: Boolean
        """
        try:
            return state.is_true(self.name)
        except:
            raise

