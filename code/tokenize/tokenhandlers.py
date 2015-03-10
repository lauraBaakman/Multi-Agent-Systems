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
    string = remove_first_character(string)
    if (expected_underscore != '_'):
        raise tokenizer.ParseError(preceding_operator, '_', expected_underscore)
    return string


def read_leading_number(string):
    """
    Read the number with which the string starts.
    :param string: the string from which the number needs to be read
    :return: (the read number, the string without the leading number)
    """
    number_as_string = re.match(r'\d+', string).group()
    number = int(number_as_string)
    string_without_number = string[len(number_as_string):]
    return (number, string_without_number)


def remove_first_character(string):
    """
    Remove the first character of rest
    :param string: The string of which the first character needs to be removed.
    :return: rest with the first character removed
    """
    return string[1:]


def knows(rest):
    """
    Tokenize the Knows operator (K)
    :param rest: of the formula
    :return: (Knows token, rest)
    """
    print ("knows")

    rest = remove_first_character(rest)
    rest = read_underscore(rest, 'K')
    (digit, rest) = read_leading_number(rest)

    return tokens.Knows(digit), rest


def possible(rest):
    """
    Tokenize the Possible operator (M)
    :param rest: of the formula
    :return: (Knows token, rest)
    """
    print ("possible")


def common_knowledge(rest):
    """
    Tokenize the Common Knowledge operator (C)
    :param rest: of the formula
    :return: (Knows token, rest)
    """
    print ("common knowledge")
