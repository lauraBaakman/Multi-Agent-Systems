# -*- coding: utf-8 -*-
from modelchecker import operators
from modelchecker.ast.nodes.unary import Unary

__author__ = 'laura'


class Agent(Unary):

    def __init__(self, type, agent, lhs=None):
        """
        Constructor for Agent nodes
        :param token: unary token
        :return:
        """
        super(Agent, self).__init__(type, lhs)
        self.agent = agent

    @classmethod
    def fromToken(cls, token):
        return cls(token.type, token.agent)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type}_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        # TODO geeft true terug als er geen relaties zijn voor deze agent uit die staat, is dat correct?
        def knowledge(lhs, state, agent):
            truth_value = True
            for outgoing_relation in state.outgoing.get(agent, []):
                truth_value = lhs.is_true(outgoing_relation.destination)
                if not truth_value:
                    break
            return truth_value

        def possible(lhs, state, agent):
            return (
                Unary(
                    type=operators.Unary.negation,
                    lhs=Agent(
                        type=operators.Agent.knowledge,
                        agent=agent,
                        lhs=Unary(
                            type=operators.Unary.negation,
                            lhs=lhs
                        )
                    )
                ).is_true(state)
            )

        operator_to_function = {
            operators.Agent.knowledge: knowledge,
            operators.Agent.possible: possible
        }
        return operator_to_function.get(self.type)(self.lhs, state, self.agent)

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter} {operator}_{{\\text{{{agent}}}}}\\left({lhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            operator=self.type.to_latex(),
            agent=self.agent
        )