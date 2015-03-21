# -*- coding: utf-8 -*-
from modelchecker import operators
from modelchecker.ast.nodes.unary import Unary
from knowledge import Knowledge
from possible import Possible

__author__ = 'laura'


class Agent(Unary):

    @classmethod
    def fromToken(cls, token):
        token_to_node = {
            operators.Agent.knowledge : Knowledge,
            operators.Agent.possible : Possible,
        }
        return token_to_node.get(token.type)(token.agent)

