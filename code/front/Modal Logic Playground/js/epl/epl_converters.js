// name, deps, callback
define("epl_converters", ["epl_regexp"], function(epl_regexp) {

    var asciiToJSON = function (ascii) {
        var json = {},
            subwffs = [];

        if (epl_regexp.proposition.test(ascii))
            json.prop = ascii;
        else if (ascii.slice(0, 1) === '~')
            json.neg = asciiToJSON(ascii.slice(1));
        else if (ascii.slice(0, 2) === '[]')
            json.nec = asciiToJSON(ascii.slice(2));
        else if (ascii.slice(0, 2) === '<>')
            json.poss = asciiToJSON(ascii.slice(2));
        else if (subwffs = ascii.match(epl_regexp.conjunction))
            json.conj = [asciiToJSON(subwffs[1]), asciiToJSON(subwffs[2])];
        else if (subwffs = ascii.match(epl_regexp.disjunction))
            json.disj = [asciiToJSON(subwffs[1]), asciiToJSON(subwffs[2])];
        else if (subwffs = ascii.match(epl_regexp.implication))
            json.impl = [asciiToJSON(subwffs[1]), asciiToJSON(subwffs[2])];
        else if (subwffs = ascii.match(epl_regexp.equivalence))
            json.equi = [asciiToJSON(subwffs[1]), asciiToJSON(subwffs[2])];
        else
            throw new Error('Invalid formula!');

        return json;
    }

    /**
     * Converts an MPL wff from JSON to ASCII.
     * @private
     */
    var jsonToASCII = function (json) {
        if (json.prop)
            return json.prop;
        else if (json.neg)
            return '~' + jsonToASCII(json.neg);
        else if (json.nec)
            return '[]' + jsonToASCII(json.nec);
        else if (json.poss)
            return '<>' + jsonToASCII(json.poss);
        else if (json.conj && json.conj.length === 2)
            return '(' + jsonToASCII(json.conj[0]) + ' & ' + jsonToASCII(json.conj[1]) + ')';
        else if (json.disj && json.disj.length === 2)
            return '(' + jsonToASCII(json.disj[0]) + ' | ' + jsonToASCII(json.disj[1]) + ')';
        else if (json.impl && json.impl.length === 2)
            return '(' + jsonToASCII(json.impl[0]) + ' -> ' + jsonToASCII(json.impl[1]) + ')';
        else if (json.equi && json.equi.length === 2)
            return '(' + jsonToASCII(json.equi[0]) + ' <-> ' + jsonToASCII(json.equi[1]) + ')';
        else
            throw new Error('Invalid JSON for formula!');
    }

    /**
     * Converts an MPL wff from ASCII to LaTeX.
     * @private
     */
    var asciiToLaTeX = function (ascii) {
        return ascii.replace(/~/g, '\\lnot{}')
            .replace(/\[\]/g, '\\Box{}')
            .replace(/<>/g, '\\Diamond{}')
            .replace(/ & /g, '\\land{}')
            .replace(/ \| /g, '\\lor{}')
            .replace(/ <-> /g, '\\leftrightarrow{}')
            .replace(/ -> /g, '\\rightarrow{}');
    }

    /**
     * Converts an MPL wff from ASCII to Unicode.
     * @private
     */
    var asciiToUnicode = function (ascii) {
        return ascii.replace(/~/g, '\u00ac')
            .replace(/\[\]/g, '\u25a1')
            .replace(/<>/g, '\u25ca')
            .replace(/&/g, '\u2227')
            .replace(/\|/g, '\u2228')
            .replace(/<->/g, '\u2194')
            .replace(/->/g, '\u2192');
    }

    // Global objects
    return {
    	asciiToJSON : asciiToJSON,
		jsonToASCII : jsonToASCII,
		asciiToLaTeX : asciiToLaTeX,
		asciiToUnicode : asciiToUnicode
    };

});
