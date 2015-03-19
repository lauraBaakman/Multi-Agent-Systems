# -*- coding: utf-8 -*-

"""
Main for coding
"""

import tokenize.tokenizer as tokenizer
import parser
from ast import ast

import models.kmmodel
import utils



if __name__ == "__main__":
    formula = "K_1 ~ a & (b -> d)"
    logic = "KM"
    filename = '../model.json'

    # try:
    #     tokens = tokenizer.tokenize(logic, input)
    #     print tokens
    #     tree = ast.Ast(tokens)
    #     print tree
    # except tokenizer.TokenizeError as e:
    #     print e.msg
    # except parser.ParserError as e:
    #     print e.message

    tree = {}
    try:
        tree = ast.Ast.from_string(formula, logic)
    except tokenizer.TokenizeError as e:
        print e.msg
    except parser.ParserError as e:
        print e.message

    print tree

    data = utils.read_json(filename)
    model = models.kmmodel.KMModel.from_json(data)

    print model



