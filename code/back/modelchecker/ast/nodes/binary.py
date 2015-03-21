# -*- coding: utf-8 -*-
from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from conjunction import Conjunction
from disjunction import Disjunction
from implication import Implication
from biimplication import BiImplication

__author__ = 'laura'

class Binary(Node):

    def __init__(self, type, lhs=None, rhs=None):
        """
        Constructor for binary nodes
        :param token: binary token
        :return: Binary Node
        """
        self.type = type
        self.rhs = rhs
        self.lhs = lhs

    @classmethod
    def fromToken(cls, token):
        token_to_node = {
            operators.Binary.conjunction : Conjunction(),
            operators.Binary.disjunction: Disjunction(),
            operators.Binary.implication: Implication(),
            operators.Binary.biimplication: BiImplication(),
        }
        return token_to_node.get(token.type, cls(token.type))