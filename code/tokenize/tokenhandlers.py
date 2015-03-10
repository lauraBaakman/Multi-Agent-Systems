# -*- coding: utf-8 -*-

"""
Functions that handle the different tokens
"""

import re

import tokenizer
import tokens

__author__ = 'laura'


def read_underscore(string, preceding_operator):
    """
    Read an underscore
    :param string: the formula
    :param preceding_operator: the formula that has been read before the underscore
    :return: rest with the underscore removed
    """
    expected_underscore = string[0]
    if expected_underscore != '_':
        raise tokenizer.ParseError(preceding_operator, '_', expected_underscore)
    string, _ = remove_first_character(string)
    return string

def read_implication(string):
    """
    Read an implication ->
    :param string: the formula
    :return: string with the implication removed
    """
    string, _ = remove_first_character(string)
    expected_pointy_bracket = string[0]
    if (expected_pointy_bracket != '>'):
        raise tokenizer.ParseError('-', '>', expected_pointy_bracket)
    string, _ = remove_first_character(string)
    return string

def read_bi_implication(string):
    """
    Read an biimplication <->
    :param string: the formula
    :return: string with the implication removed
    """
    string, _ = remove_first_character(string)

    # read dash
    expected_dash = string[0]
    if (expected_dash != '-'):
        raise tokenizer.ParseError('<', '-', expected_dash)
    string, _ = remove_first_character(string)

    # read ending pointy bracket
    expected_pointy_bracket = string[0]
    if (expected_pointy_bracket != '>'):
        raise tokenizer.ParseError('-', '>', expected_pointy_bracket)
    string, _ = remove_first_character(string)
    return string

def read_leading_number(string):
    """
    Read the number with which the string starts.
    :param string: the string from which the number needs to be read
    :return: (the read number, the string without the leading number)
    """
    number_as_string = re.match(r'\d+', string)
    if not number_as_string:
        raise tokenizer.ParseError("_", "a number", string[0])
    number = int(number_as_string.group())
    string_without_number = string[len(number_as_string):]
    return (number, string_without_number)

def remove_first_character(string):
    """
    Remove the first character of rest
    :rtype : [char]
    :param string: The string of which the first character needs to be removed.
    :return: rest with the first character removed
    """
    return string[1:], string[0]

def read_proposition(string):
    pass
    # expected_lowercase_character = string[0]
    # if  not expected_lowercase_character.isLower():
    #     # TODO Adapt parse error so that it accepts kwargs.
    #     raise Error("Propositions should start with a lowercase letter, after that they may contain letters in any case, underscores and numbers.")
    # re.match(r'\d+', string).group()
    # #  Read first characters: first character is lowercase rest may be: lowercase, number, uppercase, underscore, or dash
    #
    # return proposition, rest




def knows_handler(rest):
    """
    Tokenize the Knows operator (K)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    rest = read_underscore(rest, 'K')
    (digit, rest) = read_leading_number(rest)

    return tokens.KnowsToken(digit), rest

def possible_handler(rest):
    """
    Tokenize the Possible operator (M)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    rest = read_underscore(rest, 'M')
    (agent, rest) = read_leading_number(rest)

    return tokens.PossibleToken(agent), rest

def common_knowledge_handler(rest):
    """
    Tokenize the Common Knowledge operator (C)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.CommonKnowledgeToken(), rest

def true_handler(rest):
    """
    Tokenize the Truth (T)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.TrueToken(), rest

def false_handler(rest):
    """
    Tokenize the Falsum (F)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.FalseToken(), rest

def bracket_open_handler(rest):
    """
    Tokenize the bracket open (()
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.BracketOpen(), rest

def bracket_close_handler(rest):
    """
    Tokenize the bracket close ())
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.BracketClose(), rest

def simple_binary_handler(rest):
    """
    Tokenize the simple binary operators
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, character = remove_first_character(rest)
    return tokens.BinaryOperator(character), rest

def implication_handler(rest):
    """
    Tokenize the implication (->)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest = read_implication(rest)
    return tokens.BinaryOperator('->'), rest

def bi_implication_handler(rest):
    """
    Tokenize the implication (->)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest = read_bi_implication(rest)
    return tokens.BinaryOperator('<->'), rest

def not_handler(rest):
    """
    Tokenize the negation (!)
    :param rest: of the formula
    :return: (token, rest)
    """
    rest, _ = remove_first_character(rest)
    return tokens.NotOperator(), rest

def space_handler(rest):
    """
    Read white space
    :param rest: the string with leading white space
    :return: (None, rest)
    """
    rest = rest.lstrip()
    return None, rest

def proposition_handler(rest):
    rest, proposition = read_proposition(rest)
    return tokens.PropositionToken(proposition), rest
