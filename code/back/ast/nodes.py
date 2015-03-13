# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'


class Node(object):
    """General node class"""

class Unary(Node):

    def __init__(self, type, child):
        """
        Constructor for unary nodes
        :param type: member of the enum Operators.Unary, denotes the type of the operator.
        :param child: the formula after the unary operator
        :return: Unary Node
        """
        self.type = type
        self.child = child

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.type} ({obj.child})".format(obj=self)
        )

class Modal(Unary):

    def __init__(self, type, agent, child,):
        """
        Constructor for Modal nodes
        :param type: member of the enum Operators.Modal
        :param agent:
        :param child:
        :return:
        """
        super(Unary, self).__init__(type, child)
        self.agent = agent



class Binary(Node):

    def __init__(self, type, lhs, rhs):
        """
        Constructor for binary nodes
        :param type: member of the enum Operators.Binary, denotes the type of the operator.
        :param lhs: formula on the left of the operator in infix notation
        :param rhs: formula on the right of the operator in infix notation
        :return: Unary Node
        """
        self.type = type
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs}) {obj.type} ({obj.rhs})".format(obj=self)
        )