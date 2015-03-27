# -*- coding: utf-8 -*-

__author__ = 'laura'

from modelchecker import operators
from modelchecker.ast import nodes
from modelchecker.tokenize import tokens

def from_token(token):
    if isinstance(token, tokens.Proposition):
        return nodes.Proposition.fromToken(token)
    else:
        token_to_token_type = {
            operators.Agent : _from_agent_token,
            operators.Binary: _from_binary_token,
            operators.Unary: _from_unary_token
        }
        return token_to_token_type.get(token.type.__class__)(token)

def _from_agent_token(token):
    token_to_node = {
        operators.Agent.knowledge: nodes.Knowledge,
        operators.Agent.possible: nodes.Possible,
    }
    return token_to_node.get(token.type)(token.agent)

def _from_binary_token(token):
    token_to_node = {
        operators.Binary.conjunction: nodes.Conjunction,
        operators.Binary.disjunction: nodes.Disjunction,
        operators.Binary.implication: nodes.Implication,
        operators.Binary.biimplication: nodes.BiImplication,
    }
    return token_to_node.get(token.type)()

def _from_unary_token(token):
    token_to_node = {
        operators.Unary.negation: nodes.Negation,
        operators.Unary.common: nodes.Common,
        operators.Unary.everybody: nodes.Everybody,
        operators.Unary.intention: nodes.Intention
    }
    return token_to_node.get(token.type)()
