# -*- coding: utf-8 -*-

"""
Main for coding
"""

import tokenize.tokenizer as tokenizer
import parser
from ast import ast

if __name__ == "__main__":
    input = "C ~ a & (b -> d)"
    logic = "S5EC"

    try:
        tokens = tokenizer.tokenize(logic, input)
        print tokens
        tree = ast.Ast(tokens)
        print tree
    except tokenizer.TokenizeError as e:
        print e.msg
    except parser.ParserError as e:
        print e.message





