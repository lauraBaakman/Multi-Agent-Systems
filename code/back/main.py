# -*- coding: utf-8 -*-

"""
Main for coding
"""

import json

import tokenize.tokenizer as tokenizer
import parser
from ast import ast
import model.model


if __name__ == "__main__":
    # input = "C ~ a & (b -> d)"
    # logic = "S5EC"
    #
    # try:
    #     tokens = tokenizer.tokenize(logic, input)
    #     print tokens
    #     tree = ast.Ast(tokens)
    #     print tree
    # except tokenizer.TokenizeError as e:
    #     print e.msg
    # except parser.ParserError as e:
    #     print e.message

    file = '../model.json'
    json_data = open(file)
    data = json.load(json_data)
    json_data.close()
    model = model.model.Model.from_json(data)
    print model


