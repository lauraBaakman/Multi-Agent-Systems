# -*- coding: utf-8 -*-

__author__ = 'laura'

import modelchecker.models as models
import modelchecker.errors as errors

def from_model_name(logic_name):
    logic_name_to_class = {
        'K' : models.KModel,
        'T'  : models.TModel,
        'S4' : models.S4Model,
        'S5' : models.S5Model,
        'KEC': models.KModel,
        'TEC': models.TModel,
        'S4EC': models.S4Model,
        'S5EC': models.S5Model,
        'KI': models.KModel,
        'TI': models.TModel,
        'S4I': models.S4Model,
        'S5I': models.S5Model
    }
    class_name = logic_name_to_class.get(logic_name)
    if class_name:
        return class_name
    else:
        raise errors.ParserError('The logic {} is not supported.'.format(logic_name))