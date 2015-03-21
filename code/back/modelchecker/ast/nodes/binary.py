# -*- coding: utf-8 -*-
from string import Template
from modelchecker import operators
from modelchecker.ast.nodes.node import Node
from modelchecker.ast.nodes.unary import Unary
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
        return cls(token.type)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} {obj.type} {obj.rhs})".format(obj=self)
        )

    def is_true(self, state):
        # TODO handle code duplication
        def conjunction(lhs, rhs,  state):
            lhs_truth_value = lhs.is_true(state)
            rhs_truth_value = rhs.is_true(state)
            truth_value = lhs_truth_value and rhs_truth_value
            self._set_condition(state)
            self._set_conclusion(state, lhs_truth_value, rhs_truth_value, truth_value)
            return truth_value

        def disjunction(lhs, rhs, state):
            lhs_truth_value = lhs.is_true(state)
            rhs_truth_value = rhs.is_true(state)
            truth_value = lhs_truth_value or rhs_truth_value
            self._set_condition(state)
            self._set_conclusion(state, lhs_truth_value, rhs_truth_value, truth_value)
            return truth_value

        def implication(lhs, rhs, state):
            return Binary(
                    type=operators.Binary.disjunction,
                    lhs=Unary(
                        operators.Unary.negation,
                        lhs
                    ),
                    rhs=rhs
                ).is_true(state)

        def biimplication(lhs, rhs, state):
            return Binary(
                type=operators.Binary.conjunction,
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

        operator_to_function = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)

    def _set_condition(self, state):
        self.condition = '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state, 1)
        )

    def _truth_condition(self, state, value):
        def conjunction(self, state, value):
            return '{lhs_models} and {rhs_models}'.format(
                lhs_models=models(state, self.lhs, '$'),
                rhs_models=models(state, self.rhs, '$'),
            )

        def disjunction(self, state, value):
            return '{lhs_models} or {rhs_models}'.format(
                lhs_models=models(state, self.lhs, '$'),
                rhs_models=models(state, self.rhs, '$'),
            )

        def implication():
            raise NotImplementedError

        def biimplication():
            raise NotImplementedError

        operator_to_condition = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_condition.get(self.type)(self, state, value)

    def _set_conclusion(self, state, lhs_truth_value, rhs_truth_value, truth_value):
        def conjunction(self, state, lhs_truth_value, rhs_truth_value, truth_value):
            if (truth_value):
                self.conclusion = '{models} holds since {condition}.'.format(
                    models=models(state, self, '$'),
                    condition=self._truth_condition(state, int(truth_value))
                )
            else:
                conclusion = Template('$models does not hold since $reason.')

                if lhs_truth_value:
                    reason = '{condition} does not hold'.format(condition=models(state, self.rhs, '$'))
                elif rhs_truth_value:
                    reason = '{condition} does not hold'.format(condition=models(state, self.lhs, '$'))
                else:
                    reason = '{condition_lhs} and {condition_rhs} do not hold'.format(
                        condition_lhs=models(state, self.lhs, '$'),
                        condition_rhs=models(state, self.rhs, '$')
                    )
                self.conclusion = conclusion.substitute(reason=reason, models=models(state, self, '$'))

        def disjunction(self, state, lhs_truth_value, rhs_truth_value, truth_value):
            if (lhs_truth_value):
                self.conclusion = '{models} holds since {condition}.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.lhs, '$')
                )
            elif rhs_truth_value:
                self.conclusion = '{models} holds since {condition}.'.format(
                    models=models(state, self, '$'),
                    condition=models(state, self.rhs, '$')
                )
            else:
                self.conclusion = '{models} does not hold since neither {condition_lhs} nor {condition_rhs} holds.'.format(
                    models=models(state, self, '$'),
                    condition_lhs=models(state, self.lhs, '$'),
                    condition_rhs=models(state, self.rhs, '$')
                )

        def implication():
            raise NotImplementedError

        def biimplication():
            raise NotImplementedError

        operator_to_condition = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        operator_to_condition.get(self.type)(self, state, lhs_truth_value, rhs_truth_value, truth_value)

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