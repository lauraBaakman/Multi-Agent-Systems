# -*- coding: utf-8 -*-

__author__ = 'laura'

import json

import falcon

import modelchecker.utils.translators as utils
import modelchecker.models.modelfactory as modelfactory
import modelchecker.errors as errors
import modelchecker.ast as ast
import modelchecker.config as config
#
def get_from_data(data, key, message=None):
    result = data.get(key)
    if not message:
        message = "A {}, with the key '{}' is required".format(key, key)
    if not result:
        raise falcon.HTTPError(
            falcon.HTTP_400,
            message
        )
    return result

def read_json(request):
    try:
        raw_json = request.stream.read()
    except Exception as ex:
        raise falcon.HTTPError(falcon.HTTP_400,
            'Error',
            ex.message)

    try:
        return json.loads(raw_json, encoding='utf-8', object_hook=utils.decode_dict)
    except ValueError:
        raise falcon.HTTPError(falcon.HTTP_400,
            'Malformed JSON',
            'Could not decode the request body. The '
            'JSON was incorrect.')

def get_logic_from_data(data):
    logic = get_from_data(data, 'logic')
    if not logic in config.logics:
        raise falcon.HTTPError(
            falcon.HTTP_400,
            'Error'
            "Undefined logic in model, possible options: are {}".format(config.logics)
        )
    return logic

def get_model_from_data(data):
    json_model = get_from_data(data, 'model')
    logic = get_logic_from_data(json_model)

    try:
        model_class = modelfactory.from_model_name(logic)
        model = model_class.from_json(json_model)
    except errors.ParserError as e:
        raise falcon.HTTPError(falcon.HTTP_400, 'Model Error', e.message)
    return (logic, model)

def get_ast_from_data(logic, data):
    formula = get_from_data(data, 'formula')

    try:
        return ast.Ast.from_string(formula, logic)
    except errors.TokenizeError as e:
        raise falcon.HTTPError(falcon.HTTP_400, 'Tokenize Error', e.message)
    except errors.ParserError as e:
        raise falcon.HTTPError(falcon.HTTP_400, 'Parse Error', e.message)

def get_state_from_data(data):
    return data.get('state')
#
def evaluate_model(model, formula, state):
    try:
        return model.is_true(formula, state)
    except errors.ValuationError as e:
        raise falcon.HTTPError(falcon.HTTP_400, 'Evaluation Error', e.message)

class Resource(object):

    def on_post(self, req, resp):
        print 'Received request: {req}'.format(req=req)
        json_data = read_json(req)
        (logic, model) = get_model_from_data(json_data)
        ast = get_ast_from_data(logic, json_data)
        state = get_state_from_data(json_data)
        (truth_value, motivation) = evaluate_model(model, ast, state)

        resp.status = falcon.HTTP_202
        resp.set_header('Access-Control-Allow-Headers', req.get_header('Origin'))
        resp.body = json.dumps(
            {
                'truth_value': truth_value,
                'motivation' : utils._sub_motivation_to_html(motivation),
                'model': model.to_json()
            },
             encoding='utf-8'
        )
        resp.set_header('Access-Control-Allow-Origin', req.get_header('Origin'))
        print 'Sent response: {resp}'.format(resp=resp)
