# -*- coding: utf-8 -*-

"""
Main for coding
"""

import parser
from modelchecker.errors import TokenizeError

import modelchecker.tokenize.tokenizer as tokenizer
from modelchecker import ast
import modelchecker.models as models
import modelchecker.utils as utils


if __name__ == "__main__":
    formula = "K_1 ~ a & (b -> d)"
    logic = "K"
    filename = '../model.json'

    try:
        tree = ast.Ast.from_string(formula, logic)
        print tree

        data = utils.read_json(filename)
        model = models.KMmodel.KMmodel.from_json(data)
        print model
    except TokenizeError as e:
        print e.msg
    except parser.ParserError as e:
        print e.message
    except models.errors.ModelError as e:
        print e.message
    except models.errors.ValuationError as e:
        print e.message









