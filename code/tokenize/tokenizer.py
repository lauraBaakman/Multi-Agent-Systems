# -*- coding: utf-8 -*-

"""
This module tokenizes a string
"""

__author__ = 'laura'

import tokenhandlers as ops


class ParseError(Exception):
    """Parse errors"""

    def __init__(self, forward_character, expected_character, read_character):
        # Call the base class constructor with the parameters it needs
        message = 'After "{forward}" "{expected}" is expected not "{read}"'.format(
            forward=forward_character, expected=expected_character, read=read_character
        )
        super(Exception, self).__init__(message)


class LogicError(Exception):
    """Logic errors"""
    pass


def select_parser(logic):
    """
    Select the logic to be used.
    :param logic: The name of the logic as a string, options: KM, S5, S5EC
    :return: Dictionary with the parse functions.
    """

    km = {
        'K': ops.knows,
        'M': ops.possible,
    }

    ec = {
        'C': ops.common_knowledge
    }

    logic_to_parser_functions_mapping = {
        "KM": km,
        "S5": km,
        "S5EC": km.update(ec)
    }
    parser = logic_to_parser_functions_mapping.get(logic)

    if parser is None:
        raise ('The logic {logic} is not supported'.format(logic=logic))

    return parser


def tokenize(formula, logic="KM"):
    """
    Tokenize the formula.
    :param formula: A formula in the logic of your choice to be tokenized.
    :return: List of tokens
    :param logic: The logic to be parsed as a string, options: KM, S5, S5EC. Default: KM
    :type logic: String
    """
    token_handlers = select_parser(logic)
    rest = formula
    tokens = []
    while rest:
        (token, rest) = token_handlers.get(rest[0])(rest)
        tokens.append(token)
    return tokens