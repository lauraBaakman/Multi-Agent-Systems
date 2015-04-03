define("epl_model", [], function() {

    function EplModel() {

        var self = this;

        var states = [],
            links = [];

        var state_counter = 0;
        var link_counter = 0;

        var default_propositions = ['p', 'q', 'r', 's', 't'];
        var proposition_counter = 2;

        var max_num_agents = 5;
        var max_num_props = 5;


        this.get_prop_count = function() {
            return proposition_counter;
        };

        this.set_prop_count = function(count) {
            if (count < 0 || count > max_num_props) return;

            proposition_counter = count;
        };

        this.get_props = function() {
            return default_propositions;
        };

        this.get_num_agents = function() {
            return max_num_agents;
        };

        // Todo: Agent
        this.add_link = function(source_id, target_id) {
            // Add checks if source and target exist
            var source = self.get_state(source_id);
            if (!source) return;

            var target = self.get_state(target_id);
            if (!target) return;

            var link = {
                id: link_counter++,
                source: source,
                target: target,
                agents: []
            };
            links.push(link);

            return link.id;
        };

        this.add_agent_to_link = function(link_id, agent) {
            var link = self.get_link(link_id);
            if (!link) return;

            link.agents.push(agent);
        };

        // Todo: Agent
        this.remove_link = function(link_id) {
            console.log("removing link: " + link_id);

            var link_idx = self.get_link_idx(link_id);
            if (link_idx < 0) return;
            // Remove 1 item at index
            links.splice(link_idx, 1);

            console.log(links);
        };

        // !!BROKEN!! 
        this.add_state = function() {
            var state = {};

            state.id = state_counter++;

            current_propositions = default_propositions.slice(0, proposition_counter);

            state.vals = default_propositions.map(function() {
                return false;
            });
            state.reflexive = false;
            state.agents = [];

            states.push(state);
        };

        this.edit_state = function(state_id, valuation) {
            var state = self.get_state(state_id);
            if (!state) return;

            state.vals = default_propositions.map(function(prop, index) {
                return !valuation[index] ? false : true;
            });
        };

        this.remove_state = function(state_id) {
            var state_idx = self.get_state_idx(state_id);
            if (state_idx < 0) return;

            // Remove 1 item at index
            states.splice(state_idx, 1);

            // Get all links that link to this state
            var link_ids = [];
            links.forEach(function(link, index) {
                if (link.source.id === state_id || link.target.id === state_id) {
                    link_ids.push(link.id);
                }
            });

            link_ids.forEach(function(link_idx) {
                self.remove_link(link_idx);
            });
        };

        this.get_state_idx = function(state_id) {
            var state_idx = -1;
            states.forEach(function(state, index) {
                if (state.id === state_id) {
                    state_idx = index;
                }
            });
            return state_idx;
        };

        this.get_state = function(state_id) {
            return states.filter(function(state) {
                return state.id === state_id;
            })[0];
        };

        this.is_target_state = function(source_id, target_id) {
            var is_target = false;
            links.forEach(function(link) {
                if (link.target.id === source_id && link.source.id === target_id) {
                    is_target = true;
                }
            });
            return is_target;
        }

        this.get_states = function() {
            return states;
        };

        this.get_link_idx = function(link_id) {
            var link_idx = -1;
            links.forEach(function(link, index) {
                if (link.id === link_id) {
                    link_idx = index;
                }
            });
            return link_idx;
        }

        this.get_link = function(link_id) {
            return links.filter(function(link) {
                return link.id === link_id;
            })[0];
        }

        this.link_exists = function(source_id, target_id) {
            var link_id = null;
            links.forEach(function(link) {
                if (link.source.id === source_id && link.target.id === target_id) {
                    link_id = link.id;
                }
            });
            return link_id;
        }

        this.get_links = function() {
            return links;
        };

        this.load_from_model_string = function(model_string) {
            return;
        };

        this.save_to_model_string = function() {
            return;
        };

        function add_pre_state(state_id, state_vals) {
            var state = {};

            state_counter = Math.max(parseInt(state_id), state_counter);
            state.id = parseInt(state_id);

            state.vals = default_propositions.map(function(prop, index) {
                return !state_vals[index] ? false : true;
            });

            state.reflexive = false;
            state.agents = [];

            states.push(state);
        }

        function add_pre_link(source_id, agent, target_id) {
            var source = null;
            if (source_id === target_id) {
                source = self.get_state(source_id);
                source.reflexive = true;
                source.agents.push(agent);
                return;
            }
            var link_id = self.link_exists(source_id, target_id);
            if (link_id === null) {
                link_id = self.add_link(source_id, target_id);
            }
            self.add_agent_to_link(link_id, agent);
        }

        this.load_from_model_object = function(model_object) {
            states = [];
            state_counter = 0;

            links = [];
            link_counter = 0;

            // current_propositions = model_object.propositions;

            model_object.states.forEach(function(pre_state) {
                add_pre_state(pre_state.id, pre_state.vals);
            });

            state_counter++;

            model_object.relations.forEach(function(pre_link) {
                add_pre_link(parseInt(pre_link[0]), parseInt(pre_link[1]), parseInt(pre_link[2]));
            });
        };

        this.save_to_model_object = function() {
            var sendable_states = states.map(function(state) {
                return {
                    "id": state.id.toString(),
                    "vals": state.vals.slice(0, proposition_counter)
                };
            });

            var sendable_propositions = default_propositions.slice(0, proposition_counter);

            var sendable_relations = [];

            links.forEach(function(link) {
                console.log(link);
                var relations = link.agents.map(function(agent) {
                    return [
                        link.source.id.toString(),
                        agent.toString(),
                        link.target.id.toString()
                    ];
                });
                relations.forEach(function(relation) {
                    sendable_relations.push(relation);
                });
            });

            states.forEach(function(state) {
                if(state.reflexive) {
                    state.agents.forEach(function(agent) {
                        sendable_relations.push([state.id.toString(), agent.toString(), state.id.toString()]);
                    });
                }
            });

            return {
                "states": sendable_states,
                "propositions": sendable_propositions,
                "relations": sendable_relations,
                "logic": "S5"
            }
        };
    }
    return EplModel;
});
