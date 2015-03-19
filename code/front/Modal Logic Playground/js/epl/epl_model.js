define("epl_model", [], function() {

	function Model() {
        // Array of states (worlds) in model.
        // Each state is an object with two properties:
        // - assignment: a truth assignment (in which only true values are actually stored)
        // - successors: an array of successor state indices (in lieu of a separate accessibility relation)
        // ex: [{assignment: {},          successors: [0,1]},
        //      {assignment: {'p': true}, successors: []   }]
        var _states = [];

        /**
         * Adds a transition to the model, given source and target state indices.
         */
        this.addTransition = function(source, target) {
            if (!_states[source] || !_states[target]) return;

            var successors = _states[source].successors,
                index = successors.indexOf(target);
            if (index === -1) successors.push(target);
        };

        /**
         * Removes a transition from the model, given source and target state indices.
         */
        this.removeTransition = function(source, target) {
            if (!_states[source]) return;

            var successors = _states[source].successors,
                index = successors.indexOf(target);
            if (index !== -1) successors.splice(index, 1);
        };

        /**
         * Returns an array of successor states for a given state index.
         */
        this.getSuccessorsOf = function(source) {
            if (!_states[source]) return undefined;

            return _states[source].successors;
        };

        /**
         * Adds a state with a given assignment to the model.
         */
        this.addState = function(assignment) {
            var processedAssignment = {};
            for (var propvar in assignment)
                if (assignment[propvar] === true)
                    processedAssignment[propvar] = assignment[propvar];

            _states.push({
                assignment: processedAssignment,
                successors: []
            });
        };

        /**
         * Edits the assignment of a state in the model, given a state index and a new partial assignment.
         */
        this.editState = function(state, assignment) {
            if (!_states[state]) return;

            var stateAssignment = _states[state].assignment;
            for (var propvar in assignment)
                if (assignment[propvar] === true) stateAssignment[propvar] = true;
                else if (assignment[propvar] === false) delete stateAssignment[propvar];
        };

        /**
         * Removes a state and all related transitions from the model, given a state index.
         */
        this.removeState = function(state) {
            if (!_states[state]) return;
            var self = this;

            _states[state] = null;
            _states.forEach(function(source, index) {
                if (source) self.removeTransition(index, state);
            });
        };

        /**
         * Returns an array containing the assignment (or null) of each state in the model.
         * (Only true propositional variables are returned in each assignment.)
         */
        this.getStates = function() {
            var stateList = [];
            _states.forEach(function(state) {
                if (state) stateList.push(state.assignment);
                else stateList.push(null);
            });

            return stateList;
        };

        /**
         * Returns the truth value of a given propositional variable at a given state index.
         */
        this.valuation = function(propvar, state) {
            if (!_states[state]) throw new Error('State ' + state + ' not found!');

            return !!_states[state].assignment[propvar];
        };

        /**
         * Returns current model as a compact string suitable for use as a URL parameter.
         * ex: [{assignment: {'q': true}, successors: [0,2]}, null, {assignment: {}, successors: []}]
         *     compresses to 'AqS0,2;;AS;'
         */
        this.getModelString = function() {
            var modelString = '';

            _states.forEach(function(state) {
                if (state) {
                    modelString += 'A' + Object.keys(state.assignment).join();
                    modelString += 'S' + state.successors.join();
                }
                modelString += ';';
            });

            return modelString;
        };

        /**
         * Restores a model from a given model string.
         */
        this.loadFromModelString = function(modelString) {
            var regex = /^(?:;|(?:A|A(?:\w+,)*\w+)(?:S|S(?:\d+,)*\d+);)+$/;
            if (!regex.test(modelString)) return;

            _states = [];

            var self = this,
                successorLists = [],
                inputStates = modelString.split(';').slice(0, -1);

            // restore states
            inputStates.forEach(function(state) {
                if (!state) {
                    _states.push(null);
                    successorLists.push(null);
                    return;
                }

                var stateProperties = state.match(/A(.*)S(.*)/).slice(1, 3)
                    .map(function(substr) {
                        return (substr ? substr.split(',') : []);
                    });

                var assignment = {};
                stateProperties[0].forEach(function(propvar) {
                    assignment[propvar] = true;
                });
                _states.push({
                    assignment: assignment,
                    successors: []
                });

                var successors = stateProperties[1].map(function(succState) {
                    return +succState;
                });
                successorLists.push(successors);
            });

            // restore transitions
            successorLists.forEach(function(successors, source) {
                if (!successors) return;

                successors.forEach(function(target) {
                    self.addTransition(source, target);
                });
            });
        };
    }

    return {
    	Model: Model
    };
});
