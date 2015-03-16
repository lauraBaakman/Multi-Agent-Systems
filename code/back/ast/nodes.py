# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'


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
            "[{obj.type} ({obj.lhs})]".format(obj=self)
        )

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
            "[{obj.type}_{obj.agent} ({obj.lhs})]".format(obj=self)
        )


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
            "[({obj.lhs}) {obj.type} ({obj.rhs})]".format(obj=self)
        )

class Proposition(Node):

    def __init__(self, token):
        self.name = token.name

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.name}".format(obj=self)
        )
