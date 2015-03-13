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

class Proposition(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "PROPOSITION({obj.name})".format(obj=self)
        )

class BinaryOperator(object):

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BINOP({obj.type})".format(obj=self)
        )

class UnaryOperator(object):

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "UNOP({obj.type})".format(obj=self)
        )


class Knowledge(object):

    def __init__(self, string):
        """
        Token for the knowledge operator.
        :param string: the string representing the knowledge operator.
        :return: Knowledge token
        """
        self.agent = get_agent_from_string(string)

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "K_({obj.agent})".format(obj=self)
        )

class Possible(object):

    def __init__(self, string):
        """
        Token for the possible operator.
        :param string: the string representing the possible operator.
        :return: Possible token
        """
        self.agent = get_agent_from_string(string)

    def __repr__(self):
        """Print-friendly representation."""
        return (
            "M_({obj.agent})".format(obj=self)
        )

class BracketOpen():
    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BRACKET_OPEN"
        )

class BracketClose():
    def __repr__(self):
        """Print-friendly representation."""
        return (
            "BRACKET_CLOSE"
        )
