# -*- coding: utf-8 -*-
from string import Template
import operator as op

from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from negation import Negation
from conjunction import Conjunction
from disjunction import Disjunction
from implication import Implication
from node import models


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
        }
        return token_to_node.get(token.type, cls(token.type))

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} {obj.type} {obj.rhs})".format(obj=self)
        )

    def _eval_rhs_and_lhs(self, state):
        lhs = self.lhs.is_true()
        rhs = self.rhs.is_true()



    def is_true(self, state):

        def biimplication(lhs, rhs, state):
            (truth_value, dict) =Conjunction(
                lhs=Binary(
                    type=operators.Binary.implication,
                    lhs=lhs,
                    rhs=rhs
                ),
                rhs=Binary(
                    type=operators.Binary.implication,
                    lhs=rhs,
                    rhs=lhs
                )
            ).is_true(state)
            dict['interlude'].insert(0, self._condition(state))
            return (truth_value, dict)

        operator_to_function = {
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)

    def _condition(self, state):
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state)
        )

    def _truth_condition(self, state):

        def biimplication():
            return '{lhs_models} and {rhs_models}'.format(
                lhs_models=models(state, Binary(operators.Binary.biimplication, self.lhs, self.rhs, '$')),
                rhs_models=models(state, Binary(operators.Binary.biimplication, self.rhs, self.lhs, '$')),
            )

        operator_to_condition = {
            operators.Binary.biimplication: biimplication
        }
        return operator_to_condition.get(self.type)(self, state)

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter}\\left({lhs}{operator}{rhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs = self.lhs.to_latex(),
            operator = self.type.to_latex(),
            rhs = self.rhs.to_latex()
        )