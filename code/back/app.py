# -*- coding: utf-8 -*-

__author__ = 'laura'

import falcon

import api.resources as resources

def cors_middleware():
    """
    :return: a middleware function to deal with Cross Origin Resource Sharing (CORS)
    """
    def fn(req, resp, _):
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Origin', '*')
    return fn

api = application = falcon.API(
    after=[
        cors_middleware()
    ]
)

api.add_route('/valuate', resources.Valuate())
api.add_route('/logics', resources.Logics())