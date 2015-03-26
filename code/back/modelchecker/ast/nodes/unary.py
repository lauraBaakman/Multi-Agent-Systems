# -*- coding: utf-8 -*-
from modelchecker.ast.nodes.node import Node, models

__author__ = 'laura'

class Unary(Node):
    def __init__(self, lhs):
        self.lhs = lhs

    def to_latex(self, delimiter, operator):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter} {operator} \left({lhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            operator=operator
        )

    def is_leaf(self):
        return False

    def _is_true_one_relation(self, evaluation_state, destination_state):
        (truth_value, motivation) = self.lhs.is_true(destination_state)
        return (
            truth_value,
            {
                'condition': self._condition(evaluation_state),
                'interlude': [motivation],
                'conclusion': self._conclusion_one_relation(evaluation_state, truth_value, destination_state)
            }
        )

    def _is_true_no_relation(self, evaluation_state):
        return (
            True,
            {
                'condition': self._condition(evaluation_state),
                'conclusion': self._conclusion_no_relations(evaluation_state),
            }
        )

    def _is_true_multiple_relations(self, evaluation_state, destination_states):
        interlude = []
        for destination in destination_states:
            (destination_truth_value, destination_motivation) = self.lhs.is_true(destination)
            if destination_truth_value:
                interlude.append(destination_motivation)
                truth_value = destination_truth_value
            else:
                truth_value = destination_truth_value
                interlude = [destination_motivation]
                conclusion = self._conclusion_one_relation(evaluation_state, truth_value, destination)
                break
        if truth_value:
            conclusion = self._conclusion_multiple_relations(evaluation_state, destination_states)

        return (
            truth_value,
            {
                'condition': self._condition(evaluation_state),
                'interlude': interlude,
                'conclusion': conclusion,
            }
        )

    def _conclusion_one_relation(self, evaluation_state, truth_value, destination_state):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        if (truth_value):
            return '{models} holds since {condition} holds.'.format(
                models=models(evaluation_state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )
        else:
            return '{models} does not hold since {condition} does not hold.'.format(
                models=models(evaluation_state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )

    def _conclusion_multiple_relations(self, evaluation_state, destination_states):
        conclusion = '{models} holds since '.format(
            models=models(evaluation_state, self, '$'),
        )
        for state_idx in range(len(destination_states) - 1):
            destination_state = destination_states[state_idx].name
            conclusion = '{old_conclusion} {models}, '.format(
                old_conclusion=conclusion,
                models=models(destination_state, self.lhs, '$'),
            )
        return '{old_conclusion} and {models}.'.format(
            old_conclusion=conclusion,
            models=models(destination_states.pop().name, self.lhs, '$'),
        )