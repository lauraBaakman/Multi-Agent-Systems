# -*- coding: utf-8 -*-

import state
import relation

__author__ = 'laura'


class ModelError(Exception):
    """ Exception raised for errors in the model."""
    pass


class Model(object):
    """
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        """
        Constructor for Model
        :param states: dictonary of states indexed by their name.
        :return:
        """
        self.states = {}
        self.relations = {}

    def __repr__(self):
        """Print friendly representation"""
        # TODO relations op een zinnige manier afdrukken.
        return "States:\n {obj.states}\nRelations: {obj.relations}".format(obj=self)

    def to_json(self):
        # TODO bouwen
        raise NotImplementedError

    def add_relation(self, relation):
        """
        Add the relation to the list of relations of the model and add the relation to respectively the incoming and
        outgoing list its the destination and source node.
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
        :param relation: the state to be added to the model
        :return:
        """
        if state.name in self.states:
            if not state == self.states[state.name]:
                raise ModelError("You have two different states with the same name.")
        self.states[state.name] = state

    def get_state_by_name(self, name):
        """
        Get a state in the  model by its name.
        :param name: the name of the state
        :return: the state with the name name
        :raises: modelError if name does not represent an existing state.
        """
        state = self.states.get(name)
        if state:
            return state
        else:
            raise ModelError()


    @staticmethod
    def from_json(json_data):
        """
        Generate a model from json_data
        :param json_data: json data
        :return: a model
        """

        # {
        #   'states': [
        #       {   'vals': [True, False, False, False],
        #           'id': 'a'
        #       }, {       {
        #           'vals': [True, False, False, True],
        #            'id': 'b'
        #       }, {
        #           'vals': [True, False, True, False],
        #           'id': 'c'
        #       }, {
        #           'vals': [False, True, False, False],
        #           'id': 'd'
        #       }
        #   ],
        #   'propositions': ['p', 'q'],
        #   'relations': [['a', 1, 'b'], ['c', 2, 'd']],
        #   'logic': 'K(m)'
        # }


        # TODO: Select correct model constructor given the logic.

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

        # Create the model
        model = Model()

        try:
            # Create states
            propositions = json_data['propositions']
            # TODO list comprehension instead of for
            # TODO handle errors, what happens if propositions have a differente length from json_state['vals']?
            # TODO refactor to use self.add_states_from_json and self.add_relationships_from_json.

            for json_state in json_data['states']:
                model.add_state(
                    state.State(
                        json_state['id'],
                        _create_valuation(propositions, json_state['vals'])
                    )
                )



            # Set the relations
            for [source_name, agent, destination_name] in json_data['relations']:
                try:
                    model.add_relation(
                        relation.Relation(
                            agent,
                            model.get_state_by_name(source_name),
                            model.get_state_by_name(destination_name)
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
        except ModelError:
            raise

        return Model(states)
