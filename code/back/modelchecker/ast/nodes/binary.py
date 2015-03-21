# -*- coding: utf-8 -*-
from string import Template
import operator as op

from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from negation import Negation
from conjunction import  Conjunction
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
            operators.Binary.conjunction : Conjunction,
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

        def simple_binary(lhs, rhs, state, operator):
            (lhs_truth_value, lhs_result) = lhs.is_true(state)
            (rhs_truth_value, rhs_result) = rhs.is_true(state)
            truth_value = operator(lhs_truth_value, rhs_truth_value)
            return (
                truth_value,
                {
                    'condition': self._condition(state),
                    'interlude': [lhs_result, rhs_result],
                    'conclusion': self._conclusion(state, lhs_truth_value, rhs_truth_value, truth_value),
                }
            )

        def disjunction(lhs, rhs, state):
            return simple_binary(lhs, rhs, state, op.or_)

        def implication(lhs, rhs, state):
            (truth_value, dict) =  Binary(
                    type=operators.Binary.disjunction,
                    lhs=Negation(
                        lhs
                    ),
                    rhs=rhs
                ).is_true(state)
            dict['interlude'].insert(0, self._condition(state))
            return (truth_value, dict)

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
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)

    def _condition(self, state):
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state)
        )

    def _truth_condition(self, state):

        def disjunction(self, state):
            return '{lhs_models} or {rhs_models}'.format(
                lhs_models=models(state, self.lhs, '$'),
                rhs_models=models(state, self.rhs, '$'),
            )

        def implication(self, state):
            return 'not {lhs_models} or {rhs_models}'.format(
                lhs_models=models(state, self.lhs, '$'),
                rhs_models=models(state, self.rhs, '$'),
            )

        def biimplication():
            return '{lhs_models} and {rhs_models}'.format(
                lhs_models=models(state, Binary(operators.Binary.biimplication, self.lhs, self.rhs, '$')),
                rhs_models=models(state, Binary(operators.Binary.biimplication, self.rhs, self.lhs, '$')),
            )

        operator_to_condition = {
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_condition.get(self.type)(self, state)

    def _conclusion(self, state, lhs_truth_value, rhs_truth_value, truth_value):

        def disjunction(self, state, lhs_truth_value, rhs_truth_value, truth_value):
            if (lhs_truth_value):
                return '{models} holds since {condition}.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.lhs, '$')
                )
            elif rhs_truth_value:
                return '{models} holds since {condition}.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.rhs, '$')
                )
            else:
                return '{models} does not hold since neither {condition_lhs} nor {condition_rhs} holds.'.format(
                    models=models(state, self, '$'),
                    condition_lhs=models(state, self.lhs, '$'),
                    condition_rhs=models(state, self.rhs, '$')
                )

        operator_to_condition = {
            operators.Binary.disjunction: disjunction,
        }
        return operator_to_condition.get(self.type)(self, state, lhs_truth_value, rhs_truth_value, truth_value)

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