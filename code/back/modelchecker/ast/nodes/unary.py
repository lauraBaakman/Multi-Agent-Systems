# -*- coding: utf-8 -*-
from modelchecker.ast.nodes.node import Node

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