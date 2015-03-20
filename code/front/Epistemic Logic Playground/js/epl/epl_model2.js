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
        	if(count < 0 || count > max_num_props) return;

        	proposition_counter = count;
        };

        this.get_default_props = function() {
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
   				agents: [0]
            };
            links.push(link);
        };

        this.edit_link = function(link_id, agents) {
            var link = self.get_link(link_id);
            if (!link) return;

            link.agents = agents;
        };

        // Todo: Agent
        this.remove_link = function(link_id) {
            var link_idx = self.get_link_idx(link_id);
            if (link_idx < 0) return;
        	// Remove 1 item at index
            links.splice(link_idx, 1);
        };

        // Init a default state to add.... Bs to generate this every time
        this.add_state = function() {
            var state = {};

            state.id = state_counter++;
            state.vals = default_propositions.map(function() {
                return false;
            });
            state.reflexive = false;

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
            var link_indices = [];
            links.forEach(function(link, index) {
            	if (link.source.id === state_id || link.target.id === state_id) {
            		link_indices.push(index);
            	}
            });

            link_indices.forEach(function(link_idx) {
            	self.remove_link(link_idx);
            });
        };

        this.get_state_idx = function(state_id) {
            var state_idx = -1;
            states.forEach(function(state, index) {
            	if(state.id === state_id) {
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
        		if(link.target.id === source_id && link.source.id === target_id) {
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

        this.get_links = function() {
            return links;
        };

        this.load_from_model_string = function(model_string) {
        	return;
        };

        this.save_to_model_string = function() {
        	return;
        };

        this.load_from_model_object = function(model_object) {
            return;
        };

        this.save_to_model_object = function() {
            return;
        };
    }
    return EplModel;
});
