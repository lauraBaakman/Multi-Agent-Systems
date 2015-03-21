# -*- coding: utf-8 -*-
from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from modelchecker.ast.nodes import Common, Negation, Everybody
from node import models

__author__ = 'laura'


class Unary(Node):

    @classmethod
    def fromToken(cls, token):
        token_to_node = {
            operators.Unary.negation : Negation,
            operators.Unary.common: Common,
            operators.Unary.everybody: Everybody
        }
        return token_to_node.get(token.type)