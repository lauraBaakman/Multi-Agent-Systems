# -*- coding: utf-8 -*-

"""
Main for coding
"""

import json

import tokenize.tokenizer as tokenizer
import parser
from ast import ast
import model.model

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

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
    data = json.load(json_data, object_hook=_decode_dict)
    json_data.close()
    model = model.model.Model.from_json(data)
    print model


