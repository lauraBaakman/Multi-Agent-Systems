define("epl_valuation", ["epl_model", "epl_formula"], function(
  epl_model, epl_formula) {
    'use strict';

    /**
     * Evaluate the truth of an EPL wff (in JSON representation) at a given state within a given model.
     * @private
     */
    function _truth(model, state, json) {
        if (json.prop)
            return model.valuation(json.prop, state);
        else if (json.neg)
            return !_truth(model, state, json.neg);
        else if (json.conj)
            return (_truth(model, state, json.conj[0]) && _truth(model, state, json.conj[1]));
        else if (json.disj)
            return (_truth(model, state, json.disj[0]) || _truth(model, state, json.disj[1]));
        else if (json.impl)
            return (!_truth(model, state, json.impl[0]) || _truth(model, state, json.impl[1]));
        else if (json.equi)
            return (_truth(model, state, json.equi[0]) === _truth(model, state, json.equi[1]));
        else if (json.nec)
            return model.getSuccessorsOf(state).every(function(succState) {
                return _truth(model, succState, json.nec);
            });
        else if (json.poss)
            return model.getSuccessorsOf(state).some(function(succState) {
                return _truth(model, succState, json.poss);
            });
        else
            throw new Error('Invalid formula!');
    }

    /**
     * Evaluate the truth of an EPL wff at a given state within a given model.
     */
    function truth(model, state, wff) {
        if (!(model instanceof epl_model.Model)) throw new Error('Invalid model!');
        if (!model.getStates()[state]) throw new Error('State ' + state + ' not found!');
        if (!(wff instanceof epl_formula.Formula)) throw new Error('Invalid wff!');

        return _truth(model, state, wff.json());
    }

    // export public methods
    return {
        valuate: truth
    };

});
