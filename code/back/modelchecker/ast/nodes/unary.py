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
        return '{delimiter} {operator} \left({lhs}\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            operator=operator
        )