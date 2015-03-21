# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'

from modelchecker import operators

def models(state, formula, delimiter=''):
    return "{delimiter}\left(M, \\text{{{state}}} \\right) \models {formula}{delimiter}".format(
        state=state.name,
        formula=formula.to_latex(),
        delimiter=delimiter
    )

class Node(object):
    """General node class"""

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
            return not lhs.is_true(state)

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
        def conjunction(lhs, rhs,  state):
            return lhs.is_true(state) and rhs.is_true(state)

        def disjunction(lhs, rhs, state):
            return lhs.is_true(state) or rhs.is_true(state)

        def implication(lhs, rhs, state):
            return (not lhs.is_true(state)) or rhs.is_true(state)

        def biimplication(lsh, rhs, state):
            return implication(lsh, rhs, state) and implication(rhs, lsh, state)

        operator_to_function = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)

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


class Proposition(Node):

    def __init__(self, name):
        self.name = name

    @classmethod
    def fromToken(cls, token):
        return cls(token.name)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.name}".format(obj=self)
        )

    def is_true(self, state):
        """
        Return true if this proposition is true in the passed state in the passed model.
        :param model: A model
        :param state: A state object
        :return: Boolean
        """
        try:
            truth_value = state.is_true(self.name)
            self._condition_conclusion(state, truth_value)
            return truth_value
        except:
            raise

    def _condition_conclusion(self, state, truth_value):

        def truth_condition(state, proposition, value):
            return '$\pi\left({state_name}\\right)\left( {prop_name} \\right) = {value}$'.format(
                state_name=state.name,
                prop_name=proposition.name,
                value=value
            )

        self.condition = '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=truth_condition(state, self, 1)
        )
        if truth_value:
            self.conclusion = '{models} holds since {condition}.'.format(
                models=models(state, self, '$'),
                condition=truth_condition(state, self, int(truth_value))
            )
        else:
            self.conclusion = '{models} does not hold since {condition}.'.format(
                models=models(state, self, '$'),
                condition=truth_condition(state, self, int(truth_value))
            )

    def to_latex(self, delimiter = ''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter}\\text{{{name}}}{delimiter}'.format(delimiter=delimiter, name=self.name)