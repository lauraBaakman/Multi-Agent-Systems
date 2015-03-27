# coding=utf-8

"""."""
import re

from modelchecker.operators import Binary, Unary, Agent
from modelchecker.errors import TokenizeError
from modelchecker.tokenize import tokens
from modelchecker import config


def _get_lexicon(logic):
    """
    Select the lexicon for the scanner based on the logic.
    :param logic: the logic to be used, options: KM, S5, S5EC
    :return: list[(regular_expression, lambda function)]
    """
    agent_expressions = [
        (config.agent['knowledge'], lambda scanner, token: tokens.AgentOperator(token, Agent.knowledge)),
        (config.agent['possible'],  lambda scanner, token: tokens.AgentOperator(token, Agent.possible))
    ]

    EC_expressions = [
        (config.group['common'],       lambda scanner, _: tokens.UnaryOperator(Unary.common)),
        (config.group['everybody'],    lambda scanner, _: tokens.UnaryOperator(Unary.everybody))
    ]
    EC_expressions.extend(agent_expressions)

    I_expressions = [
        (config.group['implicit'], lambda scanner, _: tokens.UnaryOperator(Unary.implicit)),
    ]
    I_expressions.extend(agent_expressions)

    expressions_per_logic = {
        "K":   agent_expressions,
        "T": agent_expressions,
        "S4": agent_expressions,
        "S5": agent_expressions,

        "KEC": EC_expressions,
        "TEC": EC_expressions,
        "S4EC": EC_expressions,
        "S5EC": EC_expressions,

        "KI": I_expressions,
        "TI": I_expressions,
        "S4I": I_expressions,
        "S5I": I_expressions,
    }

    expressions = [
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(Binary.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(Binary.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(Binary.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(Binary.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.UnaryOperator(Unary.negation)),
        (r"[a-z][a-zA-Z1-9]*",                     lambda scanner,  token: tokens.Proposition(token)),
        (r"[[{(<]",                                lambda scanner,      _: tokens.BracketOpen()),
        (r"[]})>]",                                lambda scanner,      _: tokens.BracketClose()),
        (r"\s+",                                   None), # None == skip token.
    ]

    expressions.extend(expressions_per_logic.get(logic, []))
    return expressions

def tokenize(logic, string):
    """
    Tokenize the inputted string to a list of tokens
    :param loigc: The logic of the string, options: KM, S5, S5EC
    :param string: The string to be converted to tokens.
    :raise TokenizeError: if a unknown character is in the string.
    :return:[object]
    """
    regular_expressions = _get_lexicon(logic);
    scan = re.Scanner(regular_expressions)
    results, remainder=scan.scan(string)

    if remainder:
        msg = "Could not parse some part of the expression \"...{expression}\", you probably " \
              "used an operator that is not defined (for this logic).".format(expression = remainder)
        raise TokenizeError(remainder, msg)
    return results