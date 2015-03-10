# -*- coding: utf-8 -*-

"""
This module tokenizes a string
"""

__author__ = 'laura'

from enum import Enum

import tokenhandlers as token_handler


class ParseError(Exception):
    """Parse errors"""

    def __init__(self, **kwargs):
        """
        Create a parse error.
        :param kwargs: Either the message as a string, under the keyword message, or the expected, read, and previous
        character with the keys forward, expected, read.
        :return ParseError
        """
        if(kwargs.has_key('message')):
            message = kwargs['message']
        else:
            message = 'After "{forward}" "{expected}" is expected not "{read}"'.format(
                forward = kwargs.get('forward', '?'),
                expected = kwargs.get('expected', '?'),
                read = kwargs.get('read', '?')
            )
        super(Exception, self).__init__(message)


class LogicError(Exception):
    """Logic errors"""
    pass


class BinaryOperators(Enum):
    or_op = "|"
    and_op = "&"
    implication_op = "->"
    bi_implication_op = "<->"


def select_parser(logic):
    """
    Select the logic to be used.
    :param logic: The name of the logic as a string, options: KM, S5, S5EC
    :return: Dictionary with the parse functions.
    """

    km = {
        'K': token_handler.knows_handler,
        'M': token_handler.possible_handler,
        'T': token_handler.true_handler,
        'F': token_handler.false_handler,

        '(': token_handler.bracket_open_handler,
        ')': token_handler.bracket_close_handler,

        '&': token_handler.simple_binary_handler,
        '|': token_handler.simple_binary_handler,

        '-': token_handler.implication_handler,
        '<': token_handler.bi_implication_handler,

        '!': token_handler.not_handler,

        ' ': token_handler.space_handler,
        '\t': token_handler.space_handler,
        '\n': token_handler.space_handler
    }

    km_copy = km.copy()
    ec_part = {
        'C': token_handler.common_knowledge_handler
    }
    ec = km_copy.update(ec_part)

    logic_to_parser_functions_mapping = {
        "KM": km,
        "S5": km,
        "S5EC": ec
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
    rest = formula.strip()
    tokens = []
    while rest:
        (token, rest) = token_handlers.get(rest[0], token_handler.proposition_handler)(rest)
        if token:
            tokens.append(token)
    return tokens