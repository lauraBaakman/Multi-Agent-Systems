# -*- coding: utf-8 -*-

import state
import relation
from modelerror import  ModelError

__author__ = 'laura'


class KMModel(object):
    """
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        """
        Constructor for KMModel
        :return:
        """
        self.states = {}
        self.relations = {}

    def __repr__(self):
        """Print friendly representation"""
        return "States:\n {obj.states}\nRelations: {obj.relations}".format(obj=self)

    def to_json(self):
        """
        Generate a JSON representation of the model.
        :return: JSON object.
        """
        # TODO to_json() bouwen voor model
        raise NotImplementedError

    def add_relation(self, relation):
        """
        Add the relation to the list of relations of the models and add the relation to respectively
        the incoming and outgoing list its the destination and source node.
        :param relation: Relation
        :return: void
        """
        if relation.agent in self.relations:
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
        if state.name in self.states:
            if not state == self.states[state.name]:
                raise ModelError(
                    "The state '{state.name}' has two different definitions.".format(state=state)
                )
        self.states[state.name] = state

    def get_state_by_name(self, name):
        """
        Get a state in the  models by its name.
        :param name: the name of the state
        :return: the state with the name name
        :raises: modelError if name does not represent an existing state.
        """
        state = self.states.get(name)
        if state:
            return state
        else:
            raise ModelError()

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
                raise ModelError(
                    "The length of the list of valuations and the list of propositions differs."
                )
            return dict(zip(propositions, valuations))

        propositions = json_data['propositions']
        for json_state in json_data['states']:
            try:
                self.add_state(
                    state.State(
                        json_state['id'],
                        _create_valuation(propositions, json_state['vals'])
                    )
                )
            except:
                raise

    def add_relations_from_json(self, json_data):
        """
        Add the staes defined in json_data to the object.
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
                        agent,
                        self.get_state_by_name(source_name),
                        self.get_state_by_name(destination_name)
                    )
                )
            except ModelError:
                raise ModelError(
                    "The relationship {source}R_{agent}{destination} is not between existing states".format(
                        source=source_name,
                        destination=destination_name,
                        agent=agent
                    )
                )

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
        except:
            raise
        return model
