# -*- coding: utf-8 -*-
from modelchecker.ast.nodes.unary import Unary

__author__ = 'laura'


class Agent(Unary):
    def __init__(self, agent, lhs=None):
        super(Agent, self).__init__(lhs)
        self.agent = agent


    def to_latex(self, delimiter='', operator="AGENTOPERATOR"):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        operator_with_agent = '{operator}_{{\text{{{agent}}}}}'.format(operator=operator, agent=self.agent)
        return super(Agent, self).to_latex(delimiter, operator_with_agent)