# -*- coding: utf-8 -*-

"""
Main script to test the AST
"""
__author__ = 'laura'

from tokenize import tokenizer

if __name__ == "__main__":
    input_formula = "K_1 (M_1 | & -> <-> ! T        F   )"
    tokens = tokenizer.tokenize(input_formula)
    print tokens