# -*- coding: utf-8 -*-

__author__ = 'laura'

import falcon

import api.resources as resources

api = application = falcon.API()

api.add_route('/valuate', resources.Valuate())
api.add_route('/logics', resources.Logics())