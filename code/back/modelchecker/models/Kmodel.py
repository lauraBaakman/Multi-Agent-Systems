# -*- coding: utf-8 -*-

import json
from collections import OrderedDict

import state
import relation
from modelchecker import errors
from modelchecker.utils.closures import convergence

__author__ = 'laura'


class KModel(object):
    """
    Class representing epistemic kripke logics
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        """
        Constructor for KModel
        :return:
        """
        self.states = {}
        self.relations = {}
        self.agents = set([])

    def __repr__(self):
        """Print friendly representation"""
        return "States:\n {obj.states}\nRelations: {obj.relations}".format(obj=self)

    def get_propositions(self):
        """
        Return the list of propositions of which the valuation is determined in this model. If the model does not
        have any states it does not have any propositions, thus an empty list is returned.
        :return:
        """
        if self.states:
            return self.states.values()[0].valuations.keys()
        else:
            return []

    def get_states_for_json_dump(self):
        return [state.to_json_dump() for state in self.states.values()]

    def get_relations_for_json_dumps(self):
        """
        Return the relations of the objects in the format required for to_json.
        :return:
        """
        list = []
        for relation_list in self.relations.values():
            list.extend([relation.to_json_dump() for relation in relation_list])
        return list

    def to_json(self):
        """
        Generate a JSON representation of the model.
        :return: JSON object.
        """
        return json.dumps(
            {
                'propositions'  : self.get_propositions(),
                'states'        : self.get_states_for_json_dump(),
                'relations'     : self.get_relations_for_json_dumps(),
            }
        )

    def add_agent(self, agent):
        self.agents.add(agent)

    def add_relation(self, relation):
        """
        Add the relation to the list of relations of the models and add the relation to respectively
        the incoming and outgoing list its the destination and source node.
        :param relation: Relation
        :return: void
        """
        self.add_agent(relation.agent)
        if relation.agent in self.relations:
            if not(relation in self.relations[relation.agent]):
                self.relations[relation.agent].append(relation)
        else:
            self.relations[relation.agent] = [relation]
        relation.source.add_outgoing_relation(relation)
        relation.destination.add_incoming_relation(relation)

    def add_state(self, state):
        """
        Add a state to the list of states
        :param state: the state to be added to the models
        :return:
        """
        if state.name in self.states.keys():
            raise errors.ModelError(
                "The state '{state.name}' has two different definitions.".format(state=state)
            )
        self.states[state.name] = state

    def get_state_by_name(self, state_name):
        """
        Get a state in the  models by its name.
        :param name: the name of the state
        :return: the state with the name name
        :raises: modelError if name does not represent an existing state.
        """
        state = self.states.get(state_name, None)
        if state:
            return state
        raise errors.ModelError('Could not find the state {}'.format(state_name))

    def add_states_from_json(self, json_data):
        """
        Add the states defined in json_data to the object.
        :param json_data: python representation of a json_object, containing at least:
            {
              'states': [
                  {   'vals': [True, ...],
                      'id': 'a'
                  }, ...
              ],
              'propositions': ['p', ...],
            }
        :return: void
        :raises:
            modelError if multiple states in the list but have the same name.
        """
        def _create_valuation(propositions, valuations):
            """
            Create a valution dictionary.
            :param propositions: the list of propositions
            :param valuations: the list of valuations
            :raises ModelError: if the list of propositions does not have the same length as the list of propositions.
            :return: dictionary with valutions.
            """
            if not len(propositions) == len(valuations):
                raise errors.ModelError(
                    "The length of the list of valuations and the list of propositions differs."
                )
            return OrderedDict(zip(propositions, valuations))

        propositions = json_data['propositions']
        for json_state in json_data['states']:
            try:
                self.add_state(
                    state.State(
                        str(json_state['id']),
                        _create_valuation(propositions, json_state['vals']),
                        self
                    )
                )
            except errors.ModelError as e:
                raise e

        if len(self.states.keys()) == 0:
            raise errors.ModelError('A model should have at least one state.')

    def add_relations_from_json(self, json_data):
        """
        Add the states defined in json_data to the object.
        :param json_data: python representation of a json_object, containing at least:
            {
                'relations': [['a', 1, 'b'], ['c', 2, 'd']],
            }
        :return: void
        """
        for [source_name, agent, destination_name] in json_data['relations']:
            try:
                self.add_relation(
                    relation.Relation(
                        str(agent),
                        self.get_state_by_name(source_name),
                        self.get_state_by_name(destination_name)
                    )
                )
            except errors.ModelError:
                raise errors.ModelError(
                    "The relationship {source}R_{agent}{destination} is not between existing states".format(
                        source=source_name,
                        destination=destination_name,
                        agent=agent
                    )
                )

    def is_true(self, formula, state_name):
        """
        Determine the truth value for formula in this model and state
        :param formula: formula as an AST
        :param state: optional string, state to evaluate the formula in. Default is None. If None the formula is
        evaluated in all states.
        :return: Truth value or a list of truth values
        """
        try:
            state = self.get_state_by_name(state_name)
            return formula.is_true(state)
        except:
            raise

    def all_states_eventually_reachable_from(self, state):
        """
        Return all states that can be reached by any agent from the current state by taking at least one step.
        :param state: The state to start from.
        :type state: modelchecker.models.state
        :return: set of states
        :rtype: set[modelchecker.models.state]
        """
        reachable_states = {destination for (_, destination) in state.get_all_outgoing_as_two_tuple()}
        previous_set = set()
        while not convergence(reachable_states, previous_set):
            previous_set = reachable_states
            new_relations = set(
                destination
                for cc_state in reachable_states
                for (_, destination) in cc_state.get_all_outgoing_as_two_tuple()
            )
            reachable_states = previous_set.union(new_relations)
        return reachable_states

    @classmethod
    def from_json(cls, json_data):
        """
        Generate a models from json_data
        :param json_data: json data
        :return: a models
        """
        model = cls()
        try:
            model.add_states_from_json(json_data)
            model.add_relations_from_json(json_data)
        except errors.ModelError as e:
            raise e
        return model
