# -*- coding: utf-8 -*-

import json

"""."""

__author__ = 'laura'

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv

def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv

def read_json(filename):
    json_data = open(filename)
    data = json.load(json_data, object_hook=decode_dict)
    json_data.close()
    return data

def _interlude_to_html(interlude):
    result = ''
    for element in interlude:
        if isinstance(element, basestring):
            result = '<p>{}</p> <br> <p>{}</p>'.format(result, element)
        if isinstance(element, dict):
            result = '<p>{}</p> <br> <p>{}</p>'.format(result, motivation_to_latex(element))
    return result

def motivation_to_html(motivation):
    if motivation.has_key('interlude'):
        return '<p>{condition}</p> <br> <p>{interlude}</p> <br> <p>{conclusion}</p> <br>'.format(
            condition=motivation['condition'],
            interlude=_interlude_to_latex(motivation['interlude']),
            conclusion=motivation['conclusion']
        )
    else:
        return '<p>{condition}</p> <br>  <p>{conclusion}</p> <br>'.format(
            condition=motivation['condition'],
            conclusion=motivation['conclusion']
        )

def _interlude_to_latex(interlude):
    result = ''
    for element in interlude:
        if isinstance(element, basestring):
            result = '{} \\ {}'.format(result, element)
        if isinstance(element, dict):
            result = '{} \\ {}'.format(result, motivation_to_latex(element))
    return result

def motivation_to_latex(motivation):
    if motivation.has_key('interlude'):
        return '{condition}\\ {interlude}\\ {conclusion}\\'.format(
            condition=motivation['condition'],
            interlude=_interlude_to_latex(motivation['interlude']),
            conclusion=motivation['conclusion']
        )
    else:
        return '{condition}\\  {conclusion}\\'.format(
            condition=motivation['condition'],
            conclusion=motivation['conclusion']
        )