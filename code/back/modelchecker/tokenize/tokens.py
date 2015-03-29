# coding=utf-8

"""
Definition of the different tokens the tokenizer generates
"""

import re

def get_agent_from_string(string):
    """
    Get the agent from a string.
    :param string: the string with the agent
    :return:the number of the agent
    """
    return re.search(r"\d+", string).group()

class Token(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        return hash(self.__dict__)

class Proposition(Token):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "PROPOSITION({obj.name})".format(obj=self)
        )

class BinaryOperator(Token):

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BINOP({obj.type})".format(obj=self)
        )

class UnaryOperator(Token):

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "UNOP({obj.type})".format(obj=self)
        )


class AgentOperator(Token):

    def __init__(self, string, type):
        """
        Token for the knowledge operator.
        :param string: the string representing the knowledge operator.
        :param type: the type of the operator, as part of the enum agent
        :return: Knowledge token
        """
        self.agent = get_agent_from_string(string)
        self.type = type

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "AGENTOP({obj.type})_{obj.agent}".format(obj=self)
        )

class BracketOpen(Token):
    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BRACKET_OPEN"
        )

class BracketClose(Token):
    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BRACKET_CLOSE"
        )
