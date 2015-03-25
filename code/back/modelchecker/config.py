# -*- coding: utf-8 -*-
"""
Configuration for the tokenizer
"""
__author__ = 'laura'

# The regular expressions for the different operators.
propositional = {
    'disjunction': r"[|]",
    'conjunction': r"&",
    'bi-implication': r"<->",
    'implication': r"->",
    'negation': r"~"
}

kms5 = {
    'knowledge': r"K_[1-9]+",
    'possible': r"M_[1-9]+"
}

common = {
    'common': r"C"
    #Add everybody
}

# The supported logics:
logics = ['KM', 'T', 'S4', 'S5', 'KEC', 'TEC', 'S4EC', 'S5EC']


