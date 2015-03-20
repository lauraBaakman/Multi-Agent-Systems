# -*- coding: utf-8 -*-

__author__ = 'laura'

import falcon

import resources

api = application = falcon.API()

api.add_route('/valuate', resources.Resource())