# -*- coding: utf-8 -*-

__author__ = 'laura'

import json

import falcon

import time

import modelchecker.utils as utils
import modelchecker.models as models
import modelchecker.errors as errors
import modelchecker.ast as ast
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
    if not logic in ['KM', 'S5', 'S5EC']:
        raise falcon.HTTPError(
            falcon.HTTP_400,
            'Error'
            "Undefined logic in model, possible options: are 'KM', 'S5', 'S5EC'"
        )
    return logic

def get_model_from_data(data):
    json_model = get_from_data(data, 'model')
    logic = get_logic_from_data(json_model)

    model = {}
    try:
        if logic == "KM":
            model = models.KMModel.from_json(json_model)
        elif logic == "S5":
            # TODO: model =  models.S5.S5Model.from_json(json_model)
            raise falcon.HTTPError(falcon.HTTP_501, 'Error', 'The logic S5 is not yet implemented')
        elif logic == "S5EC":
            # TODO: model = models.S5EC.S5ECModel.from_json(json_model)
            raise falcon.HTTPError(falcon.HTTP_501, 'Error', 'The logic S5EC is not yet implemented')
    except errors.ModelError as e:
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
        resp.body = json.dumps(
            {
                'truth_value': truth_value,
                'motivation' : utils.motivation_to_html(motivation),
                'model' : model.to_json()
            },
             encoding='utf-8'
        )
        resp.set_header('Access-Control-Allow-Origin', req.get_header('Origin'))
        time.sleep(2);
        print 'Sent response: {resp}'.format(resp=resp)
