/*!
 * EPL v1.2.0
 * (http://github.com/rkirsling/modallogic)
 *
 * A library for parsing and evaluating well-formed formulas (wffs) of modal propositional logic.
 *
 * Copyright (c) 2013-2014 Ross Kirsling
 * Released under the MIT License.
 */
define("EPL", ["Converters"], function(
  Converters) {
    'use strict';

    /**
     * Constructor for EPL wff. Takes either ASCII or JSON representation as input.
     * @constructor
     */
    function Wff(asciiOrJSON) {
        // Strings for the four representations: ASCII, JSON, LaTeX, and Unicode.
        var _ascii = '',
            _json = '',
            _latex = '',
            _unicode = '';

        /**
         * Returns the ASCII representation of an EPL wff.
         */
        this.ascii = function() {
            return _ascii;
        };

        /**
         * Returns the JSON representation of an EPL wff.
         */
        this.json = function() {
            return _json;
        };

        /**
         * Returns the LaTeX representation of an EPL wff.
         */
        this.latex = function() {
            return _latex;
        };

        /**
         * Returns the Unicode representation of an EPL wff.
         */
        this.unicode = function() {
            return _unicode;
        };


        if (typeof asciiOrJSON === 'string') {
            // ASCII input: remove whitespace before conversion, re-insert it after
            var ascii = asciiOrJSON.match(/\S+/g).join('');
            _json = Converters.asciiToJSON(ascii);
            _ascii = ascii.replace(/&/g, ' & ')
                .replace(/\|/g, ' | ')
                .replace(/<->/g, '***')
                .replace(/->/g, ' -> ')
                .replace(/\*\*\*/g, ' <-> ');
        } else if (typeof asciiOrJSON === 'object') {
            // JSON input
            var json = asciiOrJSON;
            _ascii = Converters.jsonToASCII(json);
            _json = json;
        } else return;

        _latex = Converters.asciiToLaTeX(_ascii);
        _unicode = Converters.asciiToUnicode(_ascii);
    }

    /**
     * Constructor for Kripke model. Takes no initial input.
     * @constructor
     */
    

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
        if (!(model instanceof EPL.Model)) throw new Error('Invalid model!');
        if (!model.getStates()[state]) throw new Error('State ' + state + ' not found!');
        if (!(wff instanceof EPL.Wff)) throw new Error('Invalid wff!');

        return _truth(model, state, wff.json());
    }

    // export public methods
    return {
        Wff: Wff,
        truth: truth
    };

});
