"""."""
from enum import Enum
import re


import config
import tokens

class BinaryOperators(Enum):
    conjunction = 1
    disjunction  = 2
    implication = 3
    biimplication = 4


def _get_regular_expression(logic):
    """
    Create a list of regular expressions to tokenize the formula.
    :param logic: the logic to be used, options: KM, S5, S5EC
    :return: a list of regular expressions.
    """
    km_s5_expressions = [
        (config.kms5['knowledge'],      lambda scanner, token: tokens.Knowledge(token)),
        (config.kms5['possible'],      lambda scanner, token: tokens.Possible(token))
    ]

    s5EC_expressions = [
        (config.common['common'],      lambda scanner, _: tokens.Common())
    ]

    expressions_per_logic = {
        "KM": km_s5_expressions,
        "S5": km_s5_expressions,
        "S5EC": s5EC_expressions
    }

    expressions = [
        (r"[a-z]\w*",                              lambda scanner,  token: tokens.Proposition(token)),
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.Negation()),
        # TODO extend skip token to tabs and newlines
        (r"\s+", None), # None == skip token.
        # TODO add brackets
    ]

    expressions.extend(expressions_per_logic.get(logic, []))
    return expressions

def tokenize(logic, string):
    """
    Tokenize the inputted string to a list of tokens
    :param loigc: The logic of the string, options: KM, S5, S5EC
    :param string: The string to be converted to tokens.
    :return:[object]
    """
    regular_expressions = _get_regular_expression(logic);
    scan = re.Scanner(regular_expressions)
    results, remainder=scan.scan(input_formula)
    # TODO raise error if remainder is not empty
    return results

if __name__ == "__main__":
    input_formula = "C ~a | K_47 c & q"
    logic = "S5EC"
    tokens = tokenize(logic, input_formula)
    print tokens