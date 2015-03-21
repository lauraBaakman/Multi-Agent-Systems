# -*- coding: utf-8 -*-
from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from node import models

__author__ = 'laura'


class Unary(Node):

    def __init__(self, type, lhs=None):
        """
        Constructor for unary nodes
        :param token: unary token
        :return: Unary Node
        """
        self.type = type
        self.lhs = lhs

    @classmethod
    def fromToken(cls, token):
        return cls(token.type)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        def negation(lhs, state):
            (lhs_truth_value, lhs_result) = lhs.is_true(state)
            truth_value = not lhs_truth_value
            return (
                truth_value,
                {
                    'condition': self._condition(state),
                    'interlude': [lhs_result],
                    'conclusion': self._conclusion(state, truth_value),
                }
            )

        def common(lhs, state):
            # TODO implement
            raise NotImplementedError

        def everybody(lhs, state):
            #TODO implement
            raise NotImplementedError

        operator_to_function = {
            operators.Unary.negation: negation,
            operators.Unary.common: common,
            operators.Unary.everybody: everybody
        }
        return operator_to_function.get(self.type)(self.lhs, state)

    def _truth_condition(self, state):
        def negation(self, state):
            return 'not {lhs_models}'.format(
                lhs_models=models(state, self.lhs, '$'),
            )

        def common(lhs, state):
            # TODO implement
            raise NotImplementedError

        def everybody(lhs, state):
            # TODO implement
            raise NotImplementedError

        operator_to_function = {
            operators.Unary.negation: negation,
            operators.Unary.common: common,
            operators.Unary.everybody: everybody
        }
        return operator_to_function.get(self.type)(self, state)

    def _condition(self, state):
        # TODO _condition naar node trekken
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state)
        )

    def _conclusion(self, state, truth_value):
        def negation(self, state, truth_value):
            if(truth_value):
                return '{models} holds since {condition} does not hold.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.lhs, '$')
                )
            else:
                return '{models} does not hold since {condition} holds.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.lhs, '$')
                )

        def common(lhs, state):
            # TODO implement
            raise NotImplementedError

        def everybody(lhs, state):
            # TODO implement
            raise NotImplementedError

        operator_to_function = {
            operators.Unary.negation: negation,
            operators.Unary.common: common,
            operators.Unary.everybody: everybody
        }
        return operator_to_function.get(self.type)(self, state, truth_value)

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter} {operator}\\left({lhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            operator=self.type.to_latex()
        )