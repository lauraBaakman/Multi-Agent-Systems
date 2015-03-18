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

    def __init__(self, states):
        """
        Constructor for Model
        :param states: dictonary of states indexed by their name.
        :return:
        """
        if (not states):
            raise ModelError("A model needs a non empty set of states.")
        self.states = states
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
        Add the realtion to the list of relations of the model and add the relation to respectively the incoming and
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
        # 'states': ['a', 'b', 'c', 'd'],
        #   'propositions': ['p', 'q'],
        #   'relations': [['a', 1, 'b'], ['c', 2, 'd']],
        #   'valuations': [['a', ['p', 'q']], ['d', ['q']]],
        #   'logic': 'K(m)'
        # }

        # TODO: Select correct model constructor given the logic.

        try:
            # Create states
            propositions = json_data['propositions']
            states = {state_name: state.State(state_name, propositions) for state_name in json_data['states']}

            # Set the correct truth value of each proposition for each state
            [states[state_name].set_true(propositions) for [state_name, propositions] in json_data['valuations']]

            # Create the model
            model = Model(states)

            # Set the relations
            for [source_name, agent, destination_name] in json_data['relations']:
                try:
                    relationship = relation.Relation(
                        agent,
                        model.get_state_by_name(source_name),
                        model.get_state_by_name(destination_name)
                    )
                    model.add_relation(relationship)
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




        # Add relationshipsq

        # Add valuations to states
